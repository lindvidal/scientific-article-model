"""Audit and synchronize technical and scientific documentation across Scientific-Article-Model."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def check_requirements_parity() -> list[str]:
    """Verify requirements.txt lines match the mirrored block in README.md."""
    errors: list[str] = []
    req_path = PROJECT_ROOT / "requirements.txt"
    readme_path = PROJECT_ROOT / "README.md"
    if not req_path.exists() or not readme_path.exists():
        return ["Missing requirements.txt or README.md"]

    req_lines = [
        line.strip()
        for line in req_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    readme_text = readme_path.read_text(encoding="utf-8")
    match = re.search(
        r"### Dependencies.*?```text\r?\n(.*?)```",
        readme_text,
        flags=re.DOTALL,
    )
    if not match:
        errors.append("Could not locate '### Dependencies' code block in README.md")
        return errors

    readme_deps = [
        line.strip()
        for line in match.group(1).splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    missing_in_readme = sorted(set(req_lines) - set(readme_deps))
    extra_in_readme = sorted(set(readme_deps) - set(req_lines))
    if missing_in_readme:
        errors.append(f"Packages in requirements.txt missing from README.md: {missing_in_readme}")
    if extra_in_readme:
        errors.append(f"Packages in README.md missing from requirements.txt: {extra_in_readme}")
    return errors


def check_notebook_inventory() -> list[str]:
    """Verify active notebooks/*.ipynb have corresponding summaries and README listings."""
    errors: list[str] = []
    nb_dir = PROJECT_ROOT / "notebooks"
    summary_dir = PROJECT_ROOT / "docs" / "summary"
    readme_text = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    notebooks = sorted(
        nb.stem for nb in nb_dir.glob("*.ipynb") if ".ipynb_checkpoints" not in str(nb)
    )
    for stem in notebooks:
        summary_file = summary_dir / f"{stem}_summary.txt"
        if not summary_file.exists():
            errors.append(f"Missing notebook summary: docs/summary/{stem}_summary.txt")
        if f"{stem}.ipynb" not in readme_text:
            errors.append(f"Notebook not listed in README.md: {stem}.ipynb")
    return errors


def run_compile_nbs() -> int:
    """Execute scripts/compile_nbs.py to refresh docs/telemetry/nb_compiled_phase_*.txt."""
    script = PROJECT_ROOT / "scripts" / "compile_nbs.py"
    res = subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    print(res.stdout.strip())
    if res.returncode != 0:
        print(res.stderr.strip(), file=sys.stderr)
    return res.returncode


def run_manuscript_qa() -> int:
    """Execute validate_manuscript.py --strict."""
    script = (
        PROJECT_ROOT
        / ".agents"
        / "skills"
        / "manuscript_qa"
        / "scripts"
        / "validate_manuscript.py"
    )
    res = subprocess.run(
        [sys.executable, str(script), "--strict"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    print(res.stdout.strip())
    if res.returncode != 0:
        print(res.stderr.strip(), file=sys.stderr)
    return res.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Scientific-Article-Model documentation & manuscript sync.")
    parser.add_argument(
        "--compile-nbs",
        action="store_true",
        help="Recompile notebook code cells into docs/telemetry/nb_compiled_phase_*.txt.",
    )
    args = parser.parse_args()

    all_errors: list[str] = []

    if args.compile_nbs:
        print("── Compiling Notebook Sources ──")
        if run_compile_nbs() != 0:
            all_errors.append("compile_nbs.py failed")

    print("── Checking Requirements & README Parity ──")
    req_errors = check_requirements_parity()
    if req_errors:
        all_errors.extend(req_errors)
        for err in req_errors:
            print(f"ERROR   {err}")
    else:
        print("OK      requirements.txt and README.md dependency blocks match.")

    print("── Checking Notebook & Summary Inventory ──")
    nb_errors = check_notebook_inventory()
    if nb_errors:
        all_errors.extend(nb_errors)
        for err in nb_errors:
            print(f"ERROR   {err}")
    else:
        print("OK      All active notebooks are documented in README.md and docs/summary/.")

    print("── Running Strict Manuscript QA ──")
    if run_manuscript_qa() != 0:
        all_errors.append("validate_manuscript.py --strict reported issues")

    if all_errors:
        print(f"\nFAILED  {len(all_errors)} documentation audit issue(s) found.")
        return 1

    print("\nOK      All technical and scientific documentation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
