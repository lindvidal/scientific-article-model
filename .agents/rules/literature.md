# Rule: Literature Anti-Hallucination & Verification

**Behavioral Constraints:**
1. NEVER cite an academic paper, author list, journal name, or DOI from internal LLM memory without verifying it in the current session.
2. Whenever discovering literature, auditing references, or drafting citations, use `scientific_literature_research` (`verify_doi.py` via Crossref API / OpenAlex / web verification) to retrieve real metadata.
3. **Database & Tier Priority:** Prioritize peer-reviewed **Q1 journal articles** indexed in Scopus, Web of Science, ScienceDirect, Nature, Springer, Wiley, or IEEE Xplore. Use **Q2** journals only when no suitable Q1 source exists. Exclude non-peer-reviewed grey literature, preprints, or technical reports unless they are mandatory official institutional/measurement standards (e.g., ISO, WMO, national statistics bureaus).
4. Every reference entry in documentation or manuscript sections MUST include its verified `https://doi.org/...` URL (or official repository/publisher URL when a DOI does not exist) and full italicized journal name.
5. Never fabricate Journal Impact Factors or citation counts.
6. **Project Registry & In-Text Formatting:** Maintain curated verified entries in `docs/references/master_literature_review.txt`. Format multi-year same-author citations chronologically ascending with commas (`(Smith et al., 2018, 2021)`), sort multi-author parenthetical groups alphabetically with single-author entries before `et al.`, use `and` cleanly (e.g., `(García and Herrera, 2008)` for Elsevier journals or strict target journal style), and preserve author diacritics.
