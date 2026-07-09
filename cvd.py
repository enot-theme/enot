#!/usr/bin/env python3
"""Dichromacy simulation and the perceptual difference metric.

Vienot 1999 for protan/deutan, Brettel 1997 for tritan (per the
daltonlens.org review, Machado 2009 is fine for anomalous trichromacy
but is not the best choice for full dichromacy). Matrices in linear
sRGB are taken from libDaltonLens (public domain). Distinguishability
is pairwise CIEDE2000 after simulation.

Consumed by optimize.py (the max-min objective), resolve.py (metrics
at every depth) and sitedata.py (precomputed vision sets for the site
switcher). Tritanopia is not a hard constraint (project decision):
HARD lists the simulations the guarantees are enforced against.
"""

from math import atan2, cos, degrees, exp, hypot, radians, sin, sqrt

from palette import ROLES

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
HARD = ("protanopia", "deuteranopia")  # tritan is not enforced


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


# ------------------------------------------------------------- metrics

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
