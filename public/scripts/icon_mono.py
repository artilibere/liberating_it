#!/usr/bin/env python3
"""Convert structure icons to black ink on white background."""

from __future__ import annotations

from PIL import Image

MONO_PIPELINE_VERSION = "mono-v1"
MONO_BLACK = (0, 0, 0)
MONO_WHITE = (255, 255, 255)


def monochrome_structure_icon(img: Image.Image, *, luminance_threshold: int = 235, chroma_threshold: int = 30) -> Image.Image:
    """Render icon as black shapes and text on a white card."""
    rgba = img.convert("RGBA")
    width, height = rgba.size
    output = Image.new("RGB", (width, height), MONO_WHITE)
    pixels = rgba.load()
    out_pixels = output.load()

    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = pixels[x, y]
            if alpha < 16:
                continue
            chroma = max(red, green, blue) - min(red, green, blue)
            luminance = 0.299 * red + 0.587 * green + 0.114 * blue
            if chroma >= chroma_threshold or luminance < luminance_threshold:
                out_pixels[x, y] = MONO_BLACK

    return output


def resize_monochrome_icon(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize without anti-aliasing so icons stay strictly black on white."""
    resized = img.resize(size, Image.Resampling.NEAREST)
    gray = resized.convert("L")
    return gray.point(lambda pixel: 0 if pixel < 128 else 255, mode="1").convert("RGB")
