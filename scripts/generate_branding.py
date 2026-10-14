"""Generates icon.svg and the README theme preview from the real theme palettes.

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

# ---------------------------------------------------------------- theme cards
CODE = [
    [("comment", "// Okto palette")],
    [("keyword", "import"), ("fg", " { "), ("function", "bead"), ("fg", " } "), ("keyword", "from"), ("fg", " "), ("string", '"./icons"'), ("fg", ";")],
    [],
    [("keyword", "export class"), ("fg", " "), ("type", "Theme"), ("fg", " {")],
    [("fg", "  "), ("keyword", "readonly"), ("fg", " "), ("property", "accent"), ("operator", " = "), ("string", '"#FF7DB0"'), ("fg", ";")],
    [("fg", "  "), ("function", "paint"), ("fg", "("), ("param", "name"), ("fg", ": "), ("type", "string"), ("fg", ") {")],
    [("fg", "    "), ("keyword", "return"), ("fg", " "), ("function", "bead"), ("fg", "("), ("param", "name"), ("fg", ", "), ("number", "42"), ("fg", ");")],
    [("fg", "  }")],
    [("fg", "}")],
]
TREE = [("folder-src-open", "src", 0), ("typescript", "index.ts", 1), ("json", "theme.json", 1), ("style", "style.css", 1),
        ("folder-assets", "assets", 0), ("image", "logo.png", 1), ("readme", "README.md", 0), ("lock", "yarn.lock", 0)]


def panel(p, x, y, w=430, h=290):
    s = []
    esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;")  # noqa: E731
    s.append(f'<g transform="translate({x} {y})">')
    s.append(f'<rect width="{w}" height="{h}" rx="14" fill="{p["editor"]}" stroke="{p["border"]}"/>')
    s.append(f'<path d="M0 14a14 14 0 0 1 14-14H{w - 14}a14 14 0 0 1 14 14V30H0Z" fill="{p["chrome"]}"/>')
    for i, c in enumerate((p["red"], p["yellow"], p["green"])):
        s.append(f'<circle cx="{18 + i * 16}" cy="15" r="4.5" fill="{c}"/>')
    s.append(f'<text x="{w / 2}" y="19" text-anchor="middle" font-family="Inter,sans-serif" font-size="10.5" fill="{p["muted"]}">{p["name"]}</text>')
    s.append(f'<rect y="30" width="34" height="{h - 52}" fill="{p["chrome"]}"/>')
    for i in range(4):
        s.append(f'<rect x="10" y="{44 + i * 26}" width="14" height="14" rx="4" fill="{p["accent"] if i == 0 else p["dim"]}" opacity="{1 if i == 0 else .6}"/>')
    s.append(f'<rect x="34" y="30" width="136" height="{h - 52}" fill="{p["side"]}"/>')
    s.append(f'<text x="46" y="48" font-family="Inter,sans-serif" font-size="9" letter-spacing="1.2" fill="{p["muted"]}">EXPLORER</text>')
    for i, (icon_name, label, depth) in enumerate(TREE):
        ty = 58 + i * 24
        if label == "index.ts":
            s.append(f'<rect x="34" y="{ty - 1}" width="136" height="22" fill="{p["select"]}"/>')
        s.append(f'<g transform="translate({46 + depth * 12} {ty + 2}) scale(.5)">{inner(icon_name)}</g>')
        s.append(f'<text x="{68 + depth * 12}" y="{ty + 14}" font-family="Inter,sans-serif" font-size="11" fill="{p["fg"] if label == "index.ts" else p["fg2"]}">{label}</text>')
    s.append(f'<rect x="170" y="30" width="{w - 170}" height="26" fill="{p["side"]}"/>')
    s.append(f'<rect x="170" y="30" width="104" height="26" fill="{p["editor"]}"/><rect x="170" y="30" width="104" height="2" fill="{p["accent"]}"/>')
    s.append(f'<g transform="translate(182 36) scale(.5)">{inner("typescript")}</g>')
    s.append(f'<text x="204" y="47" font-family="Inter,sans-serif" font-size="11" fill="{p["fg"]}">index.ts</text>')
    for i, line in enumerate(CODE):
        ly = 82 + i * 20
        s.append(f'<text x="196" y="{ly}" text-anchor="end" font-family="JetBrains Mono,Menlo,Consolas,monospace" font-size="10.5" fill="{p["faint"] if p["mode"] == "dark" else p["dim"]}">{i + 1}</text>')
        if line:
            spans = "".join(f'<tspan fill="{p["fg"] if k == "fg" else p[k]}"{" font-style=\"italic\"" if k in ("comment", "param") else ""}>{esc(t).replace(" ", chr(160))}</tspan>' for k, t in line)
            s.append(f'<text x="208" y="{ly}" font-family="JetBrains Mono,Menlo,Consolas,monospace" font-size="10.5" xml:space="preserve">{spans}</text>')
    s.append(f'<path d="M0 {h - 22}H{w}V{h - 14}a14 14 0 0 1-14 14H14a14 14 0 0 1-14-14Z" fill="{p["status_bg"]}"/>')
    s.append(f'<text x="14" y="{h - 7}" font-family="Inter,sans-serif" font-size="10" fill="{p["status_fg"]}">⎇ main</text>')
    s.append(f'<text x="{w - 14}" y="{h - 7}" text-anchor="end" font-family="Inter,sans-serif" font-size="10" fill="{p["status_fg"]}">TypeScript   UTF-8</text>')
    s.append("</g>")
    return "".join(s)


cards = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="920" height="334" viewBox="0 0 920 334">'
    '<defs><linearGradient id="page" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A1A52"/><stop offset="1" stop-color="#150E2B"/></linearGradient></defs>'
    '<rect width="920" height="334" rx="22" fill="url(#page)"/>'
    + panel(DARK, 20, 22) + panel(LIGHT, 470, 22) + "</svg>"
)
(root / "assets" / "readme" / "theme-cards.svg").write_text(cards, encoding="utf-8")
print("branding written")
