# Installs Okto (themes + file icons + product icons) into VS Code on Windows.
# Usage (PowerShell, from the repository folder):  .\install.ps1
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$version = (Get-Content (Join-Path $root 'package.json') -Raw | ConvertFrom-Json).version
$extensions = Join-Path $env:USERPROFILE '.vscode\extensions'
$target = Join-Path $extensions "local.okto-theme-$version"

New-Item -ItemType Directory -Force -Path $extensions | Out-Null
Get-ChildItem $extensions -Directory -Filter 'local.okto-theme-*' | Remove-Item -Recurse -Force
New-Item -ItemType Directory -Force -Path $target | Out-Null
foreach ($item in 'package.json', 'icon.png', 'icon.svg', 'CHANGELOG.md', 'themes', 'fileicons', 'producticons') {
    Copy-Item (Join-Path $root $item) $target -Recurse -Force
}
Remove-Item (Join-Path $target 'producticons\generate_font.py') -ErrorAction SilentlyContinue

Write-Host "Okto $version installed to $target" -ForegroundColor Green
Write-Host @'

Restart VS Code (or run "Developer: Reload Window"), then add this to settings.json
(Ctrl+Shift+P -> "Preferences: Open User Settings (JSON)"):

  "workbench.colorTheme": "Okto Dark",
  "workbench.iconTheme": "okto-icons",
  "workbench.productIconTheme": "okto-product-icons"

Use "Okto Light" for the light theme.
'@
