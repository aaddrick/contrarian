#!/usr/bin/env python3
"""Draw the social preview card at .github/assets/social-preview.png (1280x640).

The card is the agent's argument in one picture: a room that agrees, and the
one finding that says why it shouldn't. It uses the poster's graphite + copper
palette and fonts.

    python3 scripts/make_card.py

Needs Pillow, Public Sans and IBM Plex Mono (found with fc-match). CI does not
run this. GitHub reads the social preview only from Settings > General >
Social preview, so upload the PNG there by hand after regenerating it.
"""

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".github" / "assets" / "social-preview.png"
W, H = 1280, 640

BG_TOP, BG_BOTTOM = (26, 27, 30), (36, 38, 42)  # base900 -> base800
PANEL, PANEL_LINE = (48, 52, 58), (70, 75, 83)   # base700
COPPER, COPPER_SOFT = (176, 91, 51), (226, 184, 156)
WHITE, MUTED, FAINT = (243, 244, 246), (175, 181, 190), (120, 128, 138)
GREEN = (120, 170, 130)


def font(family: str, size: int) -> ImageFont.FreeTypeFont:
    path = subprocess.run(["fc-match", "-f", "%{file}", family],
                          capture_output=True, text=True, check=True).stdout
    return ImageFont.truetype(path, size)


def main() -> None:
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM)))

    # Copper glow behind the finding, as on the poster's header band.
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([700, 120, 1300, 620], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(Image.new("RGB", (W, H), COPPER), mask=glow)
    d = ImageDraw.Draw(img)

    eyebrow = font("IBM Plex Mono:weight=medium", 18)
    title = font("Public Sans:style=ExtraBold", 84)
    sub = font("Public Sans", 30)
    mono = font("IBM Plex Mono", 21)
    mono_b = font("IBM Plex Mono:style=SemiBold", 21)
    foot = font("Public Sans", 19)

    x = 72
    ex = x
    for ch in "AGENT SKILL · SUBAGENT":  # letterspaced, as on the poster
        d.text((ex, 150), ch, font=eyebrow, fill=FAINT)
        ex += d.textlength(ch, font=eyebrow) + 4
    d.text((x, 186), "The Helpful", font=title, fill=WHITE)
    d.text((x, 280), "Contrarian", font=title, fill=COPPER)
    d.rectangle([x, 392, x + 64, 396], fill=COPPER)
    d.text((x, 418), "Stress-test plans before", font=sub, fill=MUTED)
    d.text((x, 456), "reality does.", font=sub, fill=MUTED)
    d.text((x, 566), "Claude Code · Codex · Cursor · Gemini · Copilot · +12 more", font=foot, fill=FAINT)

    # The finding card.
    cx, cy, cw, ch = 700, 150, 508, 340
    d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=14, fill=PANEL, outline=PANEL_LINE, width=2)
    d.rounded_rectangle([cx, cy, cx + 6, cy + ch], radius=3, fill=COPPER)
    px = cx + 34
    d.text((px, cy + 30), "consensus:", font=mono, fill=FAINT)
    d.text((px + 150, cy + 30), "ship it", font=mono, fill=MUTED)
    d.text((cx + cw - 34, cy + 30), "6/6 agree", font=mono, fill=GREEN, anchor="ra")
    d.line([(px, cy + 78), (cx + cw - 34, cy + 78)], fill=PANEL_LINE, width=1)

    badge = "MAJOR"
    bw = d.textlength(badge, font=mono_b) + 24
    d.rounded_rectangle([px, cy + 100, px + bw, cy + 134], radius=4, fill=COPPER)
    d.text((px + 12, cy + 104), badge, font=mono_b, fill=WHITE)
    d.text((px + bw + 14, cy + 104), "pre-mortem, month six", font=mono, fill=WHITE)

    rows = [("assumes:", "traffic stays flat"),
            ("fails if:", "the launch works"),
            ("instead:", "load-test at 10x first")]
    for i, (k, v) in enumerate(rows):
        y = cy + 162 + i * 40
        d.text((px, y), k, font=mono, fill=COPPER_SOFT)
        d.text((px + 130, y), v, font=mono, fill=MUTED)

    d.text((px, cy + ch - 46), "verdict:", font=mono, fill=FAINT)
    d.text((px + 130, cy + ch - 46), "investigate first", font=mono_b, fill=COPPER_SOFT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
