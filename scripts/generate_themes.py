"""Generates the Okto Dark and Okto Light colour themes from two palettes.

Usage: python3 scripts/generate_themes.py
"""
from pathlib import Path
import json

root = Path(__file__).resolve().parent.parent
themes_dir = root / "themes"
themes_dir.mkdir(exist_ok=True)

DARK = dict(
    name="Okto Dark", mode="dark",
    editor="#171421", side="#120F1C", chrome="#0F0C18", raised="#221D33", hover="#2A2440", select="#352D54",
    border="#2A2440", border_soft="#201B30",
    fg="#E9E5F7", fg2="#B9B2D6", muted="#8A83AA", dim="#5B5578", faint="#3A3456",
    accent="#FF7DB0", accent_soft="#FF7DB0", accent2="#9B86FF", on_accent="#1B0F25",
    status_bg="#2A1F4E", status_fg="#E4DCFF", status_prom="#FF7DB0",
    button="#FF7DB0", button_hover="#FF95C0", button_fg="#1B0F25",
    red="#FF6B86", orange="#FFB06B", yellow="#FFD97A", green="#7EE0A0", cyan="#5FD8E6", blue="#6EB8FF", purple="#B79CFF", pink="#FF7DB0",
    ansi_black="#1C1829", ansi_white="#D6D0EC", ansi_bblack="#5B5578", ansi_bwhite="#FFFFFF",
    # syntax
    comment="#7A729C", keyword="#C79BFF", string="#8FE5A9", number="#FFB36B", function="#6EC1FF",
    type="#FFD479", variable="#E9E5F7", property="#8EDBEA", constant="#FF8FA6", operator="#FF7DB0",
    tag="#FF7DB0", attribute="#FFD479", param="#F2B5FF", decorator="#62E8D2", regex="#FFC38A", escape="#FF7DB0",
    sel_alpha="55", find="#FFB06B55", word="#9B86FF2E", line_hl="#FFFFFF08",
)

LIGHT = dict(
    name="Okto Light", mode="light",
    editor="#FDFBFF", side="#F5F1FA", chrome="#EDE7F6", raised="#FFFFFF", hover="#EAE3F6", select="#DDD2F6",
    border="#E1D9EE", border_soft="#EAE4F3",
    fg="#2A2442", fg2="#4A4468", muted="#746D96", dim="#A39CC0", faint="#D3CCE6",
    accent="#D62F78", accent_soft="#E8508F", accent2="#6B4EE0", on_accent="#FFFFFF",
    status_bg="#6B4EE0", status_fg="#FFFFFF", status_prom="#D62F78",
    button="#D62F78", button_hover="#E8508F", button_fg="#FFFFFF",
    red="#D6304F", orange="#C75D0E", yellow="#A87400", green="#14875A", cyan="#0A7E92", blue="#1F6DD0", purple="#7B3FEA", pink="#D62F78",
    ansi_black="#2A2442", ansi_white="#C9C2DE", ansi_bblack="#746D96", ansi_bwhite="#FFFFFF",
    comment="#9D96BA", keyword="#7B3FEA", string="#14875A", number="#C75D0E", function="#1F6DD0",
    type="#A87400", variable="#2A2442", property="#0A7E92", constant="#D6304F", operator="#D62F78",
    tag="#D62F78", attribute="#A87400", param="#9A35BE", decorator="#0C8C78", regex="#B5530B", escape="#D62F78",
    sel_alpha="44", find="#F2A65A66", word="#6B4EE022", line_hl="#6B4EE00A",
)


def colors(p):
    a = lambda c, alpha: c[:7] + alpha  # noqa: E731 - tiny alpha helper
    dark = p["mode"] == "dark"
    c = {
        "foreground": p["fg"], "descriptionForeground": p["muted"], "disabledForeground": p["dim"],
        "focusBorder": a(p["accent"], "99"), "contrastBorder": p["border"], "contrastActiveBorder": p["accent"],
        "selection.background": a(p["accent2"], "66"), "widget.shadow": "#00000040" if dark else "#3A2A6B22",
        "errorForeground": p["red"], "icon.foreground": p["muted"],
        "textLink.foreground": p["accent2"] if not dark else p["blue"], "textLink.activeForeground": p["accent"],
        "textBlockQuote.background": p["raised"], "textBlockQuote.border": p["accent"],
        "textCodeBlock.background": p["raised"], "textPreformat.foreground": p["orange"],
        "textSeparator.foreground": p["border"],
        # buttons / badges / inputs
        "button.background": p["button"], "button.foreground": p["button_fg"], "button.hoverBackground": p["button_hover"],
        "button.secondaryBackground": p["raised"], "button.secondaryForeground": p["fg"], "button.secondaryHoverBackground": p["hover"],
        "badge.background": p["accent2"], "badge.foreground": "#FFFFFF",
        "checkbox.background": p["raised"], "checkbox.border": p["border"], "checkbox.foreground": p["fg"],
        "dropdown.background": p["raised"], "dropdown.foreground": p["fg"], "dropdown.border": p["border"],
        "input.background": p["raised"] if dark else "#FFFFFF", "input.foreground": p["fg"], "input.border": p["border"],
        "input.placeholderForeground": p["dim"],
        "inputOption.activeBorder": p["accent"], "inputOption.activeBackground": a(p["accent"], "26"),
        "inputValidation.errorBackground": a(p["red"], "22"), "inputValidation.errorBorder": p["red"],
        "inputValidation.warningBackground": a(p["orange"], "22"), "inputValidation.warningBorder": p["orange"],
        "inputValidation.infoBackground": a(p["blue"], "22"), "inputValidation.infoBorder": p["blue"],
        # lists & trees
        "list.activeSelectionBackground": p["select"], "list.activeSelectionForeground": p["fg"],
        "list.inactiveSelectionBackground": p["hover"], "list.inactiveSelectionForeground": p["fg"],
        "list.hoverBackground": a(p["hover"], "AA"), "list.focusBackground": p["select"],
        "list.focusOutline": a(p["accent"], "88"), "list.highlightForeground": p["accent"],
        "list.errorForeground": p["red"], "list.warningForeground": p["orange"],
        "list.invalidItemForeground": p["red"], "tree.indentGuidesStroke": p["faint"],
        # activity bar / side bar / title bar
        "activityBar.background": p["chrome"], "activityBar.foreground": p["fg"], "activityBar.inactiveForeground": p["dim"],
        "activityBar.border": p["border_soft"], "activityBar.activeBorder": p["accent"],
        "activityBar.activeBackground": a(p["accent"], "14"),
        "activityBarBadge.background": p["accent"], "activityBarBadge.foreground": p["on_accent"],
        "sideBar.background": p["side"], "sideBar.foreground": p["fg2"], "sideBar.border": p["border_soft"],
        "sideBarTitle.foreground": p["fg"], "sideBarSectionHeader.background": p["side"],
        "sideBarSectionHeader.foreground": p["muted"], "sideBarSectionHeader.border": p["border_soft"],
        "titleBar.activeBackground": p["chrome"], "titleBar.activeForeground": p["fg2"],
        "titleBar.inactiveBackground": p["chrome"], "titleBar.inactiveForeground": p["dim"], "titleBar.border": p["border_soft"],
        "menu.background": p["raised"], "menu.foreground": p["fg"], "menu.selectionBackground": p["select"],
        "menu.selectionForeground": p["fg"], "menu.separatorBackground": p["border"],
        "menubar.selectionBackground": p["hover"], "menubar.selectionForeground": p["fg"],
        # editor groups & tabs
        "editorGroup.border": p["border"], "editorGroup.dropBackground": a(p["accent2"], "26"),
        "editorGroupHeader.tabsBackground": p["side"], "editorGroupHeader.tabsBorder": p["border_soft"],
        "editorGroupHeader.noTabsBackground": p["editor"],
        "tab.activeBackground": p["editor"], "tab.activeForeground": p["fg"], "tab.activeBorder": p["editor"],
        "tab.activeBorderTop": p["accent"], "tab.inactiveBackground": p["side"], "tab.inactiveForeground": p["muted"],
        "tab.border": p["border_soft"], "tab.hoverBackground": p["hover"], "tab.hoverForeground": p["fg"],
        "tab.unfocusedActiveForeground": p["fg2"], "tab.unfocusedInactiveForeground": p["dim"],
        "tab.activeModifiedBorder": p["accent2"], "tab.inactiveModifiedBorder": a(p["accent2"], "88"),
        # editor
        "editor.background": p["editor"], "editor.foreground": p["fg"],
        "editorLineNumber.foreground": p["faint"] if dark else p["dim"], "editorLineNumber.activeForeground": p["accent"],
        "editorCursor.foreground": p["accent"], "editor.selectionBackground": a(p["accent2"], p["sel_alpha"]),
        "editor.inactiveSelectionBackground": a(p["accent2"], "26"),
        "editor.selectionHighlightBackground": a(p["accent2"], "26"),
        "editor.wordHighlightBackground": p["word"], "editor.wordHighlightStrongBackground": a(p["accent"], "2A"),
        "editor.findMatchBackground": p["find"], "editor.findMatchHighlightBackground": a(p["orange"], "33"),
        "editor.findRangeHighlightBackground": a(p["accent2"], "14"),
        "editor.hoverHighlightBackground": a(p["accent2"], "22"),
        "editor.lineHighlightBackground": p["line_hl"], "editor.lineHighlightBorder": "#00000000",
        "editor.rangeHighlightBackground": a(p["accent2"], "14"),
        "editor.foldBackground": a(p["accent2"], "14"),
        "editorLink.activeForeground": p["accent"],
        "editorWhitespace.foreground": p["faint"], "editorIndentGuide.background1": p["border_soft"] if dark else p["faint"],
        "editorIndentGuide.activeBackground1": p["dim"], "editorRuler.foreground": p["border"],
        "editorCodeLens.foreground": p["dim"], "editorInlayHint.foreground": p["muted"],
        "editorInlayHint.background": a(p["accent2"], "1C"),
        "editorBracketMatch.background": a(p["accent"], "26"), "editorBracketMatch.border": a(p["accent"], "99"),
        "editorBracketHighlight.foreground1": p["yellow"], "editorBracketHighlight.foreground2": p["pink"],
        "editorBracketHighlight.foreground3": p["blue"], "editorBracketHighlight.foreground4": p["green"],
        "editorBracketHighlight.foreground5": p["purple"], "editorBracketHighlight.foreground6": p["cyan"],
        "editorBracketHighlight.unexpectedBracket.foreground": p["red"],
        "editorGutter.background": p["editor"], "editorGutter.addedBackground": p["green"],
        "editorGutter.modifiedBackground": p["blue"], "editorGutter.deletedBackground": p["red"],
        "editorError.foreground": p["red"], "editorWarning.foreground": p["orange"],
        "editorInfo.foreground": p["blue"], "editorHint.foreground": p["green"],
        "editorOverviewRuler.border": "#00000000", "editorOverviewRuler.errorForeground": p["red"],
        "editorOverviewRuler.warningForeground": p["orange"], "editorOverviewRuler.infoForeground": p["blue"],
        "editorOverviewRuler.addedForeground": a(p["green"], "99"), "editorOverviewRuler.modifiedForeground": a(p["blue"], "99"),
        "editorOverviewRuler.deletedForeground": a(p["red"], "99"),
        "editorStickyScroll.background": p["side"], "editorStickyScrollHover.background": p["hover"],
        # widgets
        "editorWidget.background": p["raised"], "editorWidget.border": p["border"],
        "editorSuggestWidget.background": p["raised"], "editorSuggestWidget.border": p["border"],
        "editorSuggestWidget.selectedBackground": p["select"], "editorSuggestWidget.highlightForeground": p["accent"],
        "editorHoverWidget.background": p["raised"], "editorHoverWidget.border": p["border"],
        "peekView.border": p["accent2"], "peekViewEditor.background": p["side"], "peekViewResult.background": p["chrome"],
        "peekViewResult.selectionBackground": p["select"], "peekViewTitle.background": p["chrome"],
        "peekViewTitleLabel.foreground": p["fg"], "peekViewEditor.matchHighlightBackground": a(p["orange"], "44"),
        # diff & merge
        "diffEditor.insertedTextBackground": a(p["green"], "26"), "diffEditor.removedTextBackground": a(p["red"], "26"),
        "diffEditor.insertedLineBackground": a(p["green"], "14"), "diffEditor.removedLineBackground": a(p["red"], "14"),
        "merge.currentHeaderBackground": a(p["green"], "55"), "merge.incomingHeaderBackground": a(p["blue"], "55"),
        # panel / terminal
        "panel.background": p["side"], "panel.border": p["border"], "panelTitle.activeForeground": p["fg"],
        "panelTitle.inactiveForeground": p["muted"], "panelTitle.activeBorder": p["accent"],
        "panelSectionHeader.background": p["chrome"],
        "terminal.background": p["side"], "terminal.foreground": p["fg"], "terminalCursor.foreground": p["accent"],
        "terminal.selectionBackground": a(p["accent2"], "44"),
        "terminal.ansiBlack": p["ansi_black"], "terminal.ansiRed": p["red"], "terminal.ansiGreen": p["green"],
        "terminal.ansiYellow": p["yellow"], "terminal.ansiBlue": p["blue"], "terminal.ansiMagenta": p["purple"],
        "terminal.ansiCyan": p["cyan"], "terminal.ansiWhite": p["ansi_white"],
        "terminal.ansiBrightBlack": p["ansi_bblack"], "terminal.ansiBrightRed": p["red"],
        "terminal.ansiBrightGreen": p["green"], "terminal.ansiBrightYellow": p["yellow"],
        "terminal.ansiBrightBlue": p["blue"], "terminal.ansiBrightMagenta": p["pink"],
        "terminal.ansiBrightCyan": p["cyan"], "terminal.ansiBrightWhite": p["ansi_bwhite"],
        # status bar
        "statusBar.background": p["status_bg"], "statusBar.foreground": p["status_fg"],
        "statusBar.border": "#00000000", "statusBar.debuggingBackground": p["orange"],
        "statusBar.debuggingForeground": "#1B0F25", "statusBar.noFolderBackground": p["chrome"],
        "statusBar.noFolderForeground": p["fg2"], "statusBarItem.hoverBackground": "#FFFFFF22",
        "statusBarItem.prominentBackground": p["status_prom"], "statusBarItem.prominentForeground": p["on_accent"],
        "statusBarItem.prominentHoverBackground": p["accent_soft"], "statusBarItem.remoteBackground": p["accent"],
        "statusBarItem.remoteForeground": p["on_accent"],
        "progressBar.background": p["accent"],
        # notifications / quick input / breadcrumbs
        "notificationCenterHeader.background": p["chrome"], "notificationCenterHeader.foreground": p["fg"],
        "notifications.background": p["raised"], "notifications.foreground": p["fg"], "notifications.border": p["border"],
        "notificationLink.foreground": p["accent"],
        "notificationsErrorIcon.foreground": p["red"], "notificationsWarningIcon.foreground": p["orange"],
        "notificationsInfoIcon.foreground": p["blue"],
        "quickInput.background": p["raised"], "quickInput.foreground": p["fg"], "quickInputList.focusBackground": p["select"],
        "quickInputTitle.background": p["chrome"], "pickerGroup.foreground": p["accent"], "pickerGroup.border": p["border"],
        "breadcrumb.foreground": p["muted"], "breadcrumb.focusForeground": p["fg"],
        "breadcrumb.activeSelectionForeground": p["accent"], "breadcrumbPicker.background": p["raised"],
        # scrollbars / minimap
        "scrollbar.shadow": "#00000000", "scrollbarSlider.background": a(p["accent2"], "30"),
        "scrollbarSlider.hoverBackground": a(p["accent2"], "55"), "scrollbarSlider.activeBackground": a(p["accent2"], "77"),
        "minimap.background": p["editor"], "minimap.selectionHighlight": a(p["accent2"], "77"),
        "minimap.findMatchHighlight": p["orange"], "minimapSlider.background": a(p["accent2"], "22"),
        "minimapSlider.hoverBackground": a(p["accent2"], "44"), "minimapGutter.addedBackground": p["green"],
        "minimapGutter.modifiedBackground": p["blue"], "minimapGutter.deletedBackground": p["red"],
        # git / scm
        "gitDecoration.addedResourceForeground": p["green"], "gitDecoration.modifiedResourceForeground": p["blue"],
        "gitDecoration.deletedResourceForeground": p["red"], "gitDecoration.untrackedResourceForeground": p["cyan"],
        "gitDecoration.ignoredResourceForeground": p["dim"], "gitDecoration.conflictingResourceForeground": p["orange"],
        "gitDecoration.stageModifiedResourceForeground": p["purple"],
        "scmGraph.foreground1": p["pink"], "scmGraph.foreground2": p["blue"], "scmGraph.foreground3": p["green"],
        "scmGraph.foreground4": p["orange"], "scmGraph.foreground5": p["purple"],
        # debug
        "debugToolBar.background": p["raised"], "debugToolBar.border": p["border"],
        "debugIcon.breakpointForeground": p["red"], "debugIcon.startForeground": p["green"],
        "debugIcon.pauseForeground": p["orange"], "debugIcon.stopForeground": p["red"],
        "debugIcon.continueForeground": p["blue"], "debugIcon.stepOverForeground": p["blue"],
        "editor.stackFrameHighlightBackground": a(p["yellow"], "26"),
        "editor.focusedStackFrameHighlightBackground": a(p["green"], "26"),
        # misc
        "extensionButton.prominentBackground": p["button"], "extensionButton.prominentForeground": p["button_fg"],
        "extensionButton.prominentHoverBackground": p["button_hover"],
        "welcomePage.background": p["editor"], "welcomePage.tileBackground": p["raised"],
        "welcomePage.tileHoverBackground": p["hover"], "welcomePage.progress.foreground": p["accent"],
        "settings.headerForeground": p["fg"], "settings.modifiedItemIndicator": p["accent"],
        "keybindingLabel.background": p["hover"], "keybindingLabel.foreground": p["fg"], "keybindingLabel.border": p["border"],
        "keybindingLabel.bottomBorder": p["faint"], "toolbar.hoverBackground": p["hover"],
        "banner.background": p["select"], "banner.foreground": p["fg"],
        "charts.foreground": p["fg2"], "charts.lines": p["muted"], "charts.red": p["red"], "charts.blue": p["blue"],
        "charts.yellow": p["yellow"], "charts.orange": p["orange"], "charts.green": p["green"], "charts.purple": p["purple"],
        "symbolIcon.classForeground": p["type"], "symbolIcon.functionForeground": p["function"],
        "symbolIcon.methodForeground": p["function"], "symbolIcon.variableForeground": p["variable"],
        "symbolIcon.propertyForeground": p["property"], "symbolIcon.keywordForeground": p["keyword"],
        "symbolIcon.stringForeground": p["string"], "symbolIcon.constantForeground": p["constant"],
        "symbolIcon.interfaceForeground": p["cyan"], "symbolIcon.enumeratorForeground": p["orange"],
        "symbolIcon.moduleForeground": p["pink"], "symbolIcon.fieldForeground": p["property"],
        "symbolIcon.structForeground": p["type"], "symbolIcon.eventForeground": p["orange"],
        "symbolIcon.operatorForeground": p["operator"], "symbolIcon.typeParameterForeground": p["param"],
        "notebook.cellEditorBackground": p["side"], "notebook.focusedCellBorder": p["accent"],
        "notebook.cellBorderColor": p["border"],
    }
    return c


def token_colors(p):
    return [
        ("Comments", ["comment", "punctuation.definition.comment"], {"foreground": p["comment"], "fontStyle": "italic"}),
        ("Keywords & storage", ["keyword", "storage", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression", "keyword.operator.word"], {"foreground": p["keyword"]}),
        ("Operators", ["keyword.operator", "punctuation.separator.key-value", "punctuation.accessor"], {"foreground": p["operator"]}),
        ("Punctuation", ["punctuation", "meta.brace", "punctuation.definition.block", "punctuation.terminator"], {"foreground": p["fg2"]}),
        ("Strings", ["string", "punctuation.definition.string", "string.quoted"], {"foreground": p["string"]}),
        ("Template expressions", ["punctuation.definition.template-expression", "punctuation.section.embedded"], {"foreground": p["operator"]}),
        ("Escapes", ["constant.character.escape", "string.regexp constant.character.escape"], {"foreground": p["escape"]}),
        ("Regex", ["string.regexp"], {"foreground": p["regex"]}),
        ("Numbers", ["constant.numeric"], {"foreground": p["number"]}),
        ("Constants", ["constant.language", "constant.character", "constant.other", "support.constant", "variable.other.constant"], {"foreground": p["constant"]}),
        ("Functions", ["entity.name.function", "support.function", "meta.function-call", "variable.function", "meta.function-call entity.name.function"], {"foreground": p["function"]}),
        ("Types & classes", ["entity.name.type", "entity.name.class", "entity.name.namespace", "support.type", "support.class", "entity.other.inherited-class", "storage.type.class"], {"foreground": p["type"]}),
        ("Variables", ["variable", "variable.other.readwrite", "meta.definition.variable"], {"foreground": p["variable"]}),
        ("Parameters", ["variable.parameter", "meta.parameter"], {"foreground": p["param"], "fontStyle": "italic"}),
        ("this / self", ["variable.language", "variable.language.this", "variable.language.self"], {"foreground": p["pink"], "fontStyle": "italic"}),
        ("Properties", ["variable.other.property", "variable.other.object.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml"], {"foreground": p["property"]}),
        ("Decorators & annotations", ["meta.decorator", "entity.name.function.decorator", "punctuation.decorator", "storage.type.annotation", "meta.annotation"], {"foreground": p["decorator"]}),
        ("Tags", ["entity.name.tag", "punctuation.definition.tag", "meta.tag"], {"foreground": p["tag"]}),
        ("Attributes", ["entity.other.attribute-name", "entity.other.attribute-name.class.css"], {"foreground": p["attribute"], "fontStyle": "italic"}),
        ("CSS selectors", ["entity.other.attribute-name.id.css", "entity.name.tag.css", "meta.selector"], {"foreground": p["tag"]}),
        ("CSS properties", ["support.type.property-name.css", "support.type.vendored.property-name.css"], {"foreground": p["property"]}),
        ("CSS values", ["support.constant.property-value.css", "meta.property-value.css", "constant.other.color"], {"foreground": p["number"]}),
        ("CSS units", ["keyword.other.unit"], {"foreground": p["constant"]}),
        ("JSON keys", ["support.type.property-name.json", "meta.structure.dictionary.key.json string"], {"foreground": p["property"]}),
        ("Imports & modules", ["keyword.control.import", "keyword.control.export", "keyword.control.from", "keyword.control.as"], {"foreground": p["pink"]}),
        ("Markdown headings", ["markup.heading", "entity.name.section", "punctuation.definition.heading"], {"foreground": p["pink"], "fontStyle": "bold"}),
        ("Markdown emphasis", ["markup.italic"], {"foreground": p["purple"], "fontStyle": "italic"}),
        ("Markdown strong", ["markup.bold"], {"foreground": p["orange"], "fontStyle": "bold"}),
        ("Markdown code", ["markup.inline.raw", "markup.fenced_code.block", "markup.raw"], {"foreground": p["green"]}),
        ("Markdown links", ["markup.underline.link", "string.other.link"], {"foreground": p["function"]}),
        ("Markdown quote & lists", ["markup.quote", "punctuation.definition.list.begin", "beginning.punctuation.definition.list"], {"foreground": p["muted"]}),
        ("Diff inserted", ["markup.inserted", "meta.diff.header.to-file"], {"foreground": p["green"]}),
        ("Diff deleted", ["markup.deleted", "meta.diff.header.from-file"], {"foreground": p["red"]}),
        ("Diff changed", ["markup.changed"], {"foreground": p["blue"]}),
        ("Invalid", ["invalid", "invalid.illegal"], {"foreground": p["red"], "fontStyle": "underline"}),
        ("Deprecated", ["invalid.deprecated"], {"fontStyle": "strikethrough"}),
    ]


def semantic(p):
    return {
        "enumMember": p["orange"], "variable.constant": p["constant"], "variable.defaultLibrary": p["pink"],
        "variable": p["variable"], "parameter": {"foreground": p["param"], "italic": True},
        "property": p["property"], "function": p["function"], "method": p["function"],
        "function.defaultLibrary": p["function"], "class": p["type"], "type": p["type"],
        "interface": p["cyan"], "enum": p["type"], "struct": p["type"], "typeParameter": p["param"],
        "namespace": p["type"], "decorator": p["decorator"], "macro": p["decorator"],
        "keyword": p["keyword"], "string": p["string"], "number": p["number"], "regexp": p["regex"],
        "operator": p["operator"], "comment": {"foreground": p["comment"], "italic": True},
    }


def build(p):
    return {
        "$schema": "vscode://schemas/color-theme",
        "name": p["name"],
        "type": p["mode"],
        "semanticHighlighting": True,
        "colors": colors(p),
        "tokenColors": [{"name": n, "scope": s, "settings": st} for n, s, st in token_colors(p)],
        "semanticTokenColors": semantic(p),
    }


for old in themes_dir.glob("*.json"):
    old.unlink()
for p, filename in ((DARK, "okto-dark-color-theme.json"), (LIGHT, "okto-light-color-theme.json")):
    (themes_dir / filename).write_text(json.dumps(build(p), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("themes written")
