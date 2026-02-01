import pandas as pd

import warnings
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

import os

# 1. MODEL LOADER
# We wrap this in a function so we don't load the massive brain unless we need it.
def load_auditor_brain():
    from transformers import pipeline
    """
    Initializes the Named Entity Recognition (NER) pipeline.
    Uses a standard BERT model fine-tuned for entity detection.
    """
    print(" Waking up the AI Auditor (Loading Model)...")
    # We use a specific model 'dslim/bert-base-NER' known for good performance
    pii_identifier = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
    return pii_identifier

# 2. SCANNING LOGIC
def scan_notes_for_risk(df, column_name="Notes"):
    """
    Iterates through the DataFrame and uses AI to spot PII in the text.
    """
    # Load the brain once
    nlp = load_auditor_brain()
    
    risky_rows = []

    print(f"🕵️  Scanning {len(df)} rows for FOIP violations...")
    
    for index, row in df.iterrows():
        text_data = row[column_name]
        
        # Skip empty rows or non-text garbage
        if pd.isna(text_data) or not isinstance(text_data, str):
            continue

        # RUN THE AI PREDICTION
        # The model reads the sentence and returns a list of "Entities" it found.
        entities = nlp(text_data)
        
        # Check if any entities are 'PER' (Person) or look suspicious
        # Note: We also manually check for '@' because NER sometimes misses emails, 
        # but is great at names. This is a "Hybrid" approach.
        found_risks = []
        
        # Check 1: AI Detected Names
        for ent in entities:
            # We filter for high confidence (>85%) to avoid false alarms
            if ent['entity_group'] == 'PER' and ent['score'] > 0.85:
                found_risks.append(f"NAME_DETECTED: {ent['word']}")
        
        # Check 2: Simple Rule for Emails (Hybrid Approach)
        if "@" in text_data and "." in text_data:
             found_risks.append("POSSIBLE_EMAIL")

        # If we found anything, record the row
        if found_risks:
            risky_rows.append({
                "InvoiceID": row.get("InvoiceID", "Unknown"),
                "RiskContent": text_data,
                "DetectedFlags": ", ".join(found_risks)
            })

    return pd.DataFrame(risky_rows)

# 3. EXECUTION
if __name__ == "__main__":
    # Load the messy data we made in Day 1
    input_path = "data/raw_erp_dump/invoices.xlsx"
    
    if os.path.exists(input_path):
        df = pd.read_excel(input_path)
        
        # Run the Scan
        risk_report = scan_notes_for_risk(df)
        
        if not risk_report.empty:
            print(f"\n🚨 AI AUDIT COMPLETE: Found {len(risk_report)} Privacy Violations!")
            print(risk_report.to_string(index=False))
            
            # Save the report
            risk_report.to_csv("data/audit_reports/ai_risk_findings.csv", index=False)
        else:
            print("✅ AI Scan Complete. No privacy risks found.")
    else:
        print("❌ Error: Data file not found. Run src/data_generator.py first.")