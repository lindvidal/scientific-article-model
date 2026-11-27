# Notebook Environment & Agent Standard

Whenever creating or refactoring a Jupyter Notebook in this repository, use this exact canonical first code cell so notebooks execute identically on local machines and Google Colab:

```python
# ── Environment & Path Setup ───────────────────────────────────────────────
import sys
import os
from pathlib import Path

try:
    import google.colab
    IN_COLAB = True
    from google.colab import drive
    drive.mount("/content/drive", force_remount=True)
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    _root = Path("/content/drive/MyDrive/Projetos/Scientific-Article-Model")
else:
    _root = Path.cwd().parent if Path.cwd().name in ("notebooks", "src", "scripts") else Path.cwd()

for _p in [_root / "src"]:
    if _p.exists() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

DATA_RAW       = _root / "data" / "raw"
DATA_PROCESSED = _root / "data" / "processed"
FIGURES_PATH   = _root / "outputs" / "figures" / "manuscript"

print(f"Run mode    : {'Colab' if IN_COLAB else 'Local'}")
print(f"PROJECT_ROOT: {_root}")
```
