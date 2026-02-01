# Procurement Audit Automation
**Automated Compliance & Audit Engine for ERP procurement exports**

> **One-liner:** Turn messy ERP procurement dumps (Excel/CSV) into **audit-ready evidence**: ghost vendor detection, PO variance checks, high-value flags, and FOIP/PII risk scanning.

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Non-technical summary</div>
    <div class="card__title">What problem this solves</div>
    <p class="card__desc">Procurement exports often contain exceptions that are easy to miss in spreadsheets. This project converts those risks into traceable exception reports that can be reviewed quickly and exported as evidence.</p>
    <div class="card__meta">
      <span class="chip chip--warn">Ghost / shell vendors</span>
      <span class="chip chip--warn">Invoice vs PO mismatch</span>
      <span class="chip chip--info">High-value spend</span>
      <span class="chip chip--bad">FOIP/PII risk in Notes</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Deliverables</div>
    <div class="card__title">What this project produces</div>
    <p class="card__desc">Config-driven controls, repeatable audit checks, privacy risk scanning on unstructured text, and exportable CSV evidence tables that support compliance and internal audit workflows.</p>
    <div class="card__meta">
      <span class="chip">YAML rules</span>
      <span class="chip">Pandas validation</span>
      <span class="chip">NER-based risk flags</span>
      <span class="chip">Evidence exports</span>
    </div>
  </div>
</div>

---

## What this project delivers

<div class="cards">
  <div class="card card--third">
    <div class="card__kicker">Control plane</div>
    <div class="card__title">Config-driven audit rules</div>
    <p class="card__desc">Audit thresholds and switches live in YAML to enable change control without code churn.</p>
    <div class="card__meta">
      <span class="chip chip--info">Config reviewable</span>
      <span class="chip">Repeatable runs</span>
    </div>
  </div>

  <div class="card card--third">
    <div class="card__kicker">Rule engine</div>
    <div class="card__title">Financial + process checks</div>
    <p class="card__desc">Ghost vendor detection, PO variance computation, and high-value invoice flagging using deterministic logic.</p>
    <div class="card__meta">
      <span class="chip chip--warn">Exceptions</span>
      <span class="chip">Evidence tables</span>
    </div>
  </div>

  <div class="card card--third">
    <div class="card__kicker">Privacy</div>
    <div class="card__title">FOIP/PII risk scan</div>
    <p class="card__desc">NER + lightweight heuristics flag potential names/emails typed into unstructured Notes fields.</p>
    <div class="card__meta">
      <span class="chip chip--bad">Risk flags</span>
      <span class="chip">Exception list</span>
    </div>
  </div>
</div>

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Evidence</div>
    <div class="card__title">Audit-ready exports</div>
    <p class="card__desc">Each run produces clean CSV outputs suitable for attaching to tickets, review packages, or internal audit evidence bundles.</p>
    <div class="card__meta">
      <span class="chip">ghost_vendors_*.csv</span>
      <span class="chip">po_variance_*.csv</span>
      <span class="chip">high_value_*.csv</span>
      <span class="chip">foip_ai_findings_*.csv</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Reliability</div>
    <div class="card__title">CI-ready pipeline</div>
    <p class="card__desc">GitHub Actions runs the deterministic audit pipeline and unit tests. The AI step can be skipped in CI to keep runs stable and fast.</p>
    <div class="card__meta">
      <span class="chip chip--ok">pytest</span>
      <span class="chip">GitHub Actions</span>
      <span class="chip chip--info">SKIP_AI=1</span>
    </div>
  </div>
</div>

---

## ⚡ Quick Links

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Code</div>
    <div class="card__title">Repository</div>
    <p class="card__desc">
      <a class="btn btn--accent" href="https://github.com/devtalent2030/procurement-audit-automation" target="_blank" rel="noopener">
        Open Repository
      </a>
    </p>
    <div class="card__meta">
      <span class="chip">src/</span>
      <span class="chip">app/</span>
      <span class="chip">tests/</span>
      <span class="chip">docs/</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Primary reference</div>
    <div class="card__title">README</div>
    <p class="card__desc">
      <a class="btn" href="https://github.com/devtalent2030/procurement-audit-automation#readme" target="_blank" rel="noopener">
        View README
      </a>
    </p>
    <div class="card__meta">
      <span class="chip">Setup</span>
      <span class="chip">Commands</span>
      <span class="chip">Outputs</span>
    </div>
  </div>
</div>


---

## 🎥 Demo Flow (video + screenshot plan)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Clip A</div>
    <div class="card__title">Generate dirty ERP data</div>
    <p class="card__desc"><strong>Command:</strong> <code>python src/data_generator.py</code></p>
    <div class="card__meta">
      <span class="chip">invoices.xlsx</span>
      <span class="chip">vendor_master.csv</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Clip B</div>
    <div class="card__title">Rule engine catches anomalies</div>
    <p class="card__desc"><strong>Command:</strong> <code>python src/rule_engine.py</code></p>
    <div class="card__meta">
      <span class="chip chip--warn">Ghost vendors</span>
      <span class="chip chip--warn">PO variance</span>
      <span class="chip chip--info">Evidence exports</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Clip C</div>
    <div class="card__title">FOIP/PII scan on Notes</div>
    <p class="card__desc"><strong>Command:</strong> <code>python src/ai_auditor.py</code></p>
    <div class="card__meta">
      <span class="chip chip--bad">PII risk flags</span>
      <span class="chip">Findings CSV</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Clip D</div>
    <div class="card__title">Streamlit dashboard + exports</div>
    <p class="card__desc"><strong>Command:</strong> <code>streamlit run app/dashboard.py</code></p>
    <div class="card__meta">
      <span class="chip">Summary cards</span>
      <span class="chip">Tabs</span>
      <span class="chip">Download buttons</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Clip E</div>
    <div class="card__title">Testing + CI evidence</div>
    <p class="card__desc"><strong>Command:</strong> <code>pytest -q</code></p>
    <div class="card__meta">
      <span class="chip chip--ok">4 passed</span>
      <span class="chip">GitHub Actions</span>
      <span class="chip chip--info">AI optional</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD VIDEO / SCREENSHOTS — Clip A</div>
  <p class="evidence__hint">assets/demo/clip-a-generate.mp4 + screenshot of generated files list</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD VIDEO / SCREENSHOTS — Clip B</div>
  <p class="evidence__hint">assets/demo/clip-b-rule-engine.mp4 + screenshot of terminal output + evidence folder exports</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD VIDEO / SCREENSHOTS — Clip C</div>
  <p class="evidence__hint">assets/demo/clip-c-ai-scan.mp4 + screenshot of AI findings output + findings CSV</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD VIDEO / SCREENSHOTS — Clip D</div>
  <p class="evidence__hint">assets/demo/clip-d-dashboard.mp4 + screenshot of summary cards + export/download section</p>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOTS — Clip E</div>
  <p class="evidence__hint">screenshot of local pytest passing + screenshot of GitHub Actions run (AI skipped with SKIP_AI=1)</p>
</div>

---

## Evidence outputs

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Deterministic evidence</div>
    <div class="card__title">Rule engine reports</div>
    <p class="card__desc">Evidence tables exported to <code>data/audit_reports/</code> after each run (timestamped).</p>
    <div class="card__meta">
      <span class="chip">ghost_vendors_*.csv</span>
      <span class="chip">po_variance_*.csv</span>
      <span class="chip">high_value_*.csv</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Privacy risk evidence</div>
    <div class="card__title">FOIP/PII findings</div>
    <p class="card__desc">Exception list of flagged Notes content to support privacy review before sharing or archiving.</p>
    <div class="card__meta">
      <span class="chip chip--bad">foip_ai_findings_*.csv</span>
      <span class="chip">NER + heuristics</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">ADD SCREENSHOT</div>
  <p class="evidence__hint">Screenshot: data/audit_reports/ folder after a full local run</p>
</div>

---

## Documentation pages

<div class="cards">
  <div class="card card--third">
    <div class="card__kicker">System</div>
    <div class="card__title"><a href="architecture/">Architecture overview</a></div>
    <p class="card__desc">Pipeline flow, components, boundaries, and outputs.</p>
  </div>

  <div class="card card--third">
    <div class="card__kicker">Engine</div>
    <div class="card__title"><a href="logic_engine_concepts/">Audit rule engine concepts</a></div>
    <p class="card__desc">How rules map to evidence tables and why the checks are audit-grade.</p>
  </div>

  <div class="card card--third">
    <div class="card__kicker">Data</div>
    <div class="card__title"><a href="data_generator/">Data generator</a></div>
    <p class="card__desc">Synthetic “dirty ERP” simulation for safe development and repeatable demos.</p>
  </div>

  <div class="card card--third">
    <div class="card__kicker">Privacy</div>
    <div class="card__title"><a href="foip_pii_scanner/">FOIP/PII scanner</a></div>
    <p class="card__desc">NER-based risk detection and why it’s treated as an exception list.</p>
  </div>

  <div class="card card--third">
    <div class="card__kicker">Quality</div>
    <div class="card__title"><a href="testing_ci/">Testing &amp; CI</a></div>
    <p class="card__desc">Unit tests, CI pipeline behavior, and AI step handling.</p>
  </div>

  <div class="card card--third">
    <div class="card__kicker">Evidence</div>
    <div class="card__title"><a href="demo/">Demo &amp; artifacts</a></div>
    <p class="card__desc">What to record and where to place screenshots/videos.</p>
  </div>
</div>

---

<details>

<summary><strong> why this design is audit-grade</strong></summary>

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Change control</div>
    <div class="card__title">YAML as the policy surface</div>
    <p class="card__desc">Thresholds and switches live in a single configuration file, making changes reviewable, traceable, and consistent across runs.</p>
    <div class="card__meta">
      <span class="chip">Reviewable diffs</span>
      <span class="chip">No code churn</span>
      <span class="chip">Reproducible runs</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Detection pattern</div>
    <div class="card__title">Anti-join for ghost vendors</div>
    <p class="card__desc">Invoices are left-joined against the vendor master and missing matches are extracted as an evidence table. This is scalable and explainable.</p>
    <div class="card__meta">
      <span class="chip">Deterministic</span>
      <span class="chip">Explainable</span>
      <span class="chip">Evidence-first</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Measurable control</div>
    <div class="card__title">PO variance formula</div>
    <p class="card__desc"><code>abs(invoice - po) / po</code> produces a transparent control metric that can be tuned via config and justified during review.</p>
    <div class="card__meta">
      <span class="chip">Transparent math</span>
      <span class="chip">Config-tunable</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Privacy handling</div>
    <div class="card__title">Risk detection, not adjudication</div>
    <p class="card__desc">Unstructured Notes is the highest FOIP/PII risk surface. The scanner outputs an exception list for review (names/emails), not a compliance decision.</p>
    <div class="card__meta">
      <span class="chip chip--bad">Exception list</span>
      <span class="chip">Review workflow</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">CI stability</div>
    <div class="card__title">AI optional in CI</div>
    <p class="card__desc">CI validates deterministic logic + tests reliably. The AI step can be toggled off with <code>SKIP_AI=1</code> to keep CI stable while preserving full local demos.</p>
    <div class="card__meta">
      <span class="chip chip--ok">Stable CI</span>
      <span class="chip chip--info">SKIP_AI=1</span>
    </div>
  </div>
</div>

</details>

---

## Mapping to IT Reporting / Compliance work

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Reporting</div>
    <div class="card__title">Decision-support outputs</div>
    <p class="card__desc">Produces repeatable exception tables for review, triage, and downstream reporting.</p>
    <div class="card__meta">
      <span class="chip">Evidence tables</span>
      <span class="chip">Repeatability</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Compliance</div>
    <div class="card__title">Controls + privacy risk visibility</div>
    <p class="card__desc">Supports policy-driven checks and highlights FOIP/PII risk before data is shared or archived.</p>
    <div class="card__meta">
      <span class="chip">Controls</span>
      <span class="chip chip--bad">FOIP/PII awareness</span>
    </div>
  </div>
</div>
