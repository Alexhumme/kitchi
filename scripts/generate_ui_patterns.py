"""Genera los tiles PNG de la identidad "juguete" (Flet web, sin Pillow en runtime).

Los patrones se producen una sola vez y se cachean como assets; la app solo los
referencia. Transparentes sobre el color de fondo que ve el usuario.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "frontend" / "assets" / "ui"
INK = (32, 27, 42, 255)            # TINTA
CORAL = (255, 107, 107, 255)


def new(size, bg=(0, 0, 0, 0)):
    return Image.new("RGBA", size, bg)


def save(image: Image.Image, folder: str, name: str) -> None:
    path = OUT / folder / f"{name}.png"
    image.save(path, "PNG")
    print("saved", path.relative_to(OUT.parent.parent))


def alpha_rgba(rgb, alpha):
    return (rgb[0], rgb[1], rgb[2], alpha)


# --- patrones ---------------------------------------------------------------
def dots_soft():
    img = new((48, 48))
    d = ImageDraw.Draw(img)
    for cx, cy in ((12, 12), (36, 36)):
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=alpha_rgba(INK, 30))
    for cx, cy in ((36, 12), (12, 36)):
        d.ellipse((cx - 2.5, cy - 2.5, cx + 2.5, cy + 2.5), fill=alpha_rgba(INK, 22))
    save(img, "patterns", "dots_soft")


def dots_light():
    img = new((48, 48))
    d = ImageDraw.Draw(img)
    for cx, cy in ((12, 12), (36, 36)):
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=alpha_rgba((255, 255, 255, 255), 160))
    for cx, cy in ((36, 12), (12, 36)):
        d.ellipse((cx - 2.5, cy - 2.5, cx + 2.5, cy + 2.5), fill=alpha_rgba((255, 255, 255, 255), 120))
    save(img, "patterns", "dots_light")


def dots_dense():
    img = new((36, 36))
    d = ImageDraw.Draw(img)
    for y in range(0, 36, 9):
        for x in range(0, 36, 9):
            off = 4 if (y // 9) % 2 else 0
            d.ellipse((x + off - 1.6, y - 1.6, x + off + 1.6, y + 1.6), fill=alpha_rgba(INK, 38))
    save(img, "patterns", "dots_dense")


def checker_soft():
    img = new((32, 32))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 15, 15), fill=alpha_rgba(INK, 26))
    d.rectangle((16, 16, 31, 31), fill=alpha_rgba(INK, 26))
    save(img, "patterns", "checker_soft")


def crosshatch():
    img = new((32, 32))
    d = ImageDraw.Draw(img)
    for i in range(-32, 64, 10):
        d.line([(i, 0), (i + 32, 32)], fill=alpha_rgba(INK, 34), width=2)
        d.line([(i + 32, 0), (i, 32)], fill=alpha_rgba(INK, 34), width=2)
    save(img, "patterns", "crosshatch")


def stars_spark():
    img = new((64, 64))
    d = ImageDraw.Draw(img)

    def star(cx, cy, r, alpha):
        d.polygon(
            [
                (cx, cy - r), (cx + r * 0.28, cy - r * 0.35), (cx + r, cy - r * 0.15),
                (cx + r * 0.45, cy + r * 0.12), (cx + r * 0.75, cy + r * 0.75),
                (cx, cy + r * 0.32), (cx - r * 0.75, cy + r * 0.75),
                (cx - r * 0.45, cy + r * 0.12), (cx - r, cy - r * 0.15),
                (cx - r * 0.28, cy - r * 0.35),
            ],
            fill=alpha_rgba(INK, alpha),
        )

    star(13, 13, 4.5, 70)
    star(48, 48, 4.5, 70)
    star(48, 13, 2.7, 55)
    star(13, 48, 2.7, 55)
    save(img, "patterns", "stars_spark")


def bubbles_soft():
    img = new((48, 48))
    d = ImageDraw.Draw(img)
    for x, y, r in ((11, 11, 4.5), (37, 15, 3), (23, 30, 5.5), (12, 42, 2.7), (42, 39, 2)):
        d.ellipse((x - r, y - r, x + r, y + r), outline=alpha_rgba(INK, 40), width=2)
    save(img, "patterns", "bubbles_soft")


def grain():
    img = new((32, 32))
    d = ImageDraw.Draw(img)
    import random

    random.seed(7)
    for _ in range(260):
        x, y = random.randrange(32), random.randrange(32)
        d.point((x, y), fill=alpha_rgba(INK, random.randrange(10, 30)))
    save(img, "patterns", "grain")


def diagonal_stripes():
    img = new((32, 32))
    d = ImageDraw.Draw(img)
    for i in range(-32, 64, 12):
        d.line([(i, 0), (i + 32, 32)], fill=alpha_rgba(INK, 34), width=5)
    save(img, "patterns", "diagonal_stripes")


# --- separadores ------------------------------------------------------------
def zigzag():
    img = new((96, 14))
    d = ImageDraw.Draw(img)
    pts = []
    for x in range(0, 96 + 8, 8):
        pts.append((x, 10))
        pts.append((x + 4, 3))
    d.line(pts, fill=alpha_rgba(INK, 235), width=3, joint="curve")
    save(img, "separators", "zigzag")


def waves():
    img = new((96, 14))
    d = ImageDraw.Draw(img)
    for amp, phase in ((5, 0), (5, 48)):
        pts = [(x, 7 + amp * math.sin((x + phase) * math.tau / 24)) for x in range(96 + 1)]
        d.line(pts, fill=alpha_rgba(INK, 225), width=3)
    save(img, "separators", "waves")


def rainbow():
    img = new((96, 11))
    d = ImageDraw.Draw(img)
    bands = [
        ((255, 209, 102, 255), 2),
        ((255, 107, 107, 255), 2),
        ((112, 214, 193, 255), 2),
        ((132, 113, 255, 255), 2),
    ]
    y = 0
    for color, h in bands:
        d.rectangle((0, y, 96, y + h - 1), fill=color)
        y += h
    d.rectangle((0, 0, 96, 0), fill=alpha_rgba(INK, 220))
    d.rectangle((0, 8, 96, 8), fill=alpha_rgba(INK, 220))
    save(img, "separators", "rainbow")


def hourglass_wave():
    img = new((96, 16))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 1, 96, 2), fill=alpha_rgba(INK, 200))
    d.rectangle((0, 13, 96, 14), fill=alpha_rgba(INK, 200))
    for x in range(0, 96, 16):
        cy = 8 + 3 * math.sin(x * math.tau / 32)
        d.ellipse((x, cy - 1.5, x + 3, cy + 1.5), fill=alpha_rgba(INK, 150))
    save(img, "separators", "hourglass")


def bubble_row():
    img = new((96, 12))
    d = ImageDraw.Draw(img)
    for i in range(0, 96, 12):
        d.ellipse((i, 4, i + 5, 8), fill=alpha_rgba(INK, 210))
    save(img, "separators", "bubbles")


def main():
    print("Generando patrones UI en", OUT)
    for name, func in [
        ("dots_soft", dots_soft), ("dots_light", dots_light), ("dots_dense", dots_dense),
        ("checker_soft", checker_soft), ("crosshatch", crosshatch),
        ("stars_spark", stars_spark), ("bubbles_soft", bubbles_soft),
        ("grain", grain), ("diagonal_stripes", diagonal_stripes),
    ]:
        func()
    for name, func in [
        ("zigzag", zigzag), ("waves", waves), ("rainbow", rainbow),
        ("hourglass", hourglass_wave), ("bubbles", bubble_row),
    ]:
        func()


if __name__ == "__main__":
    main()
