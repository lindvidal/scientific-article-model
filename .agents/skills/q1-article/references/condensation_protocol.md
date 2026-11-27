# Surgical Manuscript Condensation Protocol

Use this workflow when bringing a long scientific manuscript draft (e.g., 13,000+ words) into target Q1 journal limits (e.g., 5,000–10,000 words / `~8,000` words for *Journal of Hydrology*) without losing statistical rigor, physical explanations, or 1-to-1 citation parity.

---

## Step 1: Baseline Word Audit
Run the metrics helper before touching prose so cuts target actual narrative bloat rather than tables or reference blocks:

```powershell
python <q1-article-dir>/scripts/manuscript_metrics.py <path/to/manuscript_or_sections_dir>
```

Focus trimming on **Pure Prose** and oversized **Tables**, keeping every statistical metric, threshold, and hypothesis intact.

---

## Step 2: Prioritized Cutting Hierarchy

1. **Priority 1 — Eliminate Prolix Table Repetition (Highest Savings, Zero Loss):**
   - Never narrate every row and column of a results table in prose.
   - State the top rankers, key relative deltas (`8.9%` reduction vs. baseline), statistical test confirmations ($\chi^2_F$, $W$, $p$), and physical/algorithmic reasons, pointing directly to `(Table N)`.
2. **Priority 2 — Offload Secondary Artifacts to Supplementary Material:**
   - Move exhaustive hyperparameter search grids, secondary CV diagnostics, extended per-region breakdowns, or auxiliary sensitivity tables to `Supplementary Material` (`Table S1`, `Figure S1`).
   - Keep only summary specifications and main-hypothesis evidence in the main manuscript.
3. **Priority 3 — Syntactic Compression (Academic Economy):**
   - Replace verbose scaffolding (`"was conducted in order to evaluate"`, `"it should be noted that"`, `"in the context of this study"`) with direct active/concise constructions (`"evaluated"`, `"notably"`, `"here"`).
   - Merge repetitive transitional sentences between consecutive subsections while preserving formal scientific tone.
   - Define domain acronyms (`IDW`, `KGE`, `MAE`, `HQ`) once on first occurrence and avoid re-expanding them in later sections.
4. **Priority 4 — Maintain Strict Numerical & Citation Integrity:**
   - **Never** drop sample sizes (`N`, `n`), physical floor definitions, confidence intervals, exact test statistics, or declared limitations during condensation.
   - **Citation Pruning Rule:** Whenever a sentence containing an in-text citation is shortened or deleted, immediately check whether that citation still appears elsewhere in the same section/file. If not, remove the orphaned entry from the section's end-of-document reference list in the same edit to prevent `[REF-ORPHAN]` QA failures.

---

## Step 3: Post-Condensation QA
1. Re-run `scripts/manuscript_metrics.py` and confirm target journal word count is reached.
2. Run any active workspace QA validator (e.g., `validate_manuscript.py --strict`) to verify 1-to-1 citation parity, figure numbering, and diff-guide sync (`*_HIGHLIGHTED.md`).
