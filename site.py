#!/usr/bin/env python3
"""enot theme site: static pages in site/ from palettes.json.

The page is its own demo: all chrome is styled with palette CSS
variables, the dark/light switch changes the theme, the vision switch
(normal/protan/deutan/tritan) runs the page through precomputed
dichromacy simulations. A gruvbox strip sits alongside for comparison.
Output: site/index.html, site/vim.html, site/wezterm.html + scheme files.
"""

import json
import os
import shutil
from string import Template

from cvd import SIM_FUNCS

SLUG = "enot"
BASE_URL = "https://enot-theme.github.io/site/"
ROLE_KEYS = ["bg0", "bg1", "bg2", "bg3", "fg0", "fg1", "comment", "linenr",
             "red", "orange", "yellow", "green", "aqua", "blue", "purple"]
ACCENTS = ["red", "orange", "yellow", "green", "aqua", "blue", "purple"]
# bright row of gruvbox dark and normal row of gruvbox light, same 7 roles
GRUVBOX = {
    "dark": ["#fb4934", "#fe8019", "#fabd2f", "#b8bb26",
             "#8ec07c", "#83a598", "#d3869b"],
    "light": ["#cc241d", "#d65d0e", "#d79921", "#98971a",
              "#689d6a", "#458588", "#b16286"],
}


def vision_sets(colors):
    """dict vision name -> {key: hex} for a list/dict of colors."""
    def run(fn):
        if isinstance(colors, dict):
            return {k: fn(h) for k, h in colors.items()}
        return [fn(h) for h in colors]
    sets = {"normal": run(lambda h: h)}
    for name, fn in SIM_FUNCS.items():
        sets[name] = run(fn)
    return sets


def build_data(v):
    data = {"enot": {}, "gruvbox": {}}
    for mode in ("dark", "light"):
        theme = {k: v[mode][k] for k in ROLE_KEYS}
        data["enot"][mode] = vision_sets(theme)
        data["gruvbox"][mode] = vision_sets(GRUVBOX[mode])
    return data


# ------------------------------------------------------------------ css

CSS = """
:root { color-scheme: dark light; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { transition: none !important; }
}
body {
  background: var(--bg0);
  color: var(--fg0);
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 15px;
  line-height: 1.65;
  transition: background .25s ease, color .25s ease;
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
a:focus-visible, button:focus-visible {
  outline: 2px solid var(--yellow); outline-offset: 2px;
}
.wrap { max-width: 980px; margin: 0 auto; padding: 0 24px; }

header.top {
  display: flex; align-items: center; gap: 18px;
  padding-block: 18px; flex-wrap: wrap;
}
.mark { display: flex; align-items: center; gap: 10px; color: var(--fg0); }
.mark svg { display: block; }
.mark b { font-size: 18px; font-weight: 600; letter-spacing: .08em; }
nav { display: flex; gap: 16px; flex-wrap: wrap; margin-left: auto; }
nav a { color: var(--fg1); font-size: 13px; }

.controls { display: flex; gap: 10px; flex-wrap: wrap; margin: 26px 0; }
.seg { display: flex; border: 1px solid var(--bg3); border-radius: 7px;
       overflow: hidden; }
.seg button {
  font: inherit; font-size: 12.5px; padding: 5px 12px;
  background: var(--bg1); color: var(--fg1);
  border: none; cursor: pointer;
}
.seg button + button { border-left: 1px solid var(--bg3); }
.seg button[aria-pressed="true"] { background: var(--bg3); color: var(--fg0); }
.controls .hint { font-size: 12.5px; color: var(--comment); align-self: center; }
@media (max-width: 540px) {
  .seg { display: grid; grid-template-columns: 1fr 1fr; width: 100%; }
  .seg button { border: none; }
  .seg button:nth-child(even) { border-left: 1px solid var(--bg3); }
  .seg button:nth-child(n+3) { border-top: 1px solid var(--bg3); }
}

.hero { padding-block: 30px 10px; }
.hero h1 {
  font-size: clamp(40px, 7vw, 64px); font-weight: 700;
  letter-spacing: .04em; line-height: 1.1;
}
.tail { display: flex; gap: 6px; margin: 14px 0 22px; max-width: 420px; }
.tail i {
  height: 10px; flex: 1; border-radius: 5px;
}
.hero .tagline { font-size: clamp(17px, 2.6vw, 22px); max-width: 44ch; }
.hero .sub { color: var(--fg1); max-width: 62ch; margin-top: 12px; }
.cta { display: flex; gap: 12px; margin: 26px 0 8px; flex-wrap: wrap; }
.btn {
  display: inline-block; padding: 9px 18px; border-radius: 7px;
  background: var(--green); color: var(--bg0); font-weight: 600;
  font-size: 14px;
}
.btn:hover { text-decoration: none; filter: brightness(1.06); }
.btn.alt { background: var(--bg2); color: var(--fg0); }

section { padding: 54px 0 6px; }
section > .wrap > h2 {
  font-size: 22px; font-weight: 600; letter-spacing: .14em;
  margin-bottom: 6px;
}
section .lead { color: var(--fg1); max-width: 68ch; margin-bottom: 26px; }

.editor {
  background: var(--bg0); border: 1px solid var(--bg3);
  border-radius: 9px; overflow: hidden;
  font-size: 13.5px; line-height: 1.7;
  box-shadow: 0 3px 18px rgba(0,0,0,.25);
}
.editor pre { overflow-x: auto; padding: 12px 0; }
.line { display: block; white-space: pre; }
.line .ln {
  color: var(--linenr); display: inline-block; width: 3.4ch;
  text-align: right; padding-right: 1.4ch; user-select: none;
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
  display: flex; gap: 1.5ch; background: var(--bg2); color: var(--fg1);
  padding: 3px 0; font-size: 12.5px;
}
.statusline .mode {
  background: var(--green); color: var(--bg0);
  padding: 0 1.2ch; font-weight: 600;
}
.statusline .grow { flex: 1; }
.statusline .tail-seg { padding-right: 1.2ch; }

.strip { display: flex; gap: 8px; margin: 14px 0; flex-wrap: wrap; }
.strip .sw {
  font: inherit; border: none; background: none; cursor: pointer;
  color: var(--comment); font-size: 11px; text-align: center;
}
.strip .sw i {
  display: block; width: 58px; height: 34px; border-radius: 6px;
  margin-bottom: 4px;
}
.strip.small .sw i { width: 40px; height: 22px; }
.caption { font-size: 12.5px; color: var(--comment); max-width: 60ch; }

.compare { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }
@media (max-width: 760px) { .compare { grid-template-columns: 1fr; } }
.compare h3 {
  font-size: 13px; letter-spacing: .18em; text-transform: uppercase;
  color: var(--fg1); font-weight: 600; margin-bottom: 8px;
}

.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
@media (max-width: 860px) { .cards { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .cards { grid-template-columns: 1fr; } }
.card {
  background: var(--bg1); border: 1px solid var(--bg3);
  border-radius: 9px; padding: 18px 16px;
}
.card b { font-size: 26px; font-weight: 700; display: block; }
.card span { font-size: 12.5px; color: var(--fg1); }
.invh { font-size: 14px; letter-spacing: .1em; margin: 26px 0 4px; }
.invwrap { overflow-x: auto; }
.inv { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.inv th, .inv td {
  text-align: left; padding: 6px 10px;
  border-bottom: 1px solid var(--bg2); vertical-align: top;
}
.inv th { color: var(--fg1); font-weight: 600; }
.inv td.num {
  font-variant-numeric: tabular-nums; white-space: nowrap;
  font-family: ui-monospace, monospace;
}

ol.method { max-width: 70ch; padding-left: 3ch; }
ol.method li { margin-bottom: 10px; }
ol.method li::marker { color: var(--orange); font-weight: 600; }

ul.refs { list-style: none; max-width: 76ch; }
ul.refs li { margin-bottom: 10px; padding-left: 2ch; text-indent: -2ch; }
ul.refs li::before { content: "- "; color: var(--orange); }

.apps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
@media (max-width: 760px) { .apps { grid-template-columns: 1fr; } }
.app {
  display: block; background: var(--bg1); border: 1px solid var(--bg3);
  border-radius: 9px; padding: 20px 18px; color: var(--fg0);
}
.app:hover { text-decoration: none; border-color: var(--fg1); }
.app b { font-size: 18px; display: block; margin-bottom: 4px; }
.app span { font-size: 12.5px; color: var(--fg1); }
.app.ghost { border-style: dashed; background: none; color: var(--comment); }

pre.snippet {
  background: var(--bg1); border: 1px solid var(--bg3); border-radius: 9px;
  padding: 14px 18px; overflow-x: auto; font-size: 13.5px; line-height: 1.7;
  margin: 14px 0;
}
.steps { max-width: 72ch; }
.steps h3 { font-size: 15px; margin: 26px 0 6px; }
.steps p { color: var(--fg1); }

footer {
  margin-top: 70px; border-top: 1px solid var(--bg3);
  padding: 26px 0 60px; color: var(--fg1); font-size: 13.5px;
}
footer .wrap { display: grid; gap: 8px; }
"""

# ------------------------------------------------------------------ svg

LOGO = """<svg width="$size" height="$size" viewBox="0 0 64 64" role="img"
 aria-label="enot raccoon logo" fill="none">
<path d="M10 24 L4 8 L22 13 Z" fill="currentColor"/>
<path d="M54 24 L60 8 L42 13 Z" fill="currentColor"/>
<path d="M32 8 C14 8 6 22 6 36 C6 50 17 58 32 58 C47 58 58 50 58 36
 C58 22 50 8 32 8 Z" stroke="currentColor" stroke-width="3.5"/>
<path d="M7 28 C15 24 24 23 32 23 C40 23 49 24 57 28 C57 36 52 42 44 42
 C38 42 34 39 32 36 C30 39 26 42 20 42 C12 42 7 36 7 28 Z"
 fill="currentColor"/>
<circle cx="21" cy="32" r="3.4" fill="var(--bg0)"/>
<circle cx="43" cy="32" r="3.4" fill="var(--bg0)"/>
<path d="M28 47 L36 47 L32 52 Z" fill="currentColor"/>
</svg>"""


def logo(size):
    return Template(LOGO).substitute(size=size)


def favicon():
    svg = Template(LOGO).substitute(size=64).replace(
        "var(--bg0)", "#f4f2ee").replace("currentColor", "#45423c")
    return "data:image/svg+xml," + svg.replace("\n", " ").replace(
        "#", "%23").replace('"', "'")


# ----------------------------------------------------------------- html

EDITOR = (
    '<div class="editor"><pre>'
    '<span class="line"><span class="ln">1</span><span class="tok-cm"># accents live in CIELAB, not in guesswork</span></span>'
    '<span class="line"><span class="ln">2</span><span class="tok-k">from</span> math <span class="tok-k">import</span> cos, sin, radians</span>'
    '<span class="line"><span class="ln">3</span></span>'
    '<span class="line"><span class="ln">4</span><span class="tok-k">def</span> <span class="search">lch_to_lab</span>(l, c, h):</span>'
    '<span class="line"><span class="ln">5</span>    <span class="tok-s">&quot;&quot;&quot;Cylindrical LCh to rectangular Lab.&quot;&quot;&quot;</span></span>'
    '<span class="line"><span class="ln">6</span>    hr = <span class="tok-c">radians</span>(h)</span>'
    '<span class="line"><span class="ln">7</span>    <span class="tok-k">return</span> l, <span class="vis">c * <span class="tok-c">cos</span>(hr)</span>, c * <span class="tok-c">sin</span>(hr)</span>'
    '<span class="line"><span class="ln">8</span></span>'
    '<span class="line"><span class="ln">9</span><span class="tok-y">GUARDS</span> = {<span class="tok-s">&quot;contrast&quot;</span>: <span class="tok-n">4.5</span>, <span class="tok-s">&quot;delta_e&quot;</span>: <span class="tok-n">8.0</span>}</span>'
    '<span class="line"><span class="ln">10</span></span>'
    '<span class="line"><span class="ln">11</span><span class="tok-k">for</span> name, floor <span class="tok-k">in</span> GUARDS.<span class="tok-c">items</span>():</span>'
    '<span class="line cur"><span class="ln">12</span>    ok = <span class="tok-c">holds</span>(name, <span class="search">lch_to_lab</span>(<span class="tok-n">70.0</span>, <span class="tok-n">26.0</span>, <span class="cursor">h</span>ue))</span>'
    '<span class="line"><span class="ln">13</span>    <span class="tok-b">print</span>(<span class="tok-s">f&quot;{name}: {ok}&quot;</span>)</span>'
    '</pre><div class="statusline"><span class="mode">NORMAL</span>'
    '<span>palette.py</span><span class="grow"></span><span>utf-8</span>'
    '<span>py</span><span class="tail-seg">12:24</span></div></div>'
)


def accent_strip(theme):
    sw = "".join(
        f'<button class="sw" data-hex="{theme[r]}" title="{r}">'
        f'<i style="background:var(--{r})"></i>{theme[r]}</button>'
        for r in ACCENTS)
    return f'<div class="strip">{sw}</div>'


def gruv_strip():
    sw = "".join(
        f'<span class="sw"><i style="background:var(--gruv{i})"></i></span>'
        for i in range(7))
    return f'<div class="strip small">{sw}</div>'


def enot_strip_plain():
    sw = "".join(
        f'<span class="sw"><i style="background:var(--{r})"></i></span>'
        for r in ACCENTS)
    return f'<div class="strip small">{sw}</div>'


def controls():
    return """
<div class="controls">
  <div class="seg" role="group" aria-label="theme">
    <button data-mode="dark">dark</button>
    <button data-mode="light">light</button>
  </div>
  <div class="seg" role="group" aria-label="simulated vision">
    <button data-vision="normal">normal</button>
    <button data-vision="protanopia">protanopia</button>
    <button data-vision="deuteranopia">deuteranopia</button>
    <button data-vision="tritanopia">tritanopia</button>
  </div>
  <span class="hint">the whole page re-renders through the selected vision</span>
</div>"""


def head(title, desc, root_vars, page=""):
    url = BASE_URL + page
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<link rel="icon" href="{favicon()}">
<style>:root {{ {root_vars} }}{CSS}</style>
</head>
<body>"""


def top(active=""):
    items = [("index.html#why", "why"), ("index.html#numbers", "numbers"),
             ("index.html#method", "method"), ("index.html#science", "science"),
             ("index.html#get", "get it")]
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in items)
    return (f'<header class="top wrap"><a class="mark" href="index.html">'
            f'{logo(34)}<b>enot</b></a><nav>{nav}</nav></header>')


JS = Template("""
var DATA = $data;
var state = { mode: "dark", vision: "normal" };
try {
  var q = new URLSearchParams(location.search);
  var saved = localStorage.getItem("enot-mode");
  if (window.matchMedia("(prefers-color-scheme: light)").matches)
    state.mode = "light";
  if (saved === "dark" || saved === "light") state.mode = saved;
  if (q.get("mode") === "dark" || q.get("mode") === "light")
    state.mode = q.get("mode");
  if (DATA.enot.dark[q.get("vision")]) state.vision = q.get("vision");
} catch (e) {}

function apply() {
  var root = document.documentElement.style;
  var set = DATA.enot[state.mode][state.vision];
  Object.keys(set).forEach(function (k) { root.setProperty("--" + k, set[k]); });
  DATA.gruvbox[state.mode][state.vision].forEach(function (h, i) {
    root.setProperty("--gruv" + i, h);
  });
  document.querySelectorAll("[data-mode]").forEach(function (b) {
    b.setAttribute("aria-pressed", String(b.dataset.mode === state.mode));
  });
  document.querySelectorAll("[data-vision]").forEach(function (b) {
    b.setAttribute("aria-pressed", String(b.dataset.vision === state.vision));
  });
}
document.addEventListener("click", function (e) {
  var b = e.target.closest("[data-mode],[data-vision],[data-hex]");
  if (!b) return;
  if (b.dataset.mode) {
    state.mode = b.dataset.mode;
    try { localStorage.setItem("enot-mode", state.mode); } catch (e2) {}
    apply();
  } else if (b.dataset.vision) {
    state.vision = b.dataset.vision;
    apply();
  } else if (b.dataset.hex && navigator.clipboard) {
    navigator.clipboard.writeText(b.dataset.hex);
    var old = b.lastChild.textContent;
    b.lastChild.textContent = "copied";
    setTimeout(function () { b.lastChild.textContent = old; }, 900);
  }
});
apply();
""")


INV_LABELS = {
    "accents": "min pairwise ΔE00 across the 7 accents, worst of normal / "
               "protanopia / deuteranopia",
    "ansi16": "min pairwise ΔE00 across all 16 ANSI colors",
    "tints": "min pairwise ΔE00 across the 4 diff backgrounds",
    "contrast": "min WCAG contrast over every text-on-background pair "
                "of the depth",
    "guard_accents": "min ΔE00 from accents to text and comment",
    "guard_ansi_normal": "the same guard for the normal ANSI tier",
    "guard_ansi_bright": "the same guard for the bright ANSI tier",
    "red_chroma": "chroma of red - diagnostics stay salient",
    "ansi_tier_gap": "lightness gap between ANSI tiers "
                     "(the bright tier is darker in the light theme)",
}


def invariants_html(spec, checks):
    def table(depth):
        gates = {}
        for mode, d, metric, thr in checks:
            if d == depth:
                gates.setdefault(metric, {})[mode] = thr
        rows = []
        for metric, by_mode in gates.items():
            gate = " / ".join(
                f"&ge; {thr}" + ("" if mode == "*" else f" ({mode})")
                for mode, thr in by_mode.items())
            cells = "".join(
                f'<td class="num">{spec["metrics"][m][depth][metric]}</td>'
                for m in ("dark", "light"))
            rows.append(f'<tr><td>{INV_LABELS[metric]}</td>'
                        f'<td class="num">{gate}</td>{cells}</tr>')
        return ('<div class="invwrap"><table class="inv">'
                '<tr><th>invariant</th><th>gate</th><th>dark</th>'
                '<th>light</th></tr>' + "".join(rows) + '</table></div>')

    drift = " / ".join(str(spec["metrics"][m]["256"]["drift_max"])
                       for m in ("dark", "light"))
    return f"""
  <h3 class="invh">true color - 16M</h3>
  {table('16M')}
  <h3 class="invh">xterm-256</h3>
  <p class="lead">The 256-color depth is not naive quantization: the
  xterm cube is so sparse in the muted earthy region that
  nearest-color mapping collapses roles to ΔE00 = 0. Instead the same
  max-min optimizer runs over the xterm grid, anchored to the
  true-color values (max drift {drift} ΔE00). The light theme's
  minimum is the physical ceiling of the grid at 4.5:1 contrast -
  the true-color variants carry the full guarantee.</p>
  {table('256')}
  <h3 class="invh">16 - ANSI</h3>
  <p class="lead">The 16-color depth is the ANSI palette itself,
  delivered as true color by the terminal scheme and consumed by index
  (the ranger colorscheme addresses slots 0-15). Its guarantees are the
  ANSI rows of the 16M table: minimum pairwise ΔE00 of
  {min(spec['metrics'][m]['16M']['ansi16'] for m in ('dark', 'light'))},
  disjoint lightness tiers, contrast against the background.</p>
  <p class="caption">The whole spec is data:
  <a href="colors.json" download>colors.json</a> - roles &times; depths
  &times; themes with these measured metrics embedded; the regression
  gate (check.py) fails the build if any number above drops, and every
  color literal in every generated theme must belong to the spec.</p>"""


def index_html(v, data, spec, checks):
    dark = data["enot"]["dark"]["normal"]
    root_vars = "; ".join(f"--{k}: {h}" for k, h in dark.items())
    root_vars += "; " + "; ".join(
        f"--gruv{i}: {h}" for i, h in enumerate(data["gruvbox"]["dark"]["normal"]))
    tail = "".join(f'<i style="background:var(--{r})"></i>' for r in ACCENTS)
    refs = [
        ('Sharma, Wu, Dalal. The CIEDE2000 color-difference formula: '
         'implementation notes. Color Research and Application 30(1), 2005.',
         'https://doi.org/10.1002/col.20070'),
        ('Brettel, Viénot, Mollon. Computerized simulation of color '
         'appearance for dichromats. JOSA A 14(10), 1997.',
         'https://doi.org/10.1364/JOSAA.14.002647'),
        ('Viénot, Brettel, Mollon. Digital video colourmaps for checking '
         'the legibility of displays by dichromats. Color Research and '
         'Application 24(4), 1999.',
         'https://doi.org/10.1002/(SICI)1520-6378(199908)24:4%3C243::AID-COL5%3E3.0.CO;2-3'),
        ('Burrus. Review of open source color blindness simulations. 2021.',
         'https://daltonlens.org/opensource-cvd-simulation/'),
        ('Wong. Points of view: color blindness. Nature Methods 8, 441, 2011.',
         'https://doi.org/10.1038/nmeth.1618'),
        ('Petroff. Accessible color sequences for data visualization. 2021.',
         'https://arxiv.org/abs/2107.02270'),
        ('Piepenbrock, Mayr, Buchner. Positive display polarity is '
         'particularly advantageous for small character sizes. '
         'Human Factors 56(5), 2014.',
         'https://doi.org/10.1177/0018720813515509'),
    ]
    refs_html = "".join(f'<li>{t} <a href="{u}">{u.split("//")[1].split("/")[0]}</a></li>'
                        for t, u in refs)
    acc_min = round(min(spec["metrics"][m]["16M"]["accents"]
                        for m in ("dark", "light")), 1)
    ansi_min = round(min(spec["metrics"][m]["16M"]["ansi16"]
                         for m in ("dark", "light")), 1)
    invariants = invariants_html(spec, checks)
    return head(
        "enot - an earthy colorscheme that survives color blindness",
        "Warm gruvbox-family looks, built in CIELAB, optimized so every "
        "pair of colors stays distinguishable under protanopia and "
        "deuteranopia. Dark and light. vim, WezTerm, Midnight Commander "
        "and ranger.",
        root_vars,
    ) + top() + f"""
<div class="hero wrap">
  <h1>enot</h1>
  <div class="tail" aria-hidden="true">{tail}</div>
  <p class="tagline">An earthy colorscheme that survives color blindness.</p>
  <p class="sub">Warm gruvbox-family looks, built in CIELAB and optimized so
  every pair of colors stays apart under protanopia and deuteranopia -
  the red-green vision deficiencies that affect about 8% of men.
  Dark and light. No hand-picked colors: everything is generated,
  optimized and regression-checked.</p>
  <div class="cta">
    <a class="btn" href="vim.html">Get it for vim</a>
    <a class="btn alt" href="wezterm.html">WezTerm</a>
    <a class="btn alt" href="mc.html">mc</a>
    <a class="btn alt" href="ranger.html">ranger</a>
  </div>
  {controls()}
  {EDITOR}
  {accent_strip(dark)}
  <p class="caption">Swatches and the editor are rendered through the
  selected vision; the hex values are the real colors - click to copy.</p>
</div>

<section id="why"><div class="wrap">
  <h2>most warm themes collapse</h2>
  <p class="lead">Warm themes encode meaning almost purely by hue.
  Dichromacy projects the color plane onto a single axis, folding red,
  orange, yellow and green into one ochre band. Switch the vision above
  to deuteranopia and compare:</p>
  <div class="compare">
    <div><h3>gruvbox accents</h3>{gruv_strip()}</div>
    <div><h3>enot accents</h3>{enot_strip_plain()}</div>
  </div>
  <p class="caption">enot's optimizer maximizes the minimum pairwise
  CIEDE2000 distance across normal vision, protanopia and deuteranopia,
  and spreads colors along the lightness axis - the one axis dichromacy
  never touches. The colors cannot collapse.</p>
</div></section>

<section id="numbers"><div class="wrap">
  <h2>guarantees, not vibes</h2>
  <p class="lead">Every value below is computed from the spec and
  enforced by a regression gate: the build fails if any of them drops.
  Three color depths, each with its own testable invariants.</p>
  <div class="cards">
    <div class="card"><b>&Delta;E00 &ge; {acc_min}</b><span>between any two
    syntax accents, worst case across the three simulated visions</span></div>
    <div class="card"><b>&Delta;E00 &ge; {ansi_min}</b><span>same guarantee
    for all 16 ANSI terminal colors, both tiers</span></div>
    <div class="card"><b>&ge; 4.5:1</b><span>WCAG contrast of every accent
    against the background, at every depth</span></div>
    <div class="card"><b>3 depths</b><span>true color, xterm-256 and
    ANSI 16, all derived from one spec: colors.json</span></div>
  </div>
  {invariants}
  <p class="caption" style="margin-top:14px">Tritanopia (about 0.01% of the
  population) is simulated and reported but not a hard constraint.</p>
</div></section>

<section id="method"><div class="wrap">
  <h2>method</h2>
  <ol class="method">
    <li>backgrounds and text sit on fixed CIELAB lightness steps;
    accents are optimization variables;</li>
    <li>accents are confined to gruvbox hue sectors and a lightness
    corridor, so the earthy character is a constraint, not an accident;</li>
    <li>dichromacy is simulated in linear sRGB: Viénot 1999 for protan
    and deutan, Brettel 1997 for tritan;</li>
    <li>an optimizer maximizes the minimum pairwise CIEDE2000 across
    visions: farthest-point seeding, coordinate ascent, multi-start;</li>
    <li>an aesthetic pass pulls every color back toward its gruvbox
    anchor while the guarantee holds;</li>
    <li>a regression gate re-checks all of it on every build.</li>
  </ol>
</div></section>

<section id="science"><div class="wrap">
  <h2>standing on published work</h2>
  <ul class="refs">{refs_html}</ul>
</div></section>

<section id="get"><div class="wrap">
  <h2>get it</h2>
  <div class="apps">
    <a class="app" href="vim.html"><b>vim / neovim</b>
    <span>one file, both themes, true-color with a computed 256-color
    fallback, terminal palettes included</span></a>
    <a class="app" href="wezterm.html"><b>WezTerm</b>
    <span>two TOML schemes, dark and light, with the optimized
    ANSI 16 palette</span></a>
    <a class="app" href="mc.html"><b>Midnight Commander</b>
    <span>four skins: dark and light, true color plus an xterm-256
    fallback solved on the grid</span></a>
    <a class="app" href="ranger.html"><b>ranger</b>
    <span>one colorscheme for both themes, driven by the terminal
    ANSI palette</span></a>
    <span class="app ghost"><b>your app next</b>
    <span>the palette is data - ports are generated, not hand-made</span></span>
  </div>
</div></section>

<footer><div class="wrap">
  <span>enot is the Russian word for raccoon: grey fur, a high-contrast
  mask - neutral backgrounds, distinguishable accents. Read it backwards:
  tone.</span>
  <span>Generated from colors.json. No hand-picked colors.</span>
</div></footer>
<script>{JS.substitute(data=json.dumps(data))}</script>
</body>
</html>"""


def app_page(v, data, app, title, body):
    dark = data["enot"]["dark"]["normal"]
    root_vars = "; ".join(f"--{k}: {h}" for k, h in dark.items())
    root_vars += "; " + "; ".join(
        f"--gruv{i}: {h}" for i, h in enumerate(data["gruvbox"]["dark"]["normal"]))
    return head(f"enot for {title}", f"Install the enot colorscheme in {title}.",
                root_vars, f"{app}.html") + top() + f"""
<div class="hero wrap">
  <h1>enot for {title}</h1>
  <div class="tail" aria-hidden="true">{"".join(f'<i style="background:var(--{r})"></i>' for r in ACCENTS)}</div>
  {controls()}
  {EDITOR}
</div>
<section><div class="wrap"><div class="steps">{body}</div></div></section>
<footer><div class="wrap">
  <span><a href="index.html">&larr; enot</a> - an earthy colorscheme that
  survives color blindness.</span>
</div></footer>
<script>{JS.substitute(data=json.dumps(data))}</script>
</body>
</html>"""


VIM_BODY = """
<h3>1. download</h3>
<p><a href="enot.vim" download>enot.vim</a> - one file, both themes.</p>
<h3>2. install</h3>
<pre class="snippet">mkdir -p ~/.vim/colors &amp;&amp; cp enot.vim ~/.vim/colors/
# neovim:
mkdir -p ~/.config/nvim/colors &amp;&amp; cp enot.vim ~/.config/nvim/colors/</pre>
<h3>3. enable</h3>
<pre class="snippet">set termguicolors
set background=dark   " or light
colorscheme enot</pre>
<h3>notes</h3>
<p>True color is the primary mode; a 256-color fallback is built in,
taken from the xterm-256 depth of the spec - solved by the same
optimizer, not nearest-color quantization. Terminal palettes
(g:terminal_ansi_colors for vim, g:terminal_color_0..15 for neovim) ship
with the optimized ANSI 16 set.</p>
"""

WEZTERM_BODY = """
<h3>1. download</h3>
<p><a href="enot-dark.toml" download>enot-dark.toml</a> and
<a href="enot-light.toml" download>enot-light.toml</a>.</p>
<h3>2. install</h3>
<pre class="snippet">mkdir -p ~/.config/wezterm/colors
cp enot-dark.toml enot-light.toml ~/.config/wezterm/colors/</pre>
<h3>3. enable</h3>
<pre class="snippet">-- ~/.wezterm.lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.color_scheme = 'enot-dark'   -- or 'enot-light'

return config</pre>
<p>If you already have a config, add the color_scheme line to it -
do not paste a return statement into the middle of the file: in Lua,
return must be the last statement of the chunk.</p>
<h3>follow the OS appearance</h3>
<pre class="snippet">-- wezterm.gui is nil when the mux server evaluates the config
local function get_appearance()
  if wezterm.gui then
    return wezterm.gui.get_appearance()
  end
  return 'Dark'
end
config.color_scheme = get_appearance():find('Dark')
    and 'enot-dark' or 'enot-light'</pre>
<h3>notes</h3>
<p>The ANSI 16 palette in these schemes is optimized separately from the
syntax accents: neutral slots spread along the lightness axis, six color
families in two disjoint lightness tiers, minimum pairwise
&Delta;E00 of 7.2 across simulated visions.</p>
"""


MC_BODY = """
<h3>1. download</h3>
<p><a href="enot-dark-16M.ini" download>enot-dark-16M.ini</a> and
<a href="enot-light-16M.ini" download>enot-light-16M.ini</a> - true color;
<a href="enot-dark256.ini" download>enot-dark256.ini</a> and
<a href="enot-light256.ini" download>enot-light256.ini</a> - the xterm-256
fallback.</p>
<h3>2. install</h3>
<pre class="snippet">mkdir -p ~/.local/share/mc/skins
cp enot-*.ini ~/.local/share/mc/skins/</pre>
<h3>3. enable</h3>
<pre class="snippet">mc -S enot-dark-16M     # or enot-light-16M
# or permanently: Options &gt; Appearance &gt; enot-dark-16M</pre>
<h3>notes</h3>
<p>The -16M skins need mc &ge; 4.8.19 built with S-Lang and a terminal
that advertises COLORTERM=truecolor. mc does not degrade a skin color
by color: on a terminal without true color it falls back to the default
skin entirely - that is what the 256 variants are for. They carry the
xterm-256 depth of the spec, solved by the same optimizer (see the
invariants table on the front page). Hotkeys and dialog titles are
encoded with underline and bold rather than accent colors: shape
survives any vision.</p>
"""

RANGER_BODY = """
<h3>1. download</h3>
<p><a href="enot.py" download>enot.py</a> - one file, both themes.</p>
<h3>2. install</h3>
<pre class="snippet">mkdir -p ~/.config/ranger/colorschemes
cp enot.py ~/.config/ranger/colorschemes/</pre>
<h3>3. enable</h3>
<pre class="snippet"># ~/.config/ranger/rc.conf
set colorscheme enot</pre>
<h3>notes</h3>
<p>The scheme addresses the terminal palette by index (ANSI 0-15 plus
the terminal default), so one file serves dark and light and follows
whatever palette the terminal provides. Pair it with the enot WezTerm
schemes - or any terminal carrying the enot ANSI 16 set - to get the
guaranteed palette. Requires ranger &ge; 1.9.3.</p>
"""


def llms_txt():
    b = BASE_URL
    return f"""# enot

> An earthy color scheme for vim, WezTerm, Midnight Commander and
> ranger: dark and light themes, gruvbox character, built in CIELAB
> and machine-checked to stay distinguishable under color blindness -
> minimum pairwise CIEDE2000 of 8.3 between syntax accents and 7.2
> across the 16 ANSI colors, verified against simulated protanopia
> and deuteranopia.

The name is the Russian word for raccoon; every color is generated by
an optimizer, none are hand-picked. Dichromacy is simulated with
Viénot 1999 and Brettel 1997 matrices in linear sRGB; a regression
gate fails the build if any guarantee drops.

## Scheme files

- [enot.vim]({b}enot.vim): vim/neovim colorscheme, dark and light in one file
- [enot-dark.toml]({b}enot-dark.toml): WezTerm scheme, dark
- [enot-light.toml]({b}enot-light.toml): WezTerm scheme, light
- [enot-dark-16M.ini]({b}enot-dark-16M.ini) and
  [enot-light-16M.ini]({b}enot-light-16M.ini): mc skins, true color
- [enot-dark256.ini]({b}enot-dark256.ini) and
  [enot-light256.ini]({b}enot-light256.ini): mc skins, xterm-256 fallback
- [enot.py]({b}enot.py): ranger colorscheme, both themes via the
  terminal ANSI palette
- [colors.json]({b}colors.json): the color spec - roles at three depths
  (true color, xterm-256, ANSI 16) with measured invariant metrics

## Documentation

- [Install for vim / neovim]({b}vim.html)
- [Install for WezTerm]({b}wezterm.html)
- [Install for Midnight Commander]({b}mc.html)
- [Install for ranger]({b}ranger.html)
- [Homepage with live dichromacy simulation]({b})

## Optional

- [llms-full.txt]({b}llms-full.txt): full documentation and all palette values
"""


def llms_full(v):
    lines = ["# enot - full reference", ""]
    with open("docs/enot.en.md") as f:
        doc = f.read().strip()
    if doc.startswith("# "):  # we ship our own H1, the doc body suffices
        doc = doc.split("\n", 1)[1].strip()
    lines.append(doc)
    lines.append("\n## Palette values (sRGB hex; accents also as CIELAB LCh)\n")
    for mode in ("dark", "light"):
        lines.append(f"### {mode} theme\n")
        theme = v[mode]
        for k in ROLE_KEYS:
            lch = theme.get("_lch", {}).get(k)
            suffix = (f" (L* {lch[0]}, C* {lch[1]}, h {lch[2]})"
                      if lch else "")
            lines.append(f"- {k}: {theme[k]}{suffix}")
        lines.append("")
        lines.append(f"### {mode} theme, ANSI 16\n")
        order = ["black", "red", "green", "yellow", "blue", "magenta",
                 "cyan", "white"]
        for n in order + ["br_" + n for n in order]:
            lines.append(f"- {n}: {v['ansi'][mode][n]}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    from check import CHECKS
    with open("palettes.json") as f:
        v = next(x for x in json.load(f) if x["slug"] == SLUG)
    with open("colors.json") as f:
        spec = json.load(f)
    data = build_data(v)
    os.makedirs("site", exist_ok=True)
    pages = {
        "index.html": index_html(v, data, spec, CHECKS),
        "vim.html": app_page(v, data, "vim", "vim / neovim", VIM_BODY),
        "wezterm.html": app_page(v, data, "wezterm", "WezTerm", WEZTERM_BODY),
        "mc.html": app_page(v, data, "mc", "Midnight Commander", MC_BODY),
        "ranger.html": app_page(v, data, "ranger", "ranger", RANGER_BODY),
    }
    for name, html in pages.items():
        with open(f"site/{name}", "w") as f:
            f.write(html)
        print(f"site/{name}")
    for src in ("vim/colors/enot.vim", "wezterm/enot-dark.toml",
                "wezterm/enot-light.toml", "mc/enot-dark-16M.ini",
                "mc/enot-light-16M.ini", "mc/enot-dark256.ini",
                "mc/enot-light256.ini", "ranger/colorschemes/enot.py",
                "colors.json"):
        shutil.copy(src, "site/")
    with open("site/.nojekyll", "w") as f:
        f.write("")
    with open("site/llms.txt", "w") as f:
        f.write(llms_txt())
    with open("site/llms-full.txt", "w") as f:
        f.write(llms_full(v))
    print("site/enot.vim site/enot-*.toml site/enot-*.ini site/enot.py "
          "site/colors.json")
    print("site/llms.txt site/llms-full.txt")


if __name__ == "__main__":
    main()
