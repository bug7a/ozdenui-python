# Bismillah
"""A small file tool: a tree that opens a folder when it is asked, a search in it, a menu on it, and a place to drop files
on (their real paths reach Python). python files.py some/folder: the tree of that folder."""

import os
import sys

from ozdenui import (App, Box, ContextMenu, FilePicker, HGroup, Label, SearchInput, SmartButton, SmartTable, Splitter, StatusBar, Toast,
                     Tooltip, TreeView, VGroup)

PAGE_COLOR = "#FFFFFF"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_FOUND = 200
COLUMNS = [{"key": "name", "title": "Name", "width": 180}, {"key": "size", "title": "Size", "width": 90}, {"key": "path", "title": "Path", "width": 420}]

view = {}


def nodes_of(folder):
    """The nodes of a folder, its folders first. A folder has no nodes yet: on_load_children gives them when it opens."""
    entries = [entry for entry in os.scandir(folder) if not entry.name.startswith(".")]
    entries.sort(key=lambda entry: (not entry.is_dir(), entry.name.lower()))
    nodes = []
    for entry in entries:
        if entry.is_dir():
            nodes.append({"key": entry.path, "text": entry.name, "has_children": True})
        else:
            nodes.append({"key": entry.path, "text": entry.name, "description": size_text(entry.stat().st_size)})
    return nodes


def found_nodes(root, typed):
    """The files whose names have this text, in every folder. WHY a flat list: the tree knows only the folders that were opened."""
    nodes = []
    for folder, folders, names in os.walk(root):
        folders[:] = [name for name in folders if not name.startswith(".")]
        for name in names:
            if typed in name.lower() and not name.startswith("."):
                nodes.append({"key": os.path.join(folder, name), "text": name, "description": os.path.relpath(folder, root)})
            if len(nodes) >= MAX_FOUND:
                return nodes
    return nodes


def size_text(size):
    return f"{size / 1024:.1f} KB" if size >= 1024 else f"{size} B"


def start(page):
    page.color = PAGE_COLOR
    view["root"] = sys.argv[1] if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]) else ROOT
    with VGroup(gap=0, align="left top"):
        with Box(fill=True, color="transparent"):
            split = Splitter(first_size=280, min_first=180, min_second=380)
            with split.first:
                with VGroup(width="100%", height="100%", align="left top", gap=8, padding=8):
                    view["search"] = SearchInput(placeholder="Find a file", width="100%", on_change=find_files)
                    tree = TreeView(items=nodes_of(view["root"]), width="100%", height="100%", empty_text="Nothing found.",
                                    on_select=show_node, on_load_children=load_children)
                    view["tree"] = tree
                    view["menu"] = ContextMenu(target=tree, items=[
                        {"text": "Its size", "on_click": tell_size}, "-",
                        {"text": "Close the folders", "on_click": tree.collapse_all},
                    ])
            with split.second:
                with VGroup(width="100%", height="100%", align="left top", gap=12, padding=16):
                    view["drop"] = FilePicker(width="100%", zone_height=120, multiple=True, title_text="Drop files here",
                                              on_change=show_files)
                    with HGroup(width="100%", height="auto", shrink=0, align="left center", gap=8):
                        clear_button = SmartButton(text="Clear", on_click=clear_files)
                        Tooltip(target=clear_button, text="Empties the list")
                        about_button = SmartButton(text="About")
                        view["about"] = Tooltip.popover(about_button, make_about)
                    view["table"] = SmartTable(columns=COLUMNS, rows=[], width="100%", height="100%",
                                               on_select=lambda table, row: tell(row["path"]))
        view["status"] = StatusBar(message=view["root"], items=[{"key": "count", "text": "0 files"}])


def find_files(search):
    typed = search.text.strip().lower()
    view["tree"].set_items(found_nodes(view["root"], typed) if typed else nodes_of(view["root"]))


def load_children(tree, node):
    tree.set_children(node["key"], nodes_of(node["key"]))


def show_node(tree, node):
    tell(node["key"])


def tell(text):
    view["status"].set_message(text)


def tell_size():
    key = view["tree"].value
    if key is None:
        Toast.info("Select a node first.")
    elif os.path.isfile(key):
        Toast.info(f"{os.path.basename(key)}: {size_text(os.path.getsize(key))}")
    else:
        Toast.info("It is a folder.")


def show_files():
    view["table"].set_rows([{"name": file["name"], "size": file["size_text"], "path": file["path"] or ""} for file in view["drop"].files])
    view["status"].set_item_text("count", f"{len(view['drop'].files)} files")


def clear_files():
    view["drop"].clear()
    show_files()


def make_about():
    Label(text="A tree, a menu and a place to drop files.", font_size=14)
    SmartButton(text="Close", on_click=Tooltip.close_popover)


if __name__ == "__main__":
    App(start, title="Files", size=(960, 620)).run()
