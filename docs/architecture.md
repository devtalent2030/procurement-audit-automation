---
layout: default
title: System Architecture & Audit Pipeline
permalink: /architecture/
---

# 🏗️ System Architecture & Audit Pipeline (Project 2)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">System</div>
    <div class="card__title">Procurement Audit Automation</div>
    <p class="card__desc">Self-contained audit pipeline that converts ERP-style exports into audit-ready evidence: deterministic controls + optional FOIP/PII scanning + reproducible logs.</p>
    <div class="card__meta">
      <span class="chip">ERP exports</span>
      <span class="chip chip--ok">Deterministic controls</span>
      <span class="chip chip--info">Evidence exports</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Outcome</div>
    <div class="card__title">Exceptions + evidence + traceability</div>
    <p class="card__desc">Produces exception tables (ghost vendors, PO variance, high-value flags) and optional FOIP/PII findings, saved as timestamped evidence files for review workflows.</p>
    <div class="card__meta">
      <span class="chip">CSV evidence</span>
      <span class="chip">Run logs</span>
      <span class="chip">Streamlit UI</span>
    </div>
  </div>
</div>

---

## 1) System story

<div class="cards">
  <div class="card">
    <div class="card__kicker">Why this exists</div>
    <div class="card__title">Numbers are only half the risk</div>
    <p class="card__desc">Procurement risk typically shows up in vendor integrity (ghost/shell vendors), invoice vs PO mismatches (variance/overbilling patterns), and unstructured Notes that can leak FOIP/PII. This system treats the export as a fact source and produces auditor-usable outputs: exceptions, evidence files, and reproducible logs.</p>
    <div class="card__meta">
      <span class="chip chip--warn">Vendor integrity</span>
      <span class="chip chip--warn">Budget variance</span>
      <span class="chip chip--warn">FOIP/PII risk</span>
    </div>
  </div>
</div>

---

## 2) End-to-end flow

<div class="cards">
  <div class="card">
    <div class="card__kicker">Pipeline</div>
    <div class="card__title">Generate → Check → Scan → Export → Present</div>
    <p class="card__desc">The pipeline is designed to mirror a real internal audit workflow: generate ERP-like exports, apply deterministic controls, optionally scan Notes for privacy risk signals, and export evidence artifacts for review.</p>
    <div class="card__meta">
      <span class="chip">Generator</span>
      <span class="chip">Rule engine</span>
      <span class="chip">AI auditor</span>
      <span class="chip">Evidence</span>
      <span class="chip">Dashboard</span>
    </div>
  </div>
</div>

![Pipeline Flow Diagram](assets/architecture_flow.png)

<div class="evidence">
  <div class="evidence__label">ADD DIAGRAM IMAGE</div>
  <p class="evidence__hint">Replace assets/architecture_flow.png with your exported diagram (keep filename stable for the page)</p>
</div>

<div class="cards">
  <div class="card">
    <div class="card__kicker">Order of operations</div>
    <div class="card__title">What happens during a run</div>
    <p class="card__desc">
      1) Data Generator creates a “dirty” ERP dump (<code>invoices.xlsx</code> + <code>vendor_master.csv</code>)<br/>
      2) Rule Engine reads <code>config/audit_rules.yaml</code> and flags deterministic anomalies<br/>
      3) AI Auditor scans unstructured <code>Notes</code> for FOIP/PII signals (optional in CI)<br/>
      4) Evidence exports are written to <code>data/audit_reports/</code> (timestamped)<br/>
      5) Streamlit Dashboard runs the audit and provides export buttons<br/>
      6) CI runs the same flow but may skip AI for stability (<code>SKIP_AI=1</code>)
    </p>
    <div class="card__meta">
      <span class="chip chip--ok">Repeatable</span>
      <span class="chip">Timestamped evidence</span>
      <span class="chip">CI-aligned</span>
    </div>
  </div>
</div>

---

## 3) Components (what each part does)

<div class="cards">

  <div class="card card--half">
    <div class="card__kicker">Input layer</div>
    <div class="card__title">ERP export simulation</div>
    <p class="card__desc"><strong>Component:</strong> <code>src/data_generator.py</code><br/>Produces a safe, realistic dataset without using real ERP data.</p>
    <div class="card__meta">
      <span class="chip">Synthetic data</span>
      <span class="chip">Reproducible</span>
      <span class="chip chip--ok">Public-safe</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Outputs</div>
    <div class="card__title">Raw inputs (source artifacts)</div>
    <p class="card__desc">
      <code>data/raw_erp_dump/invoices.xlsx</code><br/>
      <code>data/raw_erp_dump/vendor_master.csv</code>
    </p>
    <div class="card__meta">
      <span class="chip">ERP-like</span>
      <span class="chip">Demo-friendly</span>
    </div>
  </div>

</div>

<details>
<summary><strong>: why synthetic data is non-negotiable</strong></summary>

<div class="cards">
  <div class="card">
    <div class="card__kicker">Privacy-by-design</div>
    <div class="card__title">Same workflow, no data risk</div>
    <p class="card__desc">Real procurement exports often contain personal emails, names, phone numbers, and contract context. Synthetic data enables a public demo of FOIP/PII detection while keeping the pipeline reproducible and reviewable without privileged access.</p>
    <div class="card__meta">
      <span class="chip chip--ok">Public-safe</span>
      <span class="chip">Reproducible runs</span>
      <span class="chip">No privileged access</span>
    </div>
  </div>
</div>

</details>

---

<div class="cards">

  <div class="card card--half">
    <div class="card__kicker">Rules layer</div>
    <div class="card__title">Config-driven audit engine</div>
    <p class="card__desc"><strong>Component:</strong> <code>src/rule_engine.py</code><br/>Deterministic, explainable checks using pandas. Thresholds live in YAML for change control.</p>
    <div class="card__meta">
      <span class="chip chip--ok">Deterministic</span>
      <span class="chip">Explainable</span>
      <span class="chip">YAML policy layer</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Checks</div>
    <div class="card__title">Current controls</div>
    <p class="card__desc">
      • Ghost vendors (VendorID missing in master)<br/>
      • PO variance (<code>abs(invoice - po) / po</code> above threshold)<br/>
      • High-value invoice flags (policy threshold)
    </p>
    <div class="card__meta">
      <span class="chip">Anti-join</span>
      <span class="chip">Variance math</span>
      <span class="chip">Materiality</span>
    </div>
  </div>

</div>

<div class="cards">
  <div class="card">
    <div class="card__kicker">Evidence exports</div>
    <div class="card__title">Timestamped exception tables</div>
    <p class="card__desc">
      <code>data/audit_reports/ghost_vendors_&lt;TS&gt;.csv</code><br/>
      <code>data/audit_reports/po_variance_&lt;TS&gt;.csv</code><br/>
      <code>data/audit_reports/high_value_&lt;TS&gt;.csv</code> (if enabled/exported)
    </p>
    <div class="card__meta">
      <span class="chip chip--info">Evidence artifacts</span>
      <span class="chip">Attach to review</span>
      <span class="chip">Repeatable</span>
    </div>
  </div>
</div>

<details>
<summary><strong>: why YAML rules matter in real organizations</strong></summary>

<div class="cards">
  <div class="card">
    <div class="card__kicker">Change control</div>
    <div class="card__title">Policy thresholds must be reviewable</div>
    <p class="card__desc">Audit thresholds change and controls are sometimes toggled during transitions. YAML makes policy readable to non-developers, version-controlled via diffs, and reduces hidden logic inside code—supporting a clean approval trail.</p>
    <div class="card__meta">
      <span class="chip">Reviewable diffs</span>
      <span class="chip">Lower regression risk</span>
      <span class="chip">Audit-friendly</span>
    </div>
  </div>
</div>

</details>

---

<div class="cards">

  <div class="card card--half">
    <div class="card__kicker">AI layer</div>
    <div class="card__title">FOIP/PII scanner on Notes</div>
    <p class="card__desc"><strong>Component:</strong> <code>src/ai_auditor.py</code><br/>Flags privacy risk signals in unstructured text. Outputs evidence rows for human review.</p>
    <div class="card__meta">
      <span class="chip chip--warn">Probabilistic</span>
      <span class="chip">Assistive</span>
      <span class="chip">Evidence-first</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Output</div>
    <div class="card__title">FOIP/PII findings evidence</div>
    <p class="card__desc"><code>data/audit_reports/foip_ai_findings_&lt;TS&gt;.csv</code> (or your chosen naming)</p>
    <div class="card__meta">
      <span class="chip">InvoiceID</span>
      <span class="chip">RiskContent</span>
      <span class="chip">DetectedFlags</span>
    </div>
  </div>

</div>

<details>
<summary><strong>: trust model — AI is assistive, not authoritative</strong></summary>

<div class="cards">
  <div class="card">
    <div class="card__kicker">Audit defensibility</div>
    <div class="card__title">AI produces triage signals + raw text evidence</div>
    <p class="card__desc">Privacy/compliance workflows require human validation. The design stores the exact text snippet, the flags raised, and the invoice reference so a reviewer can verify context quickly.</p>
    <div class="card__meta">
      <span class="chip">Human review</span>
      <span class="chip">Raw evidence text</span>
      <span class="chip">Clear traceability</span>
    </div>
  </div>
</div>

</details>

---

<div class="cards">

  <div class="card card--half">
    <div class="card__kicker">Presentation layer</div>
    <div class="card__title">Streamlit dashboard</div>
    <p class="card__desc"><strong>Component:</strong> <code>app/dashboard.py</code><br/>One-screen UI: run audit, show pass/fail summary, inspect results, export evidence tables.</p>
    <div class="card__meta">
      <span class="chip">Summary cards</span>
      <span class="chip">Tabs</span>
      <span class="chip">Downloads</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Data behavior</div>
    <div class="card__title">Sample mode vs uploads</div>
    <p class="card__desc">Sample mode loads from <code>data/raw_erp_dump/</code>. Upload mode accepts invoices and vendor master files directly through the UI.</p>
    <div class="card__meta">
      <span class="chip">Sample toggle</span>
      <span class="chip">User uploads</span>
    </div>
  </div>

</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT / VIDEO</div>
  <p class="evidence__hint">Dashboard landing page + summary cards + export buttons (place assets in docs/assets/… and reference them here)</p>
</div>

---

<div class="cards">

  <div class="card card--half">
    <div class="card__kicker">Orchestration</div>
    <div class="card__title">One command run</div>
    <p class="card__desc"><strong>Component:</strong> <code>run_audit.sh</code><br/>Single entry point that generates inputs, runs checks, exports evidence, runs tests, and writes logs.</p>
    <div class="card__meta">
      <span class="chip">Reproducible</span>
      <span class="chip">Logged</span>
      <span class="chip">CI-aligned</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">CI stability</div>
    <div class="card__title">AI optional via SKIP_AI=1</div>
    <p class="card__desc">CI validates deterministic controls and tests. AI can be skipped to avoid runner instability (downloads, torch/numpy mismatches). Local runs can include the full AI step.</p>
    <div class="card__meta">
      <span class="chip">Stable builds</span>
      <span class="chip">Fast CI</span>
      <span class="chip chip--info">Full local demo</span>
    </div>
  </div>

</div>

<details>
<summary><strong>: why the AI step is optional in CI</strong></summary>

<div class="cards">
  <div class="card">
    <div class="card__kicker">Enterprise pattern</div>
    <div class="card__title">Stable controls in CI, heavier analysis in controlled environments</div>
    <p class="card__desc">CI runners vary and model downloads can be flaky. The pipeline keeps deterministic controls and tests always-on, while AI analysis runs locally or in a controlled environment. This mirrors real compliance pipelines where stability comes first.</p>
    <div class="card__meta">
      <span class="chip">Reliability-first</span>
      <span class="chip">Predictable CI</span>
      <span class="chip">Controlled AI runs</span>
    </div>
  </div>
</div>

</details>

---

## 4) Trust boundaries & data handling

<div class="cards">

  <div class="card card--half">
    <div class="card__kicker">Boundary</div>
    <div class="card__title">Public repo vs sensitive data</div>
    <p class="card__desc">Only synthetic data is generated and stored. Evidence tables are safe to publish because they are derived from synthetic inputs (no real procurement data).</p>
    <div class="card__meta">
      <span class="chip chip--ok">Public-safe</span>
      <span class="chip">Synthetic-only</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Boundary</div>
    <div class="card__title">Rules vs AI</div>
    <p class="card__desc">Rules are deterministic and repeatable. AI findings are triage signals for human review. Outputs include raw text evidence so reviewers can validate context.</p>
    <div class="card__meta">
      <span class="chip chip--ok">Deterministic rules</span>
      <span class="chip chip--warn">Assistive AI</span>
    </div>
  </div>

</div>

<div class="cards">
  <div class="card">
    <div class="card__kicker">Boundary</div>
    <div class="card__title">Local demo vs CI environment</div>
    <p class="card__desc">Local runs demonstrate the full pipeline (including AI). CI runs prioritize stability and can skip AI using <code>SKIP_AI=1</code>.</p>
    <div class="card__meta">
      <span class="chip">Local = full demo</span>
      <span class="chip">CI = stable validation</span>
    </div>
  </div>
</div>

---

## 5) Outputs (audit evidence map)

<div class="cards">
  <div class="card">
    <div class="card__kicker">Artifacts</div>
    <div class="card__title">Where outputs land, and why they matter</div>

| Output Type | Where it lands | Why it matters |
|---|---|---|
| Raw inputs | `data/raw_erp_dump/` | Reproducible “source” exports |
| Ghost vendors evidence | `data/audit_reports/ghost_vendors_<TS>.csv` | Vendor integrity exceptions |
| PO variance evidence | `data/audit_reports/po_variance_<TS>.csv` | Overbilling / mismatch evidence |
| High value evidence | `data/audit_reports/high_value_<TS>.csv` | Review prioritization (materiality) |
| FOIP/PII findings | `data/audit_reports/foip_ai_findings_<TS>.csv` | Privacy risk triage for review |
| Run logs | `data/audit_reports/run_logs/` | Traceability, debugging, audit trail |

  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">data/audit_reports/ and data/audit_reports/run_logs/ after a successful run</p>
</div>

---

## 6) Scalability roadmap (production-grade direction)

<div class="cards">

  <div class="card card--half">
    <div class="card__kicker">Data</div>
    <div class="card__title">Secure ERP integration</div>
    <p class="card__desc">Replace generator with secure connectors (export jobs, service accounts, approved access). Keep evidence artifacts unchanged.</p>
    <div class="card__meta">
      <span class="chip">Secure connectors</span>
      <span class="chip">Same evidence outputs</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Privacy</div>
    <div class="card__title">Stronger FOIP/PII detection</div>
    <p class="card__desc">Add phone/address patterns, stronger heuristics, and privacy-focused classifiers. Keep outputs as evidence-first exception lists.</p>
    <div class="card__meta">
      <span class="chip">Phones/addresses</span>
      <span class="chip">Keywords</span>
      <span class="chip">Better precision</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Rules</div>
    <div class="card__title">Modular control packs</div>
    <p class="card__desc">Split rules into financial/vendor/approvals/delegation-limits. Keep YAML policy layer with versioned thresholds.</p>
    <div class="card__meta">
      <span class="chip">Control packs</span>
      <span class="chip">YAML policy</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Traceability</div>
    <div class="card__title">Run IDs + storage</div>
    <p class="card__desc">Persist runs to SQLite/Postgres with run IDs, evidence references, and metadata. Improves lineage and audit replay.</p>
    <div class="card__meta">
      <span class="chip">Run IDs</span>
      <span class="chip">Lineage</span>
      <span class="chip">Replay</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Security</div>
    <div class="card__title">Role-based access</div>
    <p class="card__desc">Dashboard authentication + restricted evidence exports to align with least privilege and internal compliance expectations.</p>
    <div class="card__meta">
      <span class="chip">Auth</span>
      <span class="chip">Least privilege</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Packaging</div>
    <div class="card__title">Containerized execution</div>
    <p class="card__desc">Ship as a container for repeatable execution in standardized environments (local demo, controlled servers, enterprise runners).</p>
    <div class="card__meta">
      <span class="chip">Docker</span>
      <span class="chip">Repeatable</span>
    </div>
  </div>

</div>
