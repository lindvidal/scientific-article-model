---
name: q1-article
description: >-
  Authors, revises, condenses, and audits Q1 scientific manuscripts, figure captions,
  and journal submission packages (including Elsevier Journal of Hydrology guidelines),
  enforcing verified metrics/DOIs, IMRaD rhetorical structure, concise figure legends,
  and 1-to-1 reference parity. Use whenever writing, editing, shortening, or auditing
  manuscript sections, abstracts, highlights, tables, or figure captions.
---

# Q1 Scientific Manuscript & Caption Authoring (`q1-article`)

Orchestrates the creation, surgical revision, condensation, and submission QA of Q1 scientific manuscripts and figure legends.
- When generating or refactoring **plots/diagrams in Python**, pair with `elsevier-figures`.
- When discovering new papers or verifying DOIs, pair with `scientific_literature_research`.

## Progressive Reference Guides & Helpers (Load Only When Needed)

- **IMRaD rhetorical tone & section requirements:** [section_styles.md](./references/section_styles.md)
- **Surgical condensation workflow:** [condensation_protocol.md](./references/condensation_protocol.md)
- **Figure caption templates & redundancy pruning:** [caption_patterns.md](./references/caption_patterns.md)
- **Executable word-count & QA helper:** [manuscript_metrics.py](./scripts/manuscript_metrics.py) (separates pure prose from Markdown tables, equations, captions, and reference blocks; checks caption/abstract/highlight limits)
- **Journal-specific profiles:**
  - *Journal of Hydrology* (Elsevier): [journal_of_hydrology.md](./references/journals/journal_of_hydrology.md) (`5,000–10,000` words, target `~8,000`; Abstract $\le 250$ words; `3–5` Highlights $\le 85$ chars; `1–7` Keywords)
  - *Atmospheric Research* (Elsevier): [atmospheric_research.md](./references/journals/atmospheric_research.md) (`6,000–10,000` words, target `~8,000`; Abstract $\le 250$ words; `3–5` Highlights $\le 85$ chars; max `6` Keywords)
  - *Water Resources Research* (AGU / Wiley): [water_resources_research.md](./references/journals/water_resources_research.md) ($\le 25$ Publication Units; Plain Language Summary $\le 200$ words; up to `3` Key Points $\le 140$ chars; mandatory Open Research DOI statement)
  - *International Journal of Climatology* (RMetS / Wiley): [international_journal_of_climatology.md](./references/journals/international_journal_of_climatology.md) (`~6,000–8,000` words typical, max `~10,000`; Abstract `200–300` words; `5–7` Keywords; mandatory Data Availability Statement)
  - *Hydrological Sciences Journal* (IAHS / Taylor & Francis): [hydrological_sciences_journal.md](./references/journals/hydrological_sciences_journal.md) (`~6,000–8,000` words typical; Abstract `200–250` words; `4–6` Keywords)

---

## 1. Manuscript Section Drafting, Revision & Condensation Workflow

### Step 1: Context Check (Targeted Interview Only If Needed)
- Do **not** fabricate missing metrics, datasets, or user intent. Confirm target section, verified numbers/notebooks, base draft/instructions, target journal profile, and active workspace rules (`GEMINI.md`, `.agents/rules/`, workspace QA skills).
- Skip redundant interviewing when the user already supplied the section, files, and goal.

### Step 2: Literature & Metric Verification (No Hallucination)
- Never invent citations, DOIs, Impact Factors, or experimental metrics. Verify every statistic directly from workspace files/outputs and every citation via `scientific_literature_research` or verified workspace catalogs.
- Strictly prioritize **Q1 peer-reviewed journal articles** (Q2 fallback only when no suitable Q1 exists; exclude grey literature/technical reports unless official standards apply).
- Enforce APA/Elsevier in-text citation formatting: ascending comma-separated years for same-author works (`2017, 2018`), alphabetical parenthetical groups (`(Gupta et al., 2009; Kling et al., 2012)`), `and` (or journal convention) consistently, and preserved author diacritics (`Demšar`, `García`).

### Step 3: Surgical Drafting, Condensation & Reference Parity
- Read [section_styles.md](./references/section_styles.md) for rhetorical structure, or [condensation_protocol.md](./references/condensation_protocol.md) when shortening a manuscript to meet journal limits (running [manuscript_metrics.py](./scripts/manuscript_metrics.py) before and after).
- Apply **surgical edits** that preserve the author's phrasing and voice wherever sound; define domain acronyms once on first appearance and use the abbreviation thereafter.
- Avoid repeating full table matrices verbatim in prose; interpret patterns, deltas, and physical/algorithmic mechanisms concisely.
- **Standalone Section Reference Parity:** When the workspace stores standalone section files (`ms_*.md` and/or `*_HIGHLIGHTED.md`), end every file with `---` followed by `### References Cited in Section X (Verified with DOIs)` in alphabetical APA 7th style with verified DOIs/URLs, maintaining strict 1-to-1 parity with in-text citations. Run any workspace QA validator (e.g., `manuscript_qa`) before finishing.

### Step 4: Plan Approval for Substantive Revisions
- For multi-section edits, major condensation passes, structural rewrites, or script additions, present a plan and wait for user approval before overwriting manuscript files.

---

## 2. Q1 Figure Legends & Captions (`20–35` words, target $\le 45$)

Whenever authoring, revising, or tightening figure captions and Markdown alt-text (read [caption_patterns.md](./references/caption_patterns.md) for archetype templates):
1. **Audit Visual Plot & Code First:** Inspect the rendered image (`read_file`) AND the plotting script/notebook cell to verify exact `*N*`/`*n*`, panel letters `(a)`, `(b)`, time windows, units, and outlier handling. Confirm no global title or caption is embedded inside the image (`elsevier-figures`).
2. **Concise Lead + Panel Structure:**
   - `**Figure N.** <What is plotted> (<domain/period, sample size>): (a) ...; (b) ...` + brief methodological qualifiers (`outliers omitted`, `k = 5`).
3. **Prune Redundancy & Enforce Nomenclature:**
   - Omit axis units already legible on the plot, colorbar bounds, scale bars, North arrows, and summary stats already reported in prose.
   - Use canonical paper names (`GBR`, `XGB`, `MLP`) instead of Python identifiers (`GradientBoostingRegressor`), and do not re-expand previously defined acronyms.
4. **Sync Embeds & Callouts:** Keep alt-text concise (`![Figure N: <short title>.](path)`) followed by a blank line and `**Figure N.** ...`; verify sequential numbering (`Figure 1` $\rightarrow$ `Figure M`) across all sections.
