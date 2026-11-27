---
name: update-documentation
description: Audit and synchronize technical repository documentation (README.md, GEMINI.md, requirements.txt, methodological_guide.md, notebook summaries, compiled notebook telemetry) and scientific manuscript QA (ms_*.md, highlighted Word diffs, master_literature_review.txt). Invoked via /update-documentation.
---

# Documentation & Manuscript Synchronization (`/update-documentation`)

Use this skill to keep technical repository docs, notebook telemetry, and scientific manuscript assets 100% synchronized after modifying code, notebooks, or manuscript sections.

---

## Step 1: Run Automated Documentation & Manuscript Audit

Run [audit_docs_sync.py](./scripts/audit_docs_sync.py) with `--compile-nbs` using the workspace virtual environment:

```powershell
.venv\Scripts\python.exe .agents/skills/update-documentation/scripts/audit_docs_sync.py --compile-nbs
```

This command automatically:
1. Recompiles all active `notebooks/*.ipynb` code cells into `docs/telemetry/nb_compiled_phase_*.txt` via `scripts/compile_nbs.py`.
2. Checks exact package parity between `requirements.txt` and the `### Dependencies` block in `README.md`.
3. Verifies every notebook in `notebooks/*.ipynb` is listed in `README.md` and has a matching `docs/summary/*_summary.txt`.
4. Runs `.agents/skills/manuscript_qa/scripts/validate_manuscript.py --strict` across all `docs/manuscript/sections/ms_*.md` and `highlighted/*_HIGHLIGHTED.md` files.

---

## Step 2: Synchronize Dependencies & Environment (`requirements.txt`, `README.md`, `env.py`)

If new third-party imports were introduced in `src/project_pkg/` or `notebooks/`:
1. Add the package to [requirements.txt](../../../requirements.txt).
2. Mirror the exact dependency entry in [README.md](../../../README.md) under `### Dependencies`.
3. If needed for Google Colab runtime execution, update `COLAB_PACKAGES` in [env.py](../../../src/project_pkg/utils/env.py).

---

## Step 3: Synchronize Architecture & Methodological Documentation

Inspect `git status --short` and recent `git diff` across `src/project_pkg/`, `notebooks/`, and `.agents/`:
1. **Utility Modules (`src/project_pkg/utils/*.py`)**: Ensure new or refactored public functions/modules are reflected in [GEMINI.md](../../../GEMINI.md) (Section 5) and [README.md](../../../README.md) (`Repository Structure`).
2. **Pipeline Notebooks (`notebooks/1.x`–`4.x`)**: Ensure workflow descriptions in [README.md](../../../README.md) (`## Workflow`), [methodological_guide.md](../../../docs/planning/methodological_guide.md), and `docs/summary/*_summary.txt` match the current implementation and metrics.
3. **Agent Customizations (`.agents/rules/`, `.agents/skills/`)**: Keep `.agents/` structure descriptions in [README.md](../../../README.md) and [GEMINI.md](../../../GEMINI.md) up to date.

---

## Step 4: Synchronize Manuscript Sections, Word Diff Guides & Literature

When any manuscript section (`docs/manuscript/sections/ms_*.md`) or reference was modified:
1. **Literature Catalog**: Verify every cited reference with a DOI is formatted in APA style and synced in [master_literature_review.txt](../../../docs/references/master_literature_review.txt).
2. **Word Red/Yellow Diff Guides**: Update the corresponding `docs/manuscript/sections/highlighted/*_HIGHLIGHTED.md` file following [manuscript_qa](../manuscript_qa/SKILL.md) rules so that:
   - Stripping `<mark>` tags and keeping `<del>` inner text reproduces the frozen Word baseline (`docs/manuscript/baseline/<Baseline_Export>.md`).
   - Stripping `<del>...</del>` blocks and keeping `<mark>` inner text reproduces the canonical `ms_*.md` section.
3. **Final Verification**: Re-run the audit script and confirm zero errors:
   ```powershell
   .venv\Scripts\python.exe .agents/skills/update-documentation/scripts/audit_docs_sync.py
   ```

---

## Step 5: Context Window Hygiene (`/compact` Recommendation)

Because `/compact` is a user-side chat UI slash command and cannot be invoked programmatically by the agent, always conclude `/update-documentation` responses by recommending that the user run `/compact` if the conversation history has grown long after documentation and manuscript audits.
