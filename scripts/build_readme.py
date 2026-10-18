"""Builds the README banners (RU + EN) in the Okto house style: black frame, soft glows,
white-to-grey headline accents, cards and mono chips. Fonts (Golos Text, JetBrains Mono,
SIL OFL 1.1) are subset per language and embedded.

Usage: python3 scripts/build_readme.py   (run generate_file_icons.py and generate_branding.py first)
"""
from pathlib import Path
import base64
import io
import json
import re
import runpy

from fontTools import subset
from fontTools.ttLib import TTFont

root = Path(__file__).resolve().parent.parent
out_dir = root / "assets" / "readme"
out_dir.mkdir(parents=True, exist_ok=True)
for old in out_dir.glob("*"):
    old.unlink()
icons = root / "fileicons" / "icons"
pal = runpy.run_path(str(Path(__file__).with_name("generate_themes.py")))
DARK, LIGHT = pal["DARK"], pal["LIGHT"]
VERSION = json.loads((root / "package.json").read_text(encoding="utf-8"))["version"]
FONT_G = Path(__file__).with_name("fonts") / "golos.ttf"
FONT_M = Path(__file__).with_name("fonts") / "jbmono.ttf"

MUTED, DIM, STROKE = "#A3A3A3", "#6E6E6E", "#2A2A2A"

STR = {
    "ru": {
        "hero": {
            "alt": "Okto для VS Code — две цветовые темы и цветные иконки файлов и папок",
            "title": ["Темы и иконки", "для *VS Code*"],
            "sub": ["Тёмная и светлая темы, 37 иконок файлов", "и цветные папки в стиле Okto."],
            "cards": [["Две темы", "Okto Dark и Okto Light"], ["Иконки файлов", "37 типов, плоские плитки"], ["Цветные папки", "10 видов со значками"], ["Подсветка кода", "Семантическая, 30+ правил"]],
        },
        "buttons": {"download": "Скачать .vsix", "whatsNew": "Что нового"},
        "features": {
            "alt": "Возможности: темы, иконки файлов, цветные папки, подсветка кода", "chip": "Возможности", "title": "Всё для *уютного редактора*",
            "items": [
                ["Две темы", ["Фиолетово-чернильная тёмная и тёплая", "лиловая светлая, розовый акцент."]],
                ["Иконки файлов", ["37 типов: от Python и TypeScript", "до lock-файлов, .env и PDF."]],
                ["Цветные папки", ["src, docs, test, assets, config, git", "и другие — со значком на лицевой стороне."]],
                ["Подсветка кода", ["Семантические токены и TextMate:", "30+ правил, Markdown, CSS, JSON, diff."]],
            ],
        },
        "icons": {"alt": "Иконки Okto: плитки для файлов и цветные папки", "chip": "Иконки", "title": "Свой цвет *для каждого типа*"},
        "themes": {"alt": "Темы Okto Dark и Okto Light", "chip": "Темы", "title": "Два режима, *один характер*"},
    },
    "en": {
        "hero": {
            "alt": "Okto for VS Code — two color themes and colorful file and folder icons",
            "title": ["Themes and icons", "for *VS Code*"],
            "sub": ["Dark and light themes, 37 file icons", "and color-coded folders in the Okto style."],
            "cards": [["Two themes", "Okto Dark and Okto Light"], ["File icons", "37 types, flat tiles"], ["Color folders", "10 kinds with badges"], ["Code highlighting", "Semantic, 30+ rules"]],
        },
        "buttons": {"download": "Download .vsix", "whatsNew": "What’s new"},
        "features": {
            "alt": "Features: themes, file icons, color folders, code highlighting", "chip": "Features", "title": "Everything for a *cozy editor*",
            "items": [
                ["Two themes", ["An ink-violet dark and a warm lilac", "light theme with a pink accent."]],
                ["File icons", ["37 types: from Python and TypeScript", "to lock files, .env and PDF."]],
                ["Color folders", ["src, docs, test, assets, config, git", "and more — each with a badge on the front."]],
                ["Code highlighting", ["Semantic tokens plus TextMate:", "30+ rules, Markdown, CSS, JSON, diff."]],
            ],
        },
        "icons": {"alt": "Okto icons: tiles for files and color folders", "chip": "Icons", "title": "A color for *every file type*"},
        "themes": {"alt": "Okto Dark and Okto Light themes", "chip": "Themes", "title": "Two modes, *one character*"},
    },
}

all_text = ""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(s):
    global all_text
    all_text += str(s)
    return esc(s)


def style(fg, fm):
    return f"""<style>
@font-face{{font-family:"G";src:url(data:font/woff2;base64,{fg}) format("woff2");font-weight:100 900}}
@font-face{{font-family:"M";src:url(data:font/woff2;base64,{fm}) format("woff2");font-weight:100 900}}
text{{font-family:"G","Segoe UI",system-ui,sans-serif}}
.m{{font-family:"M",ui-monospace,Consolas,monospace}}
.r{{animation:rise .8s cubic-bezier(.2,.8,.2,1) backwards}}
.glow{{animation:drift 14s ease-in-out infinite}}
.glow2{{animation:drift 18s ease-in-out -6s infinite reverse}}
.sweep{{animation:sweep 6s ease-in-out infinite}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(36px,22px)}}}}
@keyframes sweep{{0%{{transform:translateX(-120%)}}60%,100%{{transform:translateX(220%)}}}}
@media (prefers-reduced-motion:reduce){{.r,.glow,.glow2,.sweep{{animation:none}}}}
</style>"""


def defs(w, h):
    return f"""<defs>
<radialGradient id="g1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#9aa4b8" stop-opacity=".14"/><stop offset="1" stop-color="#9aa4b8" stop-opacity="0"/></radialGradient>
<linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1c1c1c"/><stop offset="1" stop-color="#0a0a0a"/></linearGradient>
<linearGradient id="hl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#8d8d8d"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0d0d"/><stop offset="1" stop-color="#000"/></linearGradient>
<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".6"/></filter>
<clipPath id="clip"><rect width="{w}" height="{h}" rx="24"/></clipPath>
</defs>"""


def frame(w, h):
    return f"""<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="url(#bg)"/>
<circle class="glow" cx="{w * .82}" cy="{h * .2}" r="{h * .7}" fill="url(#g1)"/>
<circle class="glow2" cx="{w * .1}" cy="{h * .95}" r="{h * .6}" fill="url(#g2)"/>
<rect class="sweep" x="0" y="0" width="{w * .35}" height="{h}" fill="url(#sw)"/></g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="24" fill="none" stroke="#242424"/>"""


def svg(w, h, label, body):
    def render(fg, fm):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" fill="#fff" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">\n'
                f"{style(fg, fm)}\n{defs(w, h)}\n{frame(w, h)}\n{body}\n</svg>\n")
    return render


def spans(parts):
    return "".join(f'<tspan{" fill=\"url(#tg)\"" if hi else ""}>{T(s)}</tspan>' for s, hi in parts)


def accent(s):
    return [(p, i % 2 == 1) for i, p in enumerate(s.split("*")) if p]


def delay(i):
    return f'style="animation-delay:{i * .09:.2f}s"'


def card(x, y, w, h, rx=18):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#cg)" stroke="{STROKE}"/>'
            f'<rect x="{x + rx}" y="{y + .5}" width="{w - rx * 2}" height="1" fill="url(#hl)"/>')


def chip(x, y, text, check=False):
    label = text.upper()
    w = round(len(label) * 8.4 + (46 if check else 28))
    s = f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="8" fill="#141414" stroke="#333"/>'
    tx = x + 14
    if check:
        s += f'<path d="M{x + 13} {y + 15.5}l4 4 8-8.5" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        tx = x + 32
    s += f'<text class="m" x="{tx}" y="{y + 20}" font-size="12" font-weight="600" letter-spacing="1" fill="#fff">{T(label)}</text>'
    return s, w


def section_head(label, parts):
    c, _ = chip(40, 34, label, True)
    return (f'<g class="r">{c}</g>\n<g class="r" {delay(1)}><text x="40" y="104" font-size="32" font-weight="800" letter-spacing="-.6">{spans(parts)}</text></g>')


def inner(name):
    text = (icons / f"{name}.svg").read_text(encoding="utf-8")
    return re.sub(r"^<svg[^>]*>|</svg>$", "", text)


def icon_at(name, x, y, size):
    return f'<g transform="translate({x} {y}) scale({size / 32:.3f})">{inner(name)}</g>'


# ------------------------------------------------------------------ editor mock (real palettes)
CODE = [
    [("comment", "// Okto palette")],
    [("keyword", "import"), ("fg", " { "), ("function", "bead"), ("fg", " } "), ("keyword", "from"), ("fg", " "), ("string", '"./icons"'), ("fg", ";")],
    [],
    [("keyword", "export class"), ("fg", " "), ("type", "Theme"), ("fg", " {")],
    [("fg", "  "), ("keyword", "readonly"), ("fg", " "), ("property", "accent"), ("operator", " = "), ("string", '"#FF7DB0"'), ("fg", ";")],
    [("fg", "  "), ("function", "paint"), ("fg", "("), ("param", "name"), ("fg", ": "), ("type", "string"), ("fg", ") {")],
    [("fg", "    "), ("keyword", "return"), ("fg", " "), ("function", "tile"), ("fg", "("), ("param", "name"), ("fg", ", "), ("number", "32"), ("fg", ");")],
    [("fg", "  }")],
    [("fg", "}")],
]
TREE = [("folder-src-open", "src", 0), ("typescript", "index.ts", 1), ("json", "theme.json", 1), ("style", "style.css", 1),
        ("folder-assets", "assets", 0), ("image", "logo.png", 1), ("readme", "README.md", 0), ("lock", "yarn.lock", 0)]


def mock(p, x, y, scale=1.0, w=430, h=290, shadow=False):
    dark = p["mode"] == "dark"
    s = [f'<g transform="translate({x} {y}) scale({scale})"{" filter=\"url(#sh)\"" if shadow else ""}>']
    s.append(f'<rect width="{w}" height="{h}" rx="14" fill="{p["editor"]}" stroke="{p["border"]}"/>')
    s.append(f'<path d="M0 14a14 14 0 0 1 14-14H{w - 14}a14 14 0 0 1 14 14V30H0Z" fill="{p["chrome"]}"/>')
    for i, c in enumerate((p["red"], p["yellow"], p["green"])):
        s.append(f'<circle cx="{18 + i * 16}" cy="15" r="4.5" fill="{c}"/>')
    s.append(f'<text x="{w / 2}" y="19" text-anchor="middle" font-size="10.5" fill="{p["muted"]}">{T(p["name"])}</text>')
    s.append(f'<rect y="30" width="34" height="{h - 52}" fill="{p["chrome"]}"/>')
    for i in range(4):
        s.append(f'<rect x="10" y="{44 + i * 26}" width="14" height="14" rx="4" fill="{p["accent"] if i == 0 else p["dim"]}" opacity="{1 if i == 0 else .6}"/>')
    s.append(f'<rect x="34" y="30" width="136" height="{h - 52}" fill="{p["side"]}"/>')
    s.append(f'<text x="46" y="48" font-size="9" letter-spacing="1.2" fill="{p["muted"]}">{T("EXPLORER")}</text>')
    for i, (icon_name, label, depth) in enumerate(TREE):
        ty = 58 + i * 24
        if label == "index.ts":
            s.append(f'<rect x="34" y="{ty - 1}" width="136" height="22" fill="{p["select"]}"/>')
        s.append(icon_at(icon_name, 46 + depth * 12, ty + 2, 16))
        s.append(f'<text x="{68 + depth * 12}" y="{ty + 14}" font-size="11" fill="{p["fg"] if label == "index.ts" else p["fg2"]}">{T(label)}</text>')
    s.append(f'<rect x="170" y="30" width="{w - 170}" height="26" fill="{p["side"]}"/>')
    s.append(f'<rect x="170" y="30" width="104" height="26" fill="{p["editor"]}"/><rect x="170" y="30" width="104" height="2" fill="{p["accent"]}"/>')
    s.append(icon_at("typescript", 182, 36, 16))
    s.append(f'<text x="204" y="47" font-size="11" fill="{p["fg"]}">{T("index.ts")}</text>')
    for i, line in enumerate(CODE):
        ly = 82 + i * 20
        s.append(f'<text class="m" x="196" y="{ly}" text-anchor="end" font-size="10.5" fill="{p["faint"] if dark else p["dim"]}">{i + 1}</text>')
        if line:
            parts = "".join(
                f'<tspan fill="{p["fg"] if k == "fg" else p[k]}"{" font-style=\"italic\"" if k in ("comment", "param") else ""}>{T(t).replace(" ", chr(160))}</tspan>'
                for k, t in line)
            s.append(f'<text class="m" x="208" y="{ly}" font-size="10.5" xml:space="preserve">{parts}</text>')
    s.append(f'<path d="M0 {h - 22}H{w}V{h - 14}a14 14 0 0 1-14 14H14a14 14 0 0 1-14-14Z" fill="{p["status_bg"]}"/>')
    s.append(f'<text x="14" y="{h - 7}" font-size="10" fill="{p["status_fg"]}">{T("main")}</text>')
    s.append(f'<text x="{w - 14}" y="{h - 7}" text-anchor="end" font-size="10" fill="{p["status_fg"]}">{T("TypeScript · UTF-8")}</text>')
    s.append("</g>")
    return "".join(s)


# ------------------------------------------------------------------ banners
def hero(t):
    b = ""
    b += (f'<g class="r">{icon_svg_logo(40, 34, 36)}<text x="88" y="61" font-size="22" font-weight="800" letter-spacing="-.3">{T("Okto")}</text></g>')
    c, _ = chip(158, 39, "v" + VERSION)
    b += f'<g class="r" {delay(1)}>{c}</g>'
    b += (f'<g class="r" {delay(2)}><text x="40" y="146" font-size="38" font-weight="800" letter-spacing="-1">{spans(accent(t["hero"]["title"][0]))}</text>'
          f'<text x="40" y="192" font-size="38" font-weight="800" letter-spacing="-1">{spans(accent(t["hero"]["title"][1]))}</text></g>')
    b += (f'<g class="r" {delay(3)}><text x="40" y="232" font-size="16" font-weight="500" fill="{MUTED}">{T(t["hero"]["sub"][0])}</text>'
          f'<text x="40" y="256" font-size="16" font-weight="500" fill="{MUTED}">{T(t["hero"]["sub"][1])}</text></g>')
    for i, (a, d) in enumerate(t["hero"]["cards"]):
        x, y = 40 + (i % 2) * 222, 290 + (i // 2) * 86
        b += (f'<g class="r" {delay(4 + i)}>{card(x, y, 210, 74)}'
              f'<text x="{x + 18}" y="{y + 32}" font-size="15.5" font-weight="700">{T(a)}</text>'
              f'<text x="{x + 18}" y="{y + 54}" font-size="12.5" font-weight="500" fill="{MUTED}">{T(d)}</text></g>')
    b += f'<g class="r" {delay(3)}>{mock(DARK, 500, 44, .74)}</g>'
    b += f'<g class="r" {delay(5)}>{mock(LIGHT, 540, 226, .74, shadow=True)}</g>'
    return svg(880, 480, t["hero"]["alt"], b)


def icon_svg_logo(x, y, size):
    grid = ["#FF7DB0", "#FF9A6B", "#FFD97A", "#9B86FF", "#FFFFFF", "#7EE0A0", "#6EB8FF", "#5FD8E6", "#C77DFF"]
    k = size / 256
    tiles = "".join(f'<rect x="{48 + (i % 3) * 56}" y="{48 + (i // 3) * 56}" width="48" height="48" rx="14" fill="{c}"/>' for i, c in enumerate(grid))
    return f'<g transform="translate({x} {y}) scale({k:.4f})"><rect x="8" y="8" width="240" height="240" rx="56" fill="#1A1030" stroke="#3a3a3a" stroke-width="6"/>{tiles}</g>'


def features(t):
    b = section_head(t["features"]["chip"], accent(t["features"]["title"]))
    glyphs = ["code", "typescript", "folder-src", "markup"]
    for i, (title, lines) in enumerate(t["features"]["items"]):
        x, y = 40 + (i % 2) * 408, 132 + (i // 2) * 156
        b += (f'<g class="r" {delay(2 + i)}>{card(x, y, 392, 140, 20)}{icon_at(glyphs[i], x + 20, y + 20, 40)}'
              f'<text x="{x + 72}" y="{y + 48}" font-size="20" font-weight="700">{T(title)}</text>'
              + "".join(f'<text x="{x + 24}" y="{y + 92 + k * 22}" font-size="15" font-weight="500" fill="{MUTED}">{T(l)}</text>' for k, l in enumerate(lines))
              + "</g>")
    return svg(880, 470, t["features"]["alt"], b)


SHOWCASE = ["python", "typescript", "javascript", "json", "markdown", "markup", "style", "yaml", "terminal", "docker", "git", "package",
            "rust", "go", "java", "c", "cpp", "csharp", "ruby", "php", "swift", "kotlin", "vue", "svelte",
            "folder-default", "folder-src", "folder-docs", "folder-test", "folder-assets", "folder-public", "folder-config", "folder-git",
            "folder-modules", "folder-scripts", "lock", "env"]


def icons_banner(t):
    b = section_head(t["icons"]["chip"], accent(t["icons"]["title"]))
    cell, gap = 56, 10
    x0 = (880 - (12 * cell + 11 * gap)) / 2
    for i, name in enumerate(SHOWCASE):
        x, y = x0 + (i % 12) * (cell + gap), 132 + (i // 12) * (cell + gap)
        b += f'<g class="r" {delay(2 + i % 12)}>{card(x, y, cell, cell, 14)}{icon_at(name, x + 8, y + 8, 40)}</g>'
    return svg(880, 132 + 3 * (cell + gap) + 20, t["icons"]["alt"], b)


def themes_banner(t):
    b = section_head(t["themes"]["chip"], accent(t["themes"]["title"]))
    k = .9
    b += f'<g class="r" {delay(2)}>{mock(DARK, 40, 132, k)}</g><g class="r" {delay(3)}>{mock(LIGHT, 880 - 40 - 430 * k, 132, k)}</g>'
    return svg(880, round(132 + 290 * k + 40), t["themes"]["alt"], b)


def download_icon(c):
    return f'<g transform="translate(18 14)" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v10m-4-3.5 4 4 4-4M6 19h12"/></g>'


def spark_icon(c):
    return f'<g transform="translate(18 14)" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l1.8 4.6L18.5 10l-4.7 1.4L12 16l-1.8-4.6L5.5 10l4.7-1.4z"/></g>'


def button(label, icon, primary):
    def render(fg, fm):
        w = round(52 + len(label) * 9 + 22)
        ink = "#0A0A0A" if primary else "#FFFFFF"
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="52" viewBox="0 0 {w} 52" role="img" aria-label="{esc(label)}">\n'
                f'<style>@font-face{{font-family:"G";src:url(data:font/woff2;base64,{fg}) format("woff2");font-weight:100 900}}text{{font-family:"G","Segoe UI",system-ui,sans-serif}}</style>\n'
                f'<defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{"#FFFFFF" if primary else "#202020"}"/><stop offset="1" stop-color="{"#D9D9D9" if primary else "#101010"}"/></linearGradient></defs>\n'
                f'<rect x=".5" y=".5" width="{w - 1}" height="51" rx="14" fill="url(#b)" stroke="{"#fff" if primary else "#333"}"/>\n'
                f'{icon(ink)}\n<text x="50" y="32" font-size="15" font-weight="700" fill="{ink}">{T(label)}</text>\n</svg>\n')
    return render


def subset_b64(path, chars):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    font = TTFont(path)
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


for lang, t in STR.items():
    all_text = ""
    files = {
        f"hero-{lang}.svg": hero(t),
        f"btn-download-{lang}.svg": button(t["buttons"]["download"], download_icon, True),
        f"btn-new-{lang}.svg": button(t["buttons"]["whatsNew"], spark_icon, False),
        f"features-{lang}.svg": features(t),
        f"icons-{lang}.svg": icons_banner(t),
        f"themes-{lang}.svg": themes_banner(t),
    }
    for render in files.values():
        render("", "")
    chars = "".join(sorted(set(all_text + "0123456789vOkto. ·")))
    fg, fm = subset_b64(FONT_G, chars), subset_b64(FONT_M, chars)
    total = 0
    for name, render in files.items():
        text = render(fg, fm)
        (out_dir / name).write_text(text, encoding="utf-8")
        total += len(text)
    print(lang, f"{total / 1024:.0f} KB,", len(chars), "glyphs")
