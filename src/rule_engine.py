import os
import yaml
import pandas as pd
from datetime import datetime


def load_config(config_path="config/audit_rules.yaml"):
    """Loads the YAML configuration file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ Critical Error: Config file not found at {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f) or {}


# -----------------------------
# Genius Mode: Pure Audit Engine
# -----------------------------
def audit_invoices(invoices: pd.DataFrame, master_list: pd.DataFrame, config: dict) -> dict:
    """
    Pure function (no file IO, no prints):
    Takes DataFrames + config, returns structured results.
    """
    financial = config.get("financial_limits", {})
    limit = float(financial.get("max_po_variance", 0.10))

    inv = invoices.copy()
    master = master_list.copy()

    # ---- CHECK 1: Ghost Vendors (Anti-Join) ----
    merged = inv.merge(master, on="VendorID", how="left", indicator=True)
    ghosts = merged[merged["_merge"] == "left_only"].copy()

    # ---- CHECK 2: PO variance ----
    inv["InvoiceAmount"] = pd.to_numeric(inv.get("InvoiceAmount"), errors="coerce")
    inv["PO_Amount"] = pd.to_numeric(inv.get("PO_Amount"), errors="coerce")

    # Avoid divide-by-zero
    denom = inv["PO_Amount"].replace({0: pd.NA})
    inv["Variance"] = (inv["InvoiceAmount"] - inv["PO_Amount"]).abs() / denom

    failures = inv[inv["Variance"] > limit].copy()

    return {
        "limit": limit,
        "ghosts": ghosts,
        "failures": failures,
        "merged": merged,
        "invoices_with_variance": inv,
    }


def export_findings(ghosts: pd.DataFrame, failures: pd.DataFrame, out_dir="data/audit_reports") -> dict:
    """
    Writes evidence CSVs so your CLI run produces audit artifacts.
    Returns paths for logging / demo proof.
    """
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    ghost_path = os.path.join(out_dir, f"ghost_vendors_{ts}.csv")
    variance_path = os.path.join(out_dir, f"po_variance_{ts}.csv")

    ghosts.to_csv(ghost_path, index=False)
    failures.to_csv(variance_path, index=False)

    return {"ghosts_csv": ghost_path, "variance_csv": variance_path}


# -----------------------------
# Backwards-compatible CLI runner
# -----------------------------
def run_audit_checks(
    invoices_path="data/raw_erp_dump/invoices.xlsx",
    master_path="data/raw_erp_dump/vendor_master.csv",
    config_path="config/audit_rules.yaml",
):
    """
    CLI Orchestrator:
    - loads files
    - calls pure engine
    - prints output
    - exports evidence CSVs
    - returns results dict
    """
    config = load_config(config_path)

    try:
        invoices = pd.read_excel(invoices_path)
        master_list = pd.read_csv(master_path)
    except FileNotFoundError:
        print("❌ Error: Run 'src/data_generator.py' first to generate data.")
        return None

    results = audit_invoices(invoices, master_list, config)
    limit = results["limit"]
    ghosts = results["ghosts"]
    failures = results["failures"]

    print(f"🔍 Audit Started. Using Variance Limit: {limit * 100:.0f}%")

    if not ghosts.empty:
        print(f"🚨 ALERT: Found {len(ghosts)} Ghost Vendors!")
        cols = [c for c in ["InvoiceID", "VendorID", "VendorName"] if c in ghosts.columns]
        print(ghosts[cols].head(10))
    else:
        print("✅ Vendor Compliance Check Passed.")

    if not failures.empty:
        print(f"⚠️  WARNING: Found {len(failures)} Budget Variances > {limit*100:.0f}%")
        cols = [c for c in ["InvoiceID", "InvoiceAmount", "PO_Amount", "Variance"] if c in failures.columns]
        print(failures[cols].head(10))
    else:
        print("✅ Financial Logic Check Passed.")

    # Export evidence pack
    paths = export_findings(ghosts, failures)
    results["export_paths"] = paths

    print("\n📄 Evidence exports saved:")
    print(f"   - {paths['ghosts_csv']}")
    print(f"   - {paths['variance_csv']}")

    return results


if __name__ == "__main__":
    run_audit_checks()
