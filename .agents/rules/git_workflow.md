# Rule: Git & Telemetry Workflow

- **Commit Naming:** Use sequential 4-digit version prefixes `v0001 - <summary>` (`v{N:04d} - <summary>`).
- **Verbose Commit Bodies:** Include clear bullet points summarizing *what* changed, *why*, and what QA checks passed.
- **Pre-Commit QA Gate:** Run `.agents/skills/manuscript_qa/scripts/validate_manuscript.py --strict` before committing any changes under `docs/manuscript/`.
- **Telemetry Sync:** After each primary commit (`v{N:04d}`), run `.agents/skills/commit/scripts/sync_telemetry.py` to regenerate `docs/telemetry/log_github_lastrun.csv` and `docs/telemetry/log_github_lastrun.docx`, then commit telemetry as `v{N+1:04d} - Telemetry sync for <summary>`.
