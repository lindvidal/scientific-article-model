---
name: commit
description: Execute sequential git commits (v0000 - <summary>), pre-commit manuscript QA, automated telemetry generation (CSV/DOCX), and remote repository push. Invoked via /commit or when the user asks to commit and push.
---

# Commit & Telemetry Workflow (`/commit`)

> **Canonical Git & Telemetry rules live in** [git_workflow.md](../../rules/git_workflow.md). Follow Windows PowerShell syntax (`;` chaining, not `&&`) and `.venv\Scripts\python.exe`.

---

## Phase 1: Context Inspection, Version Calculation & Pre-Commit QA Gate

1. **Inspect Dirty Working Tree:**
   - Run `git status --short` and `git diff --stat`.
   - Confirm only intended files will be staged; **never** run `git add -A` when unrelated dirty files exist (e.g., `docs/telemetry/log_io_tables.csv`).
2. **Pre-Commit Manuscript QA Gate:**
   - If any file under `docs/manuscript/` is modified or untracked, run the strict manuscript validator before staging:
     ```powershell
     .venv\Scripts\python.exe .agents/skills/manuscript_qa/scripts/validate_manuscript.py --strict
     ```
   - Fix any reported citation, numbering, figure link, or Word diff parity errors before proceeding.
3. **Determine Sequential Version (`v{N:04d}`):**
   - Run the helper script to inspect the latest `v0000` tag and pending files without mutating anything:
     ```powershell
     .venv\Scripts\python.exe .agents/skills/commit/scripts/sync_telemetry.py --dry-run
     ```
   - Always zero-pad `N` to 4 digits (`v0738`, `v0004`, not `v738`).

---

## Phase 2: Primary Commit (`v{N:04d}`)

1. **Format:**
   - Header: `v{N:04d} - <concise imperative summary in English>`
   - Body: verbose bullet points explaining *what* changed and *why* (verification, edge cases, schema/citation checks).
   - Mandatory trailer:
     ```text
     Co-authored-by: AI Assistant <ai-assistant@example.org>
     ```
2. **Stage Selectively & Commit:**
   - Note for Windows sandbox agents: try `git add <paths>; git commit ...` in Standard Sandbox Mode first; if `.git/index.lock: Permission denied` blocks execution, retry with `BypassSandbox: true` and an identical `toolSummary`.

---

## Phase 3: Telemetry Regeneration (`v{N+1:04d}`)

1. **Regenerate Telemetry Inside Sandbox:**
   - Run [sync_telemetry.py](./scripts/sync_telemetry.py) using the workspace virtualenv (runs offline in Standard Sandbox Mode):
     ```powershell
     .venv\Scripts\python.exe .agents/skills/commit/scripts/sync_telemetry.py
     ```
   - This updates `docs/telemetry/log_github_lastrun.csv` and `docs/telemetry/log_github_lastrun.docx` via `scripts/github_logger.py`.
2. **Commit Telemetry:**
   - Stage only the two regenerated telemetry files:
     ```powershell
     git add docs/telemetry/log_github_lastrun.csv docs/telemetry/log_github_lastrun.docx
     ```
   - Commit with `v{N+1:04d} - Telemetry sync for <summary>` and the mandatory `Co-authored-by` trailer.

---

## Phase 4: Verification & Remote Push

1. Push both commits immediately and verify clean status on the edited files:
   ```powershell
   git push origin main; git status --short
   ```
   *(On Windows sandboxed shells, `git push` may require `BypassSandbox: true` due to Schannel / network isolation.)*
2. **Context Window Hygiene (`/compact` Recommendation):** Because `/compact` is a user-invoked chat UI slash command that the agent cannot execute directly, conclude every `/commit` completion summary by reminding the user to run `/compact` to compact the conversation context before starting the next task.
