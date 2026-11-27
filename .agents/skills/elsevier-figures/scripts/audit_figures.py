"""Audit exported publication figures against Elsevier electronic artwork specifications."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

TARGET_WIDTHS_MM = (90.0, 140.0, 190.0)
MAX_HEIGHT_MM = 240.0
MM_PER_INCH = 25.4


def _nearest_column(width_mm: float, tol_mm: float = 6.0) -> tuple[float, float]:
    nearest = min(TARGET_WIDTHS_MM, key=lambda target: abs(width_mm - target))
    return nearest, abs(width_mm - nearest)


def audit_raster(path: Path) -> tuple[str, str]:
    """Inspect raster metadata (DPI, physical dimensions, RGB mode, LZW compression)."""
    ext = path.suffix.lower()
    with Image.open(path) as img:
        w_px, h_px = img.size
        dpi = img.info.get("dpi")
        mode = img.mode
        compression = img.info.get("compression", "-")

    warnings: list[str] = []
    if not dpi or dpi[0] <= 0 or dpi[1] <= 0:
        dpi_x = dpi_y = 72.0
        warnings.append("missing DPI metadata (defaulted 72)")
    else:
        dpi_x, dpi_y = float(dpi[0]), float(dpi[1])

    width_mm = (w_px / dpi_x) * MM_PER_INCH
    height_mm = (h_px / dpi_y) * MM_PER_INCH
    nearest_col, delta_mm = _nearest_column(width_mm)

    if ext in {".tif", ".tiff"}:
        if dpi_x < 500 or dpi_y < 500:
            warnings.append(f"low TIFF DPI ({dpi_x:.0f}x{dpi_y:.0f} < 500–600)")
        if str(compression).lower() not in {"tiff_lzw", "lzw"}:
            warnings.append(f"non-LZW TIFF compression ({compression})")
    elif ext == ".png":
        if dpi_x < 290 or dpi_y < 290:
            warnings.append(f"low PNG DPI ({dpi_x:.0f}x{dpi_y:.0f} < 300)")

    if mode == "RGBA":
        warnings.append("RGBA alpha channel present (prefer RGB)")
    elif mode not in {"RGB", "L"}:
        warnings.append(f"color mode {mode} (prefer RGB)")

    if delta_mm > 6.0:
        warnings.append(f"width {width_mm:.1f}mm deviates from {nearest_col:.0f}mm spec")
    if height_mm > MAX_HEIGHT_MM:
        warnings.append(f"height {height_mm:.1f}mm > {MAX_HEIGHT_MM:.0f}mm max")

    status = "WARN" if warnings else "PASS"
    details = (
        f"{w_px}x{h_px}px | {dpi_x:.0f} DPI | {width_mm:.1f}x{height_mm:.1f}mm | "
        f"{mode} | comp={compression}"
    )
    if warnings:
        details += " | " + "; ".join(warnings)
    return status, details


def audit_pdf(path: Path) -> tuple[str, str]:
    """Inspect PDF binary stream for unembedded Type3 bitmap fonts."""
    data = path.read_bytes()
    has_type3 = b"/Subtype /Type3" in data or b"/Subtype/Type3" in data
    size_kb = len(data) / 1024.0
    if has_type3:
        return "WARN", f"{size_kb:.1f} KB | Type3 bitmap fonts detected (set pdf.fonttype=42)"
    return "PASS", f"{size_kb:.1f} KB | vector PDF (no Type3 fonts detected)"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit figure files (.tiff, .png, .jpg, .pdf) against Elsevier specs."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Files or directories to audit.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any WARN is reported.",
    )
    args = parser.parse_args()

    targets: list[Path] = []
    exts = {".tif", ".tiff", ".png", ".jpg", ".jpeg", ".pdf"}
    for p in args.paths:
        resolved = p.resolve()
        if resolved.is_dir():
            targets.extend(
                sorted(f for f in resolved.iterdir() if f.is_file() and f.suffix.lower() in exts)
            )
        elif resolved.is_file():
            targets.append(resolved)

    if not targets:
        print("No figure files found.")
        return 1

    warn_count = 0
    for fig_path in targets:
        if fig_path.suffix.lower() == ".pdf":
            status, details = audit_pdf(fig_path)
        else:
            status, details = audit_raster(fig_path)
        if status == "WARN":
            warn_count += 1
        print(f"[{status}] {fig_path.name}: {details}")

    print(f"\nAudited {len(targets)} file(s), {warn_count} warning(s).")
    return 1 if (args.strict and warn_count > 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
