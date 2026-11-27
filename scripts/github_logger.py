"""Generate git commit and active notebook telemetry in docs/telemetry/."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
TELEMETRY_DIR = ROOT / "docs" / "telemetry"


def generate_git_log() -> None:
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(
        ["git", "log", "-n", "50", "--pretty=format:%h|%ad|%an|%s", "--date=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    rows = [line.split("|", 3) for line in res.stdout.splitlines() if "|" in line]

    csv_path = TELEMETRY_DIR / "log_github_lastrun.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["hash", "date", "author", "subject"])
        writer.writerows(rows)

    doc = Document()
    doc.add_heading("Repository Git Telemetry", level=1)
    for h, d, a, s in rows:
        doc.add_paragraph(f"{d} | {h} | {a} | {s}")

    doc.add_heading("Active Notebooks", level=2)
    for nb in sorted((ROOT / "notebooks").glob("*.ipynb")):
        doc.add_paragraph(nb.name)
    doc.save(TELEMETRY_DIR / "log_github_lastrun.docx")
