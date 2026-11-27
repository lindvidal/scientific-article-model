---
name: manuscript_qa
description: Validate and synchronize canonical manuscript drafts (docs/manuscript/sections/ms_*.md) and Word-aligned red/yellow diff guides (*_HIGHLIGHTED.md), checking figure links, sequential numbering, citation ordering, punctuation hygiene, and bidirectional parity.
---

# Manuscript QA & Word Diff Synchronization (`manuscript_qa`)

Use this workspace skill whenever editing, auditing, or finalizing manuscript sections under `docs/manuscript/sections/`.

## Automated QA Validation
Run before committing any manuscript edit:

```powershell
python .agents/skills/manuscript_qa/scripts/validate_manuscript.py --strict
```

Checks enforced:
1. **Figure image links:** Every Markdown embed resolves on disk cleanly.
2. **Sequential figure captions:** Unique figure captions progress sequentially (`Figure 1` -> `Figure N`) and stay concise (`<= 45` words).
3. **APA / Elsevier citation hygiene:** Ascending comma-separated same-author years, alphabetical multi-author parenthetical groups, diacritics preserved, no bolded narrative citations.
4. **Punctuation hygiene:** No en-dashes or em-dashes in canonical `ms_*.md` bodies above `---`.
5. **Highlighted Word-diff parity:** Stripping `<del>...</del>` and markup from `highlighted/*_HIGHLIGHTED.md` matches the canonical `ms_*.md` body character-for-character.
6. **1-to-1 per-section reference parity:** Every section file ends with `---` and a verified reference block whose entries match in-text citations 1-to-1 with verified URLs/DOIs.
