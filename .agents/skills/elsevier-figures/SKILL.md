---
name: elsevier-figures
description: >-
  Applies official Elsevier journal figure and electronic artwork standards (exact 90/140/190 mm column widths, DPI/format rules, embedded standard fonts, RGB colorblind-safe palettes, no in-plot global titles, and visual QA) as the default pattern when creating, refactoring, or auditing scientific plots and diagrams.
---

# Elsevier Figure Patterns

Use Elsevier's electronic artwork specifications as the baseline standard for all scientific figures, plots, maps, and diagrams, deferring to stricter project-specific rules (e.g., `.agents/rules/visualization.md`) when present.

For complete specification tables, reusable Matplotlib/Seaborn presets, and multi-panel layout patterns, read [elsevier_specs_and_presets.md](./references/elsevier_specs_and_presets.md).

## Workflow

### 1. Size to Final Print Column Width
Design figures at their target publication dimensions rather than scaling oversized plots down later (`1 in = 25.4 mm`):
- **Single column:** `90 mm` (`3.54 in`)
- **1.5 column:** `140 mm` (`5.51 in`)
- **Double column (full page width):** `190 mm` (`7.48 in`)
- Keep minimum element width `>= 30 mm` (`1.18 in`) and maximum figure height `<= 240 mm` (`9.45 in`) so space remains for the manuscript caption.

### 2. Enforce Typography, Line Weights, and Clean Framing
- **Fonts:** Use a single standard font family across every figure in a manuscript—**Arial / Helvetica** (Elsevier default sans-serif) or **Times New Roman / Times** (serif when required by workspace or journal template).
- **Legible sizing at final print scale:** Set axis labels and panel tags `(a)`, `(b)` to **8–10 pt**, tick labels and legends to **7–9 pt**, and subscripts/annotations to **>= 6 pt**.
- **Line weights & markers:** Keep data lines and axes **>= 0.5–0.75 pt** (avoid hairlines `< 0.25 pt`); size markers (`3–5 pt`) to remain distinct after printing.
- **No global in-plot titles or embedded captions:** Never use `plt.suptitle()`, single-panel `ax.set_title()`, or figure captions inside the artwork file. Place titles and context in the manuscript caption via `q1-article`.
- **Multi-panel labels:** Use compact, consistent lowercase panel identifiers `(a)`, `(b)`, `(c)` (or canonical model names when comparing models in grids), aligned cleanly across panels.
- **Axes & legends:** Label every axis with explicit physical/SI units (e.g., `Precipitation (mm)`). Never let legends overlap data—place them outside the axes or in verified empty space.

### 3. Select Colorblind-Safe RGB Palettes
- Export in **RGB** color space (Elsevier's online standard) while avoiding hyper-saturated neon hues that shift badly during print CMYK conversion.
- Default to **Okabe–Ito** for categorical series, perceptually uniform colormaps (`viridis`, `cividis`, `plasma`) for sequential values, and zero-centered diverging colormaps (`coolwarm`, `RdBu_r`) for bias/anomalies.
- Pair color differences with redundant encoding (marker shapes, line styles, or hatching) so plots remain interpretable in grayscale print.

### 4. Export at Required Resolution and Format
Choose the format matching the artwork category (and honor stricter workspace export targets when defined):
- **Vector charts, graphs, diagrams:** **PDF** or **EPS** with embedded TrueType fonts (`pdf.fonttype = 42`, `ps.fonttype = 42`) or outlined text.
- **Combination art** (raster maps/halftones + vector text/overlays): **TIFF** (LZW) at **>= 500–600 DPI** (or hybrid vector PDF).
- **Halftones / photographs:** **TIFF** or high-quality **JPEG** at **>= 300 DPI**.
- **Raster-only line art:** **TIFF** at **>= 1000 DPI**.
- **Working/notebook previews:** PNG at **300 DPI** (`bbox_inches="tight"`, minimal outer whitespace).

### 5. Mandatory Technical & Visual Audit Before Finishing
1. Run [audit_figures.py](./scripts/audit_figures.py) on the exported `.tiff`, `.pdf`, and `.png` files to deterministically verify pixel dimensions, column width (`90 / 140 / 190 mm`), DPI (`>= 500–600` TIFF, `>= 300` PNG), `RGB` mode, LZW compression, and absence of PDF Type 3 bitmap fonts.
2. Always inspect the rendered figure directly (`read_file` on the exported image or rendered page) before completing the task:
   - Confirm zero clipped labels, overlapping tick text, occluded data points, or cramped subplots.
   - Confirm text remains crisp and readable at its intended `90 / 140 / 190 mm` column width.
   - Confirm file naming (`Fig1.tiff`, `Fig1.pdf`, or repository-standard paths) and coordinate with `q1-article` for caption & alt-text synchronization.
