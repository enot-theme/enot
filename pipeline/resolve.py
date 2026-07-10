#!/usr/bin/env python3
"""Theme color specification: enot.json + flint base -> colors.json.

All enot colors at three depths: hex (16M), xterm-256 index (256),
ANSI slot 0-15 (16). Theme renderers substitute values from here and
contain no color math; the actual per-depth metrics are written to
colors.json, the thresholds live in check.py.

The 256 depth is not quantized naively: the xterm-256 grid is sparse
in the muted earthy region, and nearest colors merge roles down to
dE00 = 0 (light aqua and blue used to fall into the same color23).
Accents and diff backgrounds are solved by the same max-min
optimizer (optimize.solve) over xterm-256 candidates with anchors at
the truecolor LCh values; neutral roles take the nearest color while
preserving contrast to the opposite endpoint. ANSI 16 is stored as
hex + slot index: no consumer needs a 256 approximation of ANSI
(wezterm and vim receive the palette in truecolor, ranger - by
indexes).
"""

import json
from math import atan2, degrees, hypot, inf

from cvd import de2000, hard_min, hex_to_lab
from optimize import (BOUNDS_ACC, BRIGHT_GUARD, C_MIN, CONTRAST_MIN, SECTORS,
                      color_from_hex, contrast, dist, hue_delta, solve)
from palette import ANSI_ORDER, ROLES, SLUG, enot_variant, lch_to_hex

ANSI_SLOTS = ANSI_ORDER + ["br_" + n for n in ANSI_ORDER]
TINTS = ["diff_add_bg", "diff_del_bg", "diff_change_bg", "diff_text_bg"]
COLORED_ANSI = [n for n in ANSI_SLOTS
                if n not in ("black", "br_black", "white", "br_white")]

# 256 candidate tolerances: truecolor corridors widened for the
# sparse grid; no chroma ceiling (candidates with moderate chroma
# are almost absent, the aesthetic pass pulls toward the anchor),
# guard as for bright ANSI - stricter is unattainable on the xterm
# grid together with the sectors; hue sectors get a tolerance: in
# the light theme the orange sector is empty on the grid
ACC_PAD_L = 8
ACC_PAD_H = 12
ACC_C_MIN = 10
TINT_PAD_L = 14
TINT_C_MIN = 4
TINT_HUE_PAD = 40
TINT_BG_GUARD = 4.0    # tint stays distinguishable from the bg ladder
# floor is fixed (slack = inf): a floating floor locked the solution in
# garish colors and kept the aesthetic pass from returning to anchors
FLOOR_ACC256 = 7.0
FLOOR_TINT256 = 3.0


def xterm256():
    levels = [0, 95, 135, 175, 215, 255]
    cols, idx = [], 16
    for r in levels:
        for g in levels:
            for b in levels:
                cols.append((idx, "#%02x%02x%02x" % (r, g, b)))
                idx += 1
    for i in range(24):
        v = 8 + i * 10
        cols.append((232 + i, "#%02x%02x%02x" % (v, v, v)))
    return [(i, h, hex_to_lab(h)) for i, h in cols]


XTERM = xterm256()


def lch_of(lab):
    l, a, b = lab
    return (round(l, 1), round(hypot(a, b), 1),
            round(degrees(atan2(b, a)) % 360, 1))


def in_sector(h, sector, pad):
    lo, hi = sector[0] - pad, sector[1] + pad
    return lo <= h <= hi or h + 360 <= hi or h - 360 >= lo


def nearest(hexval, keep_contrast_to=None):
    cands = XTERM
    if keep_contrast_to:
        cands = [x for x in XTERM
                 if contrast(x[1], keep_contrast_to) >= CONTRAST_MIN]
    lab = hex_to_lab(hexval)
    return min(cands, key=lambda x: de2000(lab, x[2]))


def xterm_cands(l_range, c_min, hue_ok, contrast_to, guards, guard_min):
    out = []
    for i, h, lab in XTERM:
        lch = lch_of(lab)
        l, c, hue = lch
        if not (l_range[0] <= l <= l_range[1] and c >= c_min
                and hue_ok(hue)):
            continue
        if contrast(h, contrast_to) < CONTRAST_MIN:
            continue
        col = color_from_hex(h, lch)
        if any(dist(col, g) < guard_min for g in guards):
            continue
        col["c256"] = i
        out.append(col)
    return out


def tints(v, mode):
    """Diff backgrounds: accent hues at a soft lightness."""
    dark = mode == "dark"
    hue = {r: v[mode]["_lch"][r][2] for r in ("red", "green", "blue")}
    soft = 26 if dark else 90
    lch = {
        "diff_add_bg": (soft, 10, hue["green"]),
        # del darkened: the add/del pair separates on lightness (survives
        # dichromacy) instead of the red-green hue axis deuteranopia collapses
        "diff_del_bg": (soft - 6, 10, hue["red"]),
        "diff_change_bg": (soft, 8, hue["blue"]),
        "diff_text_bg": (32 if dark else 84, 14, hue["blue"]),
    }
    return {n: lch_to_hex(*p) for n, p in lch.items()}, lch


def theme_spec(v, mode):
    t = {k: val for k, val in v[mode].items() if not k.startswith("_")}
    tint_hex, tint_lch = tints(v, mode)
    t.update(tint_hex)

    def entry(hexval, counter=None, counter_q=None):
        keep = counter_q if (
            counter and contrast(hexval, counter) >= CONTRAST_MIN) else None
        i, h, _ = nearest(hexval, keep)
        return {"hex": hexval, "c256": i, "c256hex": h}

    # neutral roles: the anchor endpoints, then the bg ladder toward fg0
    roles = {"bg0": entry(t["bg0"])}
    bg0q = roles["bg0"]["c256hex"]
    roles["fg0"] = entry(t["fg0"], t["bg0"], bg0q)
    fg0q = roles["fg0"]["c256hex"]
    for name in ("fg1", "comment", "linenr"):
        roles[name] = entry(t[name], t["bg0"], bg0q)
    for name in ("bg1", "bg2", "bg3"):
        roles[name] = entry(t[name], t["fg0"], fg0q)

    # 256 accents: max-min across three visions, anchors are truecolor LCh
    guards = [color_from_hex(fg0q), color_from_hex(roles["comment"]["c256hex"])]
    l_lo, l_hi, _ = BOUNDS_ACC[mode]["l"]
    cands = {r: xterm_cands(
        (l_lo - ACC_PAD_L, l_hi + ACC_PAD_L),
        max(ACC_C_MIN, C_MIN.get(r) or 0),
        lambda h, s=SECTORS[r]: in_sector(h, s, ACC_PAD_H),
        bg0q, guards, BRIGHT_GUARD) for r in ROLES}
    chosen = solve(cands, {r: tuple(v[mode]["_lch"][r]) for r in ROLES},
                   FLOOR_ACC256, "red", slack=inf)
    for r in ROLES:
        roles[r] = {"hex": t[r], "c256": chosen[r]["c256"],
                    "c256hex": chosen[r]["hex"]}

    # 256 tints: distinguishable from each other and from the backgrounds
    bg_guards = [color_from_hex(roles[n]["c256hex"]) for n in ("bg1", "bg2")]
    tcands = {n: xterm_cands(
        (tint_lch[n][0] - TINT_PAD_L, tint_lch[n][0] + TINT_PAD_L),
        TINT_C_MIN,
        lambda h, h0=tint_lch[n][2]: hue_delta(h, h0) <= TINT_HUE_PAD,
        fg0q, bg_guards, TINT_BG_GUARD) for n in TINTS}
    tchosen = solve(tcands, tint_lch, FLOOR_TINT256, "diff_add_bg",
                    slack=inf)
    for n in TINTS:
        roles[n] = {"hex": t[n], "c256": tchosen[n]["c256"],
                    "c256hex": tchosen[n]["hex"]}

    ansi = {n: {"hex": v["ansi"][mode][n], "index": i}
            for i, n in enumerate(ANSI_SLOTS)}
    return {"roles": roles, "ansi": ansi}


def theme_metrics(th, mode):
    roles, ansi = th["roles"], th["ansi"]

    def hard_guard(names, source, key, fg, comment):
        cols = [color_from_hex(source[n][key]) for n in names]
        gs = [color_from_hex(fg), color_from_hex(comment)]
        return min(dist(c, g) for c in cols for g in gs)

    def block(key, with_ansi):
        accents = {r: roles[r][key] for r in ROLES}
        tint_map = {n: roles[n][key] for n in TINTS}
        pairs = ([(roles[r][key], roles["bg0"][key])
                  for r in ["fg0", "fg1"] + ROLES]
                 + [(roles["fg0"][key], roles[n][key]) for n in TINTS])
        out = {
            "accents": round(hard_min(accents)[0], 2),
            "tints": round(hard_min(tint_map, TINTS)[0], 2),
            "guard_accents": round(hard_guard(
                ROLES, roles, key, roles["fg0"][key],
                roles["comment"][key]), 2),
            "red_chroma": round(lch_of(hex_to_lab(roles["red"][key]))[1], 1),
        }
        if with_ansi:
            amap = {n: ansi[n]["hex"] for n in ANSI_SLOTS}
            pairs += [(ansi[n]["hex"], roles["bg0"][key])
                      for n in COLORED_ANSI]
            out["ansi16"] = round(hard_min(amap, ANSI_SLOTS)[0], 2)
            for tier, names in (("normal", ANSI_ORDER),
                                ("bright", ["br_" + n for n in ANSI_ORDER])):
                colored = [n for n in names if n in COLORED_ANSI]
                out["guard_ansi_" + tier] = round(hard_guard(
                    colored, ansi, "hex", roles["fg0"]["hex"],
                    roles["comment"]["hex"]), 2)
            # lightness tiers: in light theme bright are darker than normal
            levels = {n: hex_to_lab(ansi[n]["hex"])[0]
                      for n in COLORED_ANSI}
            normal = [levels[n] for n in ANSI_ORDER if n in levels]
            bright = [v for n, v in levels.items() if n.startswith("br_")]
            out["ansi_tier_gap"] = round(
                min(bright) - max(normal) if mode == "dark"
                else min(normal) - max(bright), 1)
        out["contrast"] = round(min(contrast(a, b) for a, b in pairs), 2)
        return out

    m = {"16M": block("hex", True), "256": block("c256hex", False)}
    m["256"]["drift_max"] = round(max(
        de2000(hex_to_lab(e["hex"]), hex_to_lab(e["c256hex"]))
        for e in roles.values()), 2)
    return m


def main():
    v = enot_variant()
    spec = {"slug": SLUG,
            "comment": "enot color specification; generated by resolve.py",
            "themes": {}, "metrics": {}}
    for mode in ("dark", "light"):
        spec["themes"][mode] = theme_spec(v, mode)
        spec["metrics"][mode] = theme_metrics(spec["themes"][mode], mode)
    with open("colors.json", "w") as f:
        json.dump(spec, f, ensure_ascii=False, indent=1)
    for mode, m in spec["metrics"].items():
        print(f"colors.json {mode}: " + "; ".join(
            f"{d}: accents {x['accents']}, tints {x['tints']}, "
            f"contrast {x['contrast']}" for d, x in m.items()))


if __name__ == "__main__":
    main()
