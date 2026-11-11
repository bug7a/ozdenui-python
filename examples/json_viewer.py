# Bismillah
"""A small JSON viewer: open a file, click a row to see its path, right click to copy its value or its path.
python json_viewer.py some.json: that file."""

import sys

from ozdenui import App, JsonView, StatusBar, ToolBar, VGroup, open_file

PAGE_COLOR = "#FFFFFF"
FIRST_VALUE = {
    "status": "ok",
    "count": 2,
    "page_time": 0.042,
    "cached": False,
    "next_page": None,
    "users": [
        {"id": 7, "name": "Ada Yılmaz", "email": "ada@example.com", "active": True, "roles": ["admin", "editor"], "address": {"city": "İzmir", "zip": "35000"}},
        {"id": 12, "name": "Can Demir", "email": "can@example.com", "active": False, "roles": [], "address": None},
    ],
}

view = {"first_file": None}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=0, align="left top"):
        ToolBar(items=[
            {"key": "open", "icon": "open", "hint": "Open...", "shortcut": "Ctrl+O", "on_click": open_json},
            "-",
            {"key": "expand", "text": "Open all", "on_click": lambda: view["json"].expand_all()},
            {"key": "collapse", "text": "Close all", "on_click": lambda: view["json"].collapse_all()},
        ])
        view["json"] = JsonView(fill=True, value=FIRST_VALUE, expand_level=2,
                                on_select=show_entry, on_copy=show_copied)
        view["status"] = StatusBar(message="Click a row: its path comes here.")
    if view["first_file"]:
        read_file(view["first_file"])


def show_entry(json_view, entry):
    view["status"].set_message(f"{entry['pathText']}  ({entry['kind']})")


def show_copied(json_view, text):
    view["status"].set_message(f"Copied: {text[:60]}", "success", 3000)


def read_file(path):
    with open(path, encoding="utf-8") as file:
        is_json = view["json"].set_json_text(file.read())
    view["status"].set_message(path if is_json else f"It is not JSON: {path}", "" if is_json else "error")


def open_json():
    path = open_file(file_types=("JSON files (*.json)", "All files (*.*)"))
    if path:
        read_file(path)


if __name__ == "__main__":
    view["first_file"] = sys.argv[1] if len(sys.argv) > 1 else None
    App(start, title="A small JSON viewer", size=(720, 560)).run()
