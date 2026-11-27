# Scientific Article Model (Q1 Research & AI Workflow Template)

A domain-agnostic, reproducible scientific repository template combining structured computational phases, **Q1 manuscript & Elsevier figure QA automation**, **anti-hallucination citation verification**, and a **7-module interactive AI production class** ([class/README.md](class/README.md) on GitHub &bull; [class/index.html](class/index.html) offline).

## Quick Start

1. **Create environment variables:** Copy `.env.example` to `.env` and set your paths and `RANDOM_SEED`.
2. **Install Python dependencies:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Open the AI Scientific Production Class:** Read [class/README.md](class/README.md) natively on GitHub, or open [class/index.html](class/index.html) in any browser for offline/GitHub Pages mode.
4. **Run the QA Suite:**
   ```powershell
   python .agents/skills/manuscript_qa/scripts/validate_manuscript.py --strict
   python .agents/skills/q1-article/scripts/manuscript_metrics.py docs/manuscript/sections
   python .agents/skills/update-documentation/scripts/audit_docs_sync.py
   ```

## Repository Structure

```text
Scientific-Article-Model/
├── GEMINI.md                              # AI governance & methodological hub
├── README.md                              # Project entry point & QA commands
├── .env.example                           # Environment path & seed template
├── requirements.txt                       # Mirrored Python dependencies
├── class/
│   ├── README.md                          # 7-module interactive class (GitHub-native Markdown)
│   ├── assets/okabe_ito_palette.svg       # Inline vector palette swatch for GitHub viewer
│   └── index.html                         # 7-module interactive HTML class (offline / GitHub Pages)
├── .agents/
│   ├── AGENTS.md                          # Notebook bootstrap & agent standard
│   ├── rules/                             # literature.md, visualization.md, git_workflow.md
│   └── skills/                            # manuscript_qa, q1-article, elsevier-figures,
│                                          # scientific_literature_research, commit, update-documentation
├── docs/
│   ├── manuscript/
│   │   ├── baseline/                      # Frozen Word/PDF baseline exports
│   │   └── sections/                      # Canonical ms_*.md + highlighted/*_HIGHLIGHTED.md
│   ├── planning/                          # methodological_guide.md
│   ├── references/                        # master_literature_review.txt
│   ├── summary/                           # Per-notebook human-readable summaries
│   └── telemetry/                         # Compiled notebooks & git telemetry logs
├── notebooks/                             # Phase 0-4 Jupyter notebooks
├── scripts/                               # Repository automation helpers (compile_nbs.py, github_logger.py)
├── src/project_pkg/                       # Reusable Python utilities (plots.py)
├── data/                                  # raw/ and processed/ datasets (git-ignored binaries)
└── outputs/figures/manuscript/            # Q1 TIFF/PDF/PNG artwork exports
```

## Workflow & Active Notebooks

- [notebooks/0.0_Template_Notebook.ipynb](notebooks/0.0_Template_Notebook.ipynb): Starter computational notebook wired with the canonical local/Colab bootstrap cell and Elsevier figure utilities.

### Dependencies

```text
numpy>=1.26.0
pandas>=2.2.0
matplotlib>=3.8.0
Pillow>=10.0.0
requests>=2.31.0
python-docx>=1.1.0
```
