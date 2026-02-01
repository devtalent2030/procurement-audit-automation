---
layout: default
title: Audit Rule Engine Concepts
permalink: /logic_engine_concepts/
---

> **Goal:** Turn messy ERP exports (Excel/CSV) into **audit-grade evidence** using **config-driven rules**.
> The engine is designed to be readable by non-technical reviewers and defensible to technical auditors.

# Audit Rule Engine Concepts

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">What it does</div>
    <div class="card__title">Policy checks → exception evidence</div>
    <p class="card__desc">Applies audit controls to procurement exports and produces exception tables (ghost vendors, PO variance breaches, high-value flags) as timestamped CSV evidence.</p>
    <div class="card__meta">
      <span class="chip">Deterministic</span>
      <span class="chip chip--info">Evidence tables</span>
      <span class="chip">Timestamped exports</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Why it’s “audit-grade”</div>
    <div class="card__title">Config-driven controls (YAML)</div>
    <p class="card__desc">Thresholds and toggles live in YAML. Policy updates change controls without code changes, reducing review surface and regression risk.</p>
    <div class="card__meta">
      <span class="chip chip--ok">Change control</span>
      <span class="chip">Traceable</span>
      <span class="chip">Low churn</span>
    </div>
  </div>
</div>

---

## 🧩 Config-driven rules (YAML = change control)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Source of truth</div>
    <div class="card__title">config/audit_rules.yaml</div>
    <p class="card__desc">Audit thresholds change (variance %, high-value cutoffs, enable/disable checks). Keeping them in YAML makes approvals and change history straightforward.</p>
    <div class="card__meta">
      <span class="chip">max_po_variance</span>
      <span class="chip">high_value_threshold</span>
      <span class="chip">detect_ghost_vendors</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Mode</div>
    <div class="card__title">Policy is versionable</div>
    <p class="card__desc">Treat the YAML file like a control document: version it, review it, and align it to department tolerance (finance vs procurement vs compliance).</p>
    <div class="card__meta">
      <span class="chip chip--info">Versioned controls</span>
      <span class="chip">Reviewable diffs</span>
      <span class="chip">Department tuning</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">config/audit_rules.yaml open in editor (show the thresholds + toggles)</p>
</div>

---

## 1) 👻 Ghost vendor detection (anti-join pattern)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Definition</div>
    <div class="card__title">Invoice VendorID not in master list</div>
    <p class="card__desc">A ghost vendor is an invoice referencing a VendorID that does not exist in the vendor master. This is a strong data-integrity and control-failure signal.</p>
    <div class="card__meta">
      <span class="chip chip--bad">Control failure</span>
      <span class="chip chip--warn">Master data risk</span>
      <span class="chip">Evidence table</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Mechanism</div>
    <div class="card__title">Left join + keep missing matches</div>
    <p class="card__desc">Invoices LEFT JOIN vendor master; retain rows where the master lookup is missing. This produces a clean evidence table: InvoiceID, VendorID, VendorName.</p>
    <div class="card__meta">
      <span class="chip">Anti-join</span>
      <span class="chip">Explainable</span>
      <span class="chip">Scales well</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">Terminal output showing “Ghost Vendors: X” + sample rows</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">Exported CSV in folder: data/audit_reports/ghost_vendors_&lt;timestamp&gt;.csv</p>
</div>

### : edge cases (ghost vendors)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Edge case</div>
    <div class="card__title">Vendor exists, name drift</div>
    <p class="card__desc">VendorName can change over time or differ by source. A robust extension flags name mismatch separately (invoice name vs master name) instead of treating it as ghost.</p>
    <div class="card__meta">
      <span class="chip">Name mismatch rule</span>
      <span class="chip">Separate evidence</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Edge case</div>
    <div class="card__title">Vendor master is stale</div>
    <p class="card__desc">Sometimes invoices are valid but the master list is outdated. That becomes a master data governance issue (version the master list and treat as control gap).</p>
    <div class="card__meta">
      <span class="chip chip--warn">Governance gap</span>
      <span class="chip">Versioned master</span>
    </div>
  </div>
</div>

---

## 2) 📉 PO variance detection (variance math)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Definition</div>
    <div class="card__title">Invoice differs materially from PO</div>
    <p class="card__desc">Variance breaches detect invoice inflation, missing change control, or data errors. This is a classic finance/procurement control.</p>
    <div class="card__meta">
      <span class="chip chip--warn">Budget risk</span>
      <span class="chip">Change control</span>
      <span class="chip">Deterministic</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Formula</div>
    <div class="card__title">Transparent and defensible</div>
    <p class="card__desc"><code>Variance = abs(InvoiceAmount - PO_Amount) / PO_Amount</code> and flag when <code>Variance &gt; max_po_variance</code>.</p>
    <div class="card__meta">
      <span class="chip">Explainable math</span>
      <span class="chip">Config threshold</span>
      <span class="chip">Audit-friendly</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">Terminal output showing “Budget Variances &gt; X%” + sample rows</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">Exported CSV in folder: data/audit_reports/po_variance_&lt;timestamp&gt;.csv</p>
</div>

### : edge cases (variance)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Edge case</div>
    <div class="card__title">PO_Amount = 0</div>
    <p class="card__desc">Not a division error—an anomaly. Indicates PO was mis-entered, bypassed, or not properly linked. Treat as a separate evidence table (e.g., po_amount_zero.csv).</p>
    <div class="card__meta">
      <span class="chip chip--bad">Control gap</span>
      <span class="chip">Separate evidence</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Edge case</div>
    <div class="card__title">Split billing / partial invoices</div>
    <p class="card__desc">One PO may be paid across multiple invoices. A scalable enhancement groups by PO_ID and compares cumulative invoice totals to PO totals.</p>
    <div class="card__meta">
      <span class="chip">Group-by control</span>
      <span class="chip">Cumulative variance</span>
    </div>
  </div>
</div>

---

## 3) 💰 High-value invoice flagging (risk prioritization)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Purpose</div>
    <div class="card__title">Prioritize review effort</div>
    <p class="card__desc">High-value invoices aren’t “bad” by default—they’re high-exposure. This control creates a review queue aligned to materiality.</p>
    <div class="card__meta">
      <span class="chip">Materiality</span>
      <span class="chip chip--info">Risk queue</span>
      <span class="chip">Fast triage</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Logic</div>
    <div class="card__title">InvoiceAmount ≥ high_value_threshold</div>
    <p class="card__desc">Flags rows at/above the configured threshold and exports an evidence list (InvoiceID, VendorID, VendorName, InvoiceAmount).</p>
    <div class="card__meta">
      <span class="chip">Config threshold</span>
      <span class="chip">Evidence list</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">Streamlit “High-Value Invoices” tab showing sorted high-value rows</p>
</div>

---

## 📦 Evidence exports (why CSV is the right artifact)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Artifact</div>
    <div class="card__title">Timestamped evidence snapshots</div>
    <p class="card__desc">Every run produces timestamped CSVs (ghost vendors, PO variance, high value). These behave like immutable evidence snapshots that can be attached to tickets or audits.</p>
    <div class="card__meta">
      <span class="chip">Chain-of-custody feel</span>
      <span class="chip">Easy attachment</span>
      <span class="chip">Repeatable</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Mode</div>
    <div class="card__title">Traceability without heavy tooling</div>
    <p class="card__desc">For many audit workflows, consistent timestamped evidence exports provide enough traceability without needing a full data warehouse or ticketing integration.</p>
    <div class="card__meta">
      <span class="chip">Low overhead</span>
      <span class="chip">High trust</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">data/audit_reports/ folder showing multiple timestamped CSVs</p>
</div>

---

## ⚡ Performance notes (why Pandas is enough)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Performance</div>
    <div class="card__title">Vectorized operations</div>
    <p class="card__desc">Joins, column math, and filtering are vectorized, making runs fast for typical ERP export sizes (thousands to millions of rows depending on hardware).</p>
    <div class="card__meta">
      <span class="chip">Joins</span>
      <span class="chip">Column math</span>
      <span class="chip">Filtering</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Scaling path</div>
    <div class="card__title">Same controls, different engine</div>
    <p class="card__desc">If exports exceed memory, swap the compute layer (DuckDB/Polars) while keeping YAML rules + evidence outputs unchanged.</p>
    <div class="card__meta">
      <span class="chip">DuckDB / Polars</span>
      <span class="chip">Same YAML</span>
      <span class="chip">Same evidence</span>
    </div>
  </div>
</div>

---

## 🔒 Trust boundary: deterministic rules vs AI signals

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Rule engine</div>
    <div class="card__title">Deterministic evidence</div>
    <p class="card__desc">Same input produces the same output every time. This is the baseline for audit defensibility.</p>
    <div class="card__meta">
      <span class="chip chip--ok">Deterministic</span>
      <span class="chip">Defensible</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">AI scanner</div>
    <div class="card__title">Probabilistic risk signal</div>
    <p class="card__desc">Used only for unstructured Notes fields to surface risks. Treated as an exception list for review, not a verdict.</p>
    <div class="card__meta">
      <span class="chip chip--warn">Probabilistic</span>
      <span class="chip">Human review</span>
    </div>
  </div>
</div>

---

## 🎥 Evidence placeholders (add screenshots / video)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Clip B</div>
    <div class="card__title">Rule engine catches ghost vendor + variance</div>
    <p class="card__desc"><strong>Command:</strong> <code>python src/rule_engine.py</code> (show printed findings + evidence exports)</p>
    <div class="card__meta">
      <span class="chip">20–40s video</span>
      <span class="chip">Terminal output</span>
      <span class="chip">CSV exports</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Streamlit</div>
    <div class="card__title">Downloads create evidence instantly</div>
    <p class="card__desc">Show the summary cards and the Export Evidence section producing CSVs in-browser.</p>
    <div class="card__meta">
      <span class="chip">Summary cards</span>
      <span class="chip">Download buttons</span>
      <span class="chip">Evidence files</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD VIDEO</div>
  <p class="evidence__hint">assets/demo/clip-b-rule-engine.png</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">Terminal output showing counts + sample rows</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">data/audit_reports/ folder after a run (timestamped CSV evidence)</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">Streamlit export/download area producing evidence CSVs</p>
</div>

---

## ✅ Summary

<div class="cards">
  <div class="card">
    <div class="card__kicker">Bottom line</div>
    <div class="card__title">Policy in YAML. Logic in deterministic checks. Output as evidence.</div>
    <p class="card__desc">This is a realistic compliance pattern: thresholds are versioned, checks are explainable, and outputs are audit-ready snapshots that support review workflows.</p>
    <div class="card__meta">
      <span class="chip chip--ok">Config-driven controls</span>
      <span class="chip chip--ok">Deterministic evidence</span>
      <span class="chip chip--info">Review workflow</span>
    </div>
  </div>
</div>
