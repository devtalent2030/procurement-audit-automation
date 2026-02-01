import os
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

# ----------------------------
# ✅ Streamlit Import Fix
# ----------------------------
# Streamlit sometimes runs with `app/` as the working context,
# so `src` won't be discoverable unless we add the repo root to sys.path.
ROOT = Path(__file__).resolve().parents[1]  # repo root (procurement-audit-automation/)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Reuse your existing logic/components
from src.rule_engine import load_config, audit_invoices  # reads config/audit_rules.yaml + pure engine
from src.ai_auditor import load_auditor_brain  # loads HF model once


# ----------------------------
#  Guardrails
# ----------------------------

REQUIRED_COLUMNS = {
    "InvoiceID",
    "VendorID",
    "VendorName",
    "InvoiceAmount",
    "PO_Amount",
    "Notes",
}

DEFAULT_INVOICES_PATH = "data/raw_erp_dump/invoices.xlsx"
DEFAULT_MASTER_PATH = "data/raw_erp_dump/vendor_master.csv"
REPORT_DIR = "data/audit_reports"


def validate_invoices_df(df: pd.DataFrame) -> list[str]:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return missing


def run_rule_engine(invoices: pd.DataFrame, master: pd.DataFrame, config: dict) -> dict:
    """
    UI-friendly version of your rule_engine.py:
    - Ghost vendors via left join + indicator
    - PO variance check via vectorized calc
    - High-value threshold flag
    """
    results = {}

    financial = config.get("financial_limits", {})
    risk = config.get("risk_settings", {})

    variance_limit = float(financial.get("max_po_variance", 0.10))
    high_value_threshold = float(financial.get("high_value_threshold", 15000))
    detect_ghosts = bool(risk.get("detect_ghost_vendors", True))

    results["variance_limit"] = variance_limit
    results["high_value_threshold"] = high_value_threshold
    results["detect_ghost_vendors"] = detect_ghosts

    # --- Ghost vendor check (Anti-join pattern) ---
    if detect_ghosts:
        merged = invoices.merge(master, on="VendorID", how="left", indicator=True)
        ghosts = merged[merged["_merge"] == "left_only"].copy()
        results["ghosts"] = ghosts[["InvoiceID", "VendorID", "VendorName"]].reset_index(drop=True)
    else:
        results["ghosts"] = pd.DataFrame(columns=["InvoiceID", "VendorID", "VendorName"])

    # --- PO variance check ---
    safe = invoices.copy()
    safe["Variance"] = (safe["InvoiceAmount"] - safe["PO_Amount"]).abs() / safe["PO_Amount"].replace(0, pd.NA)
    variance_failures = safe[safe["Variance"] > variance_limit].copy()
    results["variance_failures"] = variance_failures[
        ["InvoiceID", "VendorID", "InvoiceAmount", "PO_Amount", "Variance"]
    ].sort_values("Variance", ascending=False).reset_index(drop=True)

    # --- High value flag ---
    high_value = invoices[invoices["InvoiceAmount"] >= high_value_threshold].copy()
    results["high_value"] = high_value[
        ["InvoiceID", "VendorID", "InvoiceAmount", "VendorName"]
    ].sort_values("InvoiceAmount", ascending=False).reset_index(drop=True)

    return results


@st.cache_resource
def get_cached_ner_pipeline():
    """
    performance:
    Loading transformers is expensive.
    Cache it so it loads once per Streamlit session.
    """
    return load_auditor_brain()


def run_ai_scan(invoices: pd.DataFrame) -> pd.DataFrame:
    """
    Mirrors your ai_auditor.py behavior:
    - detect PER entities with score > 0.85
    - detect emails with '@' and '.'
    Returns a findings dataframe.
    """
    nlp = get_cached_ner_pipeline()
    risky_rows = []

    for _, row in invoices.iterrows():
        text_data = row.get("Notes", None)

        if pd.isna(text_data) or not isinstance(text_data, str):
            continue

        entities = nlp(text_data)
        found_risks = []

        for ent in entities:
            if ent.get("entity_group") == "PER" and float(ent.get("score", 0)) > 0.85:
                found_risks.append(f"NAME_DETECTED: {ent.get('word')}")

        if "@" in text_data and "." in text_data:
            found_risks.append("POSSIBLE_EMAIL")

        if found_risks:
            risky_rows.append(
                {
                    "InvoiceID": row.get("InvoiceID", "Unknown"),
                    "RiskContent": text_data,
                    "DetectedFlags": ", ".join(found_risks),
                }
            )

    return pd.DataFrame(risky_rows)


def save_report(df: pd.DataFrame, filename: str) -> str:
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, filename)
    df.to_csv(path, index=False)
    return path


# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="Procurement Audit Automation", layout="wide")

st.title("🧾 Procurement Audit Automation Dashboard")
st.caption("Upload an ERP invoice Excel → run rule engine + FOIP/PII scan → export evidence tables.")

with st.sidebar:
    st.header("⚙️ Controls")

    use_sample = st.toggle("Use sample generated data (data/raw_erp_dump/)", value=True)

    st.markdown("**Upload Inputs** (only needed if not using sample data)")
    uploaded_invoices = st.file_uploader("Invoices (Excel .xlsx)", type=["xlsx"])
    uploaded_master = st.file_uploader("Vendor Master (CSV)", type=["csv"])

    st.divider()
    st.markdown("**Execution**")
    run_clicked = st.button("✅ Run Audit", type="primary")

    st.divider()
    st.markdown("**Config**")
    st.code("config/audit_rules.yaml", language="text")


# --- Load config ---
try:
    config = load_config("config/audit_rules.yaml")
except Exception as e:
    st.error(f"Config error: {e}")
    st.stop()

# --- Load data ---
invoices_df = None
master_df = None

if use_sample:
    if not (os.path.exists(DEFAULT_INVOICES_PATH) and os.path.exists(DEFAULT_MASTER_PATH)):
        st.warning("Sample files not found. Run: python src/data_generator.py")
        st.stop()
    invoices_df = pd.read_excel(DEFAULT_INVOICES_PATH)
    master_df = pd.read_csv(DEFAULT_MASTER_PATH)
else:
    if uploaded_invoices is not None:
        invoices_df = pd.read_excel(uploaded_invoices)
    if uploaded_master is not None:
        master_df = pd.read_csv(uploaded_master)

    if invoices_df is None or master_df is None:
        st.info("Upload both files (Invoices + Vendor Master), or toggle sample data on.")
        st.stop()

# --- Validate schema ---
missing_cols = validate_invoices_df(invoices_df)
if missing_cols:
    st.error(f"Invoices file is missing required columns: {missing_cols}")
    st.stop()

# Convert numeric fields safely
for col in ["InvoiceAmount", "PO_Amount"]:
    invoices_df[col] = pd.to_numeric(invoices_df[col], errors="coerce")

# ----------------------------
# Run audits
# ----------------------------
if run_clicked:
    with st.spinner("Running rule checks..."):
        rule_results = run_rule_engine(invoices_df, master_df, config)

    with st.spinner("Running FOIP/PII AI scan... (first run may download model)"):
        ai_findings = run_ai_scan(invoices_df)

    # Store in session state (so UI doesn't wipe results)
    st.session_state["rule_results"] = rule_results
    st.session_state["ai_findings"] = ai_findings
    st.session_state["ran_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ----------------------------
# Render results (if present)
# ----------------------------
if "rule_results" in st.session_state:
    rule_results = st.session_state["rule_results"]
    ai_findings = st.session_state["ai_findings"]
    ran_at = st.session_state.get("ran_at", "")

    st.subheader("📌 Audit Summary")
    st.caption(f"Last run: {ran_at}")

    col1, col2, col3, col4 = st.columns(4)

    ghosts = rule_results["ghosts"]
    variance_failures = rule_results["variance_failures"]
    high_value = rule_results["high_value"]

    def status_card(col, label, count, pass_if_zero=True):
        ok = (count == 0) if pass_if_zero else (count > 0)
        col.metric(label, count)

        if ok:
            col.success("PASS ✅")
        else:
            col.error("FAIL 🚨")

        return None


    status_card(col1, "Ghost Vendors", len(ghosts), pass_if_zero=True)
    status_card(col2, "PO Variance Breaches", len(variance_failures), pass_if_zero=True)
    status_card(col3, "High-Value Invoices", len(high_value), pass_if_zero=False)
    status_card(col4, "FOIP/PII Findings", len(ai_findings), pass_if_zero=True)

    st.divider()

    st.subheader(" Rules Used")
    st.write(
        {
            "max_po_variance": rule_results["variance_limit"],
            "high_value_threshold": rule_results["high_value_threshold"],
            "detect_ghost_vendors": rule_results["detect_ghost_vendors"],
        }
    )

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Ghost Vendors", "PO Variance", "High Value", "FOIP/PII Findings"]
    )

    with tab1:
        st.write("Invoices referencing VendorIDs not found in the master list.")
        st.dataframe(ghosts, use_container_width=True)

    with tab2:
        st.write("Invoices where abs(InvoiceAmount - PO_Amount) / PO_Amount exceeds threshold.")
        st.dataframe(variance_failures, use_container_width=True)

    with tab3:
        st.write("Invoices at/above the configured high value threshold.")
        st.dataframe(high_value, use_container_width=True)

    with tab4:
        st.write("Text findings from AI + simple email heuristic.")
        st.dataframe(ai_findings, use_container_width=True)

    st.divider()

    st.subheader("📤 Export Evidence (CSV)")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save files to data/audit_reports + also offer browser download
    ghost_path = save_report(ghosts, f"ghost_vendors_{timestamp}.csv")
    var_path = save_report(variance_failures, f"po_variance_{timestamp}.csv")
    hv_path = save_report(high_value, f"high_value_{timestamp}.csv")
    ai_path = save_report(ai_findings, f"foip_ai_findings_{timestamp}.csv")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.download_button(
            "Download Ghost Vendors CSV",
            data=ghosts.to_csv(index=False).encode("utf-8"),
            file_name=os.path.basename(ghost_path),
            mime="text/csv",
        )
    with c2:
        st.download_button(
            "Download PO Variance CSV",
            data=variance_failures.to_csv(index=False).encode("utf-8"),
            file_name=os.path.basename(var_path),
            mime="text/csv",
        )
    with c3:
        st.download_button(
            "Download High Value CSV",
            data=high_value.to_csv(index=False).encode("utf-8"),
            file_name=os.path.basename(hv_path),
            mime="text/csv",
        )
    with c4:
        st.download_button(
            "Download FOIP/PII CSV",
            data=ai_findings.to_csv(index=False).encode("utf-8"),
            file_name=os.path.basename(ai_path),
            mime="text/csv",
        )

else:
    st.info("Click **Run Audit** in the sidebar to generate the dashboard.")
