#!/usr/bin/env python3
"""Draw the social preview card and the icon into .github/assets/.

The picture is the agent's argument: a school of graphite fish swimming one
way, and one copper fish with a raised brow swimming the other. Writes
social-preview.svg (1280x640) and icon.svg (512x512), then renders each to PNG
(the icon at 1024x1024).

    python3 scripts/make_card.py

Needs Inkscape on PATH, and Public Sans and IBM Plex Mono installed for the
card's text. CI does not run this. GitHub reads the social preview only from
Settings > General > Social preview, so upload the PNG there by hand after
regenerating it.
"""

import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / ".github" / "assets"

# One fish facing right, nose at x=50, tail tips at x=-63.
BODY = "M50,2 C44,-16 22,-26 -2,-25 C-20,-24 -32,-12 -38,0 C-32,10 -20,20 0,21 C24,22 44,14 50,2 Z"
DORSAL = "M-8,-24 C-2,-40 14,-40 24,-22 Z"
VENTRAL = "M-6,19 C-2,29 8,31 14,20 Z"
TAIL = "M-34,-2 C-44,-10 -52,-22 -63,-28 C-58,-11 -56,-3 -51,1 C-56,5 -58,14 -63,27 C-52,21 -44,10 -34,3 Z"
BELLY = "M48,5 C40,15 22,21 0,21 C-18,21 -30,11 -37,2 C-20,8 12,11 48,5 Z"
GILL = "M19,-18 C11,-6 11,8 19,16"

# (body, belly, fins, lines)
GREYS = [("#464b53", "#535860", "#3a3e45", "#33373d"),
         ("#4d525a", "#5a5f68", "#40444b", "#383c42"),
         ("#41464d", "#4d525a", "#363a40", "#2f3338")]
COPPER = ("#b05b33", "#c97a50", "#8f4524", "#7a3a1d")

DEFS = """<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1b1e"/><stop offset="1" stop-color="#24262a"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#b05b33" stop-opacity=".3"/><stop offset="1" stop-color="#b05b33" stop-opacity="0"/></radialGradient>
</defs>"""


def fish(x, y, s, body, belly, fin, line, left=False, rot=0, hero=False):
    if hero:
        # Half-lidded eye under one raised brow: skeptical, not angry.
        eye = ('<circle cx="33" cy="-5" r="6.8" fill="#f3e6dc"/><circle cx="35.5" cy="-4" r="3.6" fill="#1a1b1e"/>'
               f'<path d="M25.5,-7.5 A7.6,7.6 0 0 1 40.5,-8.5 Z" fill="{body}"/>'
               f'<path d="M25.5,-7.5 L40.5,-8.5" stroke="{line}" stroke-width="1.8" stroke-linecap="round"/>'
               f'<path d="M25,-14.5 Q32,-21.5 41,-15.5" fill="none" stroke="{line}" stroke-width="3" stroke-linecap="round"/>')
    else:
        eye = '<circle cx="33" cy="-5" r="3.6" fill="#1a1b1e"/>'
    sx = -s if left else s
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({sx:.3f},{s:.3f})">'
            f'<path d="{TAIL}" fill="{fin}"/><path d="{DORSAL}" fill="{fin}"/><path d="{VENTRAL}" fill="{fin}"/>'
            f'<path d="{BODY}" fill="{body}"/><path d="{BELLY}" fill="{belly}"/>'
            f'<path d="{GILL}" fill="none" stroke="{line}" stroke-width="2" stroke-linecap="round"/>{eye}</g>')


def contrarian(x, y, s):
    """The copper fish, swimming left, nose tipped up, with a short wake behind it."""
    wake = "".join(f'<path d="M{x + s * 62 + i * 16},{y - 10 + i * 10} q8,-4 16,0" fill="none" stroke="#b05b33" '
                   f'stroke-opacity="{.5 - i * .13:.2f}" stroke-width="2.5" stroke-linecap="round"/>' for i in range(3))
    return wake + fish(x, y, s, *COPPER, left=True, rot=6, hero=True)


def school(rng, x0, y0, cols, rows, dx, dy, skip, scale):
    out = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) in skip:
                continue
            out.append(fish(x0 + c * dx + (dx / 2 if r % 2 else 0) + rng.uniform(-8, 8),
                            y0 + r * dy + rng.uniform(-6, 6),
                            scale * rng.uniform(.8, .95), *rng.choice(GREYS)))
    return "".join(out)


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{body}</svg>\n'


def card():
    rng = random.Random(7)  # fixed, so the school is the same on every run
    cx, cy = 950, 320
    return svg(1280, 640, f"""<rect width="1280" height="640" fill="url(#bg)"/>
<ellipse cx="{cx}" cy="{cy}" rx="260" ry="220" fill="url(#glow)"/>
{school(rng, 700, 160, 5, 5, 112, 80, {(2, 2), (2, 3)}, 0.95)}{contrarian(cx, cy, 1.3)}
<g font-family="Public Sans">
<text x="72" y="236" font-family="IBM Plex Mono" font-weight="500" font-size="18" letter-spacing="4" fill="#78808a">AGENT SKILL · SUBAGENT</text>
<text x="72" y="334" font-weight="800" font-size="96" fill="#f3f4f6">Contrarian</text>
<rect x="72" y="366" width="64" height="4" fill="#b05b33"/>
<text x="72" y="420" font-size="30" fill="#afb5be">Stress-test plans before</text>
<text x="72" y="458" font-size="30" fill="#afb5be">reality does.</text>
<text x="72" y="584" font-size="19" fill="#78808a">Claude Code · Codex · Cursor · Gemini · Copilot · +12 more</text>
</g>""")


def icon():
    return svg(512, 512, '<rect width="512" height="512" rx="96" fill="#1f2024"/>'
               + fish(300, 130, 1.55, *GREYS[1]) + fish(300, 384, 1.55, *GREYS[1])
               + fish(215, 256, 1.9, *COPPER, left=True, rot=6, hero=True))


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    # The icon renders at 2x (1024px) so it stays sharp on high-DPI screens.
    for name, text, width in [("social-preview", card(), 1280), ("icon", icon(), 1024)]:
        src = ASSETS / f"{name}.svg"
        src.write_text(text, encoding="utf-8")
        subprocess.run(["inkscape", str(src), "-w", str(width), "-o", str(src.with_suffix(".png"))],
                       check=True, capture_output=True)
        print(src.with_suffix(".png"))


if __name__ == "__main__":
    main()
