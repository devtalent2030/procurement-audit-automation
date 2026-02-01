---
layout: default
title: Testing & CI
permalink: /testing_ci/
---

````md

# Testing & CI Credibility (Reliability Story)

This project is intentionally built so the **audit results are reproducible**, and the **core logic is testable without network access**.

---

## What “reliability” means here

* **Deterministic rule checks** (same inputs → same outputs).
* **Evidence tables are materialized** (CSV outputs become audit artifacts).
* **AI scan is optional in CI** (keeps CI fast + offline-safe), but fully available locally.

<div class="cards">
  <div class="card card--half">
    <div class="card__kicker">Evidence</div>
    <div class="card__title">GitHub Actions run (passing)</div>
    <p class="card__desc">Screenshot proof of a green pipeline run.</p>
    <div class="card__meta">
      <span class="chip">Actions</span>
      <span class="chip chip--ok">Passed</span>
    </div>
  </div>

  <div class="card card--half">
    <div class="card__kicker">Evidence</div>
    <div class="card__title">Local run (end-to-end)</div>
    <p class="card__desc">Short clip showing <code>./run_audit.sh</code> and the dashboard in action.</p>
    <div class="card__meta">
      <span class="chip">Local demo</span>
      <span class="chip chip--info">Video</span>
    </div>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">GitHub Actions — passing pipeline</div>
  <div class="img-container">
    <a href="{{ '/assets/screenshots/e2-github-actions-success.png' | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ '/assets/screenshots/e2-github-actions-success.png' | relative_url }}" alt="GitHub Actions successful run">
    </a>
  </div>
</div>

<div class="evidence">
  <div class="evidence__label">Local run — end-to-end demo (dashboard clip)</div>
  <div class="video-container">
    <video controls loop muted playsinline>
      <source src="{{ '/assets/demo/clip-d-dashboard.mp4' | relative_url }}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
  </div>
</div>

---

## Test Suite Overview

The test suite is designed around a single principle:

> **Test the contract, not the environment.**

Meaning:

* We verify *what the functions produce* (tables/flags/decisions).
* We avoid tests that depend on external services, model downloads, or machine-specific paths.

### What is tested

| Area                    | What the test proves                               | Why it matters                               |
| ----------------------- | -------------------------------------------------- | -------------------------------------------- |
| Rule engine config      | `audit_rules.yaml` is parsed correctly             | Prevents “silent misconfiguration”           |
| Ghost vendor detection  | Anti-join logic catches missing vendor IDs         | Finds supplier master integrity issues       |
| PO variance math        | Variance threshold correctly flags outliers        | Prevents overspend / mismatched PO alignment |
| FOIP/PII scan behavior  | Name/email detection triggers as expected          | Prevents privacy leaks in notes/comments     |
| AI confidence threshold | Low-confidence entities don’t trigger false alerts | Reduces “privacy alert noise”                |

<div class="evidence">
  <div class="evidence__label">pytest — local passing run</div>
  <div class="img-container">
    <a href="{{ '/assets/demo/clip-e-tests-ci.png' | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ '/assets/demo/clip-e-tests-ci.png' | relative_url }}" alt="pytest output showing passing tests">
    </a>
  </div>
</div>

---

## What is mocked (and why)

### HuggingFace model loading is mocked in unit tests

The AI scanner uses a NER pipeline (which normally may download weights). In tests, the pipeline is **replaced with a fake predictable model**.

This ensures:

* CI doesn’t require network access.
* Tests remain fast.
* We still validate the scanner’s *decision logic*.

**What we mock:**

* `load_auditor_brain()` → returns a predictable stub pipeline.

**What we still test (real logic):**

* confidence threshold behavior (e.g., recommended ~**0.85**)
* email heuristic behavior
* output schema (`InvoiceID`, `RiskContent`, `DetectedFlags`)

<div class="evidence">
  <div class="evidence__label">Unit tests — mocked brain (monkeypatch)</div>
  <div class="img-container">
    <a href="{{ '/assets/demo/clip-e-tests-ci.png' | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ '/assets/demo/clip-e-tests-ci.png' | relative_url }}" alt="Test file showing monkeypatch / fake pipeline">
    </a>
  </div>
</div>

---

## Why CI skips AI by default (SKIP_AI)

CI should be:

* **reliable** (no flaky downloads)
* **fast** (minutes, not tens of minutes)
* **repeatable** (same outcome on any runner)

So the workflow uses an environment flag:

* `SKIP_AI=1` → **skips the model-based scan** in CI.
* Local runs (developer machine) can run the full AI auditor normally.

This mirrors real enterprise practice:

* **Production/analyst run:** full scan with AI
* **CI run:** verify rule engine + scanner logic with deterministic stubs

<div class="evidence">
  <div class="evidence__label">CI evidence — SKIP_AI behavior (Actions screenshot)</div>
  <div class="img-container">
    <a href="{{ '/assets/screenshots/e2-github-actions-success.png' | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ '/assets/screenshots/e2-github-actions-success.png' | relative_url }}" alt="GitHub Actions logs showing SKIP_AI=1 behavior">
    </a>
  </div>
</div>

---

## GitHub Actions Pipeline

The CI pipeline validates the project in an “audit-friendly” order:

1. **Generate synthetic ERP-like data** (so CI always has inputs)
2. **Run the deterministic rule engine**
3. **Skip AI scan (by default)** using `SKIP_AI=1`
4. **Run unit tests** (`pytest -q`)

### Evidence artifacts produced in CI

The pipeline outputs **evidence CSVs** (for screenshots / demo assets) and **run logs**:

* `data/audit_reports/*.csv`
* `data/audit_reports/run_logs/*.log`

<div class="evidence">
  <div class="evidence__label">Evidence exports (folder view)</div>
  <div class="img-container">
    <a href="{{ '/assets/screenshots/b2-evidence-folder.png' | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ '/assets/screenshots/b2-evidence-folder.png' | relative_url }}" alt="Evidence folder structure screenshot">
    </a>
  </div>
</div>

---

## Local verification

### Run tests

```bash
pytest -q
````

### Run the full demo pipeline (includes AI unless you set SKIP_AI)

```bash
./run_audit.sh
```

### Force skip AI locally (to simulate CI)

```bash
SKIP_AI=1 ./run_audit.sh
```

---

## Known CI warning (and why it’s acceptable)

Some runners may show a PyTorch/NumPy warning (environment-specific). This does **not** affect the correctness of:

* rule engine outputs
* unit tests (AI brain is mocked)

If you ever choose to enable AI scanning in CI, this can be addressed by pinning compatible versions.

---

## Quality gates (what “passing” means)

A green CI run means:

* Configuration parsing is correct
* Rule engine flags violations correctly
* AI scanner decision logic behaves correctly (mocked brain)
* Evidence tables are generated consistently

<div class="evidence">
  <div class="evidence__label">Actions tab — succeeded</div>
  <div class="img-container">
    <a href="{{ '/assets/screenshots/e2-github-actions-success.png' | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ '/assets/screenshots/e2-github-actions-success.png' | relative_url }}" alt="Actions tab showing succeeded">
    </a>
  </div>
</div>
```
