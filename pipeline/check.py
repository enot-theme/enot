#!/usr/bin/env python3
"""Single regression: colors.json invariants and artifact conformance.

Metrics for the three depths are computed by resolve.py and written
to colors.json; the thresholds and structural checks live here: ANSI
tiers do not overlap, in the light theme bright colors are darker
than normal, and every color literal in the generated themes belongs
to the specification. Exits 1 on any violation.

Which artifacts to scan and how is derived from ports/*/port.json:
a depth with "16M" means every hex literal must come from the spec,
a "c256_pattern" in the manifest extracts xterm-256 indexes to
verify, and an ANSI-only depth means the artifact must carry no hex
at all. A new port is checked without touching this file.

256 thresholds are below the truecolor ones and differ per theme:
the xterm-256 grid is sparse in the muted earthy region, and the
light theme at 4.5:1 contrast hits the physical limit (the
aqua-blue pair).
"""

import json
import os
import re
import sys

from assets import HEX_CHECKED

# (theme | *, depth, metric from colors.json, threshold)
CHECKS = [
    ("*", "16M", "accents", 8.0),
    ("*", "16M", "ansi16", 7.0),
    ("*", "16M", "tints", 3.0),
    ("*", "16M", "contrast", 4.5),
    ("*", "16M", "guard_accents", 10.0),
    ("*", "16M", "guard_ansi_normal", 10.0),
    ("*", "16M", "guard_ansi_bright", 6.5),
    ("*", "16M", "red_chroma", 21.5),
    ("*", "16M", "ansi_tier_gap", 2.0),
    ("dark", "256", "accents", 7.0),
    ("light", "256", "accents", 2.0),
    ("*", "256", "tints", 3.0),
    ("*", "256", "contrast", 4.5),
    ("*", "256", "guard_accents", 6.5),
    ("*", "256", "red_chroma", 21.5),
]

def port_manifests():
    for app in sorted(os.listdir("ports")):
        path = os.path.join("ports", app, "port.json")
        if os.path.isfile(path):
            with open(path) as f:
                yield json.load(f)


def fail(msgs, cond, text):
    if not cond:
        msgs.append(text)
    print(f"  {'ok  ' if cond else 'FAIL'} {text}")


def check_metrics(spec, msgs):
    for mode, depth, metric, threshold in CHECKS:
        for m in ("dark", "light") if mode == "*" else (mode,):
            val = spec["metrics"][m][depth][metric]
            fail(msgs, val >= threshold,
                 f"{m:5} {depth:3} {metric} {val} >= {threshold}")


def allowed_sets(spec):
    hexes, c256 = set(), set()
    for th in spec["themes"].values():
        for e in th["roles"].values():
            hexes.update((e["hex"], e["c256hex"]))
            c256.add(e["c256"])
        for e in th["ansi"].values():
            hexes.add(e["hex"])
    return hexes, c256


def check_hex(path, text, hexes, msgs):
    found = set(re.findall(r"#[0-9a-fA-F]{6}", text))
    alien = {h for h in found if h.lower() not in hexes}
    fail(msgs, not alien, f"{path}: hex from the specification"
         + (f" (alien: {sorted(alien)})" if alien else ""))


def check_artifacts(spec, msgs):
    hexes, c256 = allowed_sets(spec)
    for m in port_manifests():
        paths = [o["path"] for o in m["outputs"]]
        for path in paths:
            # errors="ignore" lets binary containers through: text stored
            # inside a zip (telegram) is still scanned verbatim
            text = open(path, errors="ignore").read()
            if "16M" in m["depth"]:
                check_hex(path, text, hexes, msgs)
            else:
                clean = not re.search(r"#[0-9a-fA-F]{6}", text)
                fail(msgs, clean, f"{path}: ANSI indexes only, no hex")
            if m.get("c256_pattern"):
                found = {int(x) for x in re.findall(m["c256_pattern"], text)}
                alien = found - c256
                fail(msgs, not alien,
                     f"{path}: 256 indexes from the specification"
                     + (f" (alien: {sorted(alien)})" if alien else ""))
    # README reference sheets carry only specification colors;
    # cvd-{dark,light}.svg are exempt by design (gruvbox comparison and
    # simulation outputs)
    for path in HEX_CHECKED:
        check_hex(path, open(path).read(), hexes, msgs)


def main():
    with open("colors.json") as f:
        spec = json.load(f)
    msgs = []
    check_metrics(spec, msgs)
    check_artifacts(spec, msgs)
    if msgs:
        print(f"FAILURE: {len(msgs)} violations")
        return 1
    print("all invariants hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
