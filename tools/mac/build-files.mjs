// Builds the "Okto Mac File Icons" theme: macOS-style document and folder icons.
// Pages are white with a folded corner; languages get a brand-coloured label band
// with white letters or a Phosphor glyph. Folders are macOS-blue (or tinted by role).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import opentype from "opentype.js";
import * as si from "simple-icons";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..");
const phDir = path.join(here, "node_modules", "@phosphor-icons", "core", "assets", "regular");
const outIcons = path.join(root, "fileicons", "mac");
fs.rmSync(outIcons, { recursive: true, force: true });
fs.mkdirSync(outIcons, { recursive: true });
const font = opentype.parse(fs.readFileSync(path.join(here, "fonts", "JetBrainsMono.ttf")).buffer.slice(0));

const hex = (c) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
const mix = (c, t, to) => "#" + hex(c).map((v) => Math.round(v + (to - v) * t).toString(16).padStart(2, "0")).join("");
const light = (c, t = 0.28) => mix(c, t, 255);
const dark = (c, t = 0.18) => mix(c, t, 0);

const glyphPaths = (name) =>
  [...fs.readFileSync(path.join(phDir, name + ".svg"), "utf8").matchAll(/ d="([^"]+)"/g)].map((m) => m[1]);
const glyph = (name, size, cx, cy, fill, opacity = 1) => {
  const k = size / 256;
  return `<g transform="translate(${cx - size / 2} ${cy - size / 2}) scale(${k})" fill="${fill}" fill-opacity="${opacity}">${glyphPaths(name).map((d) => `<path d="${d}"/>`).join("")}</g>`;
};
const O = { features: { liga: false, calt: false }, kerning: false };
const label = (text, cx, cy, maxW, maxSize = 11.5) => {
  let size = maxSize;
  while (font.getAdvanceWidth(text, size, O) > maxW && size > 4) size -= 0.25;
  const w = font.getAdvanceWidth(text, size, O);
  const d = font.getPath(text, cx - w / 2, cy + (size * 0.73) / 2, size, O).toPathData(2);
  return `<path d="${d}" fill="#fff" stroke="#fff" stroke-width=".7" stroke-linejoin="round"/>`;
};

const uniq = (svg, key) => svg.replace(/id="(\w)"/g, `id="$1-${key}"`).replace(/url\(#(\w)\)/g, `url(#$1-${key})`);
const wrap = (defs, body) => `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs>${defs}</defs>${body}</svg>`;
const PAGE = "M8 3h11.5l7.5 7.5V27a2.6 2.6 0 0 1-2.6 2.6H8A2.6 2.6 0 0 1 5.4 27V5.6A2.6 2.6 0 0 1 8 3z";
const doc = (color, inner) => wrap(
  `<linearGradient id="p" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#E9EBF0"/></linearGradient>` +
  (color ? `<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${light(color, 0.22)}"/><stop offset="1" stop-color="${color}"/></linearGradient>` : ""),
  `<path d="${PAGE}" fill="url(#p)" stroke="#BFC3CB" stroke-width=".9"/>` +
  `<path d="M19.5 3v5.2a2.3 2.3 0 0 0 2.3 2.3H27z" fill="#D5D9E0" stroke="#BFC3CB" stroke-width=".9" stroke-linejoin="round"/>` +
  (color ? `<rect x="3" y="15.6" width="26" height="11.4" rx="2.6" fill="url(#b)"/>` : "") + inner);

const folderSvg = (color, g, open) => {
  const back = dark(color, 0.12), top = light(color, 0.34), bot = color;
  const defs = `<linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${top}"/><stop offset="1" stop-color="${bot}"/></linearGradient>`;
  const backP = `<path d="M3 8.6A2.6 2.6 0 0 1 5.6 6h6.3l2.6 2.7h11.9A2.6 2.6 0 0 1 29 11.3V24.4A2.6 2.6 0 0 1 26.4 27H5.6A2.6 2.6 0 0 1 3 24.4z" fill="${back}"/>`;
  const front = open
    ? `<path d="M6.4 13.4H29.5a1.3 1.3 0 0 1 1.25 1.62L28.4 24.9A2.5 2.5 0 0 1 26 26.8H5a1.3 1.3 0 0 1-1.25-1.62L5 14.9a2.5 2.5 0 0 1 1.4-1.5z" fill="url(#f)"/>`
    : `<path d="M3 13.1A2.6 2.6 0 0 1 5.6 10.5H26.4A2.6 2.6 0 0 1 29 13.1V24.4A2.6 2.6 0 0 1 26.4 27H5.6A2.6 2.6 0 0 1 3 24.4z" fill="url(#f)"/>`;
  const gl = g ? glyph(g, 10, 16, open ? 20 : 19.2, "#fff", 0.92) : "";
  return wrap(defs, backP + front + gl);
};

// --- file kinds -------------------------------------------------------------
// L = letter mark, G = Phosphor glyph. Colours follow each language's brand.
const kinds = {
  javascript: ["#F0C000", "L", "JS"], typescript: ["#3178C6", "L", "TS"], python: ["#3776AB", "L", "PY"],
  json: ["#E5A93B", "G", "brackets-curly"], markdown: ["#3598D4", "L", "MD"], image: ["#3DB87A", "G", "image-square"],
  database: ["#00AFCB", "G", "database"], terminal: ["#4CAF50", "L", ">_"], style: ["#4677C4", "L", "CSS"],
  markup: ["#E8643F", "G", "code"], config: ["#D99A2B", "G", "gear-six"], package: ["#D9824A", "G", "package"],
  git: ["#F05133", "G", "git-branch"], docker: ["#2496ED", "G", "cube"], readme: ["#3DA67A", "G", "info"],
  code: ["#8172B8", "G", "code"], rust: ["#DE6B3C", "L", "RS"], go: ["#00ADD8", "L", "GO"],
  java: ["#E76F00", "L", "JV"], c: ["#5C8DC8", "L", "C"], cpp: ["#00599C", "L", "C++"],
  csharp: ["#9B4F96", "L", "C#"], ruby: ["#CC342D", "L", "RB"], php: ["#777BB4", "L", "PHP"],
  swift: ["#F05138", "L", "SW"], kotlin: ["#7F52FF", "L", "KT"], svelte: ["#FF3E00", "L", "SV"],
  vue: ["#41B883", "L", "VUE"], dart: ["#0EA5E9", "L", "DT"], lua: ["#5B7BE0", "L", "LUA"],
  scala: ["#DC322F", "L", "SC"], haskell: ["#9179D0", "L", "HS"], elixir: ["#A56CC8", "L", "EX"],
  zig: ["#F7A41D", "L", "ZG"], r: ["#2166B0", "L", "R"], perl: ["#5D87D6", "L", "PL"],
  html: ["#E8643F", "L", "<>"], xml: ["#E8643F", "L", "XML"], yaml: ["#CB171E", "L", "YML"], toml: ["#C9663A", "L", "TML"],
  csv: ["#2EA05F", "G", "table"], pdf: ["#E5484D", "L", "PDF"], archive: ["#B58A3D", "G", "archive"],
  text: ["#8A8F98", "G", "list-bullets"], log: ["#8A8F98", "G", "list-bullets"],
  lock: ["#8A8F98", "G", "lock-simple"], env: ["#D99A2B", "G", "key"], license: ["#C9A227", "G", "medal"],
  test: ["#3DB87A", "G", "flask"], web: ["#3B82F6", "G", "globe-simple"], file: ["#8A8F98", "G", null],
  sql: ["#00AFCB", "L", "SQL"], shell: ["#4CAF50", "L", ">_"], gradle: ["#3FA9C9", "L", "GR"], makefile: ["#8172B8", "G", "gear-six"],
};

// Standalone vector logos (Simple Icons, CC0) - no page, just the mark with a soft macOS-like gradient.
const siPath = (slug) => Object.values(si).find((i) => i.slug === slug).path;
const logos = {
  javascript: ["javascript", "#F7DF1E"], typescript: ["typescript", "#3A86D8"], python: ["python", "#3776AB"],
  rust: ["rust", "#F2641F"], go: ["go", "#00ADD8"], java: ["__coffee", "#F0782A"], c: ["c", "#5C8DC8"],
  cpp: ["cplusplus", "#0A6CBF"], ruby: ["ruby", "#E0403A"], php: ["php", "#8892D6"], swift: ["swift", "#F05138"],
  kotlin: ["kotlin", "#8B5CF6"], svelte: ["svelte", "#FF3E00"], vue: ["vuedotjs", "#41B883"], dart: ["dart", "#2BB7F6"],
  lua: ["lua", "#5568E8"], scala: ["scala", "#E04444"], haskell: ["haskell", "#8A78D8"], elixir: ["elixir", "#9A63D0"],
  zig: ["zig", "#F7A41D"], r: ["r", "#2E7FD6"], perl: ["perl", "#5D87D6"], html: ["html5", "#E8643F"],
  style: ["css", "#3B82F6"], shell: ["gnubash", "#4EAA25"], terminal: ["gnubash", "#4EAA25"], sql: ["sqlite", "#2B9BD6"],
  markdown: ["markdown", "#5B7C99"], json: ["json", "#E5A93B"], yaml: ["yaml", "#E5484D"], toml: ["toml", "#D2693C"],
  docker: ["docker", "#2496ED"], git: ["git", "#F05133"], gradle: ["gradle", "#2BA3BD"],
};
const logo = (slug, color) => {
  const fill = slug === "python"
    ? `<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4F8FCB"/><stop offset=".5" stop-color="#3776AB"/><stop offset=".5" stop-color="#FFD43B"/><stop offset="1" stop-color="#F5B800"/></linearGradient>`
    : `<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${light(color, 0.28)}"/><stop offset="1" stop-color="${color}"/></linearGradient>`;
  if (slug.startsWith("__")) return wrap(fill, `<g transform="translate(3 3) scale(${26 / 256})" fill="url(#g)">${glyphPaths(slug.slice(2)).map((d) => `<path d="${d}"/>`).join("")}</g>`);
  return wrap(fill, `<g transform="translate(2.5 2.5) scale(1.1667)"><path d="${siPath(slug)}" fill="url(#g)"/></g>`);
};
const csharp = () => wrap(
  `<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B773B8"/><stop offset="1" stop-color="#8C3F8E"/></linearGradient>`,
  `<path d="M16 4.5l10 5.75v11.5L16 27.5 6 21.75v-11.5z" fill="url(#g)" stroke="url(#g)" stroke-width="2.6" stroke-linejoin="round"/>${label("C#", 16, 16.2, 14, 12)}`);

const files = {};
const defs = {};
for (const [kind, [color, type, what]] of Object.entries(kinds)) {
  if (logos[kind] || kind === "csharp") {
    files[kind] = uniq(kind === "csharp" ? csharp() : logo(...logos[kind]), kind);
    fs.writeFileSync(path.join(outIcons, `${kind}.svg`), files[kind]);
    defs[`_${kind}`] = { iconPath: `./mac/${kind}.svg` };
    continue;
  }
  let inner = "";
  if (kind === "file" || kind === "text" || kind === "log") {
    inner = `<path d="M10.5 15h11M10.5 18.6h11M10.5 22.2h6.5" stroke="#9AA1AD" stroke-width="1.6" stroke-linecap="round" fill="none"/>`;
    files[kind] = uniq(doc(null, inner), kind);
  } else {
    if (type === "L") inner = label(what, 16, 21.3, 21);
    else if (what) inner = glyph(what, 8.5, 16, 21.3, "#fff");
    files[kind] = uniq(doc(color, inner), kind);
  }
  fs.writeFileSync(path.join(outIcons, `${kind}.svg`), files[kind]);
  defs[`_${kind}`] = { iconPath: `./mac/${kind}.svg` };
}

// --- folders ----------------------------------------------------------------
const BLUE = "#3B9DF0", GREEN = "#34C07A", PURPLE = "#8C7CF0", ORANGE = "#F59A4A", RED = "#F0605D", GRAY = "#8E99AB", TEAL = "#2FB7C9";
const folders = {
  folder: [BLUE, null], src: [BLUE, "code"], docs: [PURPLE, "book"], images: [GREEN, "image-square"], test: [GREEN, "flask"],
  node: [GREEN, "package"], git: [RED, "git-branch"], github: [GRAY, "git-branch"], public: [TEAL, "globe-simple"],
  config: [ORANGE, "gear-six"], scripts: [ORANGE, "terminal-window"], assets: [PURPLE, "image-square"], lib: [PURPLE, "books"],
  build: [ORANGE, "wrench"], vscode: [BLUE, "code"], components: [PURPLE, "cube"], data: [TEAL, "database"],
};
for (const [name, [color, g]] of Object.entries(folders)) {
  for (const [state, open] of [["", false], ["-open", true]]) {
    fs.writeFileSync(path.join(outIcons, `folder-${name}${state}.svg`), uniq(folderSvg(color, g, open), name + state));
    defs[`_folder_${name}${state}`] = { iconPath: `./mac/folder-${name}${state}.svg` };
  }
}

// --- associations -----------------------------------------------------------
const ext = (kind, list) => Object.fromEntries(list.split(" ").map((e) => [e, `_${kind}`]));
const fileExtensions = {
  ...ext("javascript", "js jsx mjs cjs"), ...ext("typescript", "ts tsx mts cts"), ...ext("python", "py pyi pyw ipynb"),
  ...ext("json", "json jsonc json5 geojson"), ...ext("markdown", "md mdx markdown"),
  ...ext("image", "png jpg jpeg gif webp avif bmp ico svg tiff"), ...ext("database", "db sqlite sqlite3 mdb"),
  ...ext("sql", "sql"), ...ext("shell", "sh bash zsh fish bat cmd ps1 psm1"), ...ext("style", "css scss sass less styl"),
  ...ext("html", "html htm xhtml"), ...ext("xml", "xml xsd xsl plist"), ...ext("yaml", "yml yaml"), ...ext("toml", "toml"),
  ...ext("config", "ini conf cfg properties editorconfig"), ...ext("package", "nupkg vsix"), ...ext("lock", "lock"),
  ...ext("rust", "rs"), ...ext("go", "go"), ...ext("java", "java jar class"), ...ext("c", "c h"),
  ...ext("cpp", "cpp cc cxx hpp hh hxx"), ...ext("csharp", "cs csx csproj sln"), ...ext("ruby", "rb erb gemspec"),
  ...ext("php", "php"), ...ext("swift", "swift"), ...ext("kotlin", "kt kts"), ...ext("svelte", "svelte"), ...ext("vue", "vue"),
  ...ext("dart", "dart"), ...ext("lua", "lua"), ...ext("scala", "scala sc"), ...ext("haskell", "hs lhs"),
  ...ext("elixir", "ex exs"), ...ext("zig", "zig"), ...ext("r", "r rmd"), ...ext("perl", "pl pm"),
  ...ext("csv", "csv tsv"), ...ext("pdf", "pdf"), ...ext("archive", "zip tar gz tgz 7z rar bz2 xz"),
  ...ext("text", "txt rtf"), ...ext("log", "log"), ...ext("gradle", "gradle"), ...ext("web", "wasm"),
};
const fileNames = {
  "README.md": "_readme", "README": "_readme", "README.txt": "_readme", "CHANGELOG.md": "_readme",
  "LICENSE": "_license", "LICENSE.md": "_license", "LICENSE.txt": "_license", "Dockerfile": "_docker",
  "docker-compose.yml": "_docker", "docker-compose.yaml": "_docker", ".dockerignore": "_docker",
  "package.json": "_package", "package-lock.json": "_lock", "pnpm-lock.yaml": "_lock", "yarn.lock": "_lock",
  "Cargo.toml": "_package", "Cargo.lock": "_lock", "go.mod": "_package", "go.sum": "_lock", "pyproject.toml": "_package",
  "requirements.txt": "_package", "Makefile": "_makefile", ".gitignore": "_git", ".gitattributes": "_git",
  ".gitmodules": "_git", ".env": "_env", ".env.example": "_env", ".env.local": "_env", ".editorconfig": "_config",
  "tsconfig.json": "_config", "settings.json": "_config", "vite.config.ts": "_config", "vite.config.js": "_config",
  "build.gradle": "_gradle", "build.gradle.kts": "_gradle", "settings.gradle.kts": "_gradle",
};
const languageIds = {
  javascript: "_javascript", javascriptreact: "_javascript", typescript: "_typescript", typescriptreact: "_typescript",
  python: "_python", json: "_json", jsonc: "_json", markdown: "_markdown", css: "_style", scss: "_style", less: "_style",
  html: "_html", xml: "_xml", yaml: "_yaml", sql: "_sql", shellscript: "_shell", powershell: "_shell", bat: "_shell",
  dockerfile: "_docker", rust: "_rust", go: "_go", java: "_java", c: "_c", cpp: "_cpp", csharp: "_csharp", ruby: "_ruby",
  php: "_php", swift: "_swift", kotlin: "_kotlin", svelte: "_svelte", vue: "_vue", dart: "_dart", lua: "_lua",
  scala: "_scala", haskell: "_haskell", elixir: "_elixir", zig: "_zig", r: "_r", perl: "_perl", makefile: "_makefile",
  toml: "_toml", ini: "_config", csv: "_csv",
};
const folderMap = {
  src: "src", source: "src", app: "src", docs: "docs", doc: "docs", images: "images", img: "images", test: "test",
  tests: "test", __tests__: "test", spec: "test", node_modules: "node", ".git": "git", ".github": "github",
  public: "public", static: "public", config: "config", configs: "config", ".config": "config", scripts: "scripts",
  tools: "scripts", assets: "assets", lib: "lib", libs: "lib", dist: "build", build: "build", out: "build",
  ".vscode": "vscode", components: "components", data: "data", db: "data",
};
const folderNames = {}, folderNamesExpanded = {};
for (const [n, f] of Object.entries(folderMap)) {
  folderNames[n] = `_folder_${f}`;
  folderNamesExpanded[n] = `_folder_${f}-open`;
}

const theme = {
  $schema: "vscode://schemas/icon-theme",
  iconDefinitions: defs,
  file: "_file",
  folder: "_folder_folder",
  folderExpanded: "_folder_folder-open",
  rootFolder: "_folder_folder",
  rootFolderExpanded: "_folder_folder-open",
  folderNames, folderNamesExpanded, fileExtensions, fileNames, languageIds,
};
fs.writeFileSync(path.join(root, "fileicons", "okto-mac-file-icon-theme.json"), JSON.stringify(theme, null, 2) + "\n");


const tiles = [...Object.keys(kinds).map((k) => [k, files[k]]),
  ...["folder", "src", "docs", "node", "git", "test", "images", "config"].flatMap((f) => [
    [f, fs.readFileSync(path.join(outIcons, `folder-${f}.svg`), "utf8")],
    [f + " open", fs.readFileSync(path.join(outIcons, `folder-${f}-open.svg`), "utf8")]])];
const prev = path.join(here, ".preview");
fs.mkdirSync(prev, { recursive: true });
const cell = ([n, s]) => `<div>${s.replace('width="32" height="32"', 'width="64" height="64"')}${s.replace('width="32" height="32"', 'width="16" height="16"')}<span>${n}</span></div>`;
fs.writeFileSync(path.join(prev, "files.html"), `<meta charset=utf8><style>body{background:#1e1e1e;color:#ccc;font:11px sans-serif;display:grid;grid-template-columns:repeat(auto-fill,100px);gap:10px;padding:10px}div{text-align:center}svg{margin:2px}span{display:block}</style>${tiles.map(cell).join("")}`);
console.log("kinds", Object.keys(kinds).length, "defs", Object.keys(defs).length);
