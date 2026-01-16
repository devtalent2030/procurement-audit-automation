import pandas as pd
import random
from faker import Faker
import os

# 1. SETUP
# Initialize Faker with Canadian localization
fake = Faker('en_CA')

# Set Seed for reproducibility (The "Senior" requirement)
# This ensures our "random" errors happen in the same place every time we debug.
Faker.seed(101)
random.seed(101)

# DEFINING THE "TRUTH"
# These are the only vendors that legally exist in our system.
VALID_VENDORS = [f"VENDOR-{i:03d}" for i in range(1, 21)]

def get_risky_note():
    """
    Generates a text string for the 'Notes' column.
    Most are safe. Some contain PII (Email/Phone) to test our AI Auditor.
    """
    # 85% chance of being "Clean"
    if random.random() > 0.15:
        return random.choice(["Delivered on time", "Net 30 Terms", "Annual maintenance", "Software subscription"])
    
    # 15% chance of being "Dirty" (PII Leak)
    # fake.free_email() generates realistic emails like 'jim@gmail.com'
    # This simulates an employee accidentally pasting contact info into a public field.
    return random.choice([
        f"Please forward the private contract to {fake.free_email()}",
        f"CONFIDENTIAL: Discuss with {fake.name()} before processing.",
        f"Urgent: Call personal cell {fake.phone_number()}"
    ])

def generate_erp_data(num_records=100):
    """
    Generates the Invoice Data (The 'Messy' Reality).
    Includes Ghost Vendors and Financial Mismatches.
    """
    data = []
    
    for _ in range(num_records):
        # 1. GHOST VENDOR LOGIC
        # We roll a die. If it lands on the bottom 5%, we inject a Ghost Vendor.
        if random.random() < 0.05:
            vendor_id = "VENDOR-999"         # The Saboteur ID
            vendor_name = "Unknown Shell Co"
        else:
            vendor_id = random.choice(VALID_VENDORS) # A Valid ID
            vendor_name = fake.company()

        # 2. FINANCIAL LOGIC
        invoice_amount = round(random.uniform(1000, 50000), 2)
        
        # 3. PO MISMATCH LOGIC
        # 10% chance the Invoice is higher than the Purchase Order (PO)
        if random.random() < 0.10:
            po_amount = round(invoice_amount * 0.8, 2) # Undersized PO
        else:
            po_amount = invoice_amount # Perfect Match

        # 4. BUILD THE RECORD
        row = {
            "InvoiceID": fake.bothify(text='INV-####-??'),
            "VendorID": vendor_id,
            "VendorName": vendor_name,
            "InvoiceDate": fake.date_between(start_date='-6m', end_date='today'),
            "InvoiceAmount": invoice_amount,
            "PO_Amount": po_amount,
            "Department": "IT - Tech & Innovation",
            "Notes": get_risky_note() # Injecting the text risk
        }
        data.append(row)
        
    return pd.DataFrame(data)

# 4. EXECUTION
if __name__ == "__main__":
    print("🚀 Starting 'Dirty' Data Generation Pipeline...")
    
    # Create the directory structure if it doesn't exist
    os.makedirs("data/raw_erp_dump", exist_ok=True)
    
    # STEP 1: Save the "Truth" (Master List)
    # An auditor needs a reference list to check against.
    master_df = pd.DataFrame({"VendorID": VALID_VENDORS, "Status": "Active"})
    master_path = "data/raw_erp_dump/vendor_master.csv"
    master_df.to_csv(master_path, index=False)
    print(f"✅ Master Vendor List (The Truth) saved to {master_path}")

    # STEP 2: Save the "Mess" (Invoices)
    # We generate 50 invoices. Statistically, ~2-3 will be Ghosts and ~7-8 will have PII leaks.
    invoice_df = generate_erp_data(50)
    invoice_path = "data/raw_erp_dump/invoices.xlsx"
    invoice_df.to_excel(invoice_path, index=False)
    
    print(f"✅ Raw Invoice Dump (The Reality) saved to {invoice_path}")
    
    # Peek at the data to show the user the "Dirty" rows
    print("\nSample Data (Look for PII in 'Notes'):")
    print(invoice_df[['VendorID', 'InvoiceAmount', 'Notes']].head(5))