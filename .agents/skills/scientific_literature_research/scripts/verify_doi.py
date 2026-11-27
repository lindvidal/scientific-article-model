"""Verify DOIs or search peer-reviewed articles via Crossref API and format APA 7th citations."""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request

CROSSREF_WORKS = "https://api.crossref.org/works"
USER_AGENT = "ScientificArticleModelLitVerify/1.0 (mailto:corresponding.author@example.edu)"


def _fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _format_authors_apa(authors: list[dict]) -> str:
    formatted: list[str] = []
    for a in authors:
        family = (a.get("family") or "").strip()
        given = (a.get("given") or "").strip()
        initials = " ".join(f"{part[0]}." for part in re.split(r"[\s-]+", given) if part)
        if family and initials:
            formatted.append(f"{family}, {initials}")
        elif family:
            formatted.append(family)
    if not formatted:
        return "Unknown Author"
    if len(formatted) == 1:
        return formatted[0]
    if len(formatted) <= 20:
        return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"
    return ", ".join(formatted[:19]) + f", ... {formatted[-1]}"


def _extract_year(item: dict) -> str:
    for key in ("published-print", "published-online", "issued", "created"):
        parts = item.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            return str(parts[0][0])
    return "n.d."


def format_crossref_apa(item: dict) -> str:
    """Format a Crossref work JSON dictionary into APA 7th style."""
    authors = _format_authors_apa(item.get("author", []))
    year = _extract_year(item)
    title = (item.get("title") or ["Untitled"])[0].strip().rstrip(".")
    journal = (item.get("container-title") or ["Unknown Journal"])[0].strip()
    volume = item.get("volume", "")
    issue = item.get("issue", "")
    page = item.get("page") or item.get("article-number") or ""
    doi = item.get("DOI", "")

    vol_str = f"*{journal}*"
    if volume:
        vol_str += f", {volume}"
        if issue:
            vol_str += f"({issue})"
    if page:
        vol_str += f", {page}"
    doi_url = f"https://doi.org/{doi}" if doi else ""
    return f"{authors} ({year}). {title}. {vol_str}. {doi_url}".strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify DOIs or search Crossref for APA 7th citations.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doi", help="Exact DOI (e.g. 10.1016/j.jhydrol.2009.08.003)")
    group.add_argument("--query", help="Bibliographic search query (title/authors/year)")
    parser.add_argument("--rows", type=int, default=5, help="Number of results for --query (default: 5)")
    args = parser.parse_args()

    if args.doi:
        doi_clean = args.doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
        url = f"{CROSSREF_WORKS}/{urllib.parse.quote(doi_clean, safe='')}"
        data = _fetch_json(url)
        item = data["message"]
        print(format_crossref_apa(item))
        return 0

    params = urllib.parse.urlencode({"query.bibliographic": args.query, "rows": args.rows})
    data = _fetch_json(f"{CROSSREF_WORKS}?{params}")
    items = data.get("message", {}).get("items", [])
    for idx, item in enumerate(items, 1):
        print(f"[{idx}] {format_crossref_apa(item)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
