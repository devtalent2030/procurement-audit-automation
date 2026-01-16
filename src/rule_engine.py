import pandas as pd
import yaml
import os

def load_config(config_path="config/audit_rules.yaml"):
    """Loads the YAML configuration file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ Critical Error: Config file not found at {config_path}")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_audit_checks():
    """
    Orchestrates the audit:
    1. Loads Rules
    2. Loads Data (Invoices + Master List)
    3. Finds Violations
    """
    # 1. Load the "Brain" (Config)
    config = load_config()
    limit = config['financial_limits']['max_po_variance']
    
    # 2. Load the "Reality" (Data generated in Day 1)
    try:
        invoices = pd.read_excel("data/raw_erp_dump/invoices.xlsx")
        master_list = pd.read_csv("data/raw_erp_dump/vendor_master.csv")
    except FileNotFoundError:
        print("❌ Error: Run 'src/data_generator.py' first to generate data.")
        return

    print(f"🔍 Audit Started. Using Variance Limit: {limit * 100}%")

    # --- CHECK 1: The Ghost Vendor Hunt ---
    # Merge Invoice Data (Left) with Master Data (Right)
    # 'indicator=True' adds a column telling us if the match succeeded
    merged = invoices.merge(master_list, on="VendorID", how="left", indicator=True)
    
    # 'left_only' means the ID exists in Invoices but NOT in Master List
    ghosts = merged[merged['_merge'] == 'left_only']
    
    if not ghosts.empty:
        print(f"🚨 ALERT: Found {len(ghosts)} Ghost Vendors!")
        print(ghosts[['InvoiceID', 'VendorID', 'VendorName']])
    else:
        print("✅ Vendor Compliance Check Passed.")

    # --- CHECK 2: Financial Mismatch ---
    # Vectorized Calculation (Pandas does the math for the whole column at once)
    # Logic: Calculate absolute % difference between Invoice and PO
    invoices['Variance'] = abs((invoices['InvoiceAmount'] - invoices['PO_Amount']) / invoices['PO_Amount'])
    
    # Filter rows that exceed the limit defined in YAML
    failures = invoices[invoices['Variance'] > limit]
    
    if not failures.empty:
        print(f"⚠️  WARNING: Found {len(failures)} Budget Variances > {limit*100}%")
        print(failures[['InvoiceID', 'InvoiceAmount', 'PO_Amount', 'Variance']].head())
    else:
        print("✅ Financial Logic Check Passed.")

# Execution Block
if __name__ == "__main__":
    run_audit_checks()