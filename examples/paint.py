# Bismillah
"""A small drawing program: draw with the mouse or a finger, choose a pen, take the last line back, add a shape that can be
dragged, save the drawing as a picture. The lines are drawn by the page: Python hears each finished line.
"""

import random
from functools import partial

from ozdenui import App, Canvas, StatusBar, ToolBar, VGroup, save_file

PAGE_COLOR = "#FFFFFF"
PENS = [("Black", "#373836"), ("Cyan", "#3F8D94"), ("Orange", "#E0913A"), ("Green", "#5E8C4A")]
PEN_WIDTHS = [2, 4, 8, 16]
SHAPE_COLORS = ["#5BBAC1", "#E0913A", "#9DBE8C", "#E6C35C", "#B48EAD"]
FIRST_PEN_WIDTH = 4

view = {}


def pen_icon(color):
    return f'<svg viewBox="0 0 24 24" width="20" height="20"><circle cx="12" cy="12" r="7" fill="{color}"/></svg>'


def width_icon(width):
    return (f'<svg viewBox="0 0 24 24" width="20" height="20"><line x1="4" y1="12" x2="20" y2="12" stroke="currentColor" '
            f'stroke-width="{min(width, 12)}" stroke-linecap="round"/></svg>')


def tool_items():
    pens = [{"key": name, "icon": pen_icon(color), "hint": f"The pen: {name}", "group": "pen", "checked": index == 0,
             "on_click": partial(choose_pen, color, name)} for index, (name, color) in enumerate(PENS)]
    widths = [{"key": f"width{width}", "icon": width_icon(width), "hint": f"Width {width}", "group": "width", "checked": width == FIRST_PEN_WIDTH,
               "on_click": partial(choose_width, width)} for width in PEN_WIDTHS]
    actions = [{"key": "shape", "icon": "plus", "text": "Shape", "hint": "A shape that can be dragged", "on_click": add_shape},
               {"key": "undo", "icon": "undo", "hint": "Undo", "shortcut": "Ctrl+Z", "on_click": undo},
               {"key": "clear", "icon": "delete", "hint": "Clear", "on_click": clear},
               " ",
               {"key": "save", "icon": "save", "text": "Save", "shortcut": "Ctrl+S", "on_click": save}]
    return pens + ["-"] + widths + ["-"] + actions


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=0, align="left top"):
        view["tools"] = ToolBar(items=tool_items())
        view["canvas"] = Canvas(fill=True, framed=False, drawing=True, pen_width=FIRST_PEN_WIDTH,
                                on_draw_end=lambda canvas, shape: show_count(), on_shape_move=lambda canvas, shape: tell("A shape was moved"))
        view["status"] = StatusBar(message="Draw with the mouse", items=[{"key": "count", "text": "0 shapes"}])


def tell(text):
    view["status"].set_message(text, "info", 2000)


def show_count():
    view["status"].set_item_text("count", f"{len(view['canvas'].shapes)} shapes")


def choose_pen(color, name):
    view["canvas"].set_pen(color=color)
    view["canvas"].drawing = True
    tell(f"The pen: {name}")


def choose_width(width):
    view["canvas"].set_pen(width=width)
    tell(f"The width: {width}")


def add_shape():
    """A circle or a square at a random place; it can be dragged (the free drawing does not take it)."""
    canvas = view["canvas"]
    x, y = random.randint(40, 400), random.randint(40, 300)
    color = random.choice(SHAPE_COLORS)
    if random.random() < 0.5:
        canvas.circle(x, y, 30, fill=color, draggable=True)
    else:
        canvas.rect(x - 30, y - 30, 60, 60, fill=color, round=8, draggable=True)
    canvas.drawing = False
    tell("Drag the shape; a pen draws again")
    show_count()


def undo():
    shapes = view["canvas"].shapes
    if not shapes:
        return
    view["canvas"].remove_shape(shapes[-1]["key"])
    show_count()


def clear():
    view["canvas"].clear()
    show_count()


def save():
    path = save_file(file_name="drawing.png", file_types=("Pictures (*.png;*.jpg)",))
    if not path:
        return
    view["canvas"].save_image(path)
    view["status"].set_message(f"Saved: {path}", "success", 3000)


if __name__ == "__main__":
    App(start, title="Paint", size=(900, 620)).run()
