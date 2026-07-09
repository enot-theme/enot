#!/usr/bin/env python3
"""lightline colorscheme port: dist/lightline/.../enot.vim.

Module port for the enot build. render(spec) returns {path: text};
both themes go in one file (branching on &background at load time,
like the vim scheme). Palette entries are ['#hex', c256] pairs from
the 16M and 256 depths of the spec, consumed by
lightline#colorscheme#flatten. Mode chips sit on accent fills with
bg0 text, so the statusline carries the same 4.5:1 contrast
guarantee as the editor colors.
"""

SLUG = "enot"

ROLES = ["bg0", "bg1", "bg2", "fg0", "fg1", "comment",
         "red", "green", "yellow", "blue", "purple"]

PALETTE = """\
let s:p = {'normal': {}, 'inactive': {}, 'insert': {}, 'replace': {}, 'visual': {}, 'tabline': {}}

" mode chips on accent fills, text is bg0: contrast held by the spec
let s:p.normal.left = [ [ s:bg0, s:blue ], [ s:fg0, s:bg2 ] ]
let s:p.normal.middle = [ [ s:comment, s:bg1 ] ]
let s:p.normal.right = [ [ s:fg0, s:bg2 ], [ s:fg1, s:bg1 ] ]
let s:p.normal.error = [ [ s:bg0, s:red ] ]
let s:p.normal.warning = [ [ s:bg0, s:yellow ] ]
let s:p.insert.left = [ [ s:bg0, s:green ], [ s:fg0, s:bg2 ] ]
let s:p.replace.left = [ [ s:bg0, s:red ], [ s:fg0, s:bg2 ] ]
let s:p.visual.left = [ [ s:bg0, s:purple ], [ s:fg0, s:bg2 ] ]
let s:p.inactive.left = [ [ s:comment, s:bg1 ], [ s:comment, s:bg1 ] ]
let s:p.inactive.middle = [ [ s:comment, s:bg1 ] ]
let s:p.inactive.right = [ [ s:comment, s:bg1 ], [ s:comment, s:bg1 ] ]
let s:p.tabline.left = [ [ s:fg1, s:bg1 ] ]
let s:p.tabline.tabsel = [ [ s:bg0, s:blue ] ]
let s:p.tabline.middle = [ [ s:comment, s:bg1 ] ]
let s:p.tabline.right = [ [ s:fg1, s:bg1 ] ]

let g:lightline#colorscheme#enot#palette = lightline#colorscheme#flatten(s:p)
"""


def lets(theme):
    roles = theme["roles"]
    return "\n".join(f"  let s:{r} = [ '{roles[r]['hex']}', {roles[r]['c256']} ]"
                     for r in ROLES)


def render(spec):
    body = (
        f'" {SLUG} -- earthy scheme, CIELAB, dichromacy-resistant\n'
        '" generated from colors.json by the enot build, do not edit by hand\n'
        '" both themes in one file: the palette follows &background at load;\n'
        '" after switching background call lightline#init(), then\n'
        '" lightline#colorscheme() and lightline#update()\n'
        '\n'
        "if &background ==# 'light'\n"
        f"{lets(spec['themes']['light'])}\n"
        "else\n"
        f"{lets(spec['themes']['dark'])}\n"
        "endif\n"
        "\n"
        f"{PALETTE}"
    )
    return {f"dist/lightline/autoload/lightline/colorscheme/{SLUG}.vim": body}
