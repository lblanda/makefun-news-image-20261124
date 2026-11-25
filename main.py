#!/usr/bin/env python3
"""news-image-20261124 — one image summing up the world news of
Tuesday 24 November 2026.

Pure standard library: draws a 1024x1024 editorial news poster with a
hand-written PNG encoder (zlib + CRC, no Pillow) and the 5x7 bitmap font
in font5x7.py, from the stories baked into stories.py.  No network, no
clock, no randomness: two runs write byte-identical files.

The grader runs `python3 -P -s /bot/main.py`, and -P keeps the script
directory off sys.path, so the bootstrap below inserts this file's own
directory before any sibling import.

Output: $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png when the
variable is unset.  The output directory itself is never removed (it may
be a grader mount point); only entry.png inside it is written.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import binascii
import zlib

import font5x7
import stories

W = 1024
H = 1024

# Palette.
NAVY = (13, 27, 46)
NAVY2 = (19, 38, 62)
PAPER = (244, 238, 224)
PAPER2 = (232, 224, 205)
INK = (24, 30, 38)
MUTED = (96, 104, 116)
RED = (196, 58, 43)
GOLD = (212, 160, 23)
TEAL = (31, 122, 109)
WHITE = (255, 255, 255)
SEA = (46, 92, 128)
SKY = (122, 168, 205)


class Canvas:
    """A plain RGB pixel buffer with tiny drawing primitives."""

    def __init__(self, width, height, bg):
        self.width = width
        self.height = height
        self.pixels = bytearray(bg * (width * height))

    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 3
            self.pixels[i] = color[0]
            self.pixels[i + 1] = color[1]
            self.pixels[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            base = (yy * self.width + x) * 3
            for xx in range(w):
                i = base + xx * 3
                self.pixels[i] = color[0]
                self.pixels[i + 1] = color[1]
                self.pixels[i + 2] = color[2]

    def hline(self, x, y, w, color):
        self.rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.rect(x, y, 1, h, color)

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    self.set_pixel(cx + dx, cy + dy, color)

    def disc_outline(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                d = dx * dx + dy * dy
                if (r - 2) * (r - 2) <= d <= r * r:
                    self.set_pixel(cx + dx, cy + dy, color)

    def line(self, x0, y0, x1, y1, color):
        """Bresenham line."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.set_pixel(x, y, color)
            if x == x1 and y == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def text(self, x, y, s, color, scale=1):
        return font5x7.draw_text(self, x, y, s, color, scale)

    def text_centered(self, cx, y, s, color, scale=1):
        w = font5x7.text_width(s, scale)
        return self.text(cx - w // 2, y, s, color, scale)

    def paragraph(self, x, y, s, color, scale, max_chars, line_h):
        """Wrapped paragraph; returns the y below the last line."""
        for line in font5x7.wrap_text(s, max_chars):
            self.text(x, y, line, color, scale)
            y += line_h
        return y


# ---------------------------------------------------------------- icons
# Small schematic pictograms, drawn with the same primitives.  Each one
# fits in a ~120x64 box whose top-left is (x, y).

def icon_chip(c, x, y, color):
    c.rect(x + 28, y + 8, 64, 48, color)
    c.rect(x + 40, y + 20, 40, 24, PAPER)
    c.rect(x + 50, y + 28, 20, 8, color)
    for px in (36, 52, 68, 84):
        c.rect(x + px, y + 0, 6, 8, color)
        c.rect(x + px, y + 56, 6, 8, color)
    for py in (16, 32, 48):
        c.rect(x + 20, y + py, 8, 6, color)
        c.rect(x + 92, y + py, 8, 6, color)


def icon_tanker(c, x, y, color):
    # Containers, hull, funnel, smoke, waves.
    c.rect(x + 14, y + 6, 26, 18, RED)
    c.rect(x + 44, y + 6, 26, 18, GOLD)
    c.rect(x + 74, y + 6, 26, 18, TEAL)
    c.rect(x + 6, y + 26, 108, 16, color)
    c.rect(x + 96, y + 10, 10, 16, color)
    c.circle(x + 101, y + 6, 4, MUTED)
    c.circle(x + 108, y + 2, 3, MUTED)
    for wx in (0, 28, 56, 84):
        c.rect(x + wx, y + 48, 22, 4, SEA)
    for wx in (14, 42, 70, 98):
        c.rect(x + wx, y + 56, 22, 4, SEA)


def icon_warship(c, x, y, color):
    c.rect(x + 10, y + 30, 100, 14, color)
    c.rect(x + 10, y + 30, 100, 4, PAPER2)
    c.rect(x + 52, y + 10, 8, 20, color)
    c.rect(x + 46, y + 4, 20, 6, color)
    c.circle(x + 56, y + 2, 3, RED)
    # A drone above, trailing a dashed path down to the ship.
    c.rect(x + 88, y + 8, 14, 6, INK)
    c.rect(x + 84, y + 6, 4, 10, INK)
    c.rect(x + 102, y + 6, 4, 10, INK)
    for dy in range(18, 28, 4):
        c.rect(x + 94, y + dy, 3, 2, RED)
    for wx in (0, 28, 56, 84):
        c.rect(x + wx, y + 50, 22, 4, SEA)
    for wx in (14, 42, 70, 98):
        c.rect(x + wx, y + 58, 22, 4, SEA)


def icon_tower(c, x, y, color):
    c.rect(x + 44, y + 2, 32, 58, color)
    c.rect(x + 36, y + 14, 8, 46, color)
    c.rect(x + 76, y + 14, 8, 46, color)
    for wy in (10, 22, 34, 46):
        c.rect(x + 50, y + wy, 20, 5, GOLD)
    # Impact burst at the top corner.
    c.circle(x + 84, y + 8, 10, RED)
    c.circle(x + 84, y + 8, 5, GOLD)
    c.rect(x + 96, y + 2, 14, 3, RED)
    c.rect(x + 94, y + 12, 12, 3, RED)


def icon_shop(c, x, y, color):
    c.rect(x + 8, y + 18, 104, 42, color)
    c.rect(x + 8, y + 18, 104, 12, RED)
    for ax in range(8, 112, 16):
        c.rect(x + ax, y + 18, 8, 12, PAPER)
    c.rect(x + 50, y + 38, 20, 22, PAPER)
    c.rect(x + 20, y + 38, 18, 14, SKY)
    c.rect(x + 82, y + 38, 18, 14, SKY)
    # Three people (dots + shoulders) in front of the door.
    for px in (34, 60, 86):
        c.circle(x + px, y + 14, 4, INK)
        c.rect(x + px - 6, y + 14, 12, 4, INK)


def icon_cross(c, x, y, color):
    c.rect(x + 48, y + 4, 24, 56, RED)
    c.rect(x + 28, y + 24, 64, 16, RED)
    c.rect(x + 52, y + 8, 16, 48, WHITE)
    c.rect(x + 32, y + 28, 56, 8, WHITE)
    c.disc_outline(x + 60, y + 32, 34, color)


def icon_jets(c, x, y, color):
    # Two jets in formation, dashed flight paths behind them.
    for ox, oy in ((18, 10), (52, 30)):
        c.line(x + ox, y + oy, x + ox + 34, y + oy + 10, color)
        c.line(x + ox + 34, y + oy + 10, x + ox + 8, y + oy + 12, color)
        c.line(x + ox + 8, y + oy + 12, x + ox, y + oy + 22, color)
        c.line(x + ox, y + oy + 22, x + ox + 10, y + oy + 8, color)
    for dx in range(0, 52, 10):
        c.rect(x + 2 + dx, y + 52, 6, 3, MUTED)
    c.circle(x + 100, y + 12, 8, GOLD)
    c.circle(x + 100, y + 12, 4, RED)


ICONS = {
    "chip": icon_chip,
    "tanker": icon_tanker,
    "warship": icon_warship,
    "tower": icon_tower,
    "shop": icon_shop,
    "cross": icon_cross,
    "jets": icon_jets,
}


# ---------------------------------------------------------------- layout

def card(c, x, y, w, h, accent):
    """A paper card with a coloured top rule and a thin navy border."""
    c.rect(x, y, w, h, PAPER)
    c.rect(x, y, w, 6, accent)
    c.rect(x, y, w, 1, NAVY)
    c.rect(x, y + h - 1, w, 1, NAVY)
    c.rect(x, y, 1, h, NAVY)
    c.rect(x + w - 1, y, 1, h, NAVY)


def draw_lead(c, x, y, w, h, story):
    card(c, x, y, w, h, story["accent"])
    ix = x + (w - 120) // 2
    ICONS[story["icon"]](c, ix, y + 16, NAVY2)
    c.text_centered(x + w // 2, y + 92, story["kicker"], story["accent"], 1)
    # Title: two lines max, scale 2, centred.
    title_lines = font5x7.wrap_text(story["title"], 15)
    ty = y + 112
    for line in title_lines:
        c.text_centered(x + w // 2, ty, line, INK, 2)
        ty += 20
    c.hline(x + 24, ty + 4, w - 48, story["accent"])
    c.paragraph(x + 18, ty + 14, story["body"], MUTED, 1, 44, 11)


def draw_mid(c, x, y, w, h, story):
    card(c, x, y, w, h, story["accent"])
    ICONS[story["icon"]](c, x + 14, y + 18, NAVY2)
    tx = x + 148
    c.text(tx, y + 18, story["kicker"], story["accent"], 1)
    title_lines = font5x7.wrap_text(story["title"], 30)
    ty = y + 34
    for line in title_lines:
        c.text(tx, ty, line, INK, 2)
        ty += 20
    c.paragraph(tx, ty + 6, story["body"], MUTED, 1, 52, 11)


def draw_poster():
    c = Canvas(W, H, NAVY)

    # --- masthead ------------------------------------------------------
    c.text_centered(W // 2, 22, stories.MASTHEAD, GOLD, 2)
    c.text_centered(W // 2, 52, stories.DATE_LINE, WHITE, 4)
    c.hline(48, 104, W - 96, RED)
    c.hline(48, 108, W - 96, RED)
    c.text_centered(W // 2, 122, stories.SUBHEAD, SKY, 1)

    # --- lead row: three big cards ------------------------------------
    lead_y, lead_h = 152, 318
    lead_w = 312
    gap = 16
    for i, story in enumerate(stories.LEAD):
        x = 16 + i * (lead_w + gap)
        draw_lead(c, x, lead_y, lead_w, lead_h, story)

    # --- mid grid: 2x2 -------------------------------------------------
    mid_y = lead_y + lead_h + 16
    mid_w = (W - 32 - gap) // 2
    mid_h = 152
    for i, story in enumerate(stories.MID):
        x = 16 + (i % 2) * (mid_w + gap)
        y = mid_y + (i // 2) * (mid_h + 16)
        draw_mid(c, x, y, mid_w, mid_h, story)

    # --- also-today ticker --------------------------------------------
    tick_y = mid_y + 2 * mid_h + 16 + 8
    c.text(16, tick_y, "ALSO TODAY", GOLD, 2)
    c.hline(16, tick_y + 26, W - 32, GOLD)
    ty = tick_y + 38
    per_col = 5
    col_w = (W - 32) // 2
    for i, item in enumerate(stories.TICKER):
        col = i // per_col
        row = i % per_col
        x = 16 + col * col_w
        y = ty + row * 16
        c.text(x, y, ">", RED, 1)
        c.text(x + 12, y, item, PAPER, 1)

    # --- footer ---------------------------------------------------------
    c.hline(16, H - 40, W - 32, MUTED)
    c.text_centered(W // 2, H - 28, stories.FOOTER, SKY, 1)
    return c


# ---------------------------------------------------------------- PNG

def chunk(kind, data):
    out = bytearray()
    out += len(data).to_bytes(4, "big")
    out += kind
    out += data
    out += (binascii.crc32(kind + data) & 0xFFFFFFFF).to_bytes(4, "big")
    return bytes(out)


def encode_png(canvas):
    raw = bytearray()
    stride = canvas.width * 3
    for y in range(canvas.height):
        raw.append(0)  # filter: none
        start = y * stride
        raw += canvas.pixels[start:start + stride]
    ihdr = (canvas.width.to_bytes(4, "big")
            + canvas.height.to_bytes(4, "big")
            + bytes([8, 2, 0, 0, 0]))  # 8-bit, RGB, no interlace
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return bytes(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    data = encode_png(draw_poster())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
