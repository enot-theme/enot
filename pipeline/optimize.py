#!/usr/bin/env python3
"""enot palette optimizer: "flint" base, robust to dichromacy.

Two sets per theme: 7 syntax accents (vim) and 16 ANSI slots
(wezterm). Maximizes the minimum pairwise CIEDE2000 across three
visions: normal, protanopia and deuteranopia (Vienot 1999);
tritanopia is not a hard constraint (project decision) and is
printed for reference only.

Constraints: gruvbox hue sectors, lightness corridors (normal and
bright ANSI colors are kept in non-overlapping tiers - the family is
recognized by lightness, which dichromacy does not affect), sRGB
gamut, contrast against the background, separation from fg/comment,
chroma minimums for salient roles. After maximization - an aesthetic
pass: roles return to the gruvbox anchors within the slack of the
bottleneck.

Method: greedy farthest-point + coordinate ascent on a grid.
Output: enot.json, consumed via palette.enot_variant().
"""

import json
from palette import (BASE, ROLES, lch_to_lab, lab_to_xyz, xyz_to_srgb,
                     in_gamut, lch_to_hex, build_theme)
from cvd import (SIM_FUNCS, HARD, hex_to_lab, hex_to_linear, de2000,
                 accent_pairs)

CONTRAST_MIN = 4.5
NEUTRAL_MIN = 10.0   # dE00 to fg0 and comment: tokens do not merge with text
BRIGHT_GUARD = 6.5   # strict guard is unattainable for bright ANSI: pink
                     # under deutan is inevitably close to the warm beige fg
FLOOR_ACC = 8.2      # lower bound of the aesthetic-pass floor, 7 accents
FLOOR_ANSI = 7.2     # same for the 16 ANSI slots (a denser problem)
H_STEP = 3

# hue sectors: gruvbox role recognizability is preserved
SECTORS = {
    "red": (20, 45), "orange": (50, 72), "yellow": (78, 98),
    "green": (100, 135), "aqua": (140, 200), "blue": (210, 255),
    "purple": (320, 358),
}
ANSI_SECTORS = {
    "red": (20, 45), "yellow": (78, 98), "green": (100, 135),
    "cyan": (140, 200), "blue": (210, 255), "magenta": (320, 358),
}
ANSI_HUE_ANCHOR = {"red": 32, "yellow": 84, "green": 105,
                   "cyan": 140, "blue": 215, "magenta": 352}

BOUNDS_ACC = {
    "dark": {"l": (62, 82, 2), "c": (14, 32, 2)},
    "light": {"l": (32, 46, 2), "c": (18, 38, 2)},
}
# ANSI: non-overlapping L* tiers; in the light theme bright colors are
# darker than normal ones (as in the original gruvbox light)
ANSI_L = {
    "dark": {"normal": (60, 72, 2), "bright": (76, 90, 2)},
    "light": {"normal": (38, 46, 2), "bright": (22, 34, 2)},
}
ANSI_C = {
    "dark": {"normal": (14, 32, 2), "bright": (14, 36, 2)},
    "light": {"normal": (16, 38, 2), "bright": (16, 38, 2)},
}
# neutral slots: (L range, C range), hue matches the background
NEUTRALS = {
    "dark": {"black": ((24, 34, 2), (0, 4, 2)),
             "br_black": ((42, 54, 2), (0, 4, 2)),
             "white": ((74, 84, 2), (2, 10, 2)),
             "br_white": ((90, 96, 2), (0, 6, 2))},
    "light": {"black": ((20, 30, 2), (0, 4, 2)),
              "br_black": ((40, 52, 2), (0, 4, 2)),
              "white": ((76, 86, 2), (2, 8, 2)),
              "br_white": ((90, 96, 2), (0, 4, 2))},
}
NEUTRAL_ANCHORS = {
    "dark": {"black": (28, 4, 85), "br_black": (46, 2, 85),
             "white": (78, 6, 85), "br_white": (94, 2, 85)},
    "light": {"black": (24, 3, 85), "br_black": (46, 3, 85),
              "white": (81, 5, 85), "br_white": (94, 1, 85)},
}
# red is the diagnostics color and must stay salient; bright red
# gets by with less: it is a highlight, not a diagnostic
C_MIN = {"red": 22, "br_red": 18}


# -------------------------------------------------------- primitives

def srange(lo, hi, step):
    v = lo
    while v <= hi + 1e-9:
        yield round(v, 1)
        v += step


def luminance(hexval):
    r, g, b = hex_to_linear(hexval)
    return 0.2126729 * r + 0.7151522 * g + 0.0721750 * b


def contrast(h1, h2):
    y1, y2 = sorted((luminance(h1), luminance(h2)), reverse=True)
    return (y1 + 0.05) / (y2 + 0.05)


def color_from_hex(hexval, lch=None):
    labs = [hex_to_lab(hexval)]
    for name in HARD:
        labs.append(hex_to_lab(SIM_FUNCS[name](hexval)))
    return {"lch": lch, "hex": hexval, "labs": labs}


def make_color(l, c, h):
    return color_from_hex(lch_to_hex(l, c, h), (l, c, h))


def dist(c1, c2):
    return min(de2000(a, b) for a, b in zip(c1["labs"], c2["labs"]))


def hue_delta(h1, h2):
    d = abs(h1 - h2) % 360
    return min(d, 360 - d)


def penalty(anchor, c):
    l, cc, h = c["lch"]
    l0, c0, h0 = anchor
    return hue_delta(h, h0) * 0.8 + abs(cc - c0) * 1.0 + abs(l - l0) * 0.3


def min_pairwise(chosen):
    cols = list(chosen.values())
    return min(dist(a, b) for i, a in enumerate(cols) for b in cols[i + 1:])


# ------------------------------------------------------------- solver

def slot_candidates(spec, bg, guards):
    lo, hi = spec["h"]
    c_lo = max(spec["c"][0], spec.get("c_min") or 0)
    guard_min = spec.get("guard") or 0
    out = []
    for l in srange(*spec["l"]):
        for c in srange(c_lo, spec["c"][1], spec["c"][2]):
            for h in srange(lo, hi, H_STEP):
                if not in_gamut(xyz_to_srgb(*lab_to_xyz(*lch_to_lab(l, c, h)))):
                    continue
                col = make_color(l, c, h)
                if spec.get("contrast") and \
                        contrast(col["hex"], bg) < spec["contrast"]:
                    continue
                if guard_min and \
                        any(dist(col, g) < guard_min for g in guards):
                    continue
                out.append(col)
    return out


def build_candidates(specs, bg, guards):
    cands = {}
    for name, sp in specs.items():
        cands[name] = slot_candidates(sp, bg, guards)
    return cands


def solve(cands, anchors, floor_min, seed, slack=1.5):
    for name, cs in cands.items():
        if not cs:
            raise SystemExit(f"{name}: empty candidate set")
    names = list(cands)

    def ascent_from(seed_name):
        # greedy start: seed closest to its anchor, the rest by maximin
        chosen = {seed_name: min(cands[seed_name],
                                 key=lambda c: penalty(anchors[seed_name], c))}
        for name in names:
            if name in chosen:
                continue
            chosen[name] = max(
                cands[name],
                key=lambda c: min(dist(c, x) for x in chosen.values()))
        # coordinate ascent until it stabilizes
        improved = True
        while improved:
            improved = False
            for name in names:
                rest = [c for n, c in chosen.items() if n != name]
                cur = min(dist(chosen[name], x) for x in rest)
                best = max(cands[name],
                           key=lambda c: min(dist(c, x) for x in rest))
                if min(dist(best, x) for x in rest) > cur + 1e-6:
                    chosen[name] = best
                    improved = True
        return chosen

    # multistart: local optima depend on the seed, take the best
    seeds = dict.fromkeys([seed, names[len(names) // 2], names[-1]])
    chosen = max((ascent_from(s) for s in seeds), key=min_pairwise)
    # aesthetic pass: floor slightly below the achieved maximin -
    # a small robustness concession in exchange for character; with
    # slack = inf the floor is fixed and character takes the maximum
    floor = max(floor_min, min_pairwise(chosen) - slack)
    for _ in range(3):
        changed = False
        for name in names:
            rest = [c for n, c in chosen.items() if n != name]
            ok = [c for c in cands[name]
                  if min(dist(c, x) for x in rest) >= floor]
            best = min(ok or [chosen[name]],
                       key=lambda c: penalty(anchors[name], c))
            if best["lch"] != chosen[name]["lch"]:
                chosen[name] = best
                changed = True
        if not changed:
            break
    return chosen


# --------------------------------------------------- specifications

def accent_specs(mode):
    b = BOUNDS_ACC[mode]
    return {role: {"l": b["l"], "c": b["c"], "h": SECTORS[role],
                   "contrast": CONTRAST_MIN, "guard": NEUTRAL_MIN,
                   "c_min": C_MIN.get(role)}
            for role in ROLES}


def accent_anchors(base, mode):
    accL, accC = base[mode]["acc"]
    return {r: (accL, accC * base["mult"].get(r, 1.0), base["hues"][r])
            for r in ROLES}


def ansi_specs(mode):
    specs = {}
    for tier in ("normal", "bright"):
        prefix = "" if tier == "normal" else "br_"
        guard = NEUTRAL_MIN if tier == "normal" else BRIGHT_GUARD
        for name, sector in ANSI_SECTORS.items():
            slot = prefix + name
            specs[slot] = {"l": ANSI_L[mode][tier], "c": ANSI_C[mode][tier],
                           "h": sector, "contrast": CONTRAST_MIN,
                           "guard": guard, "c_min": C_MIN.get(slot)}
    for name, (lr, cr) in NEUTRALS[mode].items():
        specs[name] = {"l": lr, "c": cr, "h": (85, 85)}
    return specs


def ansi_anchors(mode):
    anchors = {}
    if mode == "dark":
        tiers = {"normal": (66, 30), "bright": (84, 32)}
    else:
        tiers = {"normal": (44, 34), "bright": (30, 34)}
    for tier, (l0, c0) in tiers.items():
        prefix = "" if tier == "normal" else "br_"
        for name, h0 in ANSI_HUE_ANCHOR.items():
            anchors[prefix + name] = (l0, c0, h0)
    anchors.update(NEUTRAL_ANCHORS[mode])
    return anchors


# ------------------------------------------------------------- output

def report_chosen(tag, chosen, bg):
    print(f"{tag}: min dE00 (normal/protan/deutan) = "
          f"{min_pairwise(chosen):.1f}")
    tri = accent_pairs({n: SIM_FUNCS["tritanopia"](c["hex"])
                        for n, c in chosen.items()}, list(chosen))
    print(f"  tritanopia (for reference): min {tri[0][1]}-{tri[0][2]} "
          f"{tri[0][0]:.1f}")
    for name, col in chosen.items():
        l, c, h = col["lch"]
        print(f"  {name:10} L{l:5.1f} C{c:5.1f} h{h:5.1f}  {col['hex']}"
              f"  contrast {contrast(col['hex'], bg):.1f}:1")


def main():
    base = BASE
    result = {"accents": {}, "ansi": {}}
    for mode in ("dark", "light"):
        theme = build_theme(base[mode], base["hues"], base["mult"],
                            mode == "dark")
        bg = theme["bg0"]
        guards = [color_from_hex(theme["fg0"]),
                  color_from_hex(theme["comment"])]
        chosen = solve(build_candidates(accent_specs(mode), bg, guards),
                       accent_anchors(base, mode), FLOOR_ACC, "red")
        result["accents"][mode] = {r: list(chosen[r]["lch"]) for r in ROLES}
        report_chosen(f"{mode} accents", chosen, bg)
        chosen16 = solve(build_candidates(ansi_specs(mode), bg, guards),
                         ansi_anchors(mode), FLOOR_ANSI, "black")
        result["ansi"][mode] = {n: list(c["lch"])
                                for n, c in chosen16.items()}
        report_chosen(f"{mode} ansi16", chosen16, bg)
    with open("pipeline/enot.json", "w") as f:
        json.dump(result, f, indent=2)
    print("wrote pipeline/enot.json")


if __name__ == "__main__":
    main()
