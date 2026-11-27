"""Elsevier & Q1 publication figure utilities (Okabe-Ito palette, 90/140/190 mm widths)."""

from __future__ import annotations

from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image

MM_TO_INCH = 1.0 / 25.4
ELSEVIER_WIDTHS_MM = {"single": 90.0, "one_half": 140.0, "double": 190.0}

# Colorblind-safe Okabe-Ito palette
CB_PALETTE = [
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # bluish green
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#000000",  # black
]


def figsize_mm(width: str | float = "single", height_mm: float | None = None, aspect: float = 0.72) -> tuple[float, float]:
    w_mm = ELSEVIER_WIDTHS_MM[width] if isinstance(width, str) else float(width)
    h_mm = w_mm * aspect if height_mm is None else float(height_mm)
    return (w_mm * MM_TO_INCH, h_mm * MM_TO_INCH)


def apply_elsevier_style(base_pt: float = 8.5) -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": base_pt,
        "axes.labelsize": base_pt + 0.5,
        "xtick.labelsize": base_pt - 0.5,
        "ytick.labelsize": base_pt - 0.5,
        "legend.fontsize": base_pt - 0.5,
        "axes.linewidth": 0.75,
        "lines.linewidth": 1.25,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=CB_PALETTE),
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def save_publication_figure(fig: plt.Figure, output_stem: Path | str, tiff_dpi: int = 600, png_dpi: int = 300) -> list[Path]:
    """Export vector PDF, RGB 300 DPI PNG, and RGB LZW 600 DPI TIFF."""
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    pdf_path = stem.with_suffix(".pdf")
    png_path = stem.with_suffix(".png")
    tiff_path = stem.with_suffix(".tiff")

    fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.03)
    fig.savefig(png_path, dpi=png_dpi, bbox_inches="tight", pad_inches=0.03)
    fig.savefig(tiff_path, dpi=tiff_dpi, bbox_inches="tight", pad_inches=0.03)

    # Ensure strict RGB + LZW TIFF compression for Elsevier compatibility
    for raster_path, is_tiff in ((png_path, False), (tiff_path, True)):
        with Image.open(raster_path) as img:
            dpi_info = img.info.get("dpi", (tiff_dpi if is_tiff else png_dpi,) * 2)
            rgb = img.convert("RGB")
            if is_tiff:
                rgb.save(raster_path, compression="tiff_lzw", dpi=dpi_info)
            else:
                rgb.save(raster_path, dpi=dpi_info)
    return [pdf_path, png_path, tiff_path]
