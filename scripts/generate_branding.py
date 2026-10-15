"""Generates icon.svg (the README banners come from build_readme.py).

Usage: python3 scripts/generate_branding.py   (run generate_file_icons.py first)
"""
from pathlib import Path
import math
import re
import runpy

root = Path(__file__).resolve().parent.parent
icons = root / "fileicons" / "icons"
pal = runpy.run_path(str(Path(__file__).with_name("generate_themes.py")))
DARK, LIGHT = pal["DARK"], pal["LIGHT"]


def inner(name):
    """Contents of an icon svg, with ids prefixed so several icons can share one document."""
    text = (icons / f"{name}.svg").read_text(encoding="utf-8")
    body = re.sub(r"^<svg[^>]*>|</svg>$", "", text)
    return body.replace('id="', f'id="p{name}-').replace("url(#", f"url(#p{name}-").replace('"url(#p' + name + '-', '"url(#p' + name + '-')


# ---------------------------------------------------------------- app icon: 3x3 grid of flat tiles
grid = ["#FF7DB0", "#FF9A6B", "#FFD97A", "#9B86FF", "#FFFFFF", "#7EE0A0", "#6EB8FF", "#5FD8E6", "#C77DFF"]
tiles = []
for i, c in enumerate(grid):
    x, y = 48 + (i % 3) * 56, 48 + (i // 3) * 56
    tiles.append(f'<rect x="{x}" y="{y}" width="48" height="48" rx="14" fill="{c}"/>')
icon = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><defs>'
    '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2C1A57"/><stop offset="1" stop-color="#120D22"/></linearGradient></defs>'
    '<rect x="8" y="8" width="240" height="240" rx="56" fill="url(#bg)"/>' + "".join(tiles) + '</svg>'
)
(root / "icon.svg").write_text(icon, encoding="utf-8")

print("branding written")
