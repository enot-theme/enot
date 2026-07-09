#!/usr/bin/env python3
"""VS Code theme port: dist/vscode/enot.vsix.

Module port for the enot build. One extension carries both themes
(enot-dark and enot-light); the vsix is a deterministic stored zip
(fixed timestamps), so the CI diff gate holds and the JSON inside
stays scannable by the hex conformance check. Workbench colors and
TextMate token rules substitute spec values only; translucent
overlays (find matches, scrollbars, selections) are alpha suffixes
over spec colors, never colors of their own.
"""

import io
import json
import zipfile

SLUG = "enot"
VERSION = "1.0.0"
PUBLISHER = "enot-theme"

MANIFEST = f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Language="en-US" Id="{SLUG}" Version="{VERSION}" Publisher="{PUBLISHER}"/>
    <DisplayName>{SLUG}</DisplayName>
    <Description xml:space="preserve">An earthy colorscheme that survives color blindness.</Description>
    <Categories>Themes</Categories>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>
  </Installation>
  <Dependencies/>
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/>
  </Assets>
</PackageManifest>
"""

CONTENT_TYPES = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json"/>
  <Default Extension="vsixmanifest" ContentType="text/xml"/>
</Types>
"""

PACKAGE = {
    "name": SLUG,
    "displayName": SLUG,
    "description": "An earthy colorscheme that survives color blindness.",
    "version": VERSION,
    "publisher": PUBLISHER,
    "engines": {"vscode": "^1.60.0"},
    "categories": ["Themes"],
    "contributes": {
        "themes": [
            {"label": f"{SLUG}-dark", "uiTheme": "vs-dark",
             "path": "./themes/enot-dark-color-theme.json"},
            {"label": f"{SLUG}-light", "uiTheme": "vs",
             "path": "./themes/enot-light-color-theme.json"},
        ]
    },
}

ANSI_SLOTS = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta",
              "Cyan", "White"]


def workbench(r, ansi):
    c = {
        "focusBorder": r["blue"],
        "foreground": r["fg0"],
        "descriptionForeground": r["fg1"],
        "errorForeground": r["red"],
        "widget.shadow": ansi["black"] + "66",
        "selection.background": r["blue"] + "40",

        "editor.background": r["bg0"],
        "editor.foreground": r["fg0"],
        "editorLineNumber.foreground": r["linenr"],
        "editorLineNumber.activeForeground": r["fg1"],
        "editorCursor.foreground": r["fg0"],
        "editor.lineHighlightBackground": r["bg1"],
        "editor.selectionBackground": r["bg2"],
        "editor.inactiveSelectionBackground": r["bg1"],
        "editor.selectionHighlightBackground": r["blue"] + "26",
        "editor.findMatchBackground": r["orange"] + "66",
        "editor.findMatchHighlightBackground": r["yellow"] + "40",
        "editor.findMatchBorder": r["orange"],
        "editorWhitespace.foreground": r["bg3"],
        "editorIndentGuide.background1": r["bg2"],
        "editorIndentGuide.activeBackground1": r["bg3"],
        "editorRuler.foreground": r["bg2"],
        "editorBracketMatch.background": r["bg3"],
        "editorBracketMatch.border": r["bg3"],
        "editorBracketHighlight.foreground1": r["yellow"],
        "editorBracketHighlight.foreground2": r["blue"],
        "editorBracketHighlight.foreground3": r["purple"],
        "editorBracketHighlight.foreground4": r["aqua"],
        "editorBracketHighlight.foreground5": r["orange"],
        "editorBracketHighlight.foreground6": r["green"],
        "editorBracketHighlight.unexpectedBracket.foreground": r["red"],
        "editorInlayHint.background": r["bg1"],
        "editorInlayHint.foreground": r["comment"],

        "editorGutter.addedBackground": r["green"],
        "editorGutter.modifiedBackground": r["blue"],
        "editorGutter.deletedBackground": r["red"],
        "diffEditor.insertedLineBackground": r["diff_add_bg"],
        "diffEditor.insertedTextBackground": r["green"] + "26",
        "diffEditor.removedLineBackground": r["diff_del_bg"],
        "diffEditor.removedTextBackground": r["red"] + "26",

        "editorError.foreground": r["red"],
        "editorWarning.foreground": r["yellow"],
        "editorInfo.foreground": r["blue"],
        "editorHint.foreground": r["aqua"],

        "editorWidget.background": r["bg1"],
        "editorWidget.border": r["bg3"],
        "editorSuggestWidget.background": r["bg1"],
        "editorSuggestWidget.selectedBackground": r["bg3"],
        "editorSuggestWidget.highlightForeground": r["orange"],
        "editorHoverWidget.background": r["bg1"],
        "editorHoverWidget.border": r["bg3"],

        "sideBar.background": r["bg1"],
        "sideBar.foreground": r["fg1"],
        "sideBarTitle.foreground": r["fg1"],
        "sideBarSectionHeader.background": r["bg2"],
        "activityBar.background": r["bg1"],
        "activityBar.foreground": r["fg0"],
        "activityBar.inactiveForeground": r["comment"],
        "activityBarBadge.background": r["blue"],
        "activityBarBadge.foreground": r["bg0"],
        "statusBar.background": r["bg2"],
        "statusBar.foreground": r["fg1"],
        "statusBar.noFolderBackground": r["bg2"],
        "statusBar.debuggingBackground": r["orange"],
        "statusBar.debuggingForeground": r["bg0"],
        "statusBarItem.remoteBackground": r["blue"],
        "statusBarItem.remoteForeground": r["bg0"],
        "titleBar.activeBackground": r["bg1"],
        "titleBar.activeForeground": r["fg0"],
        "titleBar.inactiveBackground": r["bg1"],
        "titleBar.inactiveForeground": r["comment"],

        "tab.activeBackground": r["bg0"],
        "tab.activeForeground": r["fg0"],
        "tab.activeBorderTop": r["blue"],
        "tab.inactiveBackground": r["bg1"],
        "tab.inactiveForeground": r["fg1"],
        "tab.border": r["bg1"],
        "editorGroupHeader.tabsBackground": r["bg1"],
        "panel.background": r["bg0"],
        "panel.border": r["bg3"],
        "panelTitle.activeForeground": r["fg0"],
        "panelTitle.activeBorder": r["blue"],
        "breadcrumb.foreground": r["fg1"],
        "breadcrumb.focusForeground": r["fg0"],
        "breadcrumbPicker.background": r["bg1"],

        "list.activeSelectionBackground": r["bg2"],
        "list.activeSelectionForeground": r["fg0"],
        "list.inactiveSelectionBackground": r["bg1"],
        "list.hoverBackground": r["bg1"],
        "list.focusBackground": r["bg2"],
        "list.highlightForeground": r["orange"],
        "list.errorForeground": r["red"],
        "list.warningForeground": r["yellow"],
        "input.background": r["bg1"],
        "input.foreground": r["fg0"],
        "input.border": r["bg3"],
        "input.placeholderForeground": r["comment"],
        "inputOption.activeBorder": r["blue"],
        "dropdown.background": r["bg1"],
        "dropdown.foreground": r["fg0"],
        "dropdown.border": r["bg3"],
        "button.background": r["blue"],
        "button.foreground": r["bg0"],
        "button.hoverBackground": r["blue"],
        "button.secondaryBackground": r["bg2"],
        "button.secondaryForeground": r["fg0"],
        "badge.background": r["blue"],
        "badge.foreground": r["bg0"],
        "progressBar.background": r["blue"],
        "scrollbarSlider.background": r["fg1"] + "26",
        "scrollbarSlider.hoverBackground": r["fg1"] + "40",
        "scrollbarSlider.activeBackground": r["fg1"] + "66",

        "gitDecoration.addedResourceForeground": r["green"],
        "gitDecoration.modifiedResourceForeground": r["blue"],
        "gitDecoration.deletedResourceForeground": r["red"],
        "gitDecoration.untrackedResourceForeground": r["green"],
        "gitDecoration.ignoredResourceForeground": r["comment"],
        "gitDecoration.conflictingResourceForeground": r["purple"],

        "terminal.background": r["bg0"],
        "terminal.foreground": r["fg0"],
        "terminal.selectionBackground": r["bg2"],
        "terminalCursor.foreground": r["fg1"],
    }
    for name in ANSI_SLOTS:
        c[f"terminal.ansi{name}"] = ansi[name.lower()]
        c[f"terminal.ansiBright{name}"] = ansi["br_" + name.lower()]
    return c


def token_colors(r):
    def rule(name, scope, fg=None, style=None):
        settings = {}
        if fg:
            settings["foreground"] = fg
        if style is not None:
            settings["fontStyle"] = style
        return {"name": name, "scope": scope, "settings": settings}

    return [
        rule("Comment", "comment, punctuation.definition.comment",
             r["comment"], "italic"),
        rule("String", "string", r["aqua"]),
        rule("Escape", "constant.character.escape", r["orange"]),
        rule("Constant",
             "constant.numeric, constant.language, constant.character, "
             "constant.other", r["purple"]),
        rule("Keyword", "keyword, keyword.operator.word, storage", r["red"]),
        rule("Operator", "keyword.operator", r["fg0"]),
        rule("Import", "keyword.control.import, keyword.control.export",
             r["orange"]),
        rule("Storage type", "storage.type", r["yellow"]),
        rule("Function",
             "entity.name.function, support.function, support.macro, "
             "variable.function, variable.annotation", r["green"]),
        rule("Type",
             "entity.name.type, entity.name.class, entity.name.struct, "
             "entity.name.enum, entity.other.inherited-class, support.type, "
             "support.class", r["yellow"]),
        rule("Section", "entity.name.section", r["yellow"], "bold"),
        rule("Tag", "entity.name.tag", r["green"]),
        rule("YAML key", "entity.name.tag.yaml", r["blue"]),
        rule("Attribute", "entity.other.attribute-name", r["yellow"]),
        rule("Language variable", "variable.language", r["purple"], "italic"),
        rule("Parameter", "variable.parameter", r["blue"]),
        rule("Library constant", "support.constant", r["purple"]),
        rule("Preprocessor",
             "meta.preprocessor, keyword.other.preprocessor, "
             "punctuation.definition.preprocessor", r["orange"]),
        rule("Punctuation",
             "punctuation.separator, punctuation.terminator, "
             "punctuation.accessor", r["fg1"]),
        rule("Invalid", "invalid", r["red"], "bold"),
        rule("Deprecated", "invalid.deprecated", r["yellow"], "bold"),
        rule("Markup heading",
             "markup.heading, markup.heading punctuation.definition.heading",
             r["yellow"], "bold"),
        rule("Markup bold", "markup.bold", style="bold"),
        rule("Markup italic", "markup.italic", style="italic"),
        rule("Markup link", "markup.underline.link", r["blue"], "underline"),
        rule("Markup code", "markup.raw, markup.inline.raw", r["aqua"]),
        rule("Markup quote", "markup.quote", r["comment"], "italic"),
        rule("Markup inserted", "markup.inserted", r["green"]),
        rule("Markup deleted", "markup.deleted", r["red"]),
        rule("Markup changed", "markup.changed", r["blue"]),
        rule("Diff header", "meta.diff, meta.diff.header, meta.diff.range",
             r["purple"]),
        rule("Message error", "message.error", r["red"]),
    ]


def theme_json(spec, mode):
    roles = {k: e["hex"] for k, e in spec["themes"][mode]["roles"].items()}
    ansi = {k: e["hex"] for k, e in spec["themes"][mode]["ansi"].items()}
    return {
        "name": f"{SLUG}-{mode}",
        "type": mode,
        "semanticHighlighting": True,
        "colors": workbench(roles, ansi),
        "tokenColors": token_colors(roles),
    }


def render(spec):
    entries = [
        ("extension.vsixmanifest", MANIFEST),
        ("[Content_Types].xml", CONTENT_TYPES),
        ("extension/package.json", json.dumps(PACKAGE, indent=1) + "\n"),
    ]
    for mode in ("dark", "light"):
        entries.append((f"extension/themes/enot-{mode}-color-theme.json",
                        json.dumps(theme_json(spec, mode), indent=1) + "\n"))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
        for name, text in entries:
            z.writestr(zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0)),
                       text.encode())
    return {f"dist/vscode/{SLUG}.vsix": buf.getvalue()}
