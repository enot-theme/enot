#!/usr/bin/env python3
"""mc skins from colors.json (enot variant).

Writes mc/enot-{dark,light}-16M.ini (truecolor, mc >= 4.8.19 with
S-Lang) and mc/enot-{dark,light}256.ini (the 256 depth of the spec).
A terminal without truecolor does not degrade a skin color by color:
mc falls back to the default skin entirely, so the 256 variant is
mandatory. No colors are computed here -- pure substitution from
colors.json. Install: copy into ~/.local/share/mc/skins/ and select
in Options > Appearance or mc -S enot-dark-16M.
"""

import json
import os

SLUG = "enot"

# [aliases] entries: name -> spec role
ALIASES = [
    ("Bg0", "bg0"), ("Bg1", "bg1"), ("Bg2", "bg2"), ("Bg3", "bg3"),
    ("Fg0", "fg0"), ("Fg1", "fg1"),
    ("Comment", "comment"), ("LineNr", "linenr"),
    ("Red", "red"), ("Orange", "orange"), ("Yellow", "yellow"),
    ("Green", "green"), ("Aqua", "aqua"), ("Blue", "blue"),
    ("Purple", "purple"),
    ("DiffAdd", "diff_add_bg"), ("DiffDel", "diff_del_bg"),
    ("DiffChange", "diff_change_bg"), ("DiffText", "diff_text_bg"),
]

# [Lines] capitalized: releases <= 4.8.33 read only that spelling;
# double lines are drawn as single -- flat look, like tokyo-night
_SINGLE = {
    "horiz": "─", "vert": "│",
    "lefttop": "┌", "righttop": "┐",
    "leftbottom": "└", "rightbottom": "┘",
    "topmiddle": "┬", "bottommiddle": "┴",
    "leftmiddle": "├", "rightmiddle": "┤",
    "cross": "┼",
}
LINES = list(_SINGLE.items()) + [("d" + k, v) for k, v in _SINGLE.items()
                                 if k != "cross"]

# values are aliases or default; fields fg;bg;attrs, an empty field
# inherits via the section's _default_, then [core] _default_
SECTIONS = [
    ("core", [
        ("_default_", "Fg0;Bg0"),
        ("selected", ";Bg2"),
        ("marked", "Yellow;;bold"),
        # marked under the cursor: inverse video on yellow; accents on
        # raised backgrounds (Bg1-Bg3) do not hold 4.5 contrast
        ("markselect", "Bg0;Yellow"),
        ("gauge", "Bg0;Blue"),
        ("input", "Fg0;Bg2"),
        ("inputmark", "Bg0;Fg1"),
        ("inputunchanged", "Comment;Bg2"),
        ("inputhistory", "Fg0;Bg2"),
        ("commandhistory", "Fg0;Bg0"),
        ("commandlinemark", "Bg0;Fg1"),
        ("disabled", "Comment;Bg1"),
        ("reverse", "Bg0;Fg0"),
        ("header", "Yellow"),
        ("shadow", "Comment;Bg0"),
        # keys from master (after 4.8.33); ignored by older versions
        ("hintbar", "Fg1;Bg0"),
        ("shellprompt", "Fg0;Bg0"),
        ("commandline", "Fg0;Bg0"),
        ("frame", "Fg1;Bg0"),
    ]),
    # hotkeys and titles: underline and bold instead of accents --
    # shape reads under any vision, while accents on Bg1/Bg3
    # fall short of contrast
    ("dialog", [
        ("_default_", "Fg0;Bg1"),
        ("dfocus", "Fg0;Bg3"),
        ("dhotnormal", ";;underline"),
        ("dhotfocus", ";Bg3;underline"),
        ("dtitle", ";;bold"),
        ("dselnormal", ";Bg2"),
        ("dselfocus", ";Bg3"),
        ("dframe", "Fg1;Bg1"),
    ]),
    ("error", [
        ("_default_", "Bg0;Red"),
        ("errdfocus", "Red;Bg0"),
        ("errdhotnormal", ";;underline"),
        ("errdhotfocus", "Red;Bg0;underline"),
        ("errdtitle", ";;bold"),
        ("errdframe", "Bg0;Red"),
    ]),
    # groups match filehighlight.ini; the layout is aligned with the
    # ranger scheme: directories blue, executables green,
    # links aqua, broken files and archives red
    ("filehighlight", [
        ("directory", "Blue;;bold"),
        ("executable", "Green"),
        ("symlink", "Aqua"),
        ("hardlink", "Aqua"),
        ("stalelink", "Purple"),
        ("device", "Yellow"),
        ("special", "Purple"),
        ("core", "Red"),
        ("temp", "Comment"),
        ("archive", "Red"),
        ("doc", "Orange"),
        ("source", "Yellow"),
        ("media", "Purple"),
        ("graph", "Yellow"),
        ("database", "Orange"),
    ]),
    ("menu", [
        ("_default_", "Fg0;Bg1"),
        ("menusel", "Fg0;Bg3"),
        ("menuhot", ";;underline"),
        ("menuhotsel", ";Bg3;underline"),
        ("menuinactive", "Comment;Bg1"),
        ("menuframe", "Fg1;Bg1"),
    ]),
    ("popupmenu", [
        ("_default_", "Fg0;Bg1"),
        ("menusel", "Fg0;Bg3"),
        ("menutitle", ";;bold"),
        ("menuframe", "Fg1;Bg1"),
    ]),
    ("buttonbar", [
        ("hotkey", "Yellow;Bg0"),
        ("button", "Fg1;Bg0"),
    ]),
    ("statusbar", [
        ("_default_", "Fg0;Bg2"),
    ]),
    ("help", [
        ("_default_", "Fg0;Bg1"),
        ("helpbold", ";;bold"),
        ("helpitalic", ";;italic"),
        ("helplink", ";;underline"),
        ("helpslink", ";Bg3;underline"),
        ("helpframe", "Fg1;Bg1"),
    ]),
    ("editor", [
        ("_default_", "Fg0;Bg0"),
        ("editbold", "Yellow;;bold"),
        ("editmarked", ";Bg2"),
        ("editwhitespace", "Bg3"),
        ("editnonprintable", "Orange"),
        ("editlinestate", "LineNr;Bg1"),
        ("bookmark", "Bg0;Yellow"),
        ("bookmarkfound", "Bg0;Orange"),
        ("editrightmargin", "LineNr;Bg1"),
        ("editbg", ";Bg0"),
        ("editframe", "Bg3"),
        ("editframeactive", "Blue"),
        ("editframedrag", "Orange"),
    ]),
    ("viewer", [
        ("_default_", "Fg0;Bg0"),
        ("viewbold", ";;bold"),
        ("viewunderline", ";;underline"),
        ("viewboldunderline", ";;bold+underline"),
        ("viewselected", "Bg0;Yellow"),
        ("viewframe", "Bg3;Bg0"),
    ]),
    ("diffviewer", [
        ("added", ";DiffAdd"),
        ("changednew", ";DiffAdd"),
        ("removed", ";DiffDel"),
        ("changedline", ";DiffChange"),
        ("changed", ";DiffText"),
        ("error", "Bg0;Red"),
    ]),
]


def render(roles, mode, depth):
    if depth == "16M":
        colors = {a: roles[k]["hex"] for a, k in ALIASES}
        flag = "truecolors"
    else:
        colors = {a: "color%d" % roles[k]["c256"] for a, k in ALIASES}
        flag = "256colors"
    desc = (f"{SLUG} {mode} - earthy scheme, dichromacy-resistant"
            f" ({'truecolor' if depth == '16M' else '256 colors'})")
    out = [f"# {SLUG} -- generated by mc.py, do not edit by hand",
           "",
           "[skin]",
           f"description = {desc}",
           f"{flag} = true",
           "",
           "[Lines]"]
    out += [f"{k} = {c}" for k, c in LINES]
    out += ["", "[aliases]"]
    out += [f"{a} = {colors[a]}" for a, _ in ALIASES]
    for section, keys in SECTIONS:
        out += ["", f"[{section}]"]
        out += [f"{k} = {val}" for k, val in keys]
    return "\n".join(out) + "\n"


def main():
    with open("colors.json") as f:
        spec = json.load(f)
    os.makedirs("mc", exist_ok=True)
    for mode in ("dark", "light"):
        roles = spec["themes"][mode]["roles"]
        for depth, suffix in (("16M", "-16M"), ("256", "256")):
            path = f"mc/{SLUG}-{mode}{suffix}.ini"
            with open(path, "w") as f:
                f.write(render(roles, mode, depth))
            print(path)


if __name__ == "__main__":
    main()
