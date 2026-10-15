// Writes tools/mac/.preview/product.html showing every glyph of the Okto Mac product icon theme.
import fs from "node:fs"; import path from "node:path"; import { fileURLToPath } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const theme = JSON.parse(fs.readFileSync(path.join(root, "producticons/okto-mac-product-icon-theme.json"), "utf8"));
const out = path.join(root, "tools/mac/.preview"); fs.mkdirSync(out, { recursive: true });
fs.copyFileSync(path.join(root, "producticons/fonts/okto-mac-icons.woff"), path.join(out, "f.woff"));
const cells = Object.entries(theme).filter(([k, v]) => typeof v === "string" && k !== "$schema").map(([k, v]) => {
  const ch = String.fromCodePoint(parseInt(theme.iconDefinitions[v].fontCharacter.slice(1), 16));
  return `<div><i>${ch}</i><span>${k}</span></div>`;
}).join("");
fs.writeFileSync(path.join(out, "product.html"), `<meta charset=utf8><style>@font-face{font-family:F;src:url(data:font/woff;base64,${fs.readFileSync(path.join(out,"f.woff")).toString("base64")})}body{background:#1e1e1e;color:#ccc;font:11px sans-serif;display:grid;grid-template-columns:repeat(auto-fill,110px);gap:8px;padding:10px}div{text-align:center}i{font:normal 32px F;display:block;color:#fff}.s i{font-size:16px}span{display:block;overflow:hidden;text-overflow:ellipsis}</style>${cells}`);
