# GEMINI Context Hub

Welcome to the **Scientific Article Model** workspace (`d:\Projetos\Scientific-Article-Model`). Every AI agent operating inside this repository must adhere to these architectural, statistical, and editorial standards.

## 1. Project Goal
This repository provides a domain-agnostic, Q1-ready scientific research and manuscript production framework pairing reproducible multi-phase computational pipelines (`src/`, `notebooks/`) with automated manuscript, citation, and figure quality assurance (`.agents/skills/`).

## 2. Execution Hierarchy (The 4 Phases)
Organize notebooks and scripts chronologically so numeric prefixes map cleanly to execution stages:
- **Phase 1 (Data Engineering & Exploration):** `1.x` ingests raw datasets, enforces schema/unit validation, applies quality control, and persists tidy intermediate tables under `data/processed/`.
- **Phase 2 (Modeling & Core Analysis):** `2.x` builds baseline benchmarks and experimental models/analyses strictly on development (`train`) splits, persisting fitted artifacts under `models/` or `results/`.
- **Phase 3 (Inference & Out-of-Sample Validation):** `3.x` generates predictions/outputs across validation and held-out test partitions, running uncertainty quantification or post-processing.
- **Phase 4 (Publication Analytics & Figures):** `4.x` computes statistical hypothesis tests, effect sizes, and publication-grade Q1 figures exported to `outputs/figures/manuscript/`.

## 3. Strict Dataset Hygiene
- **Training / Tuning:** ONLY use `train` / `development` partitions for fitting, scaling, and hyperparameter tuning.
- **Model Selection / Ranking:** ONLY use `validation` partitions (or nested CV folds) to compare candidate methods.
- **Final Evaluation:** ONLY touch the held-out `test` partition once after all architectural decisions are frozen. Never leak test statistics into feature engineering or tuning.

## 4. Core Operational Protocols
Agents must follow the modular rules in `.agents/rules/` and `.agents/AGENTS.md`:
- **Environment Bootstrap:** Every Jupyter notebook must open with the canonical `Environment_Bootstrap` cell defined in `.agents/AGENTS.md`.
- **Literature Anti-Hallucination:** Never cite papers or DOIs from memory. Verify every entry live via Crossref/OpenAlex (`scientific_literature_research`), prioritize Q1 peer-reviewed journals, and keep `docs/references/master_literature_review.txt` synchronized (`.agents/rules/literature.md`).
- **Scientific Visualization (Q1 / Elsevier):** Enforce `90 / 140 / 190 mm` column widths, Arial/Helvetica `7.5-9.5 pt`, `pdf.fonttype = 42`, no global in-plot titles (`plt.suptitle()` / single-panel `ax.set_title()`), Okabe-Ito colorblind-safe palettes, external legends, and 600 DPI LZW `.tiff` + vector `.pdf` + 300 DPI `.png` exports (`.agents/rules/visualization.md`).
- **Manuscript & Word-Diff QA (`manuscript_qa`, `q1-article`):** Author canonical sections under `docs/manuscript/sections/ms_*.md` with matching `<del>`/`<mark>` revision guides in `docs/manuscript/sections/highlighted/*_HIGHLIGHTED.md` and 1-to-1 verified reference lists.
- **Git & Telemetry (`.agents/rules/git_workflow.md`):** Use sequential 4-digit verbose commits (`v0001 - <summary>`) with telemetry regeneration (`docs/telemetry/`).
- **Planning Mode & Dependencies:** Create a written plan before substantive multi-file edits. Whenever adding third-party Python packages, update both `requirements.txt` and `README.md` together.

## 5. Interactive Companion Course
Read `class/README.md` for the GitHub-native 7-module course (or open `class/index.html` in any browser for the offline interactive UI) explaining how to combine AI agents, rules, and skills to accelerate high-rigor scientific production.
