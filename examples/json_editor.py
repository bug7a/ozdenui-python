# Bismillah
"""A small JSON editor: the products of a shop in a table. A click on a cell writes in it, a title sorts, the dots of a row
move it; paste rows from a spreadsheet. The status bar counts the products at every change.
Settings... edits a dict in a window (Apply / Cancel). python json_editor.py some.json: that file (a list or a dict)."""

import json
import sys

from ozdenui import App, JsonEditor, StatusBar, ToolBar, VGroup, open_file, save_file

UNITS = ["kg", "piece", "box"]
PRODUCTS = [
    {"name": "Apple", "price": 1.2, "unit": "kg", "color": "#D64545", "in_stock": True, "tags": ["red", "sweet"]},
    {"name": "Banana", "price": 0.9, "unit": "kg", "color": "#E8D44D", "in_stock": True, "tags": ["yellow"]},
    {"name": "Watermelon", "price": 4.5, "unit": "piece", "color": "#3E8E62", "in_stock": False, "tags": ["summer"]},
    {"name": "Strawberry", "price": 3.8, "unit": "box", "color": "#E06AA0", "in_stock": True, "tags": ["red", "spring"]},
    {"name": "Lemon", "price": 1.6, "unit": "kg", "color": "#E0A038", "in_stock": False, "tags": ["sour"]},
    {"name": "Orange", "price": 1.4, "unit": "kg", "color": "#F28C28", "in_stock": True, "tags": ["sweet", "winter"]},
    {"name": "Grapes", "price": 2.9, "unit": "kg", "color": "#7B4FA0", "in_stock": True, "tags": ["sweet"]},
    {"name": "Cherry", "price": 6.5, "unit": "box", "color": "#B3243B", "in_stock": False, "tags": ["red", "summer"]},
    {"name": "Pear", "price": 1.7, "unit": "kg", "color": "#A8B545", "in_stock": True, "tags": ["autumn"]},
    {"name": "Pineapple", "price": 3.2, "unit": "piece", "color": "#E3B23C", "in_stock": True, "tags": ["sweet", "summer"]},
    {"name": "Blueberry", "price": 4.9, "unit": "box", "color": "#4A5FA8", "in_stock": True, "tags": ["summer"]},
    {"name": "Kiwi", "price": 0.6, "unit": "piece", "color": "#7A8B3A", "in_stock": False, "tags": ["sour"]},
]
SETTINGS = {
    "shop_name": "Fresh Fruit",
    "currency": "TL",
    "show_prices": True,
    "page_size": 20,
    "languages": ["en", "tr"],
    "address": {"city": "İzmir", "zip": "35000"},
}

view = {"first_file": None, "settings": SETTINGS}


def start(page):
    with VGroup(gap=0, align="left top"):
        ToolBar(items=[
            {"key": "open", "icon": "open", "hint": "Open...", "shortcut": "Ctrl+O", "on_click": open_json},
            {"key": "save", "icon": "save", "hint": "Save...", "shortcut": "Ctrl+S", "on_click": save_json},
            "-",
            {"key": "settings", "text": "Settings...", "on_click": edit_settings},
        ])
        view["editor"] = JsonEditor(fill=True, framed=False, value=PRODUCTS, title_text="Products",
                                    note_text="A row is a product. Paste rows from a spreadsheet, or a JSON list.",
                                    columns=[{"key": "unit", "options": UNITS}], on_change=count_products)
        view["status"] = StatusBar(message="Change a cell: the products are counted here.")
    if view["first_file"]:
        read_file(view["first_file"])


def count_products(editor, products):
    """products: the whole value of the table, as Python data."""
    if not isinstance(products, list):
        view["status"].set_message(f"{len(products)} names")
        return
    in_stock = [row for row in products if isinstance(row, dict) and row.get("in_stock")]
    view["status"].set_message(f"{len(products)} products, {len(in_stock)} in stock")


def read_file(path):
    with open(path, encoding="utf-8") as file:
        is_json = view["editor"].set_json_text(file.read())
    view["status"].set_message(path if is_json else f"It is not a JSON list or object: {path}", "" if is_json else "error")


def open_json():
    path = open_file(file_types=("JSON files (*.json)", "All files (*.*)"))
    if path:
        read_file(path)


def save_json():
    products = view["editor"].value
    if products is None:
        view["status"].set_message(view["editor"].error_text, "error")
        return
    path = save_file(file_name="products.json", file_types=("JSON files (*.json)",))
    if path:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(products, file, ensure_ascii=False, indent=2)
        view["status"].set_message(f"Saved: {path}", "success", 3000)


def edit_settings():
    JsonEditor.open(title_text="Settings", note_text="A row is a name and its value.", value=view["settings"],
                    on_apply=keep_settings)


def keep_settings(settings):
    view["settings"] = settings
    view["status"].set_message(f"Settings of {settings.get('shop_name')}: {len(settings)} names", "success", 3000)


if __name__ == "__main__":
    view["first_file"] = sys.argv[1] if len(sys.argv) > 1 else None
    App(start, title="A small JSON editor", size=(820, 600)).run()
