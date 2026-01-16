# Architecture Overview

## High-level flow
1. Generate or ingest ERP-style procurement data (raw exports)
2. Run **config-driven rule checks** (audit_rules.yaml)
3. Run **FOIP/PII scanning** on unstructured fields (notes/descriptions)
4. Output **audit reports** (exceptions + summary)
5. Optional: present results in a simple dashboard UI (Streamlit)

## Repo structure
- `config/` — audit rules and thresholds  
- `src/` — engine logic (rules + AI auditor)  
- `data/raw_erp_dump/` — simulated ERP exports  
- `data/audit_reports/` — generated results  
- `tests/` — test suite for reliability  
- `app/` — Streamlit UI (optional)
