#!/usr/bin/env python3
"""Build index.html for the Sightwell brand guideline site.

- embeds Archivo Expanded (stand-in for Pragmatica Extended) as base64 woff2
- converts the Figma logo export into two <symbol>s (#sw-logo, #sw-logo-mono)
- wraps everything in a full HTML document with the Adobe Fonts (Typekit) link
"""
import base64
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
TYPEKIT = "https://use.typekit.net/qcx2rwd.css"
# official logo artwork; the inline symbol drives the sidebar, footer and web mockup
LOGO_SRC = "logo_cream_ember.svg"
CREAM, AMBER = "#FDFAF6", "#E2A951"
# key -> source file; embedded so downloads work on any protocol (file://, http, sandbox)
LOGO_FILES = {
    "cream-amber": "logo_cream_ember.svg",
    "ink-amber": "logo_ink_ember.svg",
    "all-ink": "logo_all ink.svg",
    "all-cream": "logo_all cream.svg",
}
ARCHIVO = ("https://fonts.googleapis.com/css2?"
           "family=Archivo:wdth,wght@125,500;125,600&display=swap")


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read() if binary else r.read().decode("utf-8")


def build_fonts():
    """Embed the latin subset of Archivo Expanded as data URIs."""
    css = fetch(ARCHIVO)
    faces, seen = [], set()
    parts = re.split(r"/\*\s*([a-z0-9\-]+)\s*\*/", css)
    for i in range(1, len(parts) - 1, 2):
        subset, block = parts[i], parts[i + 1]
        if subset != "latin":
            continue
        weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
        url = re.search(r"src:\s*url\(([^)]+)\)", block).group(1)
        if weight in seen:
            continue
        seen.add(weight)
        data = fetch(url, binary=True)
        b64 = base64.b64encode(data).decode()
        faces.append(
            "@font-face{font-family:'Archivo Expanded';font-style:normal;"
            f"font-weight:{weight};font-display:swap;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
        print(f"  embedded Archivo Expanded {weight} ({len(data)//1024}KB)", file=sys.stderr)
    return "\n".join(faces)


def build_logo():
    """Turn the Figma SVG export into two recolorable symbols."""
    svg = (ROOT / "assets" / LOGO_SRC).read_text(encoding="utf-8")
    head, inner = svg.split(">", 1)
    inner = inner.rsplit("</svg>", 1)[0]
    m = re.search(r'viewBox="([^"]+)"', head)
    vb = m.group(1) if m else "0 0 291 103"
    # two-color: wordmark follows currentColor, rule stays amber
    duo = inner.replace(f'fill="{CREAM}"', 'fill="currentColor"')
    # single-color: everything follows currentColor
    mono = duo.replace(f'fill="{AMBER}"', 'fill="currentColor"')
    return (
        '<svg width="0" height="0" aria-hidden="true" focusable="false" '
        'style="position:absolute">\n'
        f'<symbol id="sw-logo" viewBox="{vb}">{duo}</symbol>\n'
        f'<symbol id="sw-logo-mono" viewBox="{vb}">{mono}</symbol>\n'
        "</svg>"
    )


def build_logo_files():
    """Embed each logo's SVG source so the download works without a network fetch."""
    blocks = []
    for key, name in LOGO_FILES.items():
        svg = (ROOT / "assets" / name).read_text(encoding="utf-8").strip()
        assert "</script" not in svg.lower(), f"{name} would break the script block"
        blocks.append(
            f'<script type="text/plain" id="logosrc-{key}">{svg}</script>'
        )
        print(f"  embedded {name} ({len(svg)//1024}KB) as {key}", file=sys.stderr)
    return "\n".join(blocks)


def main():
    html = (SRC / "page.html").read_text(encoding="utf-8")

    print("fonts:", file=sys.stderr)
    html = html.replace("/*__FONTS__*/", build_fonts())

    logo = build_logo()
    assert "<!--LOGO_DEFS-->" in html, "logo placeholder missing"
    html = html.replace("<!--LOGO_DEFS-->", logo)
    print(f"  logo symbols ({len(logo)//1024}KB)", file=sys.stderr)

    print("logo downloads:", file=sys.stderr)
    assert "<!--LOGO_FILES-->" in html, "logo files placeholder missing"
    html = html.replace("<!--LOGO_FILES-->", build_logo_files())

    head, body = html.split("</style>", 1)
    head += "</style>"
    doc = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<link rel="stylesheet" href="{TYPEKIT}">\n'
        f"{head}\n</head>\n<body>\n{body.lstrip()}\n</body>\n</html>\n"
    )
    out = ROOT / "index.html"
    out.write_text(doc, encoding="utf-8")
    print(f"\nwrote {out}  ({len(doc)//1024}KB)", file=sys.stderr)

    assert doc.count("<body>") == 1
    assert 'id="sw-logo"' in doc and "use.typekit.net" in doc
    print("checks passed", file=sys.stderr)


if __name__ == "__main__":
    main()
