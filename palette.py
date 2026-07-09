#!/usr/bin/env python3
"""Color math in CIELAB and the enot theme assembly.

Shared constants (roles, ANSI order, slug), LCh -> sRGB conversion
with gamut clamping, the "flint" base (fixed lightness steps for
backgrounds and text) and enot_variant(), which assembles the theme
from the optimizer output enot.json. The exploratory palette variants
and HTML previews were removed; they live in git history.
"""

import json
from math import cos, radians, sin

# --------------------------------------------------------------- color

D65 = (95.047, 100.0, 108.883)


def lch_to_lab(l, c, h):
    hr = radians(h)
    return l, c * cos(hr), c * sin(hr)


def lab_to_xyz(l, a, b):
    fy = (l + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200

    def finv(t):
        t3 = t ** 3
        return t3 if t3 > 0.008856 else (t - 16 / 116) / 7.787

    return D65[0] * finv(fx), D65[1] * finv(fy), D65[2] * finv(fz)


def xyz_to_srgb(x, y, z):
    x, y, z = x / 100, y / 100, z / 100
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    b = 0.0557 * x - 0.2040 * y + 1.0570 * z

    def gamma(c):
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

    return tuple(gamma(c) for c in (r, g, b))


def in_gamut(rgb, eps=1e-4):
    return all(-eps <= c <= 1 + eps for c in rgb)


def lch_to_hex(l, c, h):
    """sRGB hex; when out of gamut, chroma is reduced via binary search."""
    rgb = xyz_to_srgb(*lab_to_xyz(*lch_to_lab(l, c, h)))
    if not in_gamut(rgb):
        lo, hi = 0.0, c
        for _ in range(24):
            mid = (lo + hi) / 2
            if in_gamut(xyz_to_srgb(*lab_to_xyz(*lch_to_lab(l, mid, h)))):
                lo = mid
            else:
                hi = mid
        rgb = xyz_to_srgb(*lab_to_xyz(*lch_to_lab(l, lo, h)))
    return "#%02x%02x%02x" % tuple(
        round(max(0.0, min(1.0, ch)) * 255) for ch in rgb
    )


# ------------------------------------------------------------ the theme

SLUG = "enot"
ROLES = ["red", "orange", "yellow", "green", "aqua", "blue", "purple"]
NEUTRAL_ROLES = ["bg0", "bg1", "bg2", "bg3", "fg0", "fg1", "comment", "linenr"]
ANSI_ORDER = ["black", "red", "green", "yellow",
              "blue", "magenta", "cyan", "white"]

# comparison palette for the vision demos: the bright row of gruvbox
# dark and the normal row of gruvbox light, same seven role order
GRUVBOX = {
    "dark": ["#fb4934", "#fe8019", "#fabd2f", "#b8bb26",
             "#8ec07c", "#83a598", "#d3869b"],
    "light": ["#cc241d", "#d65d0e", "#d79921", "#98971a",
              "#689d6a", "#458588", "#b16286"],
}

# the "flint" base: gruvbox on neutral stone - gray backgrounds like
# #282828, warm text, the highest accent chroma. Backgrounds and text
# are fixed L* steps; the accents' (L, C, h) come from the optimizer.
BASE = {
    "hues": {"red": 32, "orange": 55, "yellow": 84, "green": 105,
             "aqua": 140, "blue": 215, "purple": 352},
    "mult": {"aqua": 0.95, "blue": 0.8, "purple": 0.95},
    "dark": {"bg": (16, 1.0, 85), "fg": (86, 18, 95), "acc": (70, 32)},
    "light": {"bg": (95.5, 2.0, 90), "fg": (29, 4, 80), "acc": (44, 38)},
}


def build_theme(spec, hues, mult, dark):
    bgL, bgC, bgH = spec["bg"]
    fgL, fgC, fgH = spec["fg"]
    sign = 1 if dark else -1
    t = {
        "bg0": lch_to_hex(bgL, bgC, bgH),
        "bg1": lch_to_hex(bgL + sign * 4.5, bgC, bgH),
        "bg2": lch_to_hex(bgL + sign * 10, bgC, bgH),
        "bg3": lch_to_hex(bgL + sign * 17, bgC, bgH),
        "fg0": lch_to_hex(fgL, fgC, fgH),
        "fg1": lch_to_hex(fgL - sign * 12, fgC * 0.8, fgH),
        "comment": lch_to_hex(54 if dark else 63, min(bgC * 1.6, 7), bgH),
        "linenr": lch_to_hex(40 if dark else 72, min(bgC * 1.4, 6), bgH),
    }
    lch = {}
    if "accents" in spec:
        # per-role (L, C, h) - optimizer output, there is no ring
        for role in ROLES:
            l, c, h = spec["accents"][role]
            t[role] = lch_to_hex(l, c, h)
            lch[role] = (round(l, 1), round(c, 1), round(h, 1))
    else:
        accL, accC = spec["acc"]
        for role in ROLES:
            c = accC * mult.get(role, 1.0)
            t[role] = lch_to_hex(accL, c, hues[role])
            lch[role] = (accL, round(c, 1), hues[role])
    t["_lch"] = lch
    t["_meta"] = {"bg": spec["bg"], "fg": spec["fg"],
                  "acc": None if "accents" in spec else spec.get("acc")}
    return t


def enot_variant():
    """The enot theme from enot.json (written by optimize.py)."""
    with open("enot.json") as f:
        acc = json.load(f)
    return {
        "dark": build_theme({**BASE["dark"], "accents": acc["accents"]["dark"]},
                            BASE["hues"], {}, True),
        "light": build_theme({**BASE["light"],
                              "accents": acc["accents"]["light"]},
                             BASE["hues"], {}, False),
        "ansi": {mode: {name: lch_to_hex(*lch)
                        for name, lch in acc["ansi"][mode].items()}
                 for mode in ("dark", "light")},
    }
