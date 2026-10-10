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

# Each file type is represented by a standalone logo mark with a restrained accent.
marks = {
    "python": '<path d="M16 7.5h-3.2c-2.1 0-3.4 1.2-3.4 3.2v2h7.1v1.2h-6c-2.2 0-3.6 1.4-3.6 3.6s1.4 3.8 3.6 3.8h2.2v-2.1c0-2.2 1.5-3.8 3.7-3.8h3.1c1.8 0 3-1.2 3-3v-1.5c0-2-1.2-3.4-3.4-3.4zm-1.8 2.1a.8.8 0 1 1 0 1.6.8.8 0 0 1 0-1.6z"/><path d="M16 22.5h3.2c2.1 0 3.4-1.2 3.4-3.2v-2h-7.1v-1.2h6c2.2 0 3.6-1.4 3.6-3.6s-1.4-3.8-3.6-3.8h-2.2v2.1c0 2.2-1.5 3.8-3.7 3.8h-3.1c-1.8 0-3 1.2-3 3v1.5c0 2 1.2 3.4 3.4 3.4zm1.8-2.1a.8.8 0 1 1 0-1.6.8.8 0 0 1 0 1.6z"/>',
    "javascript": '<text x="16" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" letter-spacing="-1">JS</text>',
    "typescript": '<text x="16" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="700" letter-spacing="-.8">TS</text>',
    "json": '<path d="M12 10c-1 0-1.4.5-1.4 1.5v1c0 .8-.3 1.2-.9 1.5.6.3.9.7.9 1.5v1c0 1 .4 1.5 1.4 1.5v-1.5c-.4 0-.5-.2-.5-.6v-.9c0-.7-.2-1.2-.7-1.5.5-.3.7-.8.7-1.5v-.9c0-.4.1-.6.5-.6zm3 0v1.5c.4 0 .5.2.5.6v.9c0 .7.2 1.2.7 1.5-.5.3-.7.8-.7 1.5v.9c0 .4-.1.6-.5.6V19c1 0 1.4-.5 1.4-1.5v-1c0-.8.3-1.2.9-1.5-.6-.3-.9-.7-.9-1.5v-1c0-1-.4-1.5-1.4-1.5z"/>',
    "markdown": '<path d="M8 19v-7l2.2 2.3 2.1-2.3v7h-1.8v-3.2l-.3.4-.3-.4V19zm6.2-7.2h1.9v4h2v-4h1.8v5.7h-5.7z"/>',
    "image": '<circle cx="18.5" cy="12.5" r="1.6"/><path d="M9 20l3.3-4.2 2.1 2.2 2-2.5 3.6 4.5z"/>',
    "database": '<ellipse cx="15.5" cy="10" rx="5.3" ry="2"/><path d="M10.2 10v7c0 1.2 2.4 2.2 5.3 2.2s5.3-1 5.3-2.2v-7M10.2 13.5c0 1.2 2.4 2.2 5.3 2.2s5.3-1 5.3-2.2" fill="none" stroke="{c}" stroke-width="1.6"/>',
    "terminal": '<path d="M9 12l3 2.5-3 2.5M14 17h5" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "style": '<text x="16" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="700" letter-spacing="-.7">CSS</text>',
    "markup": '<path d="M13 11l-3 3 3 3m5-6 3 3-3 3m-1-7-2 8" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "config": '<circle cx="15.5" cy="15" r="3.1" fill="none" stroke="{c}" stroke-width="1.5"/><path d="M15.5 9v2m0 8v2m6-6h-2m-8 0h-2m10.2-4.2-1.4 1.4m-5.6 5.6-1.4 1.4m8.4 0-1.4-1.4m-5.6-5.6-1.4-1.4" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
    "package": '<path d="M15.5 9l5 2.6v6l-5 2.6-5-2.6v-6zM10.5 11.6l5 2.7 5-2.7m-5 2.7v5.9" fill="none" stroke="{c}" stroke-width="1.4" stroke-linejoin="round"/>',
    "git": '<path d="M12 10v8m0-5 6-3v8" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="9" r="1.7"/><circle cx="12" cy="19" r="1.7"/><circle cx="18" cy="9" r="1.7"/><circle cx="18" cy="18" r="1.7"/>',
    "docker": '<path d="M9 15h12c-.5 2.7-2.3 4-5.5 4H12c-2 0-3.1-1.2-3-4zm2-3h2v2h-2zm3 0h2v2h-2zm3 0h2v2h-2zm-6-3h2v2h-2zm3 0h2v2h-2zm3 0h2v2h-2z"/>',
    "readme": '<path d="M10 11h9M10 14h9M10 17h6" fill="none" stroke="{c}" stroke-width="1.4" stroke-linecap="round"/><circle cx="8" cy="11" r=".8"/><circle cx="8" cy="14" r=".8"/><circle cx="8" cy="17" r=".8"/>',
    "code": '<path d="M13 12l-2.5 2.5L13 17m5-5 2.5 2.5L18 17m-1-6-2 8" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "rust": '<path d="M16 8.4l2 1.1 2.3-.1.9 2.1 1.8 1.4-.8 2.2.4 2.2-2 1.2-1.1 2-2.3-.3-2.1.9-1.7-1.5-2.2-.6-.4-2.2-1.4-1.8 1.2-2-.1-2.3 2.1-.9z"/><circle cx="16" cy="14.7" r="3.1" fill="none" stroke="{c}" stroke-width="1.2"/><circle cx="16" cy="14.7" r="1"/>',
    "go": '<text x="16" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="700" letter-spacing="-1.2">Go</text>',
    "java": '<path d="M15.8 7.5c-2 1.3 2.4 1.7.1 3.1m2-4.2c-3 1.9 2.7 2.2.1 4.6M10 13.5h11l-1.1 4.2c-.3 1-1 1.5-2.1 1.5h-4.6c-1.1 0-1.8-.5-2.1-1.5zm1.2 7h8.5" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "c": '<text x="16" y="21" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="700">C</text>',
    "cpp": '<text x="16" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" letter-spacing="-.7">C++</text>',
    "csharp": '<text x="16" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" letter-spacing="-.7">C#</text>',
    "ruby": '<path d="M10 11l4.1-3.3 6.3.7 1.8 4.5-5.8 8.4-7-4.8z"/><path d="M10 11l6.4 10.3 5.8-8.4m-8.1-5.2 2.3 13.6m-6.4-10.3 12.2-1.7" fill="none" stroke="{c}" stroke-width=".8"/>',
    "php": '<text x="16" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="10.5" font-style="italic" font-weight="700" letter-spacing="-.5">php</text>',
    "swift": '<path d="M8.5 11.1c2.2 2.4 4.3 4 6.4 4.7-1.2-1.8-2-3.8-2.4-5.8 2.7 3.1 5.5 5.2 9 6.2-.5 3.3-3.2 5.4-6.5 5.4-2.3 0-4.5-.9-6.1-2.6 2 .4 3.8.1 5.1-.8-2.5-.9-4.5-3.1-5.5-7.1z"/><path d="M9 22c4.2 1.3 8.4.6 11.6-1.7" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
    "kotlin": '<path d="M10 8v16" fill="none" stroke="#8B70A6" stroke-width="3.2" stroke-linecap="round"/><path d="M11 16 22 8" fill="none" stroke="#DB916A" stroke-width="3.2" stroke-linecap="round"/><path d="m13 15 9 9" fill="none" stroke="#6A9EAA" stroke-width="3.2" stroke-linecap="round"/>',
    "svelte": '<path d="M21 10c-1.6-2-5.1-2.6-7.8-1.2-3.2 1.7-3.3 4.2-.4 5.5l4.4 1.8c2.3.9 2.1 3-.4 4.3-2.7 1.4-6.5.8-8.6-1.4" fill="none" stroke="{c}" stroke-width="3.1" stroke-linecap="round"/><path d="M20.5 8.8c1.1 1.1 1.5 2.3 1.1 3.6" fill="none" stroke="#DDA18A" stroke-width="1.4" stroke-linecap="round"/>',
    "vue": '<path d="M9 10h3l3.5 5.8L19 10h3l-6.5 10.5z"/>',
    "file": '<path d="M11 12h9M11 15h9M11 18h6" fill="none" stroke="{c}" stroke-width="1.3" stroke-linecap="round"/>',
}

def svg(name, mark, color):
    if name == "file":
        artwork = '<path d="M9 4h9l5 5v18H9z" fill="#F7F5F2" stroke="#BDB9B3" stroke-width="1.5" stroke-linejoin="round"/><path d="M18 4v5h5" fill="#EAE7E2" stroke="#BDB9B3" stroke-width="1.4" stroke-linejoin="round"/><path d="M12 14h8m-8 4h8m-8 4h5" fill="none" stroke="#85858B" stroke-width="1.4" stroke-linecap="round"/>'
    else:
        artwork = f'<g transform="translate(-8 -8) scale(1.5)" fill="{color}" stroke-linecap="round" stroke-linejoin="round">{mark}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">{artwork}</svg>'.replace('stroke="{c}"', f'stroke="{color}"')

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
