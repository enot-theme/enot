#!/usr/bin/env python3
"""Generator of earthy palettes in CIELAB and a preview page.

Principle: a variant's accents lie on a single LCh(ab) circle -
constant L* and C*, only the hue h differs. Backgrounds and text are
fixed lightness steps. Output: palettes.json + preview.html.
"""

import json
from math import cos, radians, sin
from string import Template

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


# ------------------------------------------------------------ palettes

ROLES = ["red", "orange", "yellow", "green", "aqua", "blue", "purple"]

VARIANTS = [
    {
        "slug": "mokh",
        "name": "moss",
        "desc": "closest to everforest: green undergrowth, warm beige text",
        "hues": {"red": 22, "orange": 50, "yellow": 88, "green": 128,
                 "aqua": 168, "blue": 215, "purple": 342},
        "mult": {"yellow": 0.95, "green": 0.95},
        "dark": {"bg": (16.5, 3.5, 150), "fg": (84, 12, 95), "acc": (72, 26)},
        "light": {"bg": (95.5, 4.0, 95), "fg": (33, 7, 150), "acc": (46, 32)},
    },
    {
        "slug": "glina",
        "name": "clay",
        "desc": "terracotta and ochre, the warmest one; brown-tinted background",
        "hues": {"red": 30, "orange": 58, "yellow": 82, "green": 112,
                 "aqua": 165, "blue": 245, "purple": 335},
        "mult": {"red": 1.1, "orange": 1.1, "aqua": 0.8, "blue": 0.7,
                 "purple": 0.9},
        "dark": {"bg": (17, 4.5, 60), "fg": (83.5, 11, 75), "acc": (72, 27)},
        "light": {"bg": (95, 4.5, 75), "fg": (33, 8, 55), "acc": (46, 33)},
    },
    {
        "slug": "pepel",
        "name": "ash",
        "desc": "almost neutral, restrained like habamax; minimal chroma",
        "hues": {"red": 20, "orange": 55, "yellow": 90, "green": 135,
                 "aqua": 185, "blue": 255, "purple": 320},
        "mult": {},
        "dark": {"bg": (15.5, 1.0, 90), "fg": (82, 4, 90), "acc": (71, 18)},
        "light": {"bg": (95.5, 1.2, 90), "fg": (31, 3, 90), "acc": (45, 23)},
    },
    {
        "slug": "polyn",
        "name": "wormwood",
        "desc": "gray-green, cooler than the rest; sage background",
        "hues": {"red": 15, "orange": 48, "yellow": 95, "green": 142,
                 "aqua": 190, "blue": 235, "purple": 310},
        "mult": {"blue": 0.85},
        "dark": {"bg": (16.5, 2.8, 135), "fg": (83, 8, 105), "acc": (72, 22)},
        "light": {"bg": (95.5, 3.0, 120), "fg": (33, 5, 135), "acc": (46, 28)},
    },
    {
        "slug": "okhra",
        "name": "ochre",
        "desc": "a gruvbox variation: yellow-brown undertone, cream text, "
                "olive and ochre in the accents; light theme on cream paper",
        "hues": {"red": 32, "orange": 55, "yellow": 84, "green": 105,
                 "aqua": 140, "blue": 215, "purple": 352},
        "mult": {"aqua": 0.95, "blue": 0.8, "purple": 0.95},
        "dark": {"bg": (17, 4.5, 85), "fg": (85, 18, 95), "acc": (70, 30)},
        "light": {"bg": (95, 13, 95), "fg": (31, 7, 75), "acc": (45, 36)},
    },
    {
        "slug": "kremen",
        "name": "flint",
        "desc": "gruvbox on neutral stone: gray backgrounds like #282828, "
                "warm text, the highest accent chroma",
        "hues": {"red": 32, "orange": 55, "yellow": 84, "green": 105,
                 "aqua": 140, "blue": 215, "purple": 352},
        "mult": {"aqua": 0.95, "blue": 0.8, "purple": 0.95},
        "dark": {"bg": (16, 1.0, 85), "fg": (86, 18, 95), "acc": (70, 32)},
        "light": {"bg": (95.5, 2.0, 90), "fg": (29, 4, 80), "acc": (44, 38)},
    },
]


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


def load_cvd_variant():
    """The "enot" variant from enot.json (written by optimize.py)."""
    try:
        with open("enot.json") as f:
            acc = json.load(f)
    except FileNotFoundError:
        return None
    base = next(v for v in VARIANTS if v["slug"] == "kremen")
    return {
        "slug": "enot",
        "name": "enot",
        "desc": "flint rebuilt for dichromacy: a lightness corridor "
                "instead of a single circle, max-min dE00 over normal "
                "vision, protanopia and deuteranopia (Vienot 1999); "
                "plus 16 ANSI colors for the terminal",
        "cvd_hard": True,
        "hues": base["hues"],
        "mult": {},
        "dark": {**base["dark"], "accents": acc["accents"]["dark"]},
        "light": {**base["light"], "accents": acc["accents"]["light"]},
        "ansi": {mode: {name: lch_to_hex(*lch)
                        for name, lch in acc["ansi"][mode].items()}
                 for mode in ("dark", "light")},
    }


def build_all():
    variants = list(VARIANTS)
    cvd = load_cvd_variant()
    if cvd:
        variants.append(cvd)
    out = []
    for v in variants:
        entry = {
            "slug": v["slug"],
            "name": v["name"],
            "desc": v["desc"],
            "cvd_hard": v.get("cvd_hard", False),
            "dark": build_theme(v["dark"], v["hues"], v["mult"], True),
            "light": build_theme(v["light"], v["hues"], v["mult"], False),
        }
        if v.get("ansi"):
            entry["ansi"] = v["ansi"]
        out.append(entry)
    return out


# ---------------------------------------------------------------- html

CSS = Template("""
:root { color-scheme: dark; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  background: $page_bg;
  color: $page_text;
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 14px;
  line-height: 1.6;
  padding: 56px 24px 80px;
}
.wrap { max-width: 1060px; margin: 0 auto; }
header h1 {
  font-size: 34px;
  font-weight: 600;
  letter-spacing: 0.16em;
  margin-bottom: 6px;
}
header .sub { color: $page_dim; margin-bottom: 28px; }
.method {
  border-left: 2px solid $page_faint;
  padding: 4px 0 4px 18px;
  color: $page_dim;
  max-width: 74ch;
  margin-bottom: 64px;
}
.method b { color: $page_text; font-weight: 600; }

.variant { margin-bottom: 88px; }
.vhead {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  border-bottom: 1px solid $page_faint;
  padding-bottom: 14px;
  margin-bottom: 22px;
}
.vhead h2 {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 0.22em;
}
.vhead .desc { color: $page_dim; max-width: 52ch; }
.vhead .params { color: $page_dim; font-size: 12px; white-space: nowrap; }

.panes {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}
@media (max-width: 860px) { .panes { grid-template-columns: minmax(0, 1fr); } }

.pane .eyebrow {
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: $page_dim;
  margin-bottom: 8px;
}
.editor {
  background: var(--bg0);
  color: var(--fg0);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 14px rgba(0,0,0,.28);
  font-size: 12.5px;
  line-height: 1.65;
}
.editor pre { overflow-x: auto; padding: 10px 0; }
.line { display: block; white-space: pre; }
.line .ln {
  color: var(--linenr);
  display: inline-block;
  width: 3.4ch;
  text-align: right;
  padding-right: 1.4ch;
  user-select: none;
}
.line.cur { background: var(--bg1); }
.line.cur .ln { color: var(--fg1); }
.tok-k { color: var(--red); }
.tok-f { color: var(--green); }
.tok-c { color: var(--blue); }
.tok-s { color: var(--aqua); }
.tok-n { color: var(--purple); }
.tok-b { color: var(--orange); }
.tok-y { color: var(--yellow); }
.tok-cm { color: var(--comment); font-style: italic; }
.vis { background: var(--bg2); }
.search { background: var(--yellow); color: var(--bg0); }
.cursor { background: var(--fg0); color: var(--bg0); }
.statusline {
  display: flex;
  gap: 1.5ch;
  background: var(--bg2);
  color: var(--fg1);
  padding: 2px 0;
  font-size: 12px;
}
.statusline .mode {
  background: var(--green);
  color: var(--bg0);
  padding: 0 1.2ch;
  font-weight: 600;
}
.statusline .grow { flex: 1; }
.statusline .tail { padding-right: 1.2ch; }

.swatches { margin-top: 12px; }
.swrow { display: flex; gap: 6px; margin-bottom: 6px; flex-wrap: wrap; }
.sw {
  font: inherit;
  border: none;
  cursor: pointer;
  background: none;
  color: $page_dim;
  font-size: 10px;
  text-align: center;
  line-height: 1.5;
}
.sw i {
  display: block;
  width: 46px;
  height: 30px;
  border-radius: 4px;
  background: var(--sw);
  margin-bottom: 2px;
}
.swrow.small .sw i { width: 38px; height: 18px; }
.sw:focus-visible { outline: 2px solid $page_text; outline-offset: 2px; }
.sw:hover i { transform: translateY(-1px); }
@media (prefers-reduced-motion: no-preference) {
  .sw i { transition: transform .12s ease; }
}

.ansi { border-radius: 8px; padding: 12px 12px 4px; }
.ansi .swrow { margin-bottom: 8px; }
.ansi.on-light .sw { color: #77746c; }
.panes.ansi-panes { margin-top: 18px; }

.polar { flex: none; }
.polar text { fill: $page_dim; font-size: 9px; font-family: inherit; }
.polar .grid { stroke: $page_faint; fill: none; }
.polar .cap { font-size: 9px; }

footer { color: $page_dim; border-top: 1px solid $page_faint; padding-top: 18px; }
""")

# The same code fragment in every panel - a fair comparison.
# Lines are joined without newlines: inside pre they would produce blank lines.
EDITOR = (
    '<div class="editor"><pre>'
    '<span class="line"><span class="ln">1</span><span class="tok-cm"># earthy accents: one L*, one C*</span></span>'
    '<span class="line"><span class="ln">2</span><span class="tok-k">from</span> math <span class="tok-k">import</span> cos, sin, radians</span>'
    '<span class="line"><span class="ln">3</span></span>'
    '<span class="line"><span class="ln">4</span><span class="tok-k">def</span> <span class="search">lch_to_lab</span>(l, c, h):</span>'
    '<span class="line"><span class="ln">5</span>    <span class="tok-s">&quot;&quot;&quot;CIELAB from cylindrical coordinates.&quot;&quot;&quot;</span></span>'
    '<span class="line"><span class="ln">6</span>    hr = <span class="tok-c">radians</span>(h)</span>'
    '<span class="line"><span class="ln">7</span>    <span class="tok-k">return</span> l, <span class="vis">c * <span class="tok-c">cos</span>(hr)</span>, c * <span class="tok-c">sin</span>(hr)</span>'
    '<span class="line"><span class="ln">8</span></span>'
    '<span class="line"><span class="ln">9</span><span class="tok-y">HUES</span> = {<span class="tok-s">&quot;red&quot;</span>: <span class="tok-n">22</span>, <span class="tok-s">&quot;green&quot;</span>: <span class="tok-n">128</span>, <span class="tok-s">&quot;blue&quot;</span>: <span class="tok-n">215</span>}</span>'
    '<span class="line"><span class="ln">10</span></span>'
    '<span class="line"><span class="ln">11</span><span class="tok-k">for</span> name, hue <span class="tok-k">in</span> HUES.<span class="tok-c">items</span>():</span>'
    '<span class="line cur"><span class="ln">12</span>    lab = <span class="search">lch_to_lab</span>(<span class="tok-n">72.0</span>, <span class="tok-n">26.0</span>, <span class="cursor">h</span>ue)</span>'
    '<span class="line"><span class="ln">13</span>    <span class="tok-b">print</span>(<span class="tok-s">f&quot;lab={lab}&quot;</span>)</span>'
    '</pre><div class="statusline"><span class="mode">NORMAL</span>'
    '<span>palette.py</span><span class="grow"></span><span>utf-8</span>'
    '<span>py</span><span class="tail">12:24</span></div></div>'
)

NEUTRAL_ROLES = ["bg0", "bg1", "bg2", "bg3", "fg0", "fg1", "comment", "linenr"]


def css_vars(theme):
    return "; ".join(f"--{k}:{v}" for k, v in theme.items()
                     if not k.startswith("_"))


def swatch(hexval, label):
    return (f'<button class="sw" style="--sw:{hexval}" title="{label}" '
            f'data-hex="{hexval}"><i></i>{hexval}</button>')


def swatches(theme):
    acc = "".join(
        swatch(theme[r], "%s  L*%s C*%s h%s" % ((r,) + theme["_lch"][r]))
        for r in ROLES)
    neu = "".join(swatch(theme[r], r) for r in NEUTRAL_ROLES)
    return (f'<div class="swatches"><div class="swrow">{acc}</div>'
            f'<div class="swrow small">{neu}</div></div>')


def pane(title, theme):
    return (f'<div class="pane"><div class="eyebrow">{title}</div>'
            f'<div style="{css_vars(theme)}">{EDITOR}{swatches(theme)}'
            f'</div></div>')


def polar(variant):
    """Accents as (C*, h) points: dark theme filled, light theme outlined."""
    cx, cy = 105, 76
    k = 1.75  # px per unit of C*
    parts = [f'<svg class="polar" width="210" height="188" '
             f'viewBox="0 0 210 188" role="img" '
             f'aria-label="variant {variant["name"]} accents in LCh">']
    for c in (10, 20, 30):
        parts.append(f'<circle class="grid" cx="{cx}" cy="{cy}" r="{c * k}"/>')
    parts.append(f'<line class="grid" x1="{cx}" y1="{cy}" '
                 f'x2="{cx + 34 * k}" y2="{cy}" stroke-dasharray="2 3"/>')
    parts.append(f'<text x="{cx + 30 * k - 6}" y="{cy - 4}">30</text>')
    for theme, style in ((variant["dark"], "fill"), (variant["light"], "stroke")):
        for role in ROLES:
            _, c, h = theme["_lch"][role]
            x = cx + c * k * cos(radians(h))
            y = cy - c * k * sin(radians(h))
            if style == "fill":
                attrs = f'fill="{theme[role]}"'
            else:
                attrs = f'fill="none" stroke="{theme[role]}" stroke-width="2"'
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" {attrs}/>')
    parts.append(f'<text class="cap" x="{cx}" y="168" text-anchor="middle">'
                 f'C*, h at fixed L*</text>')
    parts.append(f'<text class="cap" x="{cx}" y="181" text-anchor="middle">'
                 f'fill - dark, outline - light</text></svg>')
    return "".join(parts)


def acc_params(theme):
    meta = theme["_meta"]
    if meta["acc"]:
        return f'accents L*{meta["acc"][0]} C*{meta["acc"][1]}'
    ls = [theme["_lch"][r][0] for r in ROLES]
    cs = [theme["_lch"][r][1] for r in ROLES]
    return (f'accents L*{min(ls):g}-{max(ls):g} '
            f'C*{min(cs):g}-{max(cs):g} (corridor)')


def params_line(variant):
    d, l = variant["dark"]["_meta"], variant["light"]["_meta"]
    return (f'dark: bg L*{d["bg"][0]} / text L*{d["fg"][0]} / '
            f'{acc_params(variant["dark"])}<br>'
            f'light: bg L*{l["bg"][0]} / text L*{l["fg"][0]} / '
            f'{acc_params(variant["light"])}')


ANSI_ORDER = ["black", "red", "green", "yellow",
              "blue", "magenta", "cyan", "white"]


def ansi_pane(title, amap, bg, cls=""):
    row1 = "".join(swatch(amap[n], n) for n in ANSI_ORDER)
    row2 = "".join(swatch(amap["br_" + n], "br_" + n) for n in ANSI_ORDER)
    return (f'<div class="pane"><div class="eyebrow">{title}</div>'
            f'<div class="ansi {cls}" style="background:{bg}">'
            f'<div class="swrow small">{row1}</div>'
            f'<div class="swrow small">{row2}</div></div></div>')


def ansi_section(v):
    if not v.get("ansi"):
        return ""
    return (f'<div class="panes ansi-panes">'
            + ansi_pane("ansi 16 · dark", v["ansi"]["dark"],
                        v["dark"]["bg0"])
            + ansi_pane("ansi 16 · light", v["ansi"]["light"],
                        v["light"]["bg0"], "on-light")
            + '</div>')


def variant_html(v):
    return f"""
<section class="variant" id="{v['slug']}">
  <div class="vhead">
    <div>
      <h2>{v['name']}</h2>
      <div class="desc">{v['desc']}</div>
      <div class="params">{params_line(v)}</div>
    </div>
    {polar(v)}
  </div>
  <div class="panes">
    {pane('dark', v['dark'])}
    {pane('light', v['light'])}
  </div>
  {ansi_section(v)}
</section>"""


JS = """
document.querySelectorAll('.sw').forEach(function (b) {
  b.addEventListener('click', function () {
    var hex = b.dataset.hex;
    if (navigator.clipboard) navigator.clipboard.writeText(hex);
    var old = b.lastChild.textContent;
    b.lastChild.textContent = 'copied';
    setTimeout(function () { b.lastChild.textContent = old; }, 900);
  });
});
"""


def page_html(variants):
    chrome = {
        "page_bg": lch_to_hex(42, 1, 90),
        "page_text": lch_to_hex(92, 2, 90),
        "page_dim": lch_to_hex(74, 2, 90),
        "page_faint": lch_to_hex(54, 1.5, 90),
    }
    body = "".join(variant_html(v) for v in variants)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>earthy palettes - CIELAB</title>
<style>{CSS.substitute(chrome)}</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>earthy palettes</h1>
  <div class="sub">CIELAB · variants: {len(variants)} · references: habamax, everforest, gruvbox</div>
  <div class="method">
    method: each variant's accents lie on <b>a single LCh(ab) circle</b> -
    constant lightness L* and chroma C*, only the hue h differs.
    backgrounds and text are fixed L* steps. this page's background is
    neutral gray L*=42: an even backdrop for judging color.
    clicking a swatch copies its hex.
  </div>
</header>
{body}
<footer>
  generated by palette.py · pick a variant - the site and the schemes
  for vim and wezterm come next
</footer>
</div>
<script>{JS}</script>
</body>
</html>"""


def main():
    variants = build_all()
    with open("palettes.json", "w") as f:
        json.dump(variants, f, ensure_ascii=False, indent=2)
    with open("preview.html", "w") as f:
        f.write(page_html(variants))
    for v in variants:
        print(v["name"])
        for mode in ("dark", "light"):
            t = v[mode]
            row = " ".join(t[r] for r in ROLES)
            print(f"  {mode:5}  bg {t['bg0']}  fg {t['fg0']}  {row}")


if __name__ == "__main__":
    main()
