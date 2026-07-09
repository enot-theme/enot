#!/usr/bin/env python3
"""Vim colorscheme port: vim/colors/enot.vim.

Module port for the enot build. render(spec) returns {path: text};
both themes go in one file (branching on &background), guifg/guibg
from the 16M depth of the spec, cterm from the 256 depth, vim/nvim
terminal palettes from ANSI 16. No colors are computed here -- the
group-to-role tables below are the only vim-specific mapping.
"""

SLUG = "enot"

# (group, fg, bg, attributes, guisp); names are spec roles
UI = [
    ("Normal", "fg0", "bg0", None, None),
    ("NormalFloat", "fg0", "bg1", None, None),
    ("FloatBorder", "bg3", "bg1", None, None),
    ("Cursor", "bg0", "fg0", None, None),
    ("CursorLine", None, "bg1", None, None),
    ("CursorColumn", None, "bg1", None, None),
    ("ColorColumn", None, "bg1", None, None),
    ("CursorLineNr", "fg1", "bg1", None, None),
    ("LineNr", "linenr", None, None, None),
    ("SignColumn", "linenr", None, None, None),
    ("FoldColumn", "linenr", None, None, None),
    ("Folded", "comment", "bg1", None, None),
    ("VertSplit", "bg3", None, None, None),
    ("WinSeparator", "bg3", None, None, None),
    ("StatusLine", "fg1", "bg2", None, None),
    ("StatusLineNC", "comment", "bg1", None, None),
    ("TabLine", "fg1", "bg1", None, None),
    ("TabLineSel", "fg0", "bg0", None, None),
    ("TabLineFill", None, "bg1", None, None),
    ("Pmenu", "fg0", "bg1", None, None),
    ("PmenuSel", "fg0", "bg3", None, None),
    ("PmenuSbar", None, "bg2", None, None),
    ("PmenuThumb", None, "bg3", None, None),
    ("WildMenu", "bg0", "yellow", None, None),
    ("Visual", None, "bg2", None, None),
    ("Search", "bg0", "yellow", None, None),
    ("IncSearch", "bg0", "orange", None, None),
    ("QuickFixLine", None, "bg2", None, None),
    ("MatchParen", None, "bg3", "bold", None),
    ("Conceal", "comment", None, None, None),
    ("Directory", "blue", None, None, None),
    ("Title", "yellow", None, "bold", None),
    ("ErrorMsg", "red", None, "bold", None),
    ("WarningMsg", "yellow", None, None, None),
    ("MoreMsg", "green", None, None, None),
    ("ModeMsg", "fg1", None, None, None),
    ("Question", "green", None, None, None),
    ("NonText", "bg3", None, None, None),
    ("SpecialKey", "bg3", None, None, None),
    ("Whitespace", "bg3", None, None, None),
]

SYNTAX = [
    ("Comment", "comment", None, "italic", None),
    ("Constant", "purple", None, None, None),
    ("Number", "purple", None, None, None),
    ("String", "aqua", None, None, None),
    ("Identifier", "blue", None, None, None),
    ("Function", "green", None, None, None),
    ("Statement", "red", None, None, None),
    ("Operator", "fg0", None, None, None),
    ("PreProc", "orange", None, None, None),
    ("Type", "yellow", None, None, None),
    ("Special", "orange", None, None, None),
    ("SpecialChar", "orange", None, None, None),
    ("Tag", "green", None, None, None),
    ("Delimiter", "fg1", None, None, None),
    ("SpecialComment", "comment", None, "bold", None),
    ("Debug", "orange", None, None, None),
    ("Underlined", "blue", None, "underline", None),
    ("Error", "red", None, "bold", None),
    ("Todo", "bg0", "yellow", "bold", None),
]

DIFF = [
    ("DiffAdd", None, "diff_add_bg", None, None),
    ("DiffDelete", "red", "diff_del_bg", None, None),
    ("DiffChange", None, "diff_change_bg", None, None),
    ("DiffText", None, "diff_text_bg", None, None),
    ("diffAdded", "green", None, None, None),
    ("diffRemoved", "red", None, None, None),
    ("diffChanged", "blue", None, None, None),
]

DIAG = [
    ("DiagnosticError", "red", None, None, None),
    ("DiagnosticWarn", "yellow", None, None, None),
    ("DiagnosticInfo", "blue", None, None, None),
    ("DiagnosticHint", "aqua", None, None, None),
    ("DiagnosticUnderlineError", None, None, "undercurl", "red"),
    ("DiagnosticUnderlineWarn", None, None, "undercurl", "yellow"),
    ("DiagnosticUnderlineInfo", None, None, "undercurl", "blue"),
    ("DiagnosticUnderlineHint", None, None, "undercurl", "aqua"),
    ("SpellBad", None, None, "undercurl", "red"),
    ("SpellCap", None, None, "undercurl", "blue"),
    ("SpellRare", None, None, "undercurl", "purple"),
    ("SpellLocal", None, None, "undercurl", "aqua"),
]

LINKS = [
    ("Character", "String"), ("Boolean", "Number"), ("Float", "Number"),
    ("Conditional", "Statement"), ("Repeat", "Statement"),
    ("Label", "Statement"), ("Keyword", "Statement"),
    ("Exception", "Statement"), ("Include", "PreProc"),
    ("Define", "PreProc"), ("Macro", "PreProc"), ("PreCondit", "PreProc"),
    ("StorageClass", "Type"), ("Structure", "Type"), ("Typedef", "Type"),
    ("EndOfBuffer", "NonText"), ("CurSearch", "IncSearch"),
    ("Added", "diffAdded"), ("Removed", "diffRemoved"),
    ("Changed", "diffChanged"),
    ("GitSignsAdd", "diffAdded"), ("GitSignsChange", "diffChanged"),
    ("GitSignsDelete", "diffRemoved"),
    ("GitGutterAdd", "diffAdded"), ("GitGutterChange", "diffChanged"),
    ("GitGutterDelete", "diffRemoved"),
]

ANSI_ORDER = ["black", "red", "green", "yellow",
              "blue", "magenta", "cyan", "white"]


def hl(roles, group, fg, bg, attr, sp):
    parts = [f"hi {group}"]
    if fg:
        parts += [f"guifg={roles[fg]['hex']}",
                  f"ctermfg={roles[fg]['c256']}"]
    if bg:
        parts += [f"guibg={roles[bg]['hex']}",
                  f"ctermbg={roles[bg]['c256']}"]
    # attributes are always explicit: hi clear keeps the default
    # reverse/bold on StatusLine, IncSearch and the like
    attr_val = attr or "NONE"
    cterm = "underline" if attr == "undercurl" else attr_val
    parts += [f"gui={attr_val}", f"cterm={cterm}"]
    if sp:
        parts.append(f"guisp={roles[sp]['hex']}")
    return " ".join(parts)


def terminal_lines(ansi):
    order = sorted(ansi.values(), key=lambda e: e["index"])
    quoted = ", ".join(f"'{e['hex']}'" for e in order)
    lines = [f"let g:terminal_ansi_colors = [{quoted}]"]
    lines += [f"let g:terminal_color_{e['index']} = '{e['hex']}'"
              for e in order]
    return lines


def mode_lines(theme):
    lines = []
    for section in (UI, SYNTAX, DIFF, DIAG):
        lines += [hl(theme["roles"], *spec) for spec in section]
    lines += terminal_lines(theme["ansi"])
    return lines


def render(spec):
    indent = "\n  "
    dark = indent.join(mode_lines(spec["themes"]["dark"]))
    light = indent.join(mode_lines(spec["themes"]["light"]))
    links = "\n".join(f"hi! link {a} {b}" for a, b in LINKS)
    body = f"""\" {SLUG} -- earthy scheme, CIELAB, dichromacy-resistant
\" generated from colors.json by the enot build, do not edit by hand
hi clear
if exists('syntax_on')
  syntax reset
endif
let g:colors_name = '{SLUG}'

if &background ==# 'dark'
  {dark}
else
  {light}
endif

{links}
"""
    return {f"vim/colors/{SLUG}.vim": body}
