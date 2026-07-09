#!/usr/bin/env python3
"""Check the palettes for robustness to color vision deficiencies.

Dichromacy: Vienot 1999 for protan/deutan, Brettel 1997 for tritan
(per the daltonlens.org review, Machado 2009 is fine for anomalous
trichromacy but is not the best choice for full dichromacy). Matrices
in linear sRGB are taken from libDaltonLens (public domain).
Distinguishability - pairwise CIEDE2000 after simulation.

Run: cvd.html report + summary to stdout. The regression lives in
check.py and works off colors.json; tritanopia is not hard-constrained,
it is only shown in the report.
"""

import json
from math import atan2, cos, degrees, exp, hypot, radians, sin, sqrt

from palette import CSS, EDITOR, JS, ROLES, css_vars, lch_to_hex, swatch

REPORT_SLUGS = ["pepel", "kremen", "enot"]
CRIT, RISK = 8.0, 15.0   # dE00: below CRIT pairs merge, below RISK borderline
ANSI_ORDER = ["black", "red", "green", "yellow",
              "blue", "magenta", "cyan", "white"]

VIENOT = {
    "protanopia": [
        [0.11238, 0.88762, 0.00000],
        [0.11238, 0.88762, -0.00000],
        [0.00401, -0.00401, 1.00000],
    ],
    "deuteranopia": [
        [0.29275, 0.70725, 0.00000],
        [0.29275, 0.70725, -0.00000],
        [-0.02234, 0.02234, 1.00000],
    ],
}

# Brettel 1997: two projection half-planes separated by the plane n.
BRETTEL_TRITAN = {
    "m1": [[1.01277, 0.13548, -0.14826],
           [-0.01243, 0.86812, 0.14431],
           [0.07589, 0.80500, 0.11911]],
    "m2": [[0.93678, 0.18979, -0.12657],
           [0.06154, 0.81526, 0.12320],
           [-0.37562, 1.12767, 0.24796]],
    "n": [0.03901, -0.02788, -0.01113],
}


# --------------------------------------------------------------- color

def hex_to_linear(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))

    def inv(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return [inv(r), inv(g), inv(b)]


def linear_to_hex(rgb):
    def gamma(c):
        c = max(0.0, min(1.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

    return "#%02x%02x%02x" % tuple(round(gamma(c) * 255) for c in rgb)


def apply_matrix(rgb, m):
    return [sum(m[i][j] * rgb[j] for j in range(3)) for i in range(3)]


def simulate(h, m):
    return linear_to_hex(apply_matrix(hex_to_linear(h), m))


def simulate_tritan(h):
    rgb = hex_to_linear(h)
    n = BRETTEL_TRITAN["n"]
    side = sum(a * b for a, b in zip(rgb, n))
    m = BRETTEL_TRITAN["m1"] if side >= 0 else BRETTEL_TRITAN["m2"]
    return linear_to_hex(apply_matrix(rgb, m))


SIM_FUNCS = {
    "protanopia": lambda h: simulate(h, VIENOT["protanopia"]),
    "deuteranopia": lambda h: simulate(h, VIENOT["deuteranopia"]),
    "tritanopia": simulate_tritan,
}
HARD = ("protanopia", "deuteranopia")  # tritan only in the report


def hex_to_lab(h):
    r, g, b = hex_to_linear(h)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) * 100 / 95.047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) * 100 / 100.0
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) * 100 / 108.883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def de2000(lab1, lab2):
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c1, c2 = hypot(a1, b1), hypot(a2, b2)
    g = 0.5 * (1 - sqrt(((c1 + c2) / 2) ** 7 / (((c1 + c2) / 2) ** 7 + 25 ** 7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = hypot(a1p, b1), hypot(a2p, b2)
    h1p = degrees(atan2(b1, a1p)) % 360
    h2p = degrees(atan2(b2, a2p)) % 360
    dlp, dcp = l2 - l1, c2p - c1p
    if c1p * c2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dbig_hp = 2 * sqrt(c1p * c2p) * sin(radians(dhp / 2))
    lpm, cpm = (l1 + l2) / 2, (c1p + c2p) / 2
    if c1p * c2p == 0:
        hpm = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hpm = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hpm = (h1p + h2p + 360) / 2
    else:
        hpm = (h1p + h2p - 360) / 2
    t = (1 - 0.17 * cos(radians(hpm - 30)) + 0.24 * cos(radians(2 * hpm))
         + 0.32 * cos(radians(3 * hpm + 6)) - 0.20 * cos(radians(4 * hpm - 63)))
    dtheta = 30 * exp(-(((hpm - 275) / 25) ** 2))
    rc = 2 * sqrt(cpm ** 7 / (cpm ** 7 + 25 ** 7))
    sl = 1 + 0.015 * (lpm - 50) ** 2 / sqrt(20 + (lpm - 50) ** 2)
    sc = 1 + 0.045 * cpm
    sh = 1 + 0.015 * cpm * t
    rt = -sin(radians(2 * dtheta)) * rc
    return sqrt((dlp / sl) ** 2 + (dcp / sc) ** 2 + (dbig_hp / sh) ** 2
                + rt * (dcp / sc) * (dbig_hp / sh))


# -------------------------------------------------------------- report

def sim_theme(theme, fn):
    return {k: fn(v) for k, v in theme.items() if not k.startswith("_")}


def accent_pairs(theme, names=None):
    """All color pairs with their dE00, ascending."""
    names = names or ROLES
    labs = {r: hex_to_lab(theme[r]) for r in names}
    pairs = []
    for i, r1 in enumerate(names):
        for r2 in names[i + 1:]:
            pairs.append((de2000(labs[r1], labs[r2]), r1, r2))
    return sorted(pairs)


def hard_min(theme, names=None):
    """Minimum dE00 over normal vision and the hard simulations."""
    worst = accent_pairs(theme, names)[0]
    for name in HARD:
        p = accent_pairs(sim_theme(theme, SIM_FUNCS[name]), names)[0]
        if p[0] < worst[0]:
            worst = p
    return worst


def flags_html(pairs, limit=6):
    crit = [p for p in pairs if p[0] < CRIT]
    risk = [p for p in pairs if CRIT <= p[0] < RISK]
    parts = []
    if crit:
        parts.append("merging: " + ", ".join(
            f"{r1}-{r2} {d:.1f}" for d, r1, r2 in crit))
    if risk:
        head = ", ".join(f"{r1}-{r2} {d:.1f}" for d, r1, r2 in risk[:limit])
        tail = f" and {len(risk) - limit} more" if len(risk) > limit else ""
        parts.append("borderline: " + head + tail)
    if not parts:
        d, r1, r2 = pairs[0]
        parts.append(f"all pairs distinguishable, minimum {r1}-{r2} {d:.1f}")
    return "<br>".join(parts)


def panel(title, theme, pairs):
    sw = "".join(swatch(theme[r], r) for r in ROLES)
    return (f'<div class="pane"><div class="eyebrow">{title}</div>'
            f'<div style="{css_vars(theme)}">{EDITOR}'
            f'<div class="swatches"><div class="swrow">{sw}</div></div>'
            f'</div><div class="flags">{flags_html(pairs)}</div></div>')


def theme_block(label, theme):
    panels = [panel("normal", theme, accent_pairs(theme))]
    for sim_name, fn in SIM_FUNCS.items():
        st = sim_theme(theme, fn)
        panels.append(panel(sim_name, st, accent_pairs(st)))
    return (f'<h3 class="thlabel">{label}</h3>'
            f'<div class="panes cvd">{"".join(panels)}</div>')


def ansi_rows(amap):
    row1 = "".join(swatch(amap[n], n) for n in ANSI_ORDER)
    row2 = "".join(swatch(amap["br_" + n], "br_" + n) for n in ANSI_ORDER)
    return (f'<div class="swatches"><div class="swrow small">{row1}</div>'
            f'<div class="swrow small">{row2}</div></div>')


def ansi_block(label, amap):
    names = list(amap)
    panels = []
    for sim_name in ("normal",) + tuple(SIM_FUNCS):
        m = amap if sim_name == "normal" else {
            k: SIM_FUNCS[sim_name](v) for k, v in amap.items()}
        pairs = accent_pairs(m, names)
        panels.append(f'<div class="pane"><div class="eyebrow">{sim_name}'
                      f'</div>{ansi_rows(m)}'
                      f'<div class="flags">{flags_html(pairs)}</div></div>')
    return (f'<h3 class="thlabel">{label} · ansi 16</h3>'
            f'<div class="panes cvd">{"".join(panels)}</div>')


def variant_block(v):
    html = (f'<section class="variant" id="{v["slug"]}"><div class="vhead">'
            f'<div><h2>{v["name"]}</h2><div class="desc">{v["desc"]}</div>'
            f'</div></div>'
            + theme_block("dark", v["dark"])
            + theme_block("light", v["light"]))
    if v.get("ansi"):
        html += (ansi_block("dark", v["ansi"]["dark"])
                 + ansi_block("light", v["ansi"]["light"]))
    return html + '</section>'


EXTRA_CSS = """
.thlabel {
  font-size: 12px; font-weight: 600; letter-spacing: .24em;
  text-transform: uppercase; margin: 26px 0 10px;
}
.panes.cvd { row-gap: 26px; }
.flags { font-size: 11px; line-height: 1.5; margin-top: 8px; opacity: .85; }
"""


def page(variants):
    chrome = {
        "page_bg": lch_to_hex(42, 1, 90),
        "page_text": lch_to_hex(92, 2, 90),
        "page_dim": lch_to_hex(74, 2, 90),
        "page_faint": lch_to_hex(54, 1.5, 90),
    }
    body = "".join(variant_block(v) for v in variants)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>color vision deficiencies</title>
<style>{CSS.substitute(chrome)}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>color vision</h1>
  <div class="sub">palettes under dichromacy</div>
  <div class="method">
    models: Vienot 1999 (protanopia, deuteranopia) and Brettel 1997
    (tritanopia), libDaltonLens matrices, linear sRGB.
    metric: pairwise CIEDE2000 between the seven accents after simulation.
    thresholds: dE00 &lt; {CRIT:.0f} - <b>merging</b>,
    {CRIT:.0f}-{RISK:.0f} - borderline, above - distinguishable.
    tritanopia is extremely rare and is not part of the hard constraints.
  </div>
</header>
{body}
<footer>generated by cvd.py from palettes.json</footer>
</div>
<script>{JS}</script>
</body>
</html>"""


def clean(theme):
    return {k: v for k, v in theme.items() if not k.startswith("_")}


def report(variants):
    with open("cvd.html", "w") as f:
        f.write(page(variants))
    for v in variants:
        print(v["name"])
        for mode in ("dark", "light"):
            theme = clean(v[mode])
            for sim_name in ("normal",) + tuple(SIM_FUNCS):
                t = theme if sim_name == "normal" else sim_theme(
                    theme, SIM_FUNCS[sim_name])
                pairs = accent_pairs(t)
                bad = [p for p in pairs if p[0] < RISK]
                worst = "; ".join(f"{r1}-{r2} {d:.1f}" for d, r1, r2 in bad)
                d, r1, r2 = pairs[0]
                print(f"  {mode:5} {sim_name:13} min {r1}-{r2} {d:5.1f}"
                      f"  {'issues: ' + worst if bad else 'ok'}")



def main():
    with open("palettes.json") as f:
        data = json.load(f)
    order = {s: i for i, s in enumerate(REPORT_SLUGS)}
    variants = sorted((v for v in data if v["slug"] in order),
                      key=lambda v: order[v["slug"]])
    report(variants)


if __name__ == "__main__":
    main()
