#!/usr/bin/env sh
# Installs Okto (themes + file icons + product icons) into VS Code on macOS / Linux.
# Usage (from the repository folder):  ./install.sh
set -e
root=$(cd "$(dirname "$0")" && pwd)
version=$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$root/package.json" | head -1)
extensions="$HOME/.vscode/extensions"
target="$extensions/local.okto-theme-$version"

mkdir -p "$extensions"
rm -rf "$extensions"/local.okto-theme-*
mkdir -p "$target"
for item in package.json icon.png icon.svg CHANGELOG.md themes fileicons producticons; do
  cp -R "$root/$item" "$target/"
done
rm -f "$target/producticons/generate_font.py"

echo "Okto $version installed to $target"
cat <<'TXT'

Restart VS Code (or run "Developer: Reload Window"), then add this to settings.json
(Ctrl/Cmd+Shift+P -> "Preferences: Open User Settings (JSON)"):

  "workbench.colorTheme": "Okto Dark",
  "workbench.iconTheme": "okto-icons",
  "workbench.productIconTheme": "okto-product-icons"

Use "Okto Light" for the light theme.
TXT
