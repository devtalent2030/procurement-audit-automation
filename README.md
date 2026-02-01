````md
# Procurement Audit Automation
**Config-driven audit engine for ERP procurement exports** (Excel/CSV) with **FOIP/PII risk scanning** and **audit-ready evidence outputs**.

> **:** Turn messy procurement dumps into **traceable exception reports**:  
> ghost vendor detection, PO variance checks, high-value flags, and FOIP/PII scanning in “Notes”.

---

## What this solves
Procurement exports are often reviewed manually in spreadsheets, where important issues are easy to miss:

- **Ghost / shell vendors** (invoice vendor not found in vendor master)
- **Invoice vs PO mismatches** (budget variance breaches)
- **High-value spend** that should be prioritized for review
- **FOIP/PII risk** accidentally typed into free-text notes (emails, names)

This tool converts those risks into **repeatable, exportable evidence tables** that can be reviewed quickly and attached to audit/compliance workflows.

---

## What you get (outputs)
When you run the pipeline, it produces:

- **Evidence CSVs** (timestamped) under `data/audit_reports/`
  - `ghost_vendors_<timestamp>.csv`
  - `po_variance_<timestamp>.csv`
  - `high_value_<timestamp>.csv`
  - `foip_ai_findings_<timestamp>.csv` *(when AI scan runs)*
- **Run logs** under `data/audit_reports/run_logs/`
- **Streamlit dashboard** for interactive review + downloads

---

## Repository structure
```text
procurement-audit-automation/
├── app/
│   └── dashboard.py
├── config/
│   └── audit_rules.yaml
├── data/
│   ├── raw_erp_dump/              # generated synthetic ERP-like exports
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
````

---

## Quick start (local)

### 1) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

### 2) Generate sample ERP exports (synthetic)

```bash
python src/data_generator.py
```

### 3) Run rule engine (deterministic audit checks)

```bash
python src/rule_engine.py
```

### 4) Run FOIP/PII scan (AI auditor)

```bash
python src/ai_auditor.py
```

### 5) Run tests

```bash
pytest -q
```

---

## One-command demo run

Use the orchestrator script to run the full flow (data → rules → optional AI → tests):

```bash
chmod +x run_audit.sh
./run_audit.sh
```

### Skip AI step (useful in CI / fast runs)

```bash
SKIP_AI=1 ./run_audit.sh
```

---

## Streamlit dashboard

Launch the UI for interactive review + evidence downloads:

```bash
streamlit run app/dashboard.py
```

Dashboard features:

* Summary pass/fail cards
* Tabs for each evidence table
* Export buttons to download CSV evidence

---

## Configuration (audit_rules.yaml)

Controls are defined in `config/audit_rules.yaml`, for example:

* `financial_limits.max_po_variance` (e.g., `0.10` = 10%)
* `financial_limits.high_value_threshold` (e.g., `15000`)
* `risk_settings.detect_ghost_vendors` (true/false)

Why this matters:

* Thresholds change over time
* Config changes are reviewable + version-controlled
* Minimizes code churn for policy updates

---

## How the core checks work

### Ghost vendor detection (anti-join)

Invoices are left-joined to the vendor master list; invoices that fail to match are flagged as ghost vendors.

### PO variance detection

Variance is calculated using:
`abs(InvoiceAmount - PO_Amount) / PO_Amount`

Rows exceeding the configured threshold become evidence.

### High-value flags

Invoices at/above the configured threshold are listed for prioritization.

### FOIP/PII scan (notes)

A hybrid approach:

* **NER** detects likely person names above a confidence threshold
* **Heuristics** flag likely emails (and can be extended for phones/keywords)

Outputs are **risk signals**, designed for **human review**, not legal conclusions.

---

## CI notes (GitHub Actions)

CI is designed to be stable and fast:

* Runs rule engine + unit tests
* Can skip AI (`SKIP_AI=1`) to avoid heavy model dependencies on runners

---

## Documentation (GitHub Pages)

Project documentation lives in `docs/` and is published via GitHub Pages.

Recommended entry point:

* `docs/index.md`

---

## License

Choose one (MIT/Apache-2.0) or remove this section if you’ll add it later.

```
::contentReference[oaicite:0]{index=0}
```
