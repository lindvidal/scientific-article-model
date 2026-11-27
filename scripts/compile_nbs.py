"""Compile Python code cells from notebooks/*.ipynb into docs/telemetry/nb_compiled_phase_*.txt."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
OUT_DIR = ROOT / "docs" / "telemetry"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    buckets: dict[str, list[str]] = {}
    for nb_path in sorted(NB_DIR.glob("*.ipynb")):
        if ".ipynb_checkpoints" in str(nb_path):
            continue
        phase = nb_path.stem.split(".")[0] if "." in nb_path.stem else "0"
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        lines = [f"# === {nb_path.name} ==="]
        for idx, cell in enumerate(data.get("cells", []), 1):
            if cell.get("cell_type") == "code":
                lines.append(f"# --- Cell {idx} ---")
                lines.append("".join(cell.get("source", [])))
        buckets.setdefault(phase, []).append("\n".join(lines))

    for phase, blocks in sorted(buckets.items()):
        out_file = OUT_DIR / f"nb_compiled_phase_{phase}.txt"
        out_file.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
        print(f"Compiled {out_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
