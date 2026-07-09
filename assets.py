#!/usr/bin/env python3
"""Design reference SVGs for the README, rendered from colors.json.

Three kinds of artifacts under docs/assets/:

- editor-{dark,light}.svg: a code sample in the theme, the README hero
  (picture element switches on the viewer's color scheme);
- palette-{dark,light}.svg: the reference sheet - accents, neutrals,
  diff backgrounds and the ANSI 16 rows with hex labels;
- cvd.svg: gruvbox vs enot accents under simulated dichromacy with the
  measured minimum pairwise dE00 per row - the argument in one image.

The editor and palette sheets carry only specification hexes and are
scanned by check.py (HEX_CHECKED); cvd.svg is exempt - it renders the
gruvbox comparison palette and simulation outputs by design.
"""

import json
import os
from itertools import combinations

from cvd import SIM_FUNCS, de2000, hex_to_lab
from palette import ANSI_ORDER, GRUVBOX, ROLES

OUT = "docs/assets"
HEX_CHECKED = [f"{OUT}/editor-{m}.svg" for m in ("dark", "light")] + \
              [f"{OUT}/palette-{m}.svg" for m in ("dark", "light")]
ASSETS = HEX_CHECKED + [f"{OUT}/cvd.svg"]

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
NEUTRALS = ["bg0", "bg1", "bg2", "bg3", "fg0", "fg1", "comment", "linenr"]
TINTS = ["diff_add_bg", "diff_del_bg", "diff_change_bg", "diff_text_bg"]

# the same code sample the site editor shows; token -> role
LINES = [
    [("# earthy accents: one L*, one C*", "comment")],
    [("from", "red"), (" math ", None), ("import", "red"),
     (" cos, sin, radians", None)],
    [],
    [("def", "red"), (" ", None), ("lch_to_lab", "green"),
     ("(l, c, h):", None)],
    [("    ", None), ('"""CIELAB from cylindrical coordinates."""', "aqua")],
    [("    hr = ", None), ("radians", "blue"), ("(h)", None)],
    [("    ", None), ("return", "red"), (" l, c * ", None),
     ("cos", "blue"), ("(hr), c * ", None), ("sin", "blue"), ("(hr)", None)],
    [],
    [("HUES", "yellow"), (" = {", None), ('"red"', "aqua"), (": ", None),
     ("22", "purple"), (", ", None), ('"green"', "aqua"), (": ", None),
     ("128", "purple"), (", ", None), ('"blue"', "aqua"), (": ", None),
     ("215", "purple"), ("}", None)],
    [],
    [("for", "red"), (" name, hue ", None), ("in", "red"),
     (" HUES.", None), ("items", "blue"), ("():", None)],
    [("    lab = ", None), ("lch_to_lab", "green"), ("(", None),
     ("72.0", "purple"), (", ", None), ("26.0", "purple"),
     (", hue)", None)],
    [("    ", None), ("print", "orange"), ("(", None),
     ('f"lab={lab}"', "aqua"), (")", None)],
]
CURSOR_LINE = 11  # 0-based; gets the bg1 highlight


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(width, height, body, bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">\n'
            f'<rect width="{width}" height="{height}" rx="10" fill="{bg}"/>\n'
            f'{body}</svg>\n')


def text(x, y, content, fill, size=13, anchor="start", weight=None,
         style=None):
    w = f' font-weight="{weight}"' if weight else ""
    s = f' font-style="{style}"' if style else ""
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}"{w}{s} '
            f'xml:space="preserve">{content}</text>\n')


def editor(hexes, mode):
    w, lh, y0 = 640, 22, 30
    parts = []
    if CURSOR_LINE is not None:
        parts.append(f'<rect x="6" y="{y0 + CURSOR_LINE * lh - 15}" '
                     f'width="{w - 12}" height="{lh}" fill="{hexes["bg1"]}"/>\n')
    for i, tokens in enumerate(LINES):
        y = y0 + i * lh
        ln_fill = hexes["fg1"] if i == CURSOR_LINE else hexes["linenr"]
        parts.append(text(34, y, str(i + 1), ln_fill, anchor="end"))
        spans = "".join(
            f'<tspan fill="{hexes[key] if key else hexes["fg0"]}"'
            + (' font-style="italic"' if key == "comment" else "")
            + f'>{esc(txt)}</tspan>'
            for txt, key in tokens)
        if spans:
            parts.append(text(46, y, spans, hexes["fg0"]))
    # statusline with a rounded bottom edge
    sy, sh = y0 + len(LINES) * lh - 8, 28
    parts.append(f'<path d="M0 {sy} h{w} v{sh - 10} a10 10 0 0 1 -10 10 '
                 f'h-{w - 20} a10 10 0 0 1 -10 -10 z" fill="{hexes["bg2"]}"/>\n')
    ty = sy + 18
    parts.append(f'<rect x="0" y="{sy}" width="72" height="{sh}" '
                 f'fill="{hexes["green"]}"/>\n')
    parts.append(text(36, ty, "NORMAL", hexes["bg0"], 12, "middle", 600))
    parts.append(text(84, ty, "palette.py", hexes["fg1"], 12))
    parts.append(text(w - 12, ty, f"utf-8  py  {CURSOR_LINE + 1}:24",
                      hexes["fg1"], 12, "end"))
    return svg(w, sy + sh, "".join(parts), hexes["bg0"])


def swatch_row(hexes, names, x0, y, sw, gap, h, label_of):
    parts = []
    for i, name in enumerate(names):
        x = x0 + i * (sw + gap)
        parts.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{h}" '
                     f'rx="5" fill="{hexes[name]}" '
                     f'stroke="{hexes["bg3"]}" stroke-width="1"/>\n')
        parts.append(text(x + sw / 2, y + h + 15, esc(label_of(name)),
                          hexes["fg0"], 10, "middle"))
        parts.append(text(x + sw / 2, y + h + 27, hexes[name],
                          hexes["fg1"], 9, "middle"))
    return "".join(parts)


def palette_sheet(hexes, ansi, mode):
    w = 640
    parts = [text(24, 30, "accents", hexes["fg1"], 10, weight=600)]
    parts.append(swatch_row(hexes, ROLES, 24, 38, 76, 10, 44, lambda n: n))
    parts.append(text(24, 134, "neutrals", hexes["fg1"], 10, weight=600))
    parts.append(swatch_row(hexes, NEUTRALS, 24, 142, 66, 8, 28,
                            lambda n: n))
    parts.append(text(24, 222, "diff backgrounds", hexes["fg1"], 10,
                      weight=600))
    parts.append(swatch_row(hexes, TINTS, 24, 230, 120, 10, 28,
                            lambda n: n))
    parts.append(text(24, 310, "ansi 16", hexes["fg1"], 10, weight=600))
    amap = {n: ansi[n]["hex"] for n in ansi}
    amap["bg3"] = hexes["bg3"]
    amap["fg0"], amap["fg1"] = hexes["fg0"], hexes["fg1"]
    parts.append(swatch_row(amap, ANSI_ORDER, 24, 318, 66, 8, 24,
                            lambda n: n))
    parts.append(swatch_row(amap, ["br_" + n for n in ANSI_ORDER],
                            24, 386, 66, 8, 24, lambda n: n))
    return svg(w, 454, "".join(parts), hexes["bg0"])


def min_de00(hexes):
    labs = [hex_to_lab(h) for h in hexes]
    return min(de2000(a, b) for a, b in combinations(labs, 2))


def cvd_strip(hexes):
    w = 640
    parts = []
    visions = [("normal vision", None),
               ("protanopia", SIM_FUNCS["protanopia"]),
               ("deuteranopia", SIM_FUNCS["deuteranopia"])]
    rows = [("gruvbox", GRUVBOX["dark"]),
            ("enot", [hexes[r] for r in ROLES])]
    for gi, (label, fn) in enumerate(visions):
        base = 38 + gi * 100
        parts.append(text(24, base, label, hexes["fg1"], 11, weight=600))
        for ri, (name, cols) in enumerate(rows):
            cy = base + 24 + ri * 32
            shown = cols if fn is None else [fn(h) for h in cols]
            parts.append(text(24, cy + 4, name, hexes["fg0"], 12))
            for i, h in enumerate(shown):
                parts.append(f'<circle cx="{118 + i * 32}" cy="{cy}" '
                             f'r="11" fill="{h}" stroke="{hexes["bg3"]}" '
                             f'stroke-width="1"/>\n')
            parts.append(text(w - 24, cy + 4,
                              f"min &#916;E00 {min_de00(shown):.1f}",
                              hexes["fg0"], 12, "end"))
    return svg(w, 336, "".join(parts), hexes["bg0"])


def main():
    with open("colors.json") as f:
        spec = json.load(f)
    os.makedirs(OUT, exist_ok=True)
    for mode in ("dark", "light"):
        th = spec["themes"][mode]
        hexes = {name: e["hex"] for name, e in th["roles"].items()}
        with open(f"{OUT}/editor-{mode}.svg", "w") as f:
            f.write(editor(hexes, mode))
        with open(f"{OUT}/palette-{mode}.svg", "w") as f:
            f.write(palette_sheet(hexes, th["ansi"], mode))
    dark = {n: e["hex"] for n, e in spec["themes"]["dark"]["roles"].items()}
    with open(f"{OUT}/cvd.svg", "w") as f:
        f.write(cvd_strip(dark))
    for path in ASSETS:
        print(path)


if __name__ == "__main__":
    main()
