#!/usr/bin/env python3
"""Generate card-style icons for liberating.it adaptations not on the official LS menu."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "images" / "structures"
MANIFEST_PATH = ICON_DIR / "manifest.json"
ICON_SIZE = (222, 336)
LS_MENU_ICON_SLUG = "ls-menu"
LS_MENU_ICON_REL = f"assets/images/structures/{LS_MENU_ICON_SLUG}.png"
LS_MENU_ICON_SPEC = {
    "lines": ["LS", "Menu"],
    "shape": "dots",
}
ICON_INK = "#1a2329"
ICON_CARD = "#ffffff"
ICON_BORDER = "#1a2329"

ADAPTATIONS: dict[str, dict[str, str]] = {
    "triz": {
        "lines": ["TRIZ", "inverti"],
        "shape": "diamond",
    },
    "open-space-technology-ost": {
        "lines": ["Open", "Space"],
        "shape": "circle",
    },
    "4-2-1-storming": {
        "lines": ["4-2-1", "Storming"],
        "shape": "stack",
    },
    "liquid-courage": {
        "lines": ["Liquid", "Courage"],
        "shape": "wave",
    },
    "mad-love": {
        "lines": ["Mad", "Love"],
        "shape": "heart",
    },
    "pixies-reflection": {
        "lines": ["Pixies", "Reflect"],
        "shape": "spark",
    },
    "tiny-demons": {
        "lines": ["Tiny", "Demons"],
        "shape": "dots",
    },
}


def _font(size: int, *, bold: bool = False):
    from PIL import ImageFont

    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    from PIL import ImageFont

    return ImageFont.load_default()


def _draw_shape(draw, shape: str, ink: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if shape == "diamond":
        draw.polygon([(cx, y0), (x1, cy), (cx, y1), (x0, cy)], fill=ink)
    elif shape == "circle":
        draw.ellipse(box, fill=ink)
    elif shape == "stack":
        h = (y1 - y0) // 4
        for i in range(3):
            inset = i * 10
            draw.rounded_rectangle(
                (x0 + inset, y0 + i * (h + 6), x1 - inset, y0 + i * (h + 6) + h),
                radius=8,
                fill=ink,
            )
    elif shape == "wave":
        for i in range(3):
            yy = y0 + 24 + i * 28
            draw.arc((x0, yy, x1, yy + 40), 20, 160, fill=ink, width=8)
    elif shape == "heart":
        draw.ellipse((x0 + 8, y0 + 8, cx, cy + 8), fill=ink)
        draw.ellipse((cx, y0 + 8, x1 - 8, cy + 8), fill=ink)
        draw.polygon([(x0 + 8, cy), (cx, y1 - 8), (x1 - 8, cy)], fill=ink)
    elif shape == "spark":
        draw.line((cx, y0, cx, y1), fill=ink, width=6)
        draw.line((x0 + 16, cy, x1 - 16, cy), fill=ink, width=6)
        draw.line((x0 + 28, y0 + 24, x1 - 28, y1 - 24), fill=ink, width=4)
        draw.line((x1 - 28, y0 + 24, x0 + 28, y1 - 24), fill=ink, width=4)
    else:
        r = 10
        for row in range(3):
            for col in range(3):
                px = x0 + 18 + col * 28
                py = y0 + 18 + row * 28
                draw.ellipse((px, py, px + r * 2, py + r * 2), fill=ink)


def render_icon(slug: str, spec: dict[str, str], dest: Path) -> None:
    from PIL import Image, ImageDraw

    img = Image.new("RGB", ICON_SIZE, ICON_CARD)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((12, 12, 210, 324), radius=18, fill=ICON_CARD, outline=ICON_BORDER, width=2)
    _draw_shape(draw, spec["shape"], ICON_INK, (48, 56, 174, 188))

    title_font = _font(24, bold=True)
    sub_font = _font(18, bold=True)
    line1, line2 = spec["lines"]
    draw.text((24, 210), line1, fill=ICON_INK, font=title_font)
    draw.text((24, 244), line2, fill=ICON_INK, font=sub_font)

    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "PNG", optimize=True)


def ensure_ls_menu_icon(out_root: Path | None = None) -> str:
    """Generic LS Menu card used when a structure has no dedicated icon."""
    base = out_root or ROOT
    dest = base / LS_MENU_ICON_REL
    render_icon(LS_MENU_ICON_SLUG, LS_MENU_ICON_SPEC, dest)
    return LS_MENU_ICON_REL


def ensure_adaptation_icons(out_root: Path | None = None) -> dict[str, str]:
    """Create adaptation icons and merge them into manifest.json."""
    base = out_root or ROOT
    icon_dir = base / "assets" / "images" / "structures"
    manifest_path = icon_dir / "manifest.json"
    manifest: dict[str, str] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    for slug, spec in ADAPTATIONS.items():
        rel_path = f"assets/images/structures/{slug}.png"
        dest = base / rel_path
        render_icon(slug, spec, dest)
        manifest[slug] = rel_path

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ensure_ls_menu_icon(base)
    return manifest


def main() -> None:
    manifest = ensure_adaptation_icons()
    added = sorted(ADAPTATIONS)
    print(f"Generated {len(added)} adaptation icons -> {MANIFEST_PATH}")
    print(", ".join(added))


if __name__ == "__main__":
    main()
