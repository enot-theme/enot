"""Telegram Desktop theme package: a zip of the palette rendered from
theme.tdesktop-theme.tmpl plus a solid bg0 tiled background. The
background is what removes the stock wallpaper - a plain palette file
would leave the doodle pattern under the bubbles. The zip is
deterministic (fixed timestamps, stored entries) so the CI diff gate
holds; stored text keeps the palette scannable by the hex conformance
check."""

import io
import os
import struct
import zipfile
import zlib
from string import Template

from build import namespace

HERE = os.path.dirname(os.path.abspath(__file__))
TILE = 100


def solid_png(hex_color, size=TILE):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    raw = (b"\x00" + bytes((r, g, b)) * size) * size

    def chunk(tag, data):
        body = tag + data
        return (struct.pack(">I", len(data)) + body
                + struct.pack(">I", zlib.crc32(body) & 0xffffffff))

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def theme_zip(palette_text, png):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
        for name, data in (("colors.tdesktop-theme", palette_text.encode()),
                           ("tiled.png", png)):
            z.writestr(zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0)),
                       data)
    return buf.getvalue()


def render(spec):
    tmpl = Template(
        open(os.path.join(HERE, "theme.tdesktop-theme.tmpl")).read())
    out = {}
    for theme in ("dark", "light"):
        t = spec["themes"][theme]
        text = tmpl.substitute(namespace(theme, t))
        out[f"telegram/enot-{theme}.tdesktop-theme"] = theme_zip(
            text, solid_png(t["roles"]["bg0"]["hex"]))
    return out
