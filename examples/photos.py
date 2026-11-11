# Bismillah
"""A picture gallery: the small pictures in a grid (ItemList, the gallery look), a click opens the picture large
(ImageView: the wheel zooms, a drag moves it). python photos.py some/folder: the pictures of that folder.

No package is needed. With Pillow (pip install pillow) the small pictures of a folder are made small first, so a folder
of large photos opens fast.
"""

import os
import sys

from ozdenui import App, HGroup, ImageView, ItemList, SmartButton, Splitter, StatusBar, VGroup, choose_folder

PAGE_COLOR = "#FFFFFF"
PICTURE_ENDINGS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")
MAX_PICTURES = 60
SMALL_PICTURE_SIZE = 240
LIST_WIDTH = 330

# The pictures of the first view, made here (SVG): a ground, a sun and a hill. Not square: the gallery fills its squares.
SCENES = [("Sea", "#DCEFF1", "#3F8D94"), ("Sunset", "#FBEBD3", "#E0913A"), ("Forest", "#E3EEDC", "#5E8C4A"),
          ("Night", "#2B3140", "#E6E1C5"), ("Desert", "#F6E7C8", "#C98B4B"), ("Lake", "#E4EAF6", "#4F6FB0")]

view = {}


def scene_picture(ground, sun):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="320"><rect width="480" height="320" fill="{ground}"/>'
            f'<circle cx="330" cy="120" r="60" fill="{sun}"/>'
            f'<path d="M0 320 L0 230 Q140 150 260 230 T480 210 L480 320 Z" fill="{sun}" opacity="0.55"/></svg>').encode()


def first_pictures():
    """{key: (title, picture)}: the scenes of this file."""
    return {title.lower(): (title, scene_picture(ground, sun)) for title, ground, sun in SCENES}


def folder_pictures(folder):
    """{key: (title, path)}: the pictures of a folder, by name (at most MAX_PICTURES)."""
    names = sorted(name for name in os.listdir(folder) if name.lower().endswith(PICTURE_ENDINGS) and not name.startswith("."))
    return {os.path.join(folder, name): (name, os.path.join(folder, name)) for name in names[:MAX_PICTURES]}


def small_picture(picture):
    """A small copy of a large photo when Pillow is there; otherwise (or for an SVG) the picture itself."""
    if not isinstance(picture, str) or picture.lower().endswith(".svg"):
        return picture
    try:
        from PIL import Image
    except ImportError:
        return picture
    try:
        with Image.open(picture) as image:
            image.thumbnail((SMALL_PICTURE_SIZE, SMALL_PICTURE_SIZE))
            return image.convert("RGB")
    except OSError:
        return picture  # WHY: a file Pillow can not read may still be shown by the web view (Ex: a new format)


def items_of(pictures):
    return [{"key": key, "text": title, "icon_file": small_picture(picture)} for key, (title, picture) in pictures.items()]


def start(page):
    page.color = PAGE_COLOR
    folder = sys.argv[1] if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]) else ""
    view["pictures"] = folder_pictures(folder) if folder else first_pictures()
    with VGroup(gap=0, align="left top"):
        with HGroup(width="100%", height="auto", gap=8, padding=12, align="left center", shrink=0):
            SmartButton(text="Open a folder", tone="cyan", on_click=open_folder)
        # WHY fill: the two areas take the height the bars leave.
        split = Splitter(first_size=LIST_WIDTH, min_first=160, min_second=240, fill=True)
        with split.first:
            view["list"] = ItemList(items=items_of(view["pictures"]), layout="grid", style_name="gallery", width="100%", height="100%",
                                    on_change=show_chosen)
        with split.second:
            view["image"] = ImageView(width="100%", height="100%", framed=False,
                                      on_error=lambda: view["status"].set_message("It can not be opened", "error"))
        view["status"] = StatusBar(message="Choose a picture", items=[{"key": "count", "text": count_text()}])
    first_key = next(iter(view["pictures"]), None)
    if first_key:
        view["list"].set_selected([first_key])
        show(first_key)


def count_text():
    return f"{len(view['pictures'])} pictures"


def show_chosen(lst, items):
    if items:
        show(items[0]["key"])


def show(key):
    title, picture = view["pictures"][key]
    view["image"].set_image(picture, title)
    view["status"].set_message(title)


def open_folder():
    folder = choose_folder()
    if not folder:
        return
    pictures = folder_pictures(folder)
    if not pictures:
        view["status"].set_message("No pictures in this folder", "warn", 3000)
        return
    view["pictures"] = pictures
    view["list"].set_items(items_of(pictures))
    view["status"].set_item_text("count", count_text())
    first_key = next(iter(pictures))
    view["list"].set_selected([first_key])
    show(first_key)


if __name__ == "__main__":
    App(start, title="Photos", size=(980, 640)).run()
