---
name: scientific_literature_research
description: Trigger this skill when the user requests a literature review, peer-reviewed citation discovery, DOI verification, or compilation of scientific research papers across projects.
---

# Scientific Literature Research

Follow any workspace rules (e.g., `.agents/rules/literature.md`) alongside this workflow whenever conducting literature synthesis, citation audits, or DOI verification.

## Workflow

1. **Reasoning Depth:** When delegating broad literature sweeps to a subagent via `invoke_subagent`, prefer `Model="pro"` for stronger synthesis and verification.
2. **Anti-Hallucination & Live Verification (CRITICAL):** NEVER generate citations, DOIs, journal names, or Impact Factors from memory. Verify every reference in the current session using [verify_doi.py](./scripts/verify_doi.py) (Crossref API $\rightarrow$ APA 7th), `search_web`, or OpenAlex queries.
3. **Quality Filter (Q1 First; Peer-Reviewed Journal Articles Only):**
   - Strictly prioritize **Q1 peer-reviewed journal articles** (e.g., *Journal of Hydrology*, *Water Resources Research*, *International Journal of Climatology*, *Atmospheric Research*, *Journal of Hydrometeorology*, *Nature* / *Scientific Data*).
   - Cite **Q2** journals only when no suitable Q1 paper exists; exclude technical reports (e.g., OSTI/DTIC), workshop summaries, theses, and non-peer-reviewed grey literature unless mandatory official standards/agencies (e.g., WMO, IBGE) or explicit user instructions require them.
4. **APA / Elsevier Citation Formatting:**
   - **Reference list entries:** Format in strict **APA 7th style**, including full authors, year, title, italicized journal name, volume(issue), pages/article number, and clickable DOI URL (`https://doi.org/...`).
   - **JCR Impact Factor:** Append `[Impact Factor: X.Y]` **only** when directly retrieved and verified from an authoritative source during the session—omit rather than guess.
   - **In-text sorting & conjunctions:** Sort same-author multi-year citations chronologically ascending with commas (`(Dubreuil et al., 2017, 2018)`), sort multi-author parenthetical groups alphabetically (`(Freitas et al., 2020; Gadelha et al., 2019)`, single-author entries before `et al.`), use `and` for Elsevier journals (*Journal of Hydrology*, *Atmospheric Research*) or when workspace rules specify it (and `&` inside parenthetical citations only when strict APA 7th without Elsevier override is requested), and preserve diacritics (`Demšar`, `García`).
5. **Output & Scope:** Save curated lists to the repository's designated references file (or `docs/references/`) and enforce domain/method constraints (e.g., applied environmental/hydrometeorological ML, shallow learning only when specified).
