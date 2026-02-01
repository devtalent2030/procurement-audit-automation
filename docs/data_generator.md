---
layout: default
title: Data Generator
permalink: /data_generator/
---

# Data Generator — Synthetic ERP Exports (Dirty-by-Design)

This project includes a **data generator** that creates realistic-looking procurement exports without using any real organizational data.

It produces two files that simulate what an auditor typically receives from an ERP system:

* **Vendor Master (CSV)** — the “source of truth” list of approved vendors
* **Invoices Export (Excel)** — a messy operational extract that may contain compliance issues

The generator is intentionally **dirty-by-design** so the audit engine has something meaningful to detect.

---

## What gets created

### Outputs

| File            | Path                                  | What it represents                          |
| --------------- | ------------------------------------- | ------------------------------------------- |
| Vendor Master   | `data/raw_erp_dump/vendor_master.csv` | Approved vendors (trusted reference)        |
| Invoices Export | `data/raw_erp_dump/invoices.xlsx`     | Operational invoices dump (untrusted input) |

### Open the generated files (published docs copies)

* Vendor Master: [vendor_master.csv](/data/raw_erp_dump/vendor_master.csv)
* Invoices Export: [invoices.xlsx](/data/raw_erp_dump/invoices.xlsx)

> Note: Browsers typically **download** Excel files instead of previewing them. That’s expected.

---

## How to run it

```bash
python src/data_generator.py
```

Expected terminal output:

* confirms both files were created
* prints a small sample of invoice rows (so you can immediately see seeded issues)

---

## Why this exists (real-world reason)

Audit tooling fails in demos when the dataset is too clean. In real procurement exports:

* vendor IDs don’t always match the master list
* purchase order data can be inconsistent
* staff write free-text notes that can accidentally contain personal information

This generator makes sure the dashboard and evidence exports always have realistic findings to show.

---

## What issues are intentionally seeded

### 1) Ghost Vendors (anti-join violations)

Invoices include vendor IDs that do **not** exist in the Vendor Master.

**Why this matters:**

* indicates potential fraud / shell vendor entries
* can also indicate ETL mapping issues (VendorID drift)

**What the audit engine should detect:**

* invoices where `VendorID ∉ vendor_master.VendorID`

**Evidence output produced later:**

* `data/audit_reports/ghost_vendors_20260201_124647.csv`
* Evidence file: [ghost_vendors_20260201_124647.csv](/data/audit_reports/ghost_vendors_20260201_124647.csv)

**Screenshot proof:**

<a class="doc-media" href="/assets/screenshots/a1-generated-files.png" target="_blank" rel="noopener">
  <img src="/assets/screenshots/a1-generated-files.png" alt="Generated files created (vendor master + invoices export)">
</a>

---

### 2) PO Variance Breaches (variance math)

Some invoices are generated with invoice totals that differ materially from the PO amount.

**Variance formula used by the engine:**

```text
variance = abs(invoice_amount - po_amount) / po_amount
```

**Why this matters:**

* price creep, scope changes, or approval bypass
* classic “audit flag” for procurement governance

**Evidence output produced later:**

* `data/audit_reports/po_variance_20260201_124647.csv`
* Evidence file: [po_variance_20260201_124647.csv](/data/audit_reports/po_variance_20260201_124647.csv)

**Screenshot proof:**

<a class="doc-media" href="/assets/screenshots/a2-excel-anomalies.png" target="_blank" rel="noopener">
  <img src="/assets/screenshots/a2-excel-anomalies.png" alt="Excel anomalies: ghost vendor + invoice/PO mismatch">
</a>

---

### 3) High-Value Invoices (threshold-based monitoring)

A portion of invoices are generated above a configurable high-value threshold.

**Why this matters:**

* many organizations require additional approval or review above set dollar amounts
* enables dashboards to prioritize review queues

**Evidence output produced later:**

* `data/audit_reports/high_value_20260201_125633.csv` (from dashboard export)
* Evidence file: [high_value_20260201_125633.csv](/data/audit_reports/high_value_20260201_125633.csv)

**Screenshot proof:**

<a class="doc-media" href="/assets/screenshots/b2-evidence-folder.png" target="_blank" rel="noopener">
  <img src="/assets/screenshots/b2-evidence-folder.png" alt="Evidence folder showing timestamped CSV outputs">
</a>

---

### 4) FOIP/PII risks embedded in Notes (unstructured text)

The `Notes` field is where “human messiness” lives:

* casual references to people
* email addresses
* phone numbers
* sensitive phrases (e.g., “confidential”)

**Why this matters:**

* free-text fields are the #1 place privacy risks leak into reporting exports
* this is exactly what FOIP-style reviews care about: accidental disclosure through operational text

**Expected findings later:**

* `POSSIBLE_EMAIL`
* `NAME_DETECTED: <person>` (NER)

**Evidence output produced later:**

* `data/audit_reports/foip_ai_findings_20260131_224156.csv`
* Evidence file: [foip_ai_findings_20260131_224156.csv](/data/audit_reports/foip_ai_findings_20260131_224156.csv)

**FOIP evidence capture (video):**

<video class="doc-media" controls preload="metadata">
  <source src="/assets/screenshots/c2-foip-evidence-csv.mp4" type="video/mp4">
</video>

---

## Design choices that keep this safe to publish

* **No real procurement records** are used.
* Data is generated as **synthetic demo data**, so it can be safely stored in GitHub.
* The generator creates repeatable inputs so the demo is stable across runs.

---

## Demo capture checklist (optional)

1. Run:

   ```bash
   python src/data_generator.py
   ```

2. Open:

   * `data/raw_erp_dump/vendor_master.csv`
   * `data/raw_erp_dump/invoices.xlsx`

3. Briefly scroll to show:

   * Vendor IDs in master
   * Invoice rows containing:

     * a ghost vendor ID (e.g., VENDOR-999)
     * variance between InvoiceAmount and PO_Amount
     * a Notes row with PII-like content

**Clip A (capture):**

<a class="doc-media" href="/assets/demo/clip-a-generate.png" target="_blank" rel="noopener">
  <img src="/assets/demo/clip-a-generate.png" alt="Clip A — Data generator run">
</a>
