from pathlib import Path
import json

root = Path(__file__).resolve().parent.parent
icons = root / "fileicons" / "icons"

colors = {
    "python": "#4E7099", "javascript": "#B77A22", "typescript": "#4E6F9E",
    "json": "#8A784A", "markdown": "#657D92", "image": "#668875",
    "database": "#67899A", "terminal": "#5E8770", "style": "#A46E89",
    "markup": "#B06E63", "config": "#8B7797", "package": "#B7835F",
    "git": "#B46D62", "docker": "#5E879E", "readme": "#648A78",
    "code": "#777E91", "rust": "#A3654D", "go": "#5291A0",
    "java": "#B66E50", "c": "#5578A4", "cpp": "#6579A8",
    "csharp": "#71835A", "ruby": "#AD5E61", "php": "#7A73A3",
    "swift": "#C1784D", "kotlin": "#9273A8", "svelte": "#C86C51",
    "vue": "#628D78", "file": "#85858B",
}

# Each center mark is its own compact, original symbol; the quiet paper tile and
# folded corner make the family feel cohesive while the muted accents identify type.
marks = {
    "python": '<path d="M16 10c0-2-1.4-3-3.4-3H10v4h4c1.1 0 2 .9 2 2v1h3v-2c0-1.1-.9-2-2-2h-1zM16 16c0 2 1.4 3 3.4 3H22v-4h-4c-1.1 0-2-.9-2-2v-1h-3v2c0 1.1.9 2 2 2h1z"/><circle cx="11.3" cy="9" r=".7" fill="#F7F5F2"/><circle cx="20.7" cy="17" r=".7" fill="#F7F5F2"/>',
    "javascript": '<path d="M11 12v4.2c0 1.2-.7 1.8-1.7 1.8-.7 0-1.3-.3-1.8-.8l1.1-1.2c.2.3.4.4.7.4.4 0 .6-.2.6-.7V12zm7.4 1.5c-.4-.4-.8-.6-1.4-.6-.5 0-.8.2-.8.5 0 .4.4.5 1.1.8 1.4.5 2.2 1 2.2 2.1 0 1.4-1.1 2.2-2.6 2.2-1.1 0-2.1-.4-2.8-1.1l1.1-1.2c.5.5 1 .7 1.7.7.5 0 .8-.2.8-.5 0-.4-.4-.6-1.2-.9-1.2-.5-2.1-.9-2.1-2.1 0-1.2 1-2.1 2.5-2.1 1 0 1.8.3 2.4.9z"/>',
    "typescript": '<path d="M9 13h7v1.6h-2.6v5H11.6v-5H9zm9.7 1.5c-.3-.3-.7-.5-1.2-.5-.4 0-.7.2-.7.5 0 .3.4.5 1 .7 1.2.5 1.9.9 1.9 1.9 0 1.2-.9 1.9-2.3 1.9-1 0-1.8-.4-2.4-1l1-.9c.4.4.8.5 1.4.5.4 0 .7-.2.7-.5s-.4-.5-1.1-.8c-1.1-.4-1.8-.8-1.8-1.9 0-1.1.9-1.8 2.2-1.8.8 0 1.5.3 2 .8z"/>',
    "json": '<path d="M12 10c-1 0-1.4.5-1.4 1.5v1c0 .8-.3 1.2-.9 1.5.6.3.9.7.9 1.5v1c0 1 .4 1.5 1.4 1.5v-1.5c-.4 0-.5-.2-.5-.6v-.9c0-.7-.2-1.2-.7-1.5.5-.3.7-.8.7-1.5v-.9c0-.4.1-.6.5-.6zm3 0v1.5c.4 0 .5.2.5.6v.9c0 .7.2 1.2.7 1.5-.5.3-.7.8-.7 1.5v.9c0 .4-.1.6-.5.6V19c1 0 1.4-.5 1.4-1.5v-1c0-.8.3-1.2.9-1.5-.6-.3-.9-.7-.9-1.5v-1c0-1-.4-1.5-1.4-1.5z"/>',
    "markdown": '<path d="M8 19v-7l2.2 2.3 2.1-2.3v7h-1.8v-3.2l-.3.4-.3-.4V19zm6.2-7.2h1.9v4h2v-4h1.8v5.7h-5.7z"/>',
    "image": '<circle cx="18.5" cy="12.5" r="1.6"/><path d="M9 20l3.3-4.2 2.1 2.2 2-2.5 3.6 4.5z"/>',
    "database": '<ellipse cx="15.5" cy="10" rx="5.3" ry="2"/><path d="M10.2 10v7c0 1.2 2.4 2.2 5.3 2.2s5.3-1 5.3-2.2v-7M10.2 13.5c0 1.2 2.4 2.2 5.3 2.2s5.3-1 5.3-2.2" fill="none" stroke="{c}" stroke-width="1.6"/>',
    "terminal": '<path d="M9 12l3 2.5-3 2.5M14 17h5" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "style": '<path d="M9 11h13M9 14.5h13M9 18h13" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="11" r="1.4" fill="#F7F5F2"/><circle cx="18.5" cy="14.5" r="1.4" fill="#F7F5F2"/><circle cx="14.5" cy="18" r="1.4" fill="#F7F5F2"/>',
    "markup": '<path d="M13 11l-3 3 3 3m5-6 3 3-3 3m-1-7-2 8" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "config": '<circle cx="15.5" cy="15" r="3.1" fill="none" stroke="{c}" stroke-width="1.5"/><path d="M15.5 9v2m0 8v2m6-6h-2m-8 0h-2m10.2-4.2-1.4 1.4m-5.6 5.6-1.4 1.4m8.4 0-1.4-1.4m-5.6-5.6-1.4-1.4" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
    "package": '<path d="M15.5 9l5 2.6v6l-5 2.6-5-2.6v-6zM10.5 11.6l5 2.7 5-2.7m-5 2.7v5.9" fill="none" stroke="{c}" stroke-width="1.4" stroke-linejoin="round"/>',
    "git": '<path d="M12 10v8m0-5 6-3v8" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="9" r="1.7"/><circle cx="12" cy="19" r="1.7"/><circle cx="18" cy="9" r="1.7"/><circle cx="18" cy="18" r="1.7"/>',
    "docker": '<path d="M9 15h12c-.5 2.7-2.3 4-5.5 4H12c-2 0-3.1-1.2-3-4zm2-3h2v2h-2zm3 0h2v2h-2zm3 0h2v2h-2zm-6-3h2v2h-2zm3 0h2v2h-2zm3 0h2v2h-2z"/>',
    "readme": '<path d="M10 11h9M10 14h9M10 17h6" fill="none" stroke="{c}" stroke-width="1.4" stroke-linecap="round"/><circle cx="8" cy="11" r=".8"/><circle cx="8" cy="14" r=".8"/><circle cx="8" cy="17" r=".8"/>',
    "code": '<path d="M13 12l-2.5 2.5L13 17m5-5 2.5 2.5L18 17m-1-6-2 8" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "rust": '<path d="M13 10l2.5-2 2.2 2.2-1.8 2.4 2 2.4-2.2 2.2-2.5-1.8-2.5 1.8-2.2-2.2 1.8-2.4-1.8-2.4 2.2-2.2z"/><circle cx="15.5" cy="13.5" r="1.4" fill="#F7F5F2"/>',
    "go": '<path d="M10 12.2h5.2c1.7 0 2.5.7 2.5 2s-.8 2-2.5 2h-2.1" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"/><path d="M9 18h4" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
    "java": '<path d="M16 8c-2 1.1 2 1.3 0 2.7m2-4c-2.8 1.6 2.5 2 .1 4M10 14h10l-1 3h-8zm1 4.5h8" fill="none" stroke="{c}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>',
    "c": '<path d="M19.5 11.5a5 5 0 1 0 0 4" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>',
    "cpp": '<path d="M18 11.5a4.5 4.5 0 1 0 0 4m2-4v4m-2-2h4" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>',
    "csharp": '<path d="M18.5 11.5a4.5 4.5 0 1 0 0 4M19 12v3m-1.5-1.5h3m-8.5 0h3" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>',
    "ruby": '<path d="M10 11l4-3 6 1 1 5-5 5-6-3z"/><path d="M10 11l6 8 4-10m-6-1 2 9" fill="none" stroke="#F7F5F2" stroke-width=".8"/>',
    "php": '<path d="M8 14c1-2 3-3 7-3s6 1 7 3c-1 2-3 3-7 3s-6-1-7-3z" fill="none" stroke="{c}" stroke-width="1.5"/><path d="M11 13v2m3-2v2m3-2v2" stroke="{c}" stroke-width="1.2"/>',
    "swift": '<path d="M9 10c2 2 4 3 6 3-2-2-3-4-3-5 3 3 6 5 9 5-.3 3-2.7 5-6 5-2 0-4-.8-5.5-2.3 2 .4 3.5.1 4.5-.7-2.5-.5-4.5-2-6-4z"/>',
    "kotlin": '<path d="M10 9h9l-4.5 4.5L19 18h-9z"/><path d="M10 9v9" fill="none" stroke="#F7F5F2" stroke-width="1"/>',
    "svelte": '<path d="M18.5 9.5c-1.4-2-4.2-2.2-6.8-.5l-2.8 1.8c-2.4 1.6-2.3 4.3-.8 5.8 1.4 1.4 3.8 1.4 5.8.1l3.2-2.1c1.7-1.1 2.1-3.4.8-5.1z"/><path d="M10 15l5-3" fill="none" stroke="#F7F5F2" stroke-width="1.4" stroke-linecap="round"/>',
    "vue": '<path d="M9 10h3l3.5 5.8L19 10h3l-6.5 10.5z"/><path d="M12 10h2l1.5 2.4L17 10h2l-3.5 5.8z" fill="#F7F5F2"/>',
    "file": '<path d="M11 12h9M11 15h9M11 18h6" fill="none" stroke="{c}" stroke-width="1.3" stroke-linecap="round"/>',
}

def svg(name, mark, color):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
<path d="M7 3h12l6 6v19H7z" fill="#F7F5F2" stroke="#BDB9B3" stroke-width="1.2" stroke-linejoin="round"/>
<path d="M19 3v6h6" fill="#EAE7E2" stroke="#BDB9B3" stroke-width="1.1" stroke-linejoin="round"/>
<g fill="{color}" stroke-linecap="round" stroke-linejoin="round">{mark}</g>
</svg>'''.replace('stroke="{c}"', f'stroke="{color}"')

for name, mark in marks.items():
    (icons / f"{name}.svg").write_text(svg(name, mark, colors[name]), encoding="utf-8")

# The folder remains a distinctive Okto tile, with a soft pink tab accent.
(icons / "folder.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M3.5 8h9l2.4 2.7h13.6v14.8H3.5z" fill="#EAE7E2" stroke="#BDB9B3" stroke-width="1.3" stroke-linejoin="round"/><path d="M4 12h23" stroke="#C7868B" stroke-width="1.6" stroke-linecap="round"/><rect x="8" y="15" width="6" height="5.5" rx="1.2" fill="#CFCBC5"/><rect x="15.5" y="15" width="6" height="5.5" rx="1.2" fill="#BDB9B3"/></svg>''', encoding="utf-8")
(icons / "folder-open.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M3.5 8h9l2.4 2.7h13.6v12.8H3.5z" fill="#EAE7E2" stroke="#BDB9B3" stroke-width="1.3" stroke-linejoin="round"/><path d="M3.5 14h25l-3.5 11H3z" fill="#F0EDE8" stroke="#BDB9B3" stroke-width="1.3" stroke-linejoin="round"/><path d="M6 16h19" stroke="#C7868B" stroke-width="1.3" stroke-linecap="round"/><rect x="9" y="18" width="5" height="4" rx="1" fill="#CFCBC5"/><rect x="15.5" y="18" width="5" height="4" rx="1" fill="#BDB9B3"/></svg>''', encoding="utf-8")

theme_path = root / "fileicons" / "okto-icon-theme.json"
theme = json.loads(theme_path.read_text(encoding="utf-8"))
defs = theme["iconDefinitions"]
for name in marks:
    defs[f"_{name}"] = {"iconPath": f"./icons/{name}.svg"}

for ext, icon in {
    "rs":"rust", "go":"go", "java":"java", "c":"c", "h":"c", "cpp":"cpp", "hpp":"cpp",
    "cs":"csharp", "rb":"ruby", "php":"php", "swift":"swift", "kt":"kotlin", "kts":"kotlin",
    "svelte":"svelte", "vue":"vue"
}.items():
    theme["fileExtensions"][ext] = f"_{icon}"
for language, icon in {
    "rust":"rust", "go":"go", "java":"java", "c":"c", "cpp":"cpp", "csharp":"csharp",
    "ruby":"ruby", "php":"php", "swift":"swift", "kotlin":"kotlin", "svelte":"svelte", "vue":"vue"
}.items():
    theme["languageIds"][language] = f"_{icon}"
theme_path.write_text(json.dumps(theme, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# A compact repository preview makes the complete icon family easy to inspect.
import xml.etree.ElementTree as ET

gallery = root / "assets" / "readme" / "file-icon-gallery.svg"
names = sorted(marks)
cols, cell_w, cell_h = 6, 108, 70
rows = (len(names) + cols - 1) // cols
elements = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols*cell_w}" height="{rows*cell_h}" viewBox="0 0 {cols*cell_w} {rows*cell_h}">', '<rect width="100%" height="100%" rx="18" fill="#F2F1EF"/>']
ns = "{http://www.w3.org/2000/svg}"
for i, name in enumerate(names):
    col, row = i % cols, i // cols
    x, y = col * cell_w, row * cell_h
    svg_root = ET.parse(icons / f"{name}.svg").getroot()
    elements.append(f'<g transform="translate({x+38},{y+3}) scale(1)">')
    for child in list(svg_root):
        elements.append(ET.tostring(child, encoding="unicode"))
    elements.append('</g>')
    elements.append(f'<text x="{x+cell_w/2}" y="{y+59}" text-anchor="middle" fill="#66645F" font-family="Segoe UI, sans-serif" font-size="10">{name}</text>')
elements.append('</svg>')
gallery.write_text("\n".join(elements), encoding="utf-8")
