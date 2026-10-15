// Builds the "Okto Mac" product icon font + theme from Phosphor icons (rounded, SF Symbols-like).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { Readable } from "node:stream";
import { SVGIcons2SVGFontStream } from "svgicons2svgfont";
import svg2ttf from "svg2ttf";
import ttf2woff from "ttf2woff";
import { map } from "./product-map.mjs";

const require = createRequire(import.meta.url);
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..");
const phDir = path.join(here, "node_modules", "@phosphor-icons", "core", "assets");
const mapping = require("@vscode/codicons/src/template/mapping.json");

const aliases = new Map(); // primary id -> all ids sharing the glyph
for (const [code, ids] of Object.entries(mapping)) {
  const list = Array.isArray(ids) ? ids : [ids];
  aliases.set(list[0], list);
}
const known = new Set([...aliases.values()].flat());

function findSvg(name) {
  const filled = name.endsWith("!");
  const base = filled ? name.slice(0, -1) : name;
  const file = path.join(phDir, filled ? "fill" : "regular", filled ? base + "-fill.svg" : base + ".svg");
  return fs.existsSync(file) ? { file, size: 256 } : null;
}

const glyphs = [];
const missing = [];
const unknownIds = [];
let code = 0xe000;
const defs = {};
const byGlyph = new Map(); // glyph key -> iconDefinition name

for (const [id, glyph] of Object.entries(map)) {
  if (!known.has(id)) { unknownIds.push(id); continue; }
  const found = findSvg(glyph);
  if (!found) { missing.push(`${id} -> ${glyph}`); continue; }
  let defName = byGlyph.get(glyph);
  if (!defName) {
    defName = `ph-${glyph.replace("!", "-fill")}`;
    byGlyph.set(glyph, defName);
    const svg = fs.readFileSync(found.file, "utf8");
    const d = [...svg.matchAll(/ d="([^"]+)"/g)].map((m) => m[1]);
    const scale = 1000 / found.size;
    glyphs.push({ name: defName, code, d, size: found.size });
    defs[defName] = { fontCharacter: "\\" + code.toString(16) };
    code++;
  }
  // codicon aliases (e.g. "debug-alt-small") share the primary's glyph
  const all = (aliases.get(id) ?? [id]);
  for (const a of all) defs[`__id:${a}`] = defName;
}

if (missing.length) console.warn("Missing icons:\n  " + missing.join("\n  "));
if (unknownIds.length) console.warn("Ignored ids (not codicons): " + unknownIds.join(", "));

// --- font ---
const stream = new SVGIcons2SVGFontStream({
  fontName: "okto-mac-product",
  fontHeight: 1000,
  normalize: false,
  descent: 100,
  log: () => {},
});
const chunks = [];
const done = new Promise((res, rej) => {
  stream.on("data", (c) => chunks.push(c));
  stream.on("end", res);
  stream.on("error", rej);
});
for (const g of glyphs) {
  const s = new Readable();
  s.push(null);
  const scale = 1000 / g.size;
  // Glyph y axis points down in svgicons2svgfont input; scale each icon to the 1000-unit em.
  const paths = g.d.map((d) => `<path d="${d}"/>`).join("");
  const markup = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${g.size} ${g.size}" width="${g.size}" height="${g.size}">${paths}</svg>`;
  const rs = Readable.from([markup]);
  rs.metadata = { name: g.name, unicode: [String.fromCodePoint(g.code)] };
  stream.write(rs);
}
stream.end();
await done;
const svgFont = chunks.map((c) => c.toString()).join("");
const ttf = svg2ttf(svgFont, { description: "Okto Mac product icons" });
const woff = ttf2woff(new Uint8Array(ttf.buffer));
const outDir = path.join(root, "producticons");
fs.mkdirSync(path.join(outDir, "fonts"), { recursive: true });
fs.writeFileSync(path.join(outDir, "fonts", "okto-mac-icons.woff"), Buffer.from(woff.buffer));

// --- theme json ---
const theme = {
  $schema: "vscode://schemas/product-icon-theme",
  fonts: [{
    id: "okto-mac-font",
    src: [{ path: "./fonts/okto-mac-icons.woff", format: "woff" }],
    weight: "normal",
    style: "normal",
  }],
  iconDefinitions: {},
};
const ids = {};
for (const [k, v] of Object.entries(defs)) {
  if (k.startsWith("__id:")) ids[k.slice(5)] = v;
  else theme.iconDefinitions[k] = v;
}
Object.assign(theme, ids);
fs.writeFileSync(path.join(outDir, "okto-mac-product-icon-theme.json"), JSON.stringify(theme, null, 2) + "\n");
console.log(`glyphs: ${glyphs.length}, mapped ids: ${Object.keys(ids).length} of ${known.size}, woff ${woff.length} bytes`);
