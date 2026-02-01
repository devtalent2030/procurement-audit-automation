import sys
from pathlib import Path

# Ensure repo root is importable no matter what directory tests chdir() into.
ROOT = Path(__file__).resolve().parents[1]  # repo root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
