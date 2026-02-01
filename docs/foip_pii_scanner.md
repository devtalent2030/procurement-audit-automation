---
layout: default
title: "FOIP / PII Scanner"
permalink: /foip_pii_scanner/
---

# 🔒 FOIP / PII Scanner (AI Auditor)

> **Goal:** Catch privacy-risk text inside **Notes / Comments / Description** fields **before** exports get shared, emailed, archived, or turned into reports.
> This is a **fast pre-screen** that produces **evidence tables** for review (not a legal determination).

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Problem</div>
    <div class="card__title">Unstructured text is where privacy leaks survive</div>
    <p class="card__desc">Procurement exports can look clean (VendorID, amounts, POs) until the Notes field contains personal emails, names, phone numbers, or confidential context. Structured columns are governed; free-text is not.</p>
    <div class="card__meta">
      <span class="chip chip--bad">FOIP/PII risk</span>
      <span class="chip chip--warn">Hidden in Notes</span>
      <span class="chip">Exportable evidence</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Output</div>
    <div class="card__title">Evidence table (exception list)</div>
    <p class="card__desc">Each finding becomes a row with InvoiceID, RiskContent (the exact text), and DetectedFlags. This supports review workflows and audit trails.</p>
    <div class="card__meta">
      <span class="chip">InvoiceID</span>
      <span class="chip">RiskContent</span>
      <span class="chip">DetectedFlags</span>
    </div>
  </div>
</div>

---

## ✅ What the scanner flags

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">AI</div>
    <div class="card__title">Named Entity Recognition (NER)</div>
    <p class="card__desc">Detects likely PERSON names in text (entity group: <code>PER</code>) and applies a confidence threshold to reduce noise.</p>
    <div class="card__meta">
      <span class="chip">PER entities</span>
      <span class="chip chip--info">Confidence threshold</span>
      <span class="chip">Lower noise</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Deterministic</div>
    <div class="card__title">Heuristics for machine-detectable patterns</div>
    <p class="card__desc">Flags email-like strings using simple checks (contains <code>@</code> and <code>.</code>). Additional patterns (phone/postal/keywords) can be added as policy controls.</p>
    <div class="card__meta">
      <span class="chip">POSSIBLE_EMAIL</span>
      <span class="chip">Extensible rules</span>
      <span class="chip">Policy dial</span>
    </div>
  </div>
</div>

---

## AI Rules Scanner

<div class="evidence">
  <div class="evidence__label">AI Rules Scanner Flow Diagram</div>
  <div class="img-container">
    <a href="{{ site.baseurl }}/assets/foip_risk_funnel.png" target="_blank">
      <img src="{{ site.baseurl }}/assets/foip_risk_funnel.png" alt="Pipeline Flow Diagram">
    </a>
  </div>
</div>

## threshold_tradeoff

<div class="evidence">
  <div class="evidence__label"> threshold_tradeoff </div>
  <div class="img-container">
    <a href="{{ site.baseurl }}/assets/threshold_tradeoff.png" target="_blank">
      <img src="{{ site.baseurl }}/assets/threshold_tradeoff.png" alt="Pipeline Flow Diagram">
    </a>
  </div>
</div>


<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Evidence schema</div>
    <div class="card__title">What a finding row contains</div>
    <p class="card__desc">Output is designed for review: a clear identifier, the exact risky text, and the flags that triggered it.</p>
    <div class="card__meta">
      <span class="chip">InvoiceID</span>
      <span class="chip">RiskContent</span>
      <span class="chip">DetectedFlags</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Design rule</div>
    <div class="card__title">Evidence first, decision later</div>
    <p class="card__desc">The scanner produces an exception list for human review. It does not attempt to adjudicate compliance outcomes.</p>
    <div class="card__meta">
      <span class="chip chip--info">Review workflow</span>
      <span class="chip">Audit trail</span>
    </div>
  </div>
</div>

---

##  Confidence threshold (policy dial)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Default</div>
    <div class="card__title">Why a threshold exists</div>
    <p class="card__desc">NER always returns guesses. A threshold prevents low-confidence fragments from becoming noise in audit evidence.</p>
    <div class="card__meta">
      <span class="chip chip--info">Example: 0.85</span>
      <span class="chip">Noise control</span>
      <span class="chip">Explainable behavior</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Mode</div>
    <div class="card__title">Tune to workflow risk appetite</div>
    <p class="card__desc">High-risk review may prefer more findings (lower threshold). High-volume operations may prefer less noise (higher threshold). Treat this as a versioned control like any other audit rule.</p>
    <div class="card__meta">
      <span class="chip chip--warn">False positives</span>
      <span class="chip chip--warn">False negatives</span>
      <span class="chip">Versioned policy</span>
    </div>
  </div>
</div>

---

##  False positives vs false negatives

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">False positives</div>
    <div class="card__title">Flags that are not truly privacy issues</div>
    <p class="card__desc">Common causes include vendor names that resemble people, short token fragments, or context-free name detection.</p>
    <div class="card__meta">
      <span class="chip">Mitigate via threshold</span>
      <span class="chip">Allow/deny lists (future)</span>
      <span class="chip">Multi-signal rules (future)</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">False negatives</div>
    <div class="card__title">Missed privacy risks</div>
    <p class="card__desc">Caused by initials, unusual formatting, non-English names, or PII types not covered by the model (phones/addresses).</p>
    <div class="card__meta">
      <span class="chip">Add phone/postal patterns</span>
      <span class="chip">Keyword rules</span>
      <span class="chip">Model swap option</span>
    </div>
  </div>
</div>

---

##  Performance & stability

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Runtime</div>
    <div class="card__title">Load once, reuse in Streamlit</div>
    <p class="card__desc">The model is cached in the Streamlit app so it loads once per session. Subsequent runs reuse memory and stay responsive.</p>
    <div class="card__meta">
      <span class="chip">Cached model</span>
      <span class="chip">Fast re-runs</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">CI</div>
    <div class="card__title">AI optional for stable builds</div>
    <p class="card__desc">Transformers dependencies can be heavy/volatile in CI. The pipeline supports <code>SKIP_AI=1</code> so deterministic checks and tests stay reliable.</p>
    <div class="card__meta">
      <span class="chip">Stable GitHub Actions</span>
      <span class="chip chip--info">SKIP_AI=1</span>
    </div>
  </div>
</div>

---

##  What “good” looks like (expected outputs)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">CLI</div>
    <div class="card__title">Terminal findings summary</div>
    <p class="card__desc">Console output shows total findings and a compact table of flagged rows.</p>
    <div class="card__meta">
      <span class="chip">Finding count</span>
      <span class="chip">Flag types</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Exports + UI</div>
    <div class="card__title">CSV evidence + Streamlit tab</div>
    <p class="card__desc">A timestamped findings CSV appears under <code>data/audit_reports/</code>, and Streamlit shows the Findings tab with a download button.</p>
    <div class="card__meta">
      <span class="chip">Timestamped CSV</span>
      <span class="chip">Dashboard table</span>
      <span class="chip">Download</span>
    </div>
  </div>
</div>

---

##  Evidence (media)

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Clip C</div>
    <div class="card__title">AI FOIP/PII scan demo</div>
    <p class="card__desc"><strong>Command:</strong> <code>python src/ai_auditor.py</code> (show findings printed + CSV created)</p>
    <div class="card__meta">
      <span class="chip">20–40s video</span>
      <span class="chip">Terminal output</span>
      <span class="chip">CSV evidence</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Streamlit</div>
    <div class="card__title">Findings tab + download</div>
    <p class="card__desc">Show the “FOIP/PII Findings” summary card, the Findings table, and the export/download area.</p>
    <div class="card__meta">
      <span class="chip">Summary card</span>
      <span class="chip">Findings table</span>
      <span class="chip">Download button</span>
    </div>
  </div>
</div>

<!-- Clip C media (PNG screenshot) -->

<div class="evidence">
  <div class="evidence__label">Clip C — AI scan (screenshot)</div>
  <div class="img-container">
    <a href="{{ '/assets/demo/clip-c-ai-scan.png' | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ '/assets/demo/clip-c-ai-scan.png' | relative_url }}" alt="Clip C - AI scan screenshot">
    </a>
  </div>
</div>

<!-- Findings CSV: include BOTH a link + a screenshot image (use the screenshot for the docs page) -->

<div class="evidence">
  <div class="evidence__label">FOIP/PII findings evidence (CSV)</div>
  <p class="evidence__hint">CSV file in repo: <code>data/audit_reports/foip_ai_findings_20260131_224156.csv</code></p>
  <p class="card__desc">
    <a class="btn btn--accent" href="https://github.com/devtalent2030/procurement-audit-automation/blob/main/data/audit_reports/foip_ai_findings_20260131_224156.csv" target="_blank" rel="noopener">
      Open findings CSV (GitHub)
    </a>
  </p>
  <div class="img-container">
    <a href="{{ '/assets/screenshots/csv-foip-findings.png' | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ '/assets/screenshots/csv-foip-findings.png' | relative_url }}" alt="FOIP findings CSV screenshot">
    </a>
  </div>
</div>

<!-- Dashboard home (MP4 video) -->

<div class="evidence">
  <div class="evidence__label">Dashboard home (video)</div>
  <div class="video-container">
    <video controls loop muted playsinline>
      <source src="{{ '/assets/screenshots/d1-dashboard-home.mp4' | relative_url }}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
  </div>
</div>
