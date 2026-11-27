# Section Styles & Mandatory Actions

When drafting or refining a manuscript section with `q1-article`, adhere to the rhetorical focus below and layer any project-specific rules from the active workspace (`GEMINI.md` / `.agents/`):

## 1. Introduction
- **Tone:** Persuasive, gap-identifying, literature-anchored.
- **Focus:** Establish the broader scientific problem, synthesize relevant state-of-the-art studies, isolate the exact research gap, and state concrete objectives/hypotheses without exhaustive literature dumps.

## 2. Study Area / Materials & Methods
- **Tone:** Procedural, precise, reproducible; objective scientific prose.
- **Focus:** Exact protocols, physical thresholds, spatial/temporal partitioning rules, algorithms, and hyperparameter/evaluation designs directly verified against project artifacts.
- **Mandatory Action (Methodological Anchoring):** Anchor methodological and preprocessing decisions in verified **peer-reviewed journal articles** (Q1 first; Q2 fallback only when no suitable Q1 paper exists; filter out technical reports or grey literature unless mandatory standards such as national/international agencies apply). Log or document citation rationales if required by the workspace.

## 3. Results
- **Tone:** Objective, quantitative, comparative, concise.
- **Focus:** Verified test/validation statistics, relative deltas, statistical significance outcomes, and direct cross-references to numbered Figures and Tables without repeating entire table matrices verbatim.
- **Mandatory Action (Literature Benchmarking):** Benchmark achieved performance and observed patterns against comparable peer-reviewed studies (Q1 prioritized) to contextualize improvements cleanly.

## 4. Discussion
- **Tone:** Interpretative, mechanistic, limitation-aware.
- **Focus:** Explain *why* quantitative outcomes and spatial/regime differences occur physically and algorithmically, reconcile unexpected trade-offs, and address methodological limitations transparently.

## 5. Conclusions
- **Tone:** Decisive, summarizing, operational, forward-looking.
- **Focus:** Clear evidence-backed recommendations grounded in Results metrics and actionable directions for future work without introducing new unanalyzed data.

## 6. Per-Document Reference Lists (Standalone Section Files)
- **Placement:** When a workspace maintains standalone manuscript section files (`ms_*.md`), every section file must end with `\n---\n` followed by `### References Cited in Section X (Verified with DOIs)` (and `## 3. Referências ...` in highlighted diff guides).
- **1-to-1 Synchronization:** List every in-text citation appearing in that file's body in alphabetical APA 7th format with verified DOIs (or official repository/publisher URLs when no DOI exists). Never leave an in-text citation unreferenced or an unused reference entry orphaned in the file. For zero-citation overview or conclusion files, retain the reference block heading with an explicit italic note explaining that no direct in-text citations appear.
