---
layout: default
title: Demo & Evidence Artifacts
permalink: /demo/
---

# Demo & Evidence

This page documents the end-to-end demo flow for the project and links directly to the **actual clips, screenshots, inputs, and evidence exports already in this repo**.

---

## Demo Flow (5 short clips)

Each clip shows **one action + one result**.

---

## Clip A — Generate Dirty ERP Data

**Caption:** Generate ERP dump with seeded anomalies

**Command:**

```bash
python src/data_generator.py
```

### Outputs created

* [data/raw_erp_dump/invoices.xlsx](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/raw_erp_dump/invoices.xlsx)
* [data/raw_erp_dump/vendor_master.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/raw_erp_dump/vendor_master.csv)

### What this clip shows

* Files created successfully
* Quick peek at the generated dataset (ghost vendor / PO mismatch seeded)

**Clip (image):**

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/demo/clip-a-generate.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/demo/clip-a-generate.png" alt="Clip A — Generate Dirty ERP Data">
  </a>
</div>

**Screenshots:**

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/screenshots/a1-generated-files.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/screenshots/a1-generated-files.png" alt="Generated files created">
  </a>
</div>

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/screenshots/a2-excel-anomalies.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/screenshots/a2-excel-anomalies.png" alt="Excel anomalies view 1">
  </a>
</div>

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/screenshots/a2-excel-anomalies1.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/screenshots/a2-excel-anomalies1.png" alt="Excel anomalies view 2">
  </a>
</div>

---

## Clip B — Rule Engine Detects Exceptions

**Caption:** Config-driven rule engine detects ghost vendors & PO variance

**Command:**

```bash
python src/rule_engine.py
```

### Evidence exports (example run)

These are real files from the repo (timestamped):

* [data/audit_reports/ghost_vendors_20260201_125633.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/audit_reports/ghost_vendors_20260201_125633.csv)
* [data/audit_reports/po_variance_20260201_125633.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/audit_reports/po_variance_20260201_125633.csv)

### What this clip shows

* Rule engine summary output (counts)
* Evidence CSVs produced under `data/audit_reports/`

**Clip (image):**

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/demo/clip-b-rule-engine.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/demo/clip-b-rule-engine.png" alt="Clip B — Rule Engine">
  </a>
</div>

**Screenshot:**

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/screenshots/b2-evidence-folder.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/screenshots/b2-evidence-folder.png" alt="Evidence folder after run">
  </a>
</div>

---

## Clip C — FOIP/PII Scan (AI/NLP)

**Caption:** AI flags privacy risk inside unstructured Notes

**Command:**

```bash
python src/ai_auditor.py
```

### Evidence export (example run)

* [data/audit_reports/foip_ai_findings_20260201_125633.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/audit_reports/foip_ai_findings_20260201_125633.csv)

### What this clip shows

* Findings printed during the scan
* Timestamped findings CSV written to `data/audit_reports/`

**Clip (image):**

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/demo/clip-c-ai-scan.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/demo/clip-c-ai-scan.png" alt="Clip C — AI FOIP/PII Scan">
  </a>
</div>

**Short walkthrough (video):**

<div class="video-container">
  <video controls loop muted>
    <source src="{{ site.baseurl }}/assets/screenshots/c2-foip-evidence-csv.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>

---

## Clip D — Streamlit Dashboard

**Caption:** Dashboard summary + exportable evidence tables

**Command:**

```bash
streamlit run app/dashboard.py
```

### What this clip shows

* Summary cards (Ghost Vendors / PO Variance / High-Value / FOIP Findings)
* Export/download actions

**Clip (video):**

<div class="video-container">
  <video controls loop muted>
    <source src="{{ site.baseurl }}/assets/demo/clip-d-dashboard.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>

**Dashboard UI walkthrough (video):**

<div class="video-container">
  <video controls loop muted>
    <source src="{{ site.baseurl }}/assets/screenshots/d1-dashboard-home.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>

---

## Clip E — Tests & CI

**Caption:** Tests + CI confirm reliability

### Local unit tests

**Command:**

```bash
pytest -q
```

### CI evidence

**Clip (image):**

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/demo/clip-e-tests-ci.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/demo/clip-e-tests-ci.png" alt="Clip E — Tests & CI">
  </a>
</div>

**Screenshot:**

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/screenshots/e2-github-actions-success.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/screenshots/e2-github-actions-success.png" alt="GitHub Actions success">
  </a>
</div>

---

# Outputs

## Raw inputs

* [data/raw_erp_dump/invoices.xlsx](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/raw_erp_dump/invoices.xlsx)
* [data/raw_erp_dump/vendor_master.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/raw_erp_dump/vendor_master.csv)

## Evidence exports

All saved under [data/audit_reports/](https://github.com/devtalent2030/procurement-audit-automation/tree/main/docs/data/audit_reports).

Representative evidence files already present:

* Ghost vendors: [data/audit_reports/ghost_vendors_20260201_125633.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/audit_reports/ghost_vendors_20260201_125633.csv)
* PO variance: [data/audit_reports/po_variance_20260201_125633.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/audit_reports/po_variance_20260201_125633.csv)
* High value: [data/audit_reports/high_value_20260201_125633.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/audit_reports/high_value_20260201_125633.csv)
* FOIP/PII findings: [data/audit_reports/foip_ai_findings_20260201_125633.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/audit_reports/foip_ai_findings_20260201_125633.csv)
* AI risk findings (aggregate): [data/audit_reports/ai_risk_findings.csv](https://github.com/devtalent2030/procurement-audit-automation/blob/main/docs/data/audit_reports/ai_risk_findings.csv)

## Run logs

* [data/audit_reports/run_logs/](https://github.com/devtalent2030/procurement-audit-automation/tree/main/docs/data/audit_reports/run_logs)

---

## Related pages

* **Architecture Overview:** [architecture.md](architecture.md)
* **Audit Rule Engine Concepts:** [logic_engine_concepts.md](logic_engine_concepts.md)
* **Data Generator:** [data_generator.md](data_generator.md)
* **FOIP / PII Scanner:** [foip_pii_scanner.md](foip_pii_scanner.md)
* **Testing & CI:** [testing_ci.md](testing_ci.md)

---

## Clip A (your capture):

<div class="img-container">
  <a href="{{ site.baseurl }}/assets/demo/clip-a-generate.png" target="_blank">
    <img src="{{ site.baseurl }}/assets/demo/clip-a-generate.png" alt="Clip A — Data generator run">
  </a>
</div>
