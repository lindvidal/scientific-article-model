"""Analyze manuscript word counts (prose vs. tables/math/captions/refs) and JoH limits."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")
CAPTION_RE = re.compile(r"^\*\*Figure\s+(\d+)\.\*\*\s*(.+)$")
IMAGE_RE = re.compile(r"^!\[[^\]]*\]\([^)]+\)\s*$")
HIGHLIGHT_BULLET_RE = re.compile(r"^\s*[-*]\s+(.+)$")


def _count_words(text: str) -> int:
    return len(text.split())


def analyze_markdown(md_path: Path, max_caption_words: int = 45) -> dict:
    """Compute prose, table, caption/math, total body, and total file word counts."""
    raw = md_path.read_text(encoding="utf-8")
    body = raw.split("\n---\n", 1)[0]

    prose_lines: list[str] = []
    table_lines: list[str] = []
    caption_math_lines: list[str] = []
    long_captions: list[tuple[str, int]] = []

    in_display_math = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("$$"):
            caption_math_lines.append(line)
            if not (stripped.endswith("$$") and len(stripped) > 2):
                in_display_math = not in_display_math
            continue
        if in_display_math:
            caption_math_lines.append(line)
            continue

        cap_match = CAPTION_RE.match(stripped)
        if cap_match:
            caption_math_lines.append(line)
            cap_words = _count_words(cap_match.group(2))
            if cap_words > max_caption_words:
                long_captions.append((f"Figure {cap_match.group(1)}", cap_words))
            continue

        if IMAGE_RE.match(stripped):
            caption_math_lines.append(line)
            continue

        if TABLE_LINE_RE.match(stripped):
            table_lines.append(line)
            continue

        prose_lines.append(line)

    abstract_warn = None
    abs_match = re.search(
        r"^#{1,3}\s*Abstract\b.*?\n(.*?)(?=\n#{1,3}\s|\n\*\*Keywords|\Z)",
        body,
        flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
    )
    if abs_match:
        abs_words = _count_words(abs_match.group(1))
        if abs_words > 250:
            abstract_warn = f"Abstract has {abs_words} words (limit <= 250)"

    highlight_warns: list[str] = []
    hl_match = re.search(
        r"^#{1,3}\s*Highlights\b.*?\n(.*?)(?=\n#{1,3}\s|\Z)",
        body,
        flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
    )
    if hl_match:
        for idx, hline in enumerate(hl_match.group(1).splitlines(), 1):
            bm = HIGHLIGHT_BULLET_RE.match(hline)
            if bm:
                chars = len(bm.group(1).strip())
                if chars > 85:
                    highlight_warns.append(f"Highlight #{idx} has {chars} chars (limit <= 85)")

    return {
        "name": md_path.name,
        "prose": _count_words("\n".join(prose_lines)),
        "tables": _count_words("\n".join(table_lines)),
        "captions_math": _count_words("\n".join(caption_math_lines)),
        "body_total": _count_words(body),
        "file_total": _count_words(raw),
        "long_captions": long_captions,
        "abstract_warn": abstract_warn,
        "highlight_warns": highlight_warns,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Count manuscript prose, table, caption/math, and total words."
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Path to a Markdown file or directory containing ms_*.md sections.",
    )
    parser.add_argument(
        "--max-caption-words",
        type=int,
        default=45,
        help="Maximum caption body word threshold (default: 45).",
    )
    args = parser.parse_args()

    target = args.target.resolve()
    if target.is_dir():
        files = sorted(target.glob("ms_*.md"))
        if not files:
            files = sorted(p for p in target.glob("*.md") if not p.name.endswith("_HIGHLIGHTED.md"))
    else:
        files = [target]

    if not files:
        print(f"No Markdown files found in {target}")
        return 1

    results = [analyze_markdown(f, max_caption_words=args.max_caption_words) for f in files]

    header = f"{'File':<58} {'Prose':>7} {'Tables':>7} {'Cap/Math':>8} {'Body':>7} {'Total':>7}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(
            f"{r['name'][:57]:<58} {r['prose']:>7,} {r['tables']:>7,} "
            f"{r['captions_math']:>8,} {r['body_total']:>7,} {r['file_total']:>7,}"
        )
    print("-" * len(header))
    print(
        f"{'TOTAL':<58} "
        f"{sum(r['prose'] for r in results):>7,} "
        f"{sum(r['tables'] for r in results):>7,} "
        f"{sum(r['captions_math'] for r in results):>8,} "
        f"{sum(r['body_total'] for r in results):>7,} "
        f"{sum(r['file_total'] for r in results):>7,}"
    )

    warnings: list[str] = []
    for r in results:
        for fig, wc in r["long_captions"]:
            warnings.append(f"[CAPTION] {r['name']} {fig}: {wc} words (> {args.max_caption_words})")
        if r["abstract_warn"]:
            warnings.append(f"[ABSTRACT] {r['name']}: {r['abstract_warn']}")
        for hw in r["highlight_warns"]:
            warnings.append(f"[HIGHLIGHT] {r['name']}: {hw}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  {w}")
    else:
        print("\nOK: All captions, abstracts, and highlights within checked thresholds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
