#!/usr/bin/env python3
"""Build the site logo and the favicons: a Fraunces "M" on a petrol disc.

Writes
    assets/img/logo.svg            header logo (languages.*.toml: logo), inlined by
                                   Blowfish; its colours come from the paasbox
                                   theme's CSS (.pb-logo-disc, .pb-logo-mark), so it
                                   follows the accent and the dark mode
    static/favicon.svg             the same, standalone, with a dark-mode swap
    static/favicon-16x16.png       the disc on transparent
    static/favicon-32x32.png
    static/favicon.ico             16 + 32 + 48
    static/apple-touch-icon.png    180, full-bleed petrol square (iOS rounds it)
    static/android-chrome-192x192.png, -512x512.png   same, for the manifest
    static/site.webmanifest

The "M" is the glyph itself, not text: a favicon cannot load web fonts. It is
cut from the theme's Fraunces at weight 500, optical size 48.

Needs fontTools and brotli (pip install fonttools brotli), rsvg-convert and
ImageMagick (brew install librsvg imagemagick). Run from the repository root:

    python3 scripts/logo.py
"""
import json
import subprocess
import tempfile
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "themes/paasbox/static/fonts/fraunces-latin-standard-normal.woff2"

# The paasbox theme's petrol accent and paper (themes/paasbox/assets/css/schemes/paasbox.css).
PETROL, PAPER = "#00657f", "#fbf8f1"
PETROL_DARK, PAPER_DARK = "#7fc7df", "#12161f"

SIZE = 64          # viewBox
CAP = 0.44         # height of the M relative to the box
OPTICAL_DROP = 0.5 # the M sits this many units below the exact centre, which looks centred


def m_path(size: float, cap: float) -> str:
    """The M as an SVG path in a size×size box, centred, y down."""
    font = instantiateVariableFont(TTFont(FONT), {"wght": 500, "opsz": 48})
    glyphs = font.getGlyphSet()
    name = font.getBestCmap()[ord("M")]
    bounds = BoundsPen(glyphs)
    glyphs[name].draw(bounds)
    x0, y0, x1, y1 = bounds.bounds
    scale = cap * size / (y1 - y0)
    width = (x1 - x0) * scale
    dx = (size - width) / 2 - x0 * scale
    baseline = size / 2 + (y1 - y0) * scale / 2 + OPTICAL_DROP
    pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, dx, baseline)))
    return pen.getCommands()


def svg(d: str, *, square: bool = False, style: str = "", disc: str = PETROL, mark: str = PAPER,
        classes: bool = False) -> str:
    shape = (f'<rect width="{SIZE}" height="{SIZE}"' if square
             else f'<circle cx="{SIZE / 2:g}" cy="{SIZE / 2:g}" r="{SIZE / 2:g}"')
    disc_cls = ' class="pb-logo-disc"' if classes else ""
    mark_cls = ' class="pb-logo-mark"' if classes else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" role="img" aria-label="Mitja Martini">'
            f"{style}{shape}{disc_cls} fill=\"{disc}\"/>"
            f'<path{mark_cls} fill="{mark}" d="{d}"/></svg>\n')


def png(source: str, out: Path, px: int) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
        f.write(source)
    subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px), "-o", str(out), f.name], check=True)


def main() -> None:
    d = m_path(SIZE, CAP)
    static = ROOT / "static"
    static.mkdir(exist_ok=True)

    (ROOT / "assets/img/logo.svg").write_text(svg(d, classes=True))

    dark = (f"<style>@media (prefers-color-scheme: dark) {{ circle {{ fill: {PETROL_DARK}; }} "
            f"path {{ fill: {PAPER_DARK}; }} }}</style>")
    (static / "favicon.svg").write_text(svg(d, style=dark))

    disc, square = svg(d), svg(d, square=True)
    for px in (16, 32, 48):
        png(disc, static / f"favicon-{px}x{px}.png", px)
    subprocess.run(["magick", *(str(static / f"favicon-{px}x{px}.png") for px in (16, 32, 48)),
                    str(static / "favicon.ico")], check=True)
    (static / "favicon-48x48.png").unlink()
    png(square, static / "apple-touch-icon.png", 180)
    for px in (192, 512):
        png(square, static / f"android-chrome-{px}x{px}.png", px)

    manifest = {
        "name": "Mitja Martini",
        "short_name": "Mitja Martini",
        "icons": [{"src": f"/android-chrome-{px}x{px}.png", "sizes": f"{px}x{px}", "type": "image/png"}
                  for px in (192, 512)],
        "theme_color": PETROL,
        "background_color": PAPER,
        "display": "standalone",
    }
    (static / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
