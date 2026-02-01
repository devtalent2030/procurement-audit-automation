import os
import pandas as pd
import pytest


# ----------------------------
# Tests
# ----------------------------
# Principle: tests must be
# - deterministic (same result every run)
# - fast (no external downloads)
# - isolated (temp folder, no real data touched)


def _write_fixture_files(tmp_path):
    """
    Creates a known-bad "ERP dump" + config in a temporary repo-like structure.

    This is the key TDD move:
    We control the input, so we can prove the engine catches it.
    """
    # Mimic repo layout
    (tmp_path / "config").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data" / "raw_erp_dump").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data" / "audit_reports").mkdir(parents=True, exist_ok=True)

    # Config: 10% allowed variance
    (tmp_path / "config" / "audit_rules.yaml").write_text(
        "financial_limits:\n"
        "  max_po_variance: 0.10\n"
    )

    # Vendor master list (truth)
    master = pd.DataFrame({"VendorID": ["VENDOR-001", "VENDOR-002"], "Status": ["Active", "Active"]})
    master.to_csv(tmp_path / "data" / "raw_erp_dump" / "vendor_master.csv", index=False)

    # Invoices (reality): includes a ghost vendor + a variance breach
    invoices = pd.DataFrame(
        [
            {
                "InvoiceID": "INV-0001-AA",
                "VendorID": "VENDOR-999",          # ghost vendor
                "VendorName": "Unknown Shell Co",
                "InvoiceAmount": 1000.00,
                "PO_Amount": 1000.00,
                "Notes": "Delivered on time",
            },
            {
                "InvoiceID": "INV-0002-BB",
                "VendorID": "VENDOR-001",
                "VendorName": "Legit Vendor Inc",
                "InvoiceAmount": 1000.00,
                "PO_Amount": 800.00,               # variance = 25% > 10%
                "Notes": "Standard contract",
            },
        ]
    )
    invoices.to_excel(tmp_path / "data" / "raw_erp_dump" / "invoices.xlsx", index=False)


def test_rule_engine_catches_ghost_vendor_and_variance(tmp_path, capsys, monkeypatch):
    """
    Integration-style unit test:
    - sets up known-bad inputs
    - runs run_audit_checks()
    - asserts the printed output contains expected violations

    Why print-based assert?
    Because your current rule_engine.py reports via stdout.
    This test proves the tool signals the right failures without rewriting your engine yet.
    """
    _write_fixture_files(tmp_path)

    # Run in temp directory so rule_engine reads the temp config + data paths
    monkeypatch.chdir(tmp_path)

    from src.rule_engine import run_audit_checks

    run_audit_checks()
    out = capsys.readouterr().out

    assert "ALERT: Found" in out, "Expected ghost vendor alert was not printed."
    assert "Ghost Vendors" in out or "Ghost" in out, "Expected ghost vendor language missing."
    assert "Budget Variances" in out or "Variance" in out, "Expected variance warning was not printed."


def test_load_config_reads_yaml(tmp_path, monkeypatch):
    """
    Pure unit test: proves config parsing works.
    """
    (tmp_path / "config").mkdir(parents=True, exist_ok=True)
    (tmp_path / "config" / "audit_rules.yaml").write_text(
        "financial_limits:\n"
        "  max_po_variance: 0.25\n"
    )

    monkeypatch.chdir(tmp_path)

    from src.rule_engine import load_config
    cfg = load_config("config/audit_rules.yaml")

    assert cfg["financial_limits"]["max_po_variance"] == 0.25


def test_ai_auditor_flags_name_and_email_without_downloading_models(monkeypatch):
    """
    True unit test for ai_auditor:
    - DOES NOT load HuggingFace
    - monkeypatches the NER brain with a fake predictable model
    """
    from src import ai_auditor

    # Fake NER model: always claims it found a PER entity with high confidence
    def fake_brain():
        def fake_nlp(_text):
            return [{"entity_group": "PER", "score": 0.95, "word": "John Doe"}]
        return fake_nlp

    monkeypatch.setattr(ai_auditor, "load_auditor_brain", fake_brain)

    df = pd.DataFrame(
        [
            {"InvoiceID": "INV-1", "Notes": "Please email john@gmail.com for approval."},
            {"InvoiceID": "INV-2", "Notes": "Standard delivery."},
        ]
    )

    findings = ai_auditor.scan_notes_for_risk(df, column_name="Notes")

    # Should flag INV-1 (name + email), and not necessarily flag INV-2
    assert not findings.empty
    assert "INV-1" in findings["InvoiceID"].values
    row = findings[findings["InvoiceID"] == "INV-1"].iloc[0]
    assert "NAME_DETECTED" in row["DetectedFlags"]
    assert "POSSIBLE_EMAIL" in row["DetectedFlags"]


def test_ai_auditor_respects_confidence_threshold(monkeypatch):
    """
    Ensures low-confidence entities do NOT trigger NAME_DETECTED.
    Email heuristic should still trigger if email exists.
    """
    from src import ai_auditor

    def fake_brain():
        def fake_nlp(_text):
            return [{"entity_group": "PER", "score": 0.10, "word": "Random Person"}]  # too low
        return fake_nlp

    monkeypatch.setattr(ai_auditor, "load_auditor_brain", fake_brain)

    df = pd.DataFrame([{"InvoiceID": "INV-3", "Notes": "Contact me at a@b.com"}])
    findings = ai_auditor.scan_notes_for_risk(df, column_name="Notes")

    assert not findings.empty
    flags = findings.iloc[0]["DetectedFlags"]
    assert "NAME_DETECTED" not in flags
    assert "POSSIBLE_EMAIL" in flags
