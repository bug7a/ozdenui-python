# Bismillah
"""A CSV file in a table: open one (a sample is shown first), filter it, click a row to see it. A SmartTable makes only
the rows that are seen: "100000 rows" shows that a big file stays fast."""

import csv

from ozdenui import App, Box, HGroup, Label, SmartButton, SmartTable, Toast, VGroup, open_file

PAGE_COLOR = "#F4F5F7"
TEXT_SOFT = "#5A6270"
TABLE_WIDTH = 820
TABLE_HEIGHT = 400
COLUMN_WIDTH = 170
MANY_ROWS = 100000

SAMPLE = [
    {"city": "İstanbul", "country": "Türkiye", "people": "15,655,924"},
    {"city": "Ankara", "country": "Türkiye", "people": "5,803,482"},
    {"city": "Berlin", "country": "Germany", "people": "3,878,100"},
    {"city": "Madrid", "country": "Spain", "people": "3,332,035"},
    {"city": "Rome", "country": "Italy", "people": "2,748,109"},
    {"city": "Paris", "country": "France", "people": "2,102,650"},
    {"city": "Vienna", "country": "Austria", "people": "2,005,760"},
    {"city": "Lisbon", "country": "Portugal", "people": "567,131"},
]

view = {}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=14, padding=30, align="left top"):
        with HGroup(hug=True, gap=14, align="left center"):
            Label(text="CSV viewer", font_size=24, bold=True)
            SmartButton(text="Open a CSV", tone="cyan", on_click=open_csv)
            SmartButton(text=f"{MANY_ROWS} rows", on_click=show_many_rows)
        view["file"] = Label(text="A sample: some cities", font_size=14, text_color=TEXT_SOFT)
        view["holder"] = Box(width=TABLE_WIDTH, height=TABLE_HEIGHT, color="transparent")
        view["detail"] = Label(text="Click a row.", font_size=15)
    show_rows(SAMPLE)


def show_rows(records):
    """A new table for the rows (a new file has other columns)."""
    if "table" in view:
        view["table"].remove()
    names = list(records[0].keys()) if records else []
    columns = [{"key": name, "title": name, "width": COLUMN_WIDTH} for name in names]
    with view["holder"]:
        view["table"] = SmartTable(columns=columns, rows=records, width="100%", height="100%", on_select=show_row)


def show_row(table, row):
    view["detail"].text = "   ".join(f"{key}: {value}" for key, value in row.items())


def show_many_rows():
    view["file"].text = f"{MANY_ROWS} rows made in Python"
    show_rows([{"number": index, "square": index * index, "half": index / 2} for index in range(MANY_ROWS)])


def open_csv():
    path = open_file(file_types=("CSV files (*.csv)", "All files (*.*)"))
    if not path:
        return
    try:
        with open(path, newline="", encoding="utf-8-sig") as file:
            records = list(csv.DictReader(file))
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        Toast.error(str(error), title="Could not read it")
        return
    view["file"].text = path
    show_rows(records)


if __name__ == "__main__":
    App(start, title="CSV viewer", size=(900, 640)).run()
