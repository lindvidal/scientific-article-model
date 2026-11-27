# Rule: Scientific Visualization Protocol (Q1 / Elsevier Standards)

All figures exported by repository scripts or notebooks must follow Q1 publication standards (`src/project_pkg/utils/plots.py`):
- **Target Column Widths:** Design directly at Elsevier print widths (`90 mm` single column, `140 mm` 1.5-column, `190 mm` double column; height `<= 240 mm`).
- **No Global In-Plot Titles:** NEVER use `plt.suptitle()` or single-panel `ax.set_title()`. Place titles and methodological descriptions in the manuscript caption. Multi-panel grids may use compact lowercase panel identifiers `(a)`, `(b)`, `(c)`.
- **Legend Placement:** Legends must NEVER occlude plotted data. Place them outside the axes (`bbox_to_anchor`) or in verified open space.
- **Color Palettes:** Use Okabe-Ito (`CB_PALETTE`) for categorical groups, perceptually uniform colormaps (`viridis`, `cividis`, `plasma`) for sequential data, and symmetric diverging colormaps (`coolwarm`, `RdBu_r`) for bias/anomalies.
- **Typography & Export Formats:** Use a consistent sans-serif family (`Arial`/`Helvetica`, `7.5-9.5 pt` at target width), explicit axis labels with parenthesized physical units, `pdf.fonttype = 42`, and export **600 DPI RGB LZW `.tiff`**, **vector `.pdf`**, and **300 DPI `.png`** previews.
