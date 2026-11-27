"""Helper CLI for sequential autocommit version inspection and GitHub telemetry sync."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def run_git(*args: str) -> str:
    """Run a read-only git command inside PROJECT_ROOT and return stripped stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_version_info() -> tuple[int, int]:
    """Return (last_version, next_version) parsed from the latest v0000 - <summary> commit."""
    latest = run_git("log", "-n", "10", "--oneline")
    match = re.search(r"\bv(\d+)\s*-\s*", latest)
    last_v = int(match.group(1)) if match else 0
    return last_v, last_v + 1


def main() -> int:
    """Inspect working tree / versions or regenerate GitHub telemetry CSV/DOCX logs."""
    parser = argparse.ArgumentParser(description="Autocommit version inspector & telemetry generator.")
    parser.add_argument("--dry-run", action="store_true", help="Print next sequential versions and git status without writing telemetry.")
    args = parser.parse_args()

    last_v, next_v = get_version_info()
    status = run_git("status", "--short")
    print(f"Latest version : v{last_v:04d}")
    print(f"Next primary   : v{next_v:04d}")
    print(f"Next telemetry : v{next_v + 1:04d}")
    print(f"Working tree   :\n{status or '  (clean)'}")

    if args.dry_run:
        return 0

    os.environ["PROJECT_ROOT"] = str(PROJECT_ROOT).replace("\\", "/")
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from scripts.github_logger import generate_git_log

    generate_git_log()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
