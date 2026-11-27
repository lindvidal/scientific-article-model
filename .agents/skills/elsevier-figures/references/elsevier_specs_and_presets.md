# Elsevier Figure Specifications & Matplotlib Presets

Reference guide for [SKILL.md](../SKILL.md) implementing Elsevier's Electronic Artwork Instructions in Python scientific plotting workflows.

---

## 1. Quick-Reference Specification Matrix

| Parameter | Elsevier Standard | Notes / Matplotlib Mapping |
| :--- | :--- | :--- |
| **Single column width** | **90 mm** (`3.54 in`) | Compact scatter, single time series, 1-panel distributions |
| **1.5 column width** | **140 mm** (`5.51 in`) | Medium 2-panel comparisons, moderate matrix heatmaps |
| **Double column width** | **190 mm** (`7.48 in`) | Multi-panel grids, spatial maps, complex workflows |
| **Minimum width** | **30 mm** (`1.18 in`) | Smallest inset or standalone graphic |
| **Max page height** | **<= 240 mm** (`9.45 in`) | Leaves room on page for caption below figure |
| **Vector line art** | **EPS / PDF** | Resolution-independent; set `pdf.fonttype = 42`, `ps.fonttype = 42` |
| **Combination art** | **>= 500 DPI** (TIFF / PDF) | Halftone/raster map + vector labels/lines (`600 DPI` recommended) |
| **Halftones / photos** | **>= 300 DPI** (TIFF / JPEG) | Continuous imagery or photography |
| **Raster line art** | **>= 1000 DPI** (TIFF) | Monochrome/bitmap charts when vector export is unavailable |
| **Color mode** | **RGB** | Required for online articles; print auto-converts RGB -> CMYK |
| **Approved fonts** | **Arial, Helvetica, Times / Times New Roman, Courier, Symbol** | Consistent family across all manuscript figures |
| **Font sizes (at print size)** | Titles/panel tags/axes: **8–10 pt**; ticks/legend: **7–9 pt**; sub/superscripts: **>= 6 pt** | Applied directly at final `figsize` in inches |
| **Line widths** | **>= 0.5–0.75 pt** (data `1.0–1.5 pt`) | Prevents hairlines vanishing in print |

---

## 2. Reusable Python / Matplotlib Preset

Use this baseline configuration (adjusting `serif` vs. `sans-serif` only when a manuscript or workspace rule mandates a specific family):

```python
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt

MM_TO_INCH = 1.0 / 25.4

ELSEVIER_WIDTHS_MM = {
    "single": 90.0,
    "one_half": 140.0,
    "double": 190.0,
}

# Okabe-Ito colorblind-safe categorical palette
OKABE_ITO_PALETTE = [
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # bluish green
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#000000",  # black
    "#7F7F7F",  # neutral grey
]


def figsize_mm(width="single", height_mm=None, aspect=0.75):
    """Return (width_in, height_in) for exact Elsevier column widths."""
    w_mm = ELSEVIER_WIDTHS_MM[width] if isinstance(width, str) else float(width)
    h_mm = w_mm * aspect if height_mm is None else float(height_mm)
    return (w_mm * MM_TO_INCH, h_mm * MM_TO_INCH)


def apply_elsevier_style(font_family="sans-serif", base_pt=8.5, preview_dpi=300):
    """Configure Matplotlib rcParams to match Elsevier electronic artwork rules."""
    sans_fonts = ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"]
    serif_fonts = ["Times New Roman", "Times", "DejaVu Serif", "Liberation Serif"]

    mpl.rcParams.update({
        "font.family": font_family,
        "font.sans-serif": sans_fonts,
        "font.serif": serif_fonts,
        "font.size": base_pt,
        "axes.titlesize": base_pt + 0.5,
        "axes.labelsize": base_pt + 0.5,
        "xtick.labelsize": base_pt - 0.5,
        "ytick.labelsize": base_pt - 0.5,
        "legend.fontsize": base_pt - 0.5,
        "axes.linewidth": 0.75,
        "grid.linewidth": 0.5,
        "lines.linewidth": 1.25,
        "lines.markersize": 4.0,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=OKABE_ITO_PALETTE),
        "figure.dpi": preview_dpi,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        # Embed TrueType fonts cleanly in PDF/EPS exports
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })


def add_panel_label(ax, label, x=-0.12, y=1.06, fontsize=9.5):
    """Place consistent bold panel identifiers such as '(a)' outside/top-left."""
    ax.text(
        x, y, label,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight="bold",
        va="bottom",
        ha="left",
    )


def save_elsevier_figure(fig, output_stem, formats=("pdf", "tiff"), dpi=600):
    """Save figure in Elsevier-compliant vector and/or lossless TIFF formats."""
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for fmt in formats:
        ext = fmt.lower().lstrip(".")
        out_path = stem.with_suffix(f".{ext}")
        save_kwargs = {"bbox_inches": "tight", "pad_inches": 0.03}
        if ext in {"tif", "tiff", "png", "jpg", "jpeg"}:
            save_kwargs["dpi"] = dpi
        if ext in {"tif", "tiff"}:
            save_kwargs["pil_kwargs"] = {"compression": "tiff_lzw"}
        fig.savefig(out_path, format=ext, **save_kwargs)
        saved.append(out_path)
    return saved
```

---

## 3. Multi-Panel & Layout Patterns

- **Consistent panel geometry:** Prefer `plt.subplots(..., constrained_layout=True)` over manual magic numbers; align shared x/y axes (`sharex=True`, `sharey=True`) and hide redundant inner tick labels.
- **External legends:** For multi-series plots, place legends above or right of the axes (`bbox_to_anchor=(0.5, 1.02)`, `loc="lower center"`, `ncol=...`, `frameon=False`) so zero data points are covered.
- **Shared colorbars:** Use a single shared colorbar across multi-panel maps or heatmaps (`fig.colorbar(..., ax=axes, shrink=0.85, pad=0.02)`) with explicit units in its label.
- **File organization:** Save one figure per file (`Fig1.pdf`, `Fig1.tiff`, etc., or workspace naming convention) without embedded figure titles or captions inside the canvas.

---

## 4. Pre-Submission Visual QA Checklist

- [ ] Width matches Elsevier column spec (`90 mm`, `140 mm`, or `190 mm`) and height `<= 240 mm`.
- [ ] No global `plt.suptitle()`, single-panel `ax.set_title()`, or embedded caption text inside the graphic.
- [ ] Font family is standard (`Arial`/`Helvetica` or `Times New Roman`) and embedded (`pdf.fonttype = 42` / `ps.fonttype = 42`).
- [ ] All text is `>= 7 pt` (subscripts `>= 6 pt`) and line weights `>= 0.5 pt` at final print dimensions.
- [ ] Axis labels include explicit physical/SI units; legends never overlap data.
- [ ] Colorblind-safe RGB palette used, with redundant linestyles/markers/hatching where applicable.
- [ ] Exported format and DPI match artwork type (Vector PDF/EPS, Combination >= 500–600 DPI TIFF, Halftone >= 300 DPI, Raster line art >= 1000 DPI) or stricter workspace rules.
- [ ] Rendered image inspected directly via `read_file` with zero clipping, overlap, or excessive whitespace.
