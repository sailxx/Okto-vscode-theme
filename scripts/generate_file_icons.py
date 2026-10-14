"""Generates the Okto flat file icon theme.

Every file type is a flat colour tile with a white glyph; folders are matching
flat folders with a small glyph badge. Text glyphs are converted to outlines
(Inter Bold) so the SVGs render identically everywhere.

Usage: python3 scripts/generate_file_icons.py [path/to/Inter-Bold.otf]
"""
from pathlib import Path
import json
import math
import sys
import xml.etree.ElementTree as ET

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

root = Path(__file__).resolve().parent.parent
icons = root / "fileicons" / "icons"
icons.mkdir(parents=True, exist_ok=True)
for old in icons.glob("*.svg"):
    old.unlink()

FONT_PATH = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
font = TTFont(FONT_PATH)
glyph_set = font.getGlyphSet()
cmap = font.getBestCmap()
units = font["head"].unitsPerEm


def text_path(text, size, tracking=0.0, dx=0.0, dy=0.0):
    """Outline `text`, centered on (dx, dy) by its ink bounds, as an SVG path."""
    scale = size / units
    rec = RecordingPen()
    x = 0
    for ch in text:
        name = cmap[ord(ch)]
        glyph = glyph_set[name]
        glyph.draw(TransformPen(rec, (1, 0, 0, 1, x, 0)))
        x += glyph.width + tracking * units
    bounds = BoundsPen(glyph_set)
    rec.replay(bounds)
    x0, y0, x1, y1 = bounds.bounds
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    out = SVGPathPen(glyph_set, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    rec.replay(TransformPen(out, (scale, 0, 0, -scale, dx - cx * scale, dy + cy * scale)))
    return out.getCommands()


def T(text, size, tracking=0.0, dx=0.0, dy=0.0):
    return f'<path fill="G" d="{text_path(text, size, tracking, dx, dy)}"/>'


def stroke(d, w=1.8, extra="", cap="round"):
    return f'<path d="{d}" fill="none" stroke="G" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round" {extra}/>'


def gear(teeth=8, inner=5.0, outer=7.6, hub=2.5, w=1.8):
    ticks = []
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        ticks.append(f"M{inner * math.cos(a) + .6 * math.cos(a):.2f} {inner * math.sin(a) + .6 * math.sin(a):.2f}L{outer * math.cos(a):.2f} {outer * math.sin(a):.2f}")
    ring = f'<circle r="{inner}" fill="none" stroke="G" stroke-width="{w}"/>'
    teeth_p = f'<path d="{"".join(ticks)}" stroke="G" stroke-width="{w + .9}" stroke-linecap="round"/>'
    hub_p = f'<circle r="{hub}" fill="G"/>' if hub else ""
    return ring + teeth_p + hub_p


# ---------------------------------------------------------------- glyphs
# Centered on (0, 0), roughly within +-8 units. "G" = glyph colour, "D" = deep bead colour.
glyphs = {
    "javascript": T("JS", 10.5, -.02),
    "typescript": T("TS", 10.5, -.02),
    "style": T("CSS", 7.4, 0),
    "json": T("{}", 12.5, .02),
    "yaml": T("YML", 7.2, 0),
    "pdf": T("PDF", 6.8, 0),
    "go": T("GO", 9, 0),
    "c": T("C", 14.5, 0),
    "cpp": T("C++", 8.6, -.02),
    "csharp": T("C#", 9.2, -.02),
    "kotlin": T("K", 14.5, 0),
    "svelte": '<g transform="skewX(-9)">' + T("S", 14.5) + "</g>",
    "php": '<g transform="skewX(-10)">' + T("php", 8.6, -.02) + "</g>",
    "markdown": T("M", 9.5, 0, -2.6) + stroke("M5.4 -3.4V3.4M3 1.2L5.4 3.6L7.8 1.2", 1.7),
    "code": stroke("M-3.6 -4.6L-8 0L-3.6 4.6M3.6 -4.6L8 0L3.6 4.6M1.7 -6.8L-1.7 6.8", 1.9),
    "markup": stroke("M-2.6 -5L-7.6 0L-2.6 5M2.6 -5L7.6 0L2.6 5", 2.1),
    "terminal": stroke("M-6.2 -4.6L-1.6 0L-6.2 4.6M1 5.4H7.2", 2.1),
    "git": (
        '<g fill="none" stroke="G" stroke-width="1.8" stroke-linecap="round">'
        '<circle cx="-3.6" cy="-5" r="1.9"/><circle cx="-3.6" cy="5" r="1.9"/><circle cx="4" cy="-1.6" r="1.9"/>'
        '<path d="M-3.6 -3.1V3.1M4 .3Q4 3.6 -1.4 3.9Q-3.6 4.1 -3.6 3.1"/></g>'
    ),
    "database": (
        '<ellipse cy="-4.6" rx="6" ry="2.4" fill="G"/>'
        + stroke("M-6 -4.6V4.6C-6 6.4 -3.3 7.1 0 7.1S6 6.4 6 4.6V-4.6M-6 0C-6 1.8 -3.3 2.5 0 2.5S6 1.8 6 0", 1.7)
    ),
    "image": (
        '<rect x="-7.4" y="-6.8" width="14.8" height="13.6" rx="2.2" fill="none" stroke="G" stroke-width="1.5"/>'
        '<path d="M-7 6.2L-2.2 -.6L1.2 3.8L3.4 1.4L7 6.2Z" fill="G"/><circle cx="3.6" cy="-3.2" r="1.7" fill="G"/>'
    ),
    "package": stroke("M0 -7.5L6.5 -4V3.8L0 7.5L-6.5 3.8V-4ZM-6.5 -4L0 -.3L6.5 -4M0 -.3V7.5", 1.7),
    "config": gear(8),
    "rust": gear(10, 5.6, 7.9, 0, 1.6) + T("R", 6.6),
    "readme": stroke("M0 -4.4C-2 -6 -5 -6 -7 -5V5.6C-5 4.6 -2 4.6 0 6.1C2 4.6 5 4.6 7 5.6V-5C5 -6 2 -6 0 -4.4ZM0 -4.4V6.1", 1.6),
    "file": stroke("M-5 -7.5H1.6L5.6 -3.5V7.5H-5ZM1.6 -7.5V-3.5H5.6M-2 1.5H2.8M-2 4.4H2.8", 1.6),
    "text": stroke("M-6 -5H6M-6 -1.7H6M-6 1.6H6M-6 4.9H2.4", 1.9),
    "lock": (
        '<rect x="-5.6" y="-1" width="11.2" height="8.4" rx="1.9" fill="G"/>'
        + stroke("M-3.2 -1V-3.1A3.2 3.2 0 0 1 3.2 -3.1V-1", 1.9)
        + '<circle cy="2.6" r="1.3" fill="D"/><rect x="-.55" y="3" width="1.1" height="2.6" rx=".5" fill="D"/>'
    ),
    "env": (
        '<circle cx="-3.2" cy="-2.6" r="3.3" fill="none" stroke="G" stroke-width="1.9"/>'
        + stroke("M-.8 -.2L6.6 7.2M3.9 4.5L6 2.4", 1.9)
    ),
    "test": stroke("M-1.4 -7H1.4M-1.4 -7V-1.2L-6 5.4Q-6.9 7.2 -5 7.2H5Q6.9 7.2 6 5.4L1.4 -1.2V-7M-4 3H4", 1.6),
    "license": stroke("M0 -7.5L6.5 -5V0C6.5 4 3.5 6.5 0 7.9C-3.5 6.5 -6.5 4 -6.5 0V-5ZM-2.6 .2L-.6 2.3L3.1 -2.4", 1.7),
    "zip": (
        '<rect x="-6" y="-7" width="12" height="14" rx="2.2" fill="none" stroke="G" stroke-width="1.6"/>'
        + stroke("M0 -6.2V.4", 1.8, 'stroke-dasharray="1.5 1.6"', "butt")
        + '<rect x="-1.9" y="1.6" width="3.8" height="4.4" rx="1.1" fill="G"/>'
    ),
    "docker": (
        '<g transform="translate(-15 -13.6) scale(1.1)"><path fill="G" d="M9 15h12c-.5 2.7-2.300 4-5.500 4H12c-2 0-3.100-1.200-3-4zm2-3h2v2h-2zm3 0h2v2h-2zm3 0h2v2h-2zm-6-3h2v2h-2zm3 0h2v2h-2zm3 0h2v2h-2z"/></g>'
    ),
    "python": (
        '<g transform="translate(-16 -15) scale(1.06)">'
        '<path fill="G" d="M16 7.5h-3.2c-2.1 0-3.4 1.2-3.4 3.2v2h7.1v1.2h-6c-2.2 0-3.6 1.4-3.6 3.6s1.4 3.8 3.6 3.8h2.2v-2.1c0-2.2 1.5-3.8 3.7-3.8h3.1c1.8 0 3-1.2 3-3v-1.5c0-2-1.2-3.4-3.4-3.4zm-1.8 2.1a.8.8 0 1 1 0 1.6.8.8 0 0 1 0-1.6z"/>'
        '<path fill="#FFE27A" d="M16 22.5h3.2c2.1 0 3.4-1.2 3.4-3.2v-2h-7.1v-1.2h6c2.2 0 3.6-1.4 3.6-3.6s-1.4-3.8-3.6-3.8h-2.2v2.1c0 2.2-1.5 3.8-3.7 3.8h-3.1c-1.8 0-3 1.2-3 3v1.5c0 2 1.2 3.4 3.4 3.4zm1.8-2.1a.8.8 0 1 1 0-1.6.8.8 0 0 1 0 1.6z"/></g>'
    ),
    "java": (
        '<g transform="translate(-15.5 -14) scale(1.05)">'
        '<path d="M15.8 7.5c-2 1.3 2.4 1.7.1 3.1m2-4.2c-3 1.9 2.7 2.2.1 4.6M10 13.5h11l-1.1 4.2c-.3 1-1 1.5-2.1 1.5h-4.6c-1.1 0-1.8-.5-2.1-1.5zm1.2 7h8.5" fill="none" stroke="G" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></g>'
    ),
    "swift": (
        '<g transform="translate(-16.2 -16.2) scale(1.04)"><path fill="G" d="M8.5 11.1c2.2 2.4 4.3 4 6.4 4.7-1.2-1.8-2-3.8-2.4-5.8 2.7 3.1 5.5 5.2 9 6.2-.5 3.3-3.2 5.4-6.5 5.4-2.3 0-4.5-.9-6.1-2.6 2 .4 3.8.1 5.1-.8-2.5-.9-4.5-3.1-5.5-7.1z"/>'
        '<path d="M9 22c4.2 1.3 8.4.6 11.6-1.700" fill="none" stroke="G" stroke-width="1.5" stroke-linecap="round"/></g>'
    ),
    "ruby": stroke("M-7 -2L-3.6 -6.6H3.6L7 -2L0 7ZM-7 -2H7M-3.6 -6.6L-1.9 -2L0 7M3.6 -6.6L1.9 -2L0 7", 1.5),
    "vue": '<path fill="G" d="M-7.2 -5.6H-3.2L0 0L3.2 -5.6H7.2L0 7Z"/>',
}

# name: (top, base, deep, glyph colour)
beads = {
    "python": ("#6FB2F2", "#3A78C2", "#1F4584"),
    "javascript": ("#FFE470", "#F7C21B", "#C98A00", "#3A2B00"),
    "typescript": ("#5AA6F2", "#2F6FD0", "#1B429A"),
    "json": ("#FFC878", "#F2A03A", "#BD6A12"),
    "markdown": ("#76CFF8", "#2F9DE2", "#1A68B0"),
    "image": ("#7BE6AC", "#31C27C", "#188852"),
    "database": ("#5ADCEB", "#16B3CE", "#0B7C97"),
    "terminal": ("#6D7188", "#3F4256", "#20222E", "#7CFFB4"),
    "style": ("#9C96FF", "#6560EC", "#3D36B6"),
    "markup": ("#FFA277", "#EF5E37", "#B33615"),
    "yaml": ("#FF98B8", "#E94D83", "#A92757"),
    "config": ("#C4CCE0", "#8A96B4", "#586380"),
    "package": ("#E2B27B", "#BC803F", "#80501F"),
    "lock": ("#FFD487", "#E5A53A", "#A56E12", "#FFFFFF"),
    "git": ("#FF8777", "#E9442F", "#A82314"),
    "docker": ("#68C9FF", "#2098F2", "#1066BA"),
    "readme": ("#86E6C8", "#2FC09A", "#178A6D"),
    "code": ("#BFA6FF", "#8765EA", "#5838BA"),
    "rust": ("#F6AE76", "#CF6E30", "#8F4014"),
    "go": ("#66E4F2", "#16BAD8", "#0A7F99"),
    "java": ("#FFA25E", "#EA6A1D", "#A9410B"),
    "c": ("#88B9F4", "#4F86D3", "#2B5298"),
    "cpp": ("#62A1E4", "#326CBC", "#1A417D"),
    "csharp": ("#CB88E6", "#9A4DBC", "#652A82"),
    "ruby": ("#FF7483", "#D92B40", "#921527"),
    "php": ("#ADB0EC", "#7B7FC8", "#4C4F93"),
    "swift": ("#FF9A72", "#F2552E", "#B23212"),
    "kotlin": ("#B096FF", "#8052F2", "#552ABA"),
    "svelte": ("#FF8556", "#F2461E", "#B22C0B"),
    "vue": ("#6BE6B0", "#30BC84", "#188B5E"),
    "file": ("#E0DEEE", "#B9B5D0", "#8884A4", "#FFFFFF"),
    "text": ("#C7CBDA", "#9097AF", "#5E6580"),
    "env": ("#EBE174", "#C0B531", "#847B0E", "#FFFFFF"),
    "test": ("#74E6CF", "#27BFA2", "#12887A"),
    "license": ("#CDD2EA", "#8E98C6", "#5C6598"),
    "zip": ("#E6A8F4", "#BE5AD8", "#842F9C"),
    "pdf": ("#FF8484", "#E23C3C", "#9E1B1B"),
}

# kind: (top, base, deep, glyph or None)
folders = {
    "default": ("#B1ACFF", "#7F78F2", "#4F48C6", None),
    "src": ("#82EBAE", "#38C47C", "#1D8F56", "code"),
    "docs": ("#82CEFF", "#3E9DEB", "#2269B6", "readme"),
    "test": ("#FFD684", "#F5A430", "#BA6D10", "test"),
    "assets": ("#FFA3C6", "#EF5F95", "#B33164", "image"),
    "public": ("#74EBE3", "#25C0B8", "#108985", "globe"),
    "config": ("#CDD4E8", "#909CBB", "#606B8A", "config"),
    "git": ("#FF8F7D", "#E94A3D", "#A9291D", "git"),
    "modules": ("#93E37F", "#52BA42", "#318527", "package"),
    "scripts": ("#8E92AB", "#585B73", "#363849", "terminal"),
}
glyphs["globe"] = (
    '<g fill="none" stroke="G" stroke-width="1.6"><circle r="6.2"/><ellipse rx="2.7" ry="6.2"/><path d="M-6.2 0H6.2"/></g>'
)


def clamp(v):
    return max(0, min(255, round(v)))


def tint(hex_color, f):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f >= 0:
        r, g, b = (clamp(v + (255 - v) * f) for v in (r, g, b))
    else:
        r, g, b = (clamp(v * (1 + f)) for v in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def paint(frag, glyph_color, deep):
    return frag.replace('"G"', f'"{glyph_color}"').replace('"D"', f'"{deep}"')


def glyph_group(name, glyph_color, deep, transform):
    return f'<g transform="{transform}">{paint(glyphs[name], glyph_color, deep)}</g>'


def bead_svg(name, top, base, deep, glyph_color="#FFFFFF"):
    gid = f"t-{name}"
    body = (
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
        f'<stop offset="1" stop-color="{base}"/></linearGradient></defs>'
        f'<rect x="2.5" y="2.5" width="27" height="27" rx="8" fill="url(#{gid})"/>'
        + glyph_group(name, glyph_color, base, "translate(16 16) scale(1.02)")
    )
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">{body}</svg>'


FOLDER_BACK = "M3 8.2A2.2 2.2 0 0 1 5.200 6H12l2.600 2.900H26.800A2.200 2.200 0 0 1 29 11.100V24.200A2.200 2.200 0 0 1 26.800 26.400H5.200A2.200 2.200 0 0 1 3 24.200Z"
FOLDER_FRONT = "M3 13.300A2.200 2.200 0 0 1 5.200 11.100H26.800A2.200 2.200 0 0 1 29 13.300V24.200A2.200 2.200 0 0 1 26.800 26.400H5.200A2.200 2.200 0 0 1 3 24.200Z"
FOLDER_OPEN_FRONT = "M6.400 13.600Q6.900 12.400 8.200 12.400H29.600Q31.500 12.400 31 14.300L28.200 24.700Q27.700 26.400 26 26.400H4.600Q3 26.400 3.300 24.800Z"


def folder_svg(kind, top, base, deep, glyph, opened):
    gid = f"f-{kind}{'-o' if opened else ''}"
    front = FOLDER_OPEN_FRONT if opened else FOLDER_FRONT
    badge = ""
    if glyph:
        cx, cy = (17, 20.3) if opened else (16, 19.4)
        badge = glyph_group(glyph, "#FFFFFF", deep, f"translate({cx} {cy}) scale(.56)")
    body = (
        f'<path d="{FOLDER_BACK}" fill="{deep}"/>'
        f'<path d="{front}" fill="{base}"/>'
        f'{badge}'
    )
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">{body}</svg>'


for name in glyphs:
    if name == "globe":
        continue
    if name not in beads:
        raise SystemExit(f"missing bead colours for {name}")
for name, spec in beads.items():
    (icons / f"{name}.svg").write_text(bead_svg(name, *spec), encoding="utf-8")
for kind, (top, base, deep, glyph) in folders.items():
    (icons / f"folder-{kind}.svg").write_text(folder_svg(kind, top, base, deep, glyph, False), encoding="utf-8")
    (icons / f"folder-{kind}-open.svg").write_text(folder_svg(kind, top, base, deep, glyph, True), encoding="utf-8")

# ---------------------------------------------------------------- theme mapping
defs = {f"_{n}": {"iconPath": f"./icons/{n}.svg"} for n in beads}
for kind in folders:
    defs[f"_folder_{kind}"] = {"iconPath": f"./icons/folder-{kind}.svg"}
    defs[f"_folder_{kind}_open"] = {"iconPath": f"./icons/folder-{kind}-open.svg"}

ext_map = {
    "javascript": "js mjs cjs jsx", "typescript": "ts tsx mts cts", "json": "json jsonc json5 map",
    "markdown": "md mdx markdown", "image": "png jpg jpeg gif webp avif bmp ico svg",
    "markup": "html htm xhtml xml", "style": "css scss sass less styl",
    "yaml": "yml yaml", "config": "toml ini conf cfg properties editorconfig",
    "terminal": "sh bash zsh fish bat cmd ps1", "python": "py pyi pyw",
    "database": "sql db sqlite sqlite3", "rust": "rs", "go": "go", "java": "java",
    "c": "c h", "cpp": "cpp cc cxx hpp hh hxx", "csharp": "cs csx", "ruby": "rb",
    "php": "php", "swift": "swift", "kotlin": "kt kts", "svelte": "svelte", "vue": "vue",
    "lock": "lock", "text": "txt log", "pdf": "pdf", "zip": "zip tar gz tgz rar 7z",
    "env": "env", "test": "test.ts spec.ts test.tsx spec.tsx test.js spec.js test.jsx spec.jsx",
}
file_extensions = {e: f"_{icon}" for icon, exts in ext_map.items() for e in exts.split()}

file_names = {}
for n in ("README.md", "README.txt", "README", "CHANGELOG.md", "CONTRIBUTING.md"):
    file_names[n] = "_readme"
for n in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
    file_names[n] = "_license"
for n in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".dockerignore"):
    file_names[n] = "_docker"
for n in ("package.json", "Cargo.toml", "requirements.txt", "composer.json", "Gemfile"):
    file_names[n] = "_package"
for n in ("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Cargo.lock", "poetry.lock", "Gemfile.lock", "composer.lock", "go.sum"):
    file_names[n] = "_lock"
for n in (".gitignore", ".gitattributes", ".gitmodules"):
    file_names[n] = "_git"
for n in (".env", ".env.example", ".env.local", ".env.production", ".env.development"):
    file_names[n] = "_env"
for n in ("tsconfig.json", "settings.json", ".editorconfig", ".prettierrc", ".eslintrc.json"):
    file_names[n] = "_config"
file_names.update({"Makefile": "_code", "go.mod": "_go", "pyproject.toml": "_python"})

folder_names = {}
for kind, names in {
    "src": "src source lib app",
    "docs": "doc docs documentation",
    "test": "test tests __tests__ spec specs",
    "assets": "assets images img static media",
    "public": "public dist build out www",
    "config": ".vscode config .config .idea",
    "git": ".git .github .gitlab",
    "modules": "node_modules vendor",
    "scripts": "scripts bin tools",
}.items():
    for n in names.split():
        folder_names[n] = f"_folder_{kind}"
folder_names_open = {n: f"{v}_open" for n, v in folder_names.items()}

language_ids = {
    "javascript": "javascript", "javascriptreact": "javascript", "typescript": "typescript",
    "typescriptreact": "typescript", "json": "json", "jsonc": "json", "markdown": "markdown",
    "html": "markup", "xml": "markup", "css": "style", "scss": "style", "less": "style",
    "yaml": "yaml", "python": "python", "sql": "database", "rust": "rust", "go": "go",
    "java": "java", "c": "c", "cpp": "cpp", "csharp": "csharp", "ruby": "ruby", "php": "php",
    "swift": "swift", "kotlin": "kotlin", "svelte": "svelte", "vue": "vue",
    "shellscript": "terminal", "powershell": "terminal", "dockerfile": "docker",
}

theme = {
    "$schema": "vscode://schemas/icon-theme",
    "iconDefinitions": defs,
    "file": "_file",
    "folder": "_folder_default",
    "folderExpanded": "_folder_default_open",
    "rootFolder": "_folder_default",
    "rootFolderExpanded": "_folder_default_open",
    "folderNames": folder_names,
    "folderNamesExpanded": folder_names_open,
    "fileExtensions": file_extensions,
    "fileNames": file_names,
    "languageIds": {k: f"_{v}" for k, v in language_ids.items()},
}
(root / "fileicons" / "okto-icon-theme.json").write_text(json.dumps(theme, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- README gallery
gallery_names = sorted(beads) + [f"folder-{k}" for k in folders]
cols, cell_w, cell_h = 8, 108, 78
rows = (len(gallery_names) + cols - 1) // cols
width, height = cols * cell_w, rows * cell_h + 16
out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#241446"/><stop offset="1" stop-color="#160E2E"/></linearGradient></defs>',
    f'<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>',
]
for i, name in enumerate(gallery_names):
    col, row = i % cols, i // cols
    x, y = col * cell_w, row * cell_h + 8
    svg_root = ET.parse(icons / f"{name}.svg").getroot()
    out.append(f'<g transform="translate({x + 34},{y + 4}) scale(1.2)">')
    for child in list(svg_root):
        out.append(ET.tostring(child, encoding="unicode").replace("ns0:", "").replace(' xmlns:ns0="http://www.w3.org/2000/svg"', ""))
    out.append("</g>")
    out.append(f'<text x="{x + cell_w / 2}" y="{y + 66}" text-anchor="middle" fill="#CFC3EA" font-family="Inter, Segoe UI, sans-serif" font-size="10.5">{name.replace("folder-", "📁 ").replace("📁 ", "folder · ")}</text>')
out.append("</svg>")
(root / "assets" / "readme" / "file-icon-gallery.svg").write_text("\n".join(out), encoding="utf-8")
print(f"{len(beads)} beads, {len(folders) * 2} folders")
