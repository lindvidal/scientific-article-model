# Manuscript Conventions & Word Sync Standard

## 1. Source Hierarchy
- **Canonical Word Baseline (Read-Only):** `docs/manuscript/baseline/` — verbatim Markdown/PDF export used as diff baseline.
- **Canonical Revised Sections:** `docs/manuscript/sections/ms_*.md`.
- **Visual Word-Edit Guides:** `docs/manuscript/sections/highlighted/*_HIGHLIGHTED.md`.

## 2. Red/Yellow Word-Diff Format (`*_HIGHLIGHTED.md`)
Each highlighted guide contains:
1. Color legend (`#fff176` yellow `<mark>` insertions, `#ffebee`/`#c62828` red strikethrough `<del>` deletions).
2. `## 1. Word Revision Summary` table mapping paragraph locations to key edits.
3. `## 2. Full Section Text with Revision Markup` containing the aligned full section (using `<strong>...</strong>` inside HTML spans rather than `**...**`).
4. `---` followed by `## 3. References Cited in Section X (Verified with DOIs)` matching the canonical section reference list.
