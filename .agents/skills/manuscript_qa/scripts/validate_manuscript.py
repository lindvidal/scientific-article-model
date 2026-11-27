"""Automated QA validator for Scientific-Article-Model manuscript section Markdowns."""

from __future__ import annotations

import argparse
import html
import re
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
SECTIONS_DIR = PROJECT_ROOT / "docs" / "manuscript" / "sections"
HIGHLIGHTED_DIR = SECTIONS_DIR / "highlighted"

SECTION_ORDER = [
    "ms_1_Introduction.md",
    "ms_2_Study_Area.md",
    "ms_3_0_Methodology_Intro.md",
    "ms_3_1_Reference_sub_daily_rainfall_dataset.md",
    "ms_3_2_Spatial_Feature_Engineering_and_Predictor_Matrix_Construction.md",
    "ms_3_3_Algorithm_Selection_and_Hyperparameter_Optimization.md",
    "ms_3_4_Multi_Objective_Performance_Evaluation.md",
    "ms_4_0_Results_and_Discussion_Intro.md",
    "ms_4_1_Overall_Model_Performance_and_Comparative_Deltas.md",
    "ms_4_2_Statistical_Significance_of_Performance_Differences.md",
    "ms_4_3_Geospatial_Patterns_and_Error_Stratification.md",
    "ms_4_4_Physical_and_Spatial_Mechanisms.md",
    "ms_4_5_Confrontation_with_International_Literature.md",
    "ms_4_6_Limitations_and_Uncertainty_Sources.md",
    "ms_5_1_Main_Findings_and_Model_Recommendations.md",
    "ms_5_2_Future_Research_Directions.md",
]

BROKEN_FEATURE_TOKENS = (
    r"\bain_mm_\w+",
    r"\bertical_dist_\w+",
    r"\bearing(?:_sin|_cos)?\b",
)


def check_figure_links(files: list[Path]) -> tuple[list[str], int]:
    """Verify every Markdown image embed exists on disk and avoids legacy folders."""
    errors: list[str] = []
    count = 0
    pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    for md in files:
        for line_no, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for target in pattern.findall(line):
                count += 1
                if "4 - Figures" in target:
                    errors.append(f"[LINK] {md.name}:{line_no} uses legacy path: {target}")
                resolved = (md.parent / target).resolve()
                if not resolved.exists():
                    errors.append(f"[LINK] {md.name}:{line_no} missing target: {target}")
    return errors, count


def check_figure_captions(canonical_files: list[Path]) -> list[str]:
    """Verify unique figure captions progress sequentially and stay concise."""
    warnings: list[str] = []
    seen_captions: list[tuple[str, int]] = []
    max_caption_words = 45
    caption_re = re.compile(r"^(?:\*\*Figure\s+(\d+)\.\*\*|!\[Figure\s+(\d+):)")
    bold_caption_re = re.compile(r"^\*\*Figure\s+(\d+)\.\*\*\s*(.+)$")
    for md in canonical_files:
        for line in md.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            match = caption_re.match(stripped)
            if not match:
                continue
            bold_match = bold_caption_re.match(stripped)
            if bold_match:
                word_count = len(bold_match.group(2).split())
                if word_count > max_caption_words:
                    warnings.append(
                        f"[FIG-LEN] {md.name} Figure {bold_match.group(1)} caption has {word_count} words (target <= {max_caption_words})"
                    )
            num = int(match.group(1) or match.group(2))
            if md.name.startswith("ms_S"):
                continue
            if seen_captions and seen_captions[-1][1] == num:
                continue
            seen_captions.append((md.name, num))

    expected = 1
    for fname, num in seen_captions:
        if num != expected:
            warnings.append(f"[FIG-SEQ] {fname} caption has Figure {num}, expected Figure {expected}")
        expected = num + 1
    return warnings


def _extract_sort_key(cite: str) -> tuple[str, int, str]:
    """Return (folded_surname, multi_author_rank, folded_full) for APA alphabetical checks."""
    cleaned = re.sub(r"^(?:[A-Z]\.\s+)+", "", cite.strip())
    first_segment = cleaned.split(",")[0].strip()
    is_multi = 1 if (" et al." in first_segment or " & " in first_segment or " and " in first_segment) else 0
    surname = re.split(r"\s+(?:et al\.|&|and)\b", first_segment)[0].strip()
    folded_surname = unicodedata.normalize("NFKD", surname).encode("ascii", "ignore").decode("ascii").lower()
    folded_full = unicodedata.normalize("NFKD", cleaned).encode("ascii", "ignore").decode("ascii").lower()
    return folded_surname, is_multi, folded_full


def check_citations(canonical_files: list[Path]) -> list[str]:
    """Flag descending years, semicolon same-author years, ordering, '&' vs 'and', diacritics, and bold citations."""
    warnings: list[str] = []
    paren_re = re.compile(r"\(([A-ZÀ-ÿ][^()]*\d{4}[^()]*)\)")
    multi_year_re = re.compile(r"\b(\d{4})\s*([,;])\s*(\d{4})\b")
    bold_cite_re = re.compile(r"\*\*[A-ZÀ-ÿ][^*()]*\(\d{4}[a-z]?\)\*\*")
    for md in canonical_files:
        for line_no, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if not re.match(r"^\s*\d+\.\s+\*\*", line):
                for bold_match in bold_cite_re.findall(line):
                    warnings.append(f"[CITE] {md.name}:{line_no} bolded narrative citation: {bold_match}")
            for group in paren_re.findall(line):
                if re.search(r"\b(?:Demsar|Garcia)\b", group):
                    warnings.append(f"[CITE] {md.name}:{line_no} missing diacritics (Demšar/García): ({group})")
                for y1, sep, y2 in multi_year_re.findall(group):
                    if sep == ";":
                        warnings.append(f"[CITE] {md.name}:{line_no} semicolon between years: {y1}; {y2}")
                    if int(y1) > int(y2):
                        warnings.append(f"[CITE] {md.name}:{line_no} descending years: {y1}, {y2}")
                parts = [p.strip() for p in group.split(";") if re.search(r"[A-Za-zÀ-ÿ].*\d{4}", p)]
                for part in parts:
                    if re.search(r"^[A-ZÀ-ÿ][^,;]+?\s+&\s+[A-ZÀ-ÿ]", part):
                        warnings.append(f"[CITE] {md.name}:{line_no} use 'and' instead of '&' in in-text citations: {part}")
                if len(parts) > 1:
                    keys = [_extract_sort_key(p) for p in parts]
                    if keys != sorted(keys):
                        warnings.append(f"[CITE] {md.name}:{line_no} non-alphabetical group: ({group})")
    return warnings


def check_corrupted_tokens(canonical_files: list[Path]) -> list[str]:
    """Detect missing leading-character feature names caused by unescaped backslashes."""
    errors: list[str] = []
    regex = re.compile("|".join(BROKEN_FEATURE_TOKENS))
    for md in canonical_files:
        for line_no, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for match in regex.findall(line):
                errors.append(f"[TOKEN] {md.name}:{line_no} truncated identifier '{match}'")
    return errors


def check_dash_hygiene(canonical_files: list[Path]) -> list[str]:
    """Flag en-dashes (U+2013) or em-dashes (U+2014) in the body of canonical manuscript sections."""
    warnings: list[str] = []
    for md in canonical_files:
        body = md.read_text(encoding="utf-8-sig").split("\n---\n", 1)[0]
        for line_no, line in enumerate(body.splitlines(), 1):
            if "\u2013" in line or "\u2014" in line:
                warnings.append(
                    f"[DASH-HYGIENE] {md.name}:{line_no} contains en-dash (–) or em-dash (—) in prose/table body"
                )
    return warnings


def _strip_highlighted_to_canonical(full_section_text: str) -> str:
    """Strip styled Word-diff tags from a Level-2 highlighted body for parity checks."""
    body = full_section_text.split("\n---\n", 1)[0]
    clean = re.sub(r"<del[^>]*>.*?</del>", "", body, flags=re.DOTALL)
    clean = re.sub(r"```latex\r?\n.*?\r?\n```\s*", "", clean, flags=re.DOTALL)
    clean = re.sub(r"<mark[^>]*>\[Quebra de (?:parágrafo|linha)\]</mark>\s*", "", clean)
    clean = clean.replace("<strong>", "**").replace("</strong>", "**")
    clean = clean.replace("<code>", "`").replace("</code>", "`")
    clean = clean.replace("<em>", "*").replace("</em>", "*")
    clean = re.sub(r"</?mark[^>]*>", "", clean)
    clean = html.unescape(clean)
    clean = clean.replace(r"\*", "*")
    clean = re.sub(r" {2,}", " ", clean)
    clean = re.sub(r"(?<!\|) ([.,;:])", r"\1", clean)
    clean = clean.replace("( ", "(")
    clean = "\n".join(line.strip() for line in clean.splitlines())
    clean = re.sub(r"\n{3,}", "\n\n", clean)
    return clean.replace("(../../../../outputs/", "(../../../outputs/")


def _normalize_heading_syntax(text: str) -> str:
    """Normalize section heading level, trailing section dot, and escaped asterisks."""
    normalized = text.replace(r"\*", "*")
    return re.sub(r"^#{2,3}\s+(\d+(?:\.\d+)?)\.?\s+", r"## \1 ", normalized, flags=re.MULTILINE)


def _fold_ascii(text: str) -> str:
    """Fold Unicode diacritics to lowercase ASCII for citation matching."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower().strip()


def _extract_body_citations(body: str) -> set[tuple[str, str]]:
    """Extract normalized (lead_surname, year) pairs from parenthetical and narrative citations."""
    cites: set[tuple[str, str]] = set()
    skip_words = {
        "january",
        "february",
        "table",
        "figure",
        "section",
        "equation",
        "period",
        "holdout",
        "telemetry",
        "brazil",
        "validation",
    }

    for group in re.findall(r"\(([^()]*?\b(?:19|20)\d{2}[a-z]?[^()]*)\)", body):
        for raw_part in group.split(";"):
            part = re.sub(r"^(?:adapted from|e\.g\.,|see|after)\s+", "", raw_part.strip(), flags=re.IGNORECASE).strip()
            match = re.match(r"^([A-ZÀ-ÿ][^,\d()]+?),\s*(\d{4}[a-z]?(?:\s*,\s*\d{4}[a-z]?)*)$", part)
            if not match:
                continue
            auth_raw, years_raw = match.group(1).strip(), match.group(2)
            if any(word in auth_raw for word in ("January", "Validation", "Holdout", "Table", "Figure")):
                continue
            bracket = re.search(r"\[([A-Z0-9]+)\]", auth_raw)
            if bracket:
                key_auth = _fold_ascii(bracket.group(1))
            else:
                lead = re.split(r"\s+(?:et\s+al\.?|and|&)(?:\s|$)", auth_raw)[0].strip()
                lead = re.sub(r"^(?:[A-Z]\.\s*)+", "", lead).strip()
                key_auth = _fold_ascii(lead)
            for yr in years_raw.split(","):
                cites.add((key_auth, yr.strip()))

    narr_pat = re.compile(
        r"\b(?:[A-Z]\.\s+)?"
        r"(?P<lead>(?:(?:Di|Da|De|Van|Von|Costa|Bayer)\s+)?[A-ZÀ-ÿ][A-Za-zÀ-ÿ\-]+)"
        r"(?:\s+et\s+al\.|\s+and\s+(?:(?:Di|Da|De|Van|Von|Costa|Bayer)\s+)?[A-ZÀ-ÿ][A-Za-zÀ-ÿ\-]+)?"
        r"\s*\((?P<yrs>\d{4}[a-z]?(?:\s*,\s*\d{4}[a-z]?)*)\)"
    )
    for match in narr_pat.finditer(body):
        lead = match.group("lead").strip()
        key_auth = _fold_ascii(lead)
        if key_auth in skip_words:
            continue
        for yr in match.group("yrs").split(","):
            cites.add((key_auth, yr.strip()))
    return cites


def _extract_reference_entries(ref_block: str) -> list[tuple[set[str], str, str, bool]]:
    """Parse numbered APA reference entries into (author_aliases, year, snippet, has_url)."""
    raw_entries: list[str] = []
    cur: list[str] = []
    for line in ref_block.splitlines():
        if re.match(r"^\d+\.\s+", line.strip()):
            if cur:
                raw_entries.append("\n".join(cur))
            cur = [line.strip()]
        elif cur and (line.startswith("   ") or line.startswith("\t")):
            cur.append(line.strip())
        elif cur and not line.strip():
            raw_entries.append("\n".join(cur))
            cur = []
    if cur:
        raw_entries.append("\n".join(cur))

    parsed: list[tuple[set[str], str, str, bool]] = []
    for entry in raw_entries:
        entry_lines = entry.splitlines()
        apa_line = (
            entry_lines[1]
            if (len(entry_lines) > 1 and re.match(r"^\d+\.\s+\*\*", entry_lines[0]))
            else re.sub(r"^\d+\.\s+", "", entry)
        )
        apa_line = re.sub(r"^\d+\.\s+", "", apa_line).strip()
        year_match = re.search(r"\((\d{4}[a-z]?)\)", apa_line)
        year = year_match.group(1) if year_match else ""
        prefix = apa_line[:year_match.start()].strip() if year_match else apa_line
        aliases = {_fold_ascii(br) for br in re.findall(r"\[([A-Z0-9]+)\]", prefix)}
        aliases.add(_fold_ascii(prefix.split(",")[0].strip()))
        has_url = bool(re.search(r"https?://\S+", entry))
        parsed.append((aliases, year, apa_line[:70], has_url))
    return parsed


def check_section_references(
    canonical_files: list[Path],
    highlighted_files: list[Path],
) -> tuple[list[str], list[str]]:
    """Verify every section ends with a verified reference block matching in-text citations 1-to-1."""
    errors: list[str] = []
    warnings: list[str] = []
    canonical_counts: dict[str, int] = {}

    for md in canonical_files:
        text = md.read_text(encoding="utf-8-sig")
        if "\n---\n" not in text:
            errors.append(f"[REF-BLOCK] {md.name} missing '\\n---\\n' end-of-document references separator")
            continue
        body, ref_block = text.split("\n---\n", 1)
        if not re.search(r"^###\s+References\s+Cited\s+in\s+(?:Section|Supplementary Material)\b", ref_block, flags=re.MULTILINE):
            errors.append(f"[REF-BLOCK] {md.name} missing '### References Cited in Section ...' heading")
            continue

        cites = _extract_body_citations(body)
        refs = _extract_reference_entries(ref_block)
        canonical_counts[md.name] = len(refs)

        if not cites and not refs:
            if not re.search(r"\*No direct in-text citations appear\b", ref_block):
                warnings.append(f"[REF-BLOCK] {md.name} has 0 citations; document with explicit zero-citation note")
            continue

        for auth, yr in sorted(cites):
            if not any((auth in aliases and yr == ref_yr) for aliases, ref_yr, _, _ in refs):
                errors.append(f"[REF-MISS] {md.name} cites '{auth} ({yr})' in prose without a matching reference entry")

        for aliases, ref_yr, snippet, has_url in refs:
            if not any((ca in aliases and cy == ref_yr) for ca, cy in cites):
                warnings.append(f"[REF-ORPHAN] {md.name} lists uncited reference ({ref_yr}): {snippet}")
            if not has_url:
                errors.append(f"[REF-URL] {md.name} reference missing DOI/publication URL: {snippet}")

    marker_re = re.compile(r"^## 2\. (?:Texto Completo|Full Section Text)[^\n]*\n\n", flags=re.MULTILINE)
    for hi in highlighted_files:
        text = hi.read_text(encoding="utf-8-sig")
        split_match = marker_re.search(text)
        if not split_match:
            continue
        section_body_onwards = text[split_match.end():]
        if "\n---\n" not in section_body_onwards:
            errors.append(f"[REF-BLOCK] {hi.name} missing '\\n---\\n' end-of-document references separator")
            continue
        _, hi_ref_block = section_body_onwards.split("\n---\n", 1)
        if not re.search(r"^##\s+3\.\s+(?:Referências|References)\b", hi_ref_block, flags=re.MULTILINE):
            errors.append(f"[REF-BLOCK] {hi.name} missing '## 3. Referências ...' heading")
            continue
        hi_refs = _extract_reference_entries(hi_ref_block)
        canonical_name = hi.name.replace("_HIGHLIGHTED.md", ".md")
        expected_count = canonical_counts.get(canonical_name)
        if expected_count is not None and len(hi_refs) != expected_count:
            errors.append(
                f"[REF-SYNC] {hi.name} lists {len(hi_refs)} reference(s), expected {expected_count} matching {canonical_name}"
            )

    return errors, warnings


def check_highlighted_guides(highlighted_files: list[Path]) -> tuple[list[str], list[str]]:
    """Verify styled red/yellow formatting and exact parity with canonical ms_*.md."""
    errors: list[str] = []
    warnings: list[str] = []
    marker_re = re.compile(r"^## 2\. (?:Texto Completo|Full Section Text)[^\n]*\n\n", flags=re.MULTILINE)
    for hi in highlighted_files:
        text = hi.read_text(encoding="utf-8-sig")
        if "<ins>" in text or re.search(r"<del>", text):
            warnings.append(f"[STYLE] {hi.name} uses bare <ins>/<del> instead of red/yellow inline styles")
        split_match = marker_re.search(text)
        if not split_match:
            continue
        canonical_name = hi.name.replace("_HIGHLIGHTED.md", ".md")
        canonical_path = SECTIONS_DIR / canonical_name
        if not canonical_path.exists():
            errors.append(f"[PARITY] Missing canonical file for {hi.name}: {canonical_name}")
            continue
        stripped = _normalize_heading_syntax(_strip_highlighted_to_canonical(text[split_match.end():]).strip())
        canonical_body = canonical_path.read_text(encoding="utf-8-sig").split("\n---\n", 1)[0].strip()
        canonical_lines = "\n".join(line.strip() for line in re.sub(r" {2,}", " ", canonical_body).splitlines())
        canonical_norm = _normalize_heading_syntax(re.sub(r"\n{3,}", "\n\n", canonical_lines))
        if stripped != canonical_norm:
            errors.append(f"[PARITY] {hi.name} stripped body does not match {canonical_name}")
    return errors, warnings


def main() -> int:
    """Run all manuscript QA checks and print a concise diagnostic report."""
    parser = argparse.ArgumentParser(description="Validate Scientific-Article-Model manuscript sections.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on warnings as well as errors.")
    args = parser.parse_args()

    canonical_files = sorted(p for p in SECTIONS_DIR.glob("ms_*.md") if not p.name.startswith("ms_S")) if SECTIONS_DIR.exists() else []
    if (SECTIONS_DIR / "ms_S1_Supplementary_Material.md").exists():
        canonical_files.append(SECTIONS_DIR / "ms_S1_Supplementary_Material.md")
    highlighted_files = sorted(HIGHLIGHTED_DIR.glob("*_HIGHLIGHTED.md")) if HIGHLIGHTED_DIR.exists() else []

    errors: list[str] = []
    warnings: list[str] = []

    link_errors, link_count = check_figure_links(canonical_files + highlighted_files)
    errors.extend(link_errors)
    errors.extend(check_corrupted_tokens(canonical_files))
    warnings.extend(check_figure_captions(canonical_files))
    warnings.extend(check_citations(canonical_files))
    warnings.extend(check_dash_hygiene(canonical_files))

    hi_errors, hi_warnings = check_highlighted_guides(highlighted_files)
    errors.extend(hi_errors)
    warnings.extend(hi_warnings)

    ref_errors, ref_warnings = check_section_references(canonical_files, highlighted_files)
    errors.extend(ref_errors)
    warnings.extend(ref_warnings)

    print(f"Checked {len(canonical_files)} canonical section(s), {len(highlighted_files)} highlighted guide(s), {link_count} image embed(s).")
    for item in errors:
        print(f"ERROR   {item}")
    for item in warnings:
        print(f"WARNING {item}")

    if not errors and not warnings:
        print("OK      All checks passed.")
        return 0
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
