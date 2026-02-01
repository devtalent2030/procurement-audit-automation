# Demo & Evidence

This section documents the full end-to-end demo flow for the project, including commands, outputs, and exportable evidence tables.

---

## Demo Flow (5 short clips)

Each clip is designed to be **20–40 seconds** and shows **one action + one result**.

---

## Clip A — Generate Dirty ERP Data

**Caption:** Day 1 — Generate ERP dump with anomalies

**Command:**

```bash
python src/data_generator.py
```

### Expected outputs

* `data/raw_erp_dump/invoices.xlsx`
* `data/raw_erp_dump/vendor_master.csv`

### What to capture

* Terminal output confirming file generation
* Folder view showing the two files created
* Excel view showing:

  * one ghost vendor example
  * one PO mismatch example

📌 **VIDEO PLACEHOLDER:** `assets/demo/clip-a-generate.mp4`
📌 **SCREENSHOT PLACEHOLDER:** terminal output after running generator
📌 **SCREENSHOT PLACEHOLDER:** `data/raw_erp_dump/` folder showing files
📌 **SCREENSHOT PLACEHOLDER:** Excel highlight (ghost vendor + mismatch)

---

## Clip B — Rule Engine Detects Exceptions

**Caption:** Day 2 — Config-driven rule engine detects ghost vendors & PO variance

**Command:**

```bash
python src/rule_engine.py
```

### Expected outputs

Exports saved under:

* `data/audit_reports/ghost_vendors_<timestamp>.csv`
* `data/audit_reports/po_variance_<timestamp>.csv`

### What to capture

* Terminal output showing ghost vendor count and PO variance breaches
* Folder view showing the exported CSV evidence files

📌 **VIDEO PLACEHOLDER:** `assets/demo/clip-b-rule-engine.mp4`
📌 **SCREENSHOT PLACEHOLDER:** terminal output showing violations
📌 **SCREENSHOT PLACEHOLDER:** `data/audit_reports/` folder showing new CSV outputs

---

## Clip C — FOIP/PII Scan (AI/NLP)

**Caption:** Day 3 — AI detects privacy risks inside unstructured Notes

**Command:**

```bash
python src/ai_auditor.py
```

### Expected outputs

* Console results listing flagged content (e.g., possible emails / detected names)
* Evidence export (when enabled):

  * `data/audit_reports/foip_ai_findings_<timestamp>.csv`

### What to capture

* Terminal output showing AI findings (rows flagged)
* Folder view showing the findings CSV in `data/audit_reports/`

📌 **VIDEO PLACEHOLDER:** `assets/demo/clip-c-ai-scan.mp4`
📌 **SCREENSHOT PLACEHOLDER:** terminal output showing AI findings
📌 **SCREENSHOT PLACEHOLDER:** `data/audit_reports/` showing FOIP/PII findings file

> Note: CI runs are configured to skip AI by default using `SKIP_AI=1` for stability.
> The AI scan is intended for local demo runs.

---

## Clip D — Streamlit Dashboard

**Caption:** Day 4 — Interactive dashboard + exportable evidence tables

**Command:**

```bash
streamlit run app/dashboard.py
```

### What to do in the UI

* Keep **Use sample generated data** enabled (no uploads needed)
* Click **Run Audit**
* Show summary cards:

  * Ghost Vendors
  * PO Variance Breaches
  * High-Value Invoices
  * FOIP/PII Findings
* Use the export buttons to download evidence tables

📌 **VIDEO PLACEHOLDER:** `assets/demo/clip-d-dashboard.mp4`
📌 **SCREENSHOT PLACEHOLDER:** dashboard summary cards section
📌 **SCREENSHOT PLACEHOLDER:** evidence export section + download buttons
📌 **SCREENSHOT PLACEHOLDER (optional):** downloaded CSV files visible locally

---

## Clip E — Tests & CI

**Caption:** Day 5 — Unit tests + CI/CD confirm reliability

### Local unit tests

**Command:**

```bash
pytest -q
```

📌 **SCREENSHOT PLACEHOLDER:** terminal showing `4 passed`

### GitHub Actions (CI)

CI runs the pipeline in a CI-safe mode:

* Generates data
* Runs rule engine
* Skips AI (by design)
* Runs unit tests

📌 **SCREENSHOT PLACEHOLDER:** GitHub Actions run summary ✅
📌 **SCREENSHOT PLACEHOLDER:** logs showing `Skipping AI auditor (SKIP_AI=1)`

---

# Outputs Checklist

## Raw inputs

* `data/raw_erp_dump/invoices.xlsx`
* `data/raw_erp_dump/vendor_master.csv`

📌 **SCREENSHOT PLACEHOLDER:** raw files after Clip A

## Evidence exports

Saved under:

* `data/audit_reports/`

Typical files:

* `ghost_vendors_<timestamp>.csv`
* `po_variance_<timestamp>.csv`
* `high_value_<timestamp>.csv`
* `foip_ai_findings_<timestamp>.csv` (local demo)

📌 **SCREENSHOT PLACEHOLDER:** `data/audit_reports/` folder after a run

---

## Related pages

* **Architecture Overview:** [architecture.md](architecture.md)
* **Audit Rule Engine Concepts:** [logic_engine_concepts.md](logic_engine_concepts.md)
* **Data Generator:** [data_generator.md](data_generator.md)
* **FOIP/PII Scanner:** [foip_pii_scanner.md](foip_pii_scanner.md)
* **Testing & CI:** [testing_ci.md](testing_ci.md)
