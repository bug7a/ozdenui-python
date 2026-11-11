# Bismillah
"""A place to look at a picture: open a file, or draw a plot again and again: the zoom and the place stay.

No package is needed for this example. ImageView.set_image() also takes a Pillow image and a matplotlib figure:
    view.set_image(plt.gcf())
"""

import math
import struct
import zlib

from ozdenui import App, HGroup, ImageView, SmartButton, StatusBar, VGroup, open_file

PLOT_WIDTH = 640
PLOT_HEIGHT = 400
PAGE_COLOR = "#FFFFFF"
GROUND = (255, 255, 255)
GRID = (225, 228, 232)
CURVE = (43, 140, 150)
CURVE_WIDTH = 3
PHASE_STEP = 0.5

view = {}


def png_of(pixels, width, height):
    """The bytes of a PNG file. pixels: bytes of RGB, row after row."""

    def chunk(name, data):
        return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data))

    rows = b"".join(b"\x00" + bytes(pixels[y * width * 3:(y + 1) * width * 3]) for y in range(height))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")


def plot_png(phase):
    """A plot, drawn pixel by pixel: as a program of yours would draw one."""
    pixels = bytearray(bytes(GROUND) * (PLOT_WIDTH * PLOT_HEIGHT))

    def put(x, y, color):
        if 0 <= x < PLOT_WIDTH and 0 <= y < PLOT_HEIGHT:
            pixels[(y * PLOT_WIDTH + x) * 3:(y * PLOT_WIDTH + x) * 3 + 3] = bytes(color)

    for x in range(0, PLOT_WIDTH, 40):
        for y in range(PLOT_HEIGHT):
            put(x, y, GRID)
    for y in range(0, PLOT_HEIGHT, 40):
        for x in range(PLOT_WIDTH):
            put(x, y, GRID)
    for x in range(PLOT_WIDTH):
        y = PLOT_HEIGHT // 2 - int(math.sin(x / 50 + phase) * (PLOT_HEIGHT * 0.35))
        for thickness in range(CURVE_WIDTH):
            put(x, y + thickness, CURVE)
    return png_of(pixels, PLOT_WIDTH, PLOT_HEIGHT)


def start(page):
    page.color = PAGE_COLOR
    view["phase"] = 0.0
    with VGroup(gap=0, align="left top"):
        with HGroup(width="100%", height="auto", gap=8, padding=12, align="left center", shrink=0):
            SmartButton(text="Open a picture", tone="cyan", on_click=open_picture)
            SmartButton(text="Draw the plot again", on_click=draw_again)
        view["image"] = ImageView(fill=True, framed=False, image=plot_png(0), alt="A plot",
                                  on_zoom_change=show_size, on_error=lambda: view["status"].set_message("It can not be opened", "error"))
        view["status"] = StatusBar(message="A plot", items=[{"key": "size", "text": "-"}])


def show_size(image):
    view["status"].set_item_text("size", f"{image.natural_width} x {image.natural_height} at {round(image.zoom_level * 100)}%")


def draw_again():
    view["phase"] += PHASE_STEP
    view["image"].set_image(plot_png(view["phase"]))
    view["status"].set_message("Drawn again: the zoom and the place stay", "success", 2000)


def open_picture():
    path = open_file(file_types=("Pictures (*.png;*.jpg;*.jpeg;*.gif;*.webp;*.svg)", "All files (*.*)"))
    if path:
        view["image"].set_image(path)
        view["status"].set_message(path)


if __name__ == "__main__":
    App(start, title="Image viewer", size=(760, 560)).run()
