#!/usr/bin/env bash
set -euo pipefail

# ============================================
# Procurement Audit Automation - One-Command Demo
# - Generate dirty data
# - Run rule engine
# - Run AI auditor (optional via SKIP_AI=1)
# - Run unit tests
# - Print evidence locations (for recording)
# ============================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

TS="$(date +"%Y%m%d_%H%M%S")"
LOG_DIR="data/audit_reports/run_logs"
EVID_DIR="data/audit_reports"
RAW_DIR="data/raw_erp_dump"

mkdir -p "$LOG_DIR" "$EVID_DIR" "$RAW_DIR"

echo "============================================================"
echo "🚀 Procurement Audit Automation - FULL DEMO RUN"
echo "Timestamp: $TS"
echo "Repo: $ROOT_DIR"
echo "============================================================"
echo ""

echo "🧪 Environment"
python --version
echo ""

# 1) Generate dirty data
echo "------------------------------------------------------------"
echo "1) 🧬 Generating dirty ERP data..."
echo "Command: python src/data_generator.py"
echo "------------------------------------------------------------"
python src/data_generator.py | tee "$LOG_DIR/01_data_generator_$TS.log"
echo ""

# Sanity check output files exist
if [[ ! -f "$RAW_DIR/invoices.xlsx" ]]; then
  echo "❌ Missing expected file: $RAW_DIR/invoices.xlsx"
  exit 1
fi

if [[ ! -f "$RAW_DIR/vendor_master.csv" ]]; then
  echo "❌ Missing expected file: $RAW_DIR/vendor_master.csv"
  exit 1
fi

echo "✅ Generated:"
echo "   - $RAW_DIR/invoices.xlsx"
echo "   - $RAW_DIR/vendor_master.csv"
echo ""

# 2) Run rule engine
echo "------------------------------------------------------------"
echo "2) ⚙️ Running Rule Engine (Ghost Vendors + PO Variance)..."
echo "Command: python src/rule_engine.py"
echo "------------------------------------------------------------"
python src/rule_engine.py | tee "$LOG_DIR/02_rule_engine_$TS.log"
echo ""

# 3) Run AI auditor (optional)
echo "------------------------------------------------------------"
echo "3) 🤖 AI Auditor (FOIP/PII scan on Notes)"
echo "Command: python src/ai_auditor.py"
echo "------------------------------------------------------------"

if [[ "${SKIP_AI:-0}" == "1" ]]; then
  echo "⏭️  Skipping AI auditor (SKIP_AI=1)"
  echo "⏭️  Tip: run locally with ./run_audit.sh (no SKIP_AI) to include AI"
else
  python src/ai_auditor.py | tee "$LOG_DIR/03_ai_auditor_$TS.log"
fi
echo ""

# 4) Run tests
echo "------------------------------------------------------------"
echo "4) ✅ Running Unit Tests (pytest)..."
echo "Command: pytest -q"
echo "------------------------------------------------------------"
pytest -q | tee "$LOG_DIR/04_pytest_$TS.log"
echo ""

# Summary + evidence pointers
echo "============================================================"
echo "✅ FULL DEMO COMPLETE"
echo "============================================================"
echo ""
echo "📌 Evidence files for your screenshots / videos:"
echo "  Raw inputs:"
echo "   - $RAW_DIR/invoices.xlsx"
echo "   - $RAW_DIR/vendor_master.csv"
echo ""
echo "  Reports:"
if [[ -f "$EVID_DIR/ai_risk_findings.csv" ]]; then
  echo "   - $EVID_DIR/ai_risk_findings.csv"
else
  echo "   - (No ai_risk_findings.csv found yet — AI auditor may have been skipped or found 0 items)"
fi
echo ""
echo "  Run logs:"
echo "   - $LOG_DIR/01_data_generator_$TS.log"
echo "   - $LOG_DIR/02_rule_engine_$TS.log"
if [[ "${SKIP_AI:-0}" == "1" ]]; then
  echo "   - (AI skipped — no 03_ai_auditor log)"
else
  echo "   - $LOG_DIR/03_ai_auditor_$TS.log"
fi
echo "   - $LOG_DIR/04_pytest_$TS.log"
echo ""
echo "🎥 Optional UI demo (separate recording):"
echo "   streamlit run app/dashboard.py"
echo ""
echo "Done."
