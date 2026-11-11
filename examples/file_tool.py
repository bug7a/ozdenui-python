# Bismillah
"""A file tool: choose a text file; its lines and words are counted in a background job with a progress bar."""

import os

from ozdenui import App, Label, ProgressBar, SmartButton, Toast, VGroup, open_file, run_in_background

PAGE_COLOR = "#F4F5F7"
TEXT_SOFT = "#5A6270"
LINES_PER_STEP = 2000  # the progress bar moves every 2000 lines
FILE_TYPES = ("Text files (*.txt;*.md;*.csv;*.py;*.json)", "All files (*.*)")

view = {}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=16, padding=40, align="left top"):
        Label(text="Word counter", font_size=24, bold=True)
        Label(text="Choose a text file: its lines and words are counted.", font_size=15, text_color=TEXT_SOFT)
        view["button"] = SmartButton(text="Choose a file", tone="cyan", on_click=choose_file)
        view["file"] = Label(text="", font_size=14, text_color=TEXT_SOFT)
        view["bar"] = ProgressBar(title_text="Counting", value=0, width=440)
        view["result"] = Label(text="", font_size=18)


def choose_file():
    path = open_file(file_types=FILE_TYPES)
    if path:
        count_file(path)


def count_file(path):
    view["file"].text = path
    view["result"].text = ""
    view["bar"].value = 0
    view["button"].waiting = True
    run_in_background(count_words, path)


def count_words(path):
    """Runs on a thread of its own: the window keeps working, and the objects may be changed from here."""
    size = os.path.getsize(path) or 1
    lines = 0
    words = 0
    read = 0
    with open(path, encoding="utf-8", errors="replace") as file:
        for line in file:
            lines += 1
            words += len(line.split())
            read += len(line.encode("utf-8"))
            if lines % LINES_PER_STEP == 0:
                view["bar"].value = round(read * 100 / size)
    view["bar"].value = 100
    view["result"].text = f"{lines:,} lines, {words:,} words"
    view["button"].waiting = False
    Toast.success("Counted.")


if __name__ == "__main__":
    App(start, title="Word counter", size=(560, 420)).run()
