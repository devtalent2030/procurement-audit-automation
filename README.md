# Procurement Audit Automation

**Config-driven audit engine for ERP procurement exports (Excel/CSV)** with **FOIP/PII risk scanning** and **audit-ready evidence outputs**.

> **:** Turn messy procurement dumps into **traceable exception reports**: ghost vendor detection, PO variance checks, high‑value flags, and FOIP/PII scanning in free‑text “Notes”.

---

## What this solves

Procurement exports are often reviewed manually in spreadsheets, where important issues are easy to miss:

* **Ghost / shell vendors** — invoice vendor not found in the vendor master
* **Invoice vs PO mismatches** — budget variance breaches
* **High‑value spend** — items that should be prioritized for review
* **FOIP/PII risk in Notes** — accidental emails/names in unstructured comments

This tool converts those risks into **repeatable, exportable evidence tables** that can be reviewed quickly and attached to audit/compliance workflows.

---

## What you get (outputs)

When you run the pipeline, it produces:

* **Evidence CSVs (timestamped)** under `data/audit_reports/`

  * `ghost_vendors_<timestamp>.csv`
  * `po_variance_<timestamp>.csv`
  * `high_value_<timestamp>.csv`
  * `foip_ai_findings_<timestamp>.csv` *(when AI scan runs)*
* **Run logs** under `data/audit_reports/run_logs/`
* **Streamlit dashboard** for interactive review + downloads

---

## Quick start

### 1) Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the full demo pipeline

```bash
./run_audit.sh
```

> CI can skip the AI step using `SKIP_AI=1` for stability:

```bash
SKIP_AI=1 ./run_audit.sh
```

---

## Run parts individually

### Generate sample ERP exports (synthetic)

```bash
python src/data_generator.py
```

### Run rule engine (ghost vendors, PO variance, high value)

```bash
python src/rule_engine.py
```

### Run FOIP/PII scan (AI auditor)

```bash
python src/ai_auditor.py
```

### Launch the dashboard

```bash
streamlit run app/dashboard.py
```

---

## Testing

```bash
pytest -q
```

---

## Repository layout

```text
procurement-audit-automation/
├── app/
│   └── dashboard.py
├── config/
│   └── audit_rules.yaml
├── data/
│   ├── raw_erp_dump/              # synthetic ERP-like exports
│   └── audit_reports/             # evidence exports + logs
├── docs/                          # GitHub Pages documentation
├── src/
│   ├── data_generator.py
│   ├── rule_engine.py
│   └── ai_auditor.py
├── tests/
│   ├── conftest.py
│   └── test_auditors.py
├── run_audit.sh
└── requirements.txt
```

---

## Documentation (GitHub Pages)

Project site: [https://devtalent2030.github.io/procurement-audit-automation/](https://devtalent2030.github.io/procurement-audit-automation/)

Key pages live under `docs/`:

* Architecture overview
* Rule engine concepts
* Data generator
* FOIP/PII scanner
* Testing & CI
* Demo/evidence guide

---

## Notes on data safety

This repository is designed for public demonstration:

* The dataset is **synthetic** (generated), not taken from real procurement systems.
* Any “PII-like” strings are injected **only as test cases**.

---

## License

MIT (or update this section if you are using a different license).
