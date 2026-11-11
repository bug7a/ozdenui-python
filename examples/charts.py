# Bismillah
"""Charts with no other library: a live line, bars with a format, a doughnut, two lines with a target. The page draws them."""

import math

from ozdenui import App, GraphBox, HGroup, Label, ScrollArea, SmartButton, Toast, VGroup, every, save_file

PAGE_COLOR = "#F4F5F7"
TEXT_SOFT = "#5A6270"
CHART_WIDTH = 410
CHART_HEIGHT = 250
LIVE_POINTS = 24
TICK_MS = 1000
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

view = {"tick": 0}


def live_value(tick):
    return round(20 + 6 * math.sin(tick / 3), 1)


def start(page):
    page.color = PAGE_COLOR
    with ScrollArea(align="center top", gap=16, padding=24):
        Label(text="Charts", font_size=24, bold=True)
        with HGroup(width="100%", height="auto", align="center top", gap=16, wrap=True):
            view["live"] = GraphBox(type="area", title_text="Temperature", subtitle_text="A new value every second",
                                    labels=[str(tick) for tick in range(LIVE_POINTS)],
                                    values=[live_value(tick) for tick in range(LIVE_POINTS)],
                                    curve="smooth", show_points=False, max_count=LIVE_POINTS, min_value=0, max_labels=6,
                                    format_value="{:.1f}°", width=CHART_WIDTH, height=CHART_HEIGHT)
            view["sales"] = GraphBox(type="bar", title_text="Sales", labels=MONTHS, values=[1200, 1900, 700, 1500, 2300, 1800],
                                     format_value="{:,.0f} TL", on_click=show_month, width=CHART_WIDTH, height=CHART_HEIGHT)
            view["share"] = GraphBox(type="doughnut", title_text="Where they came from", labels=["Search", "A friend", "An ad"],
                                     values=[55, 30, 15], center_text="100", center_sub_text="people", format_value="{}%",
                                     width=CHART_WIDTH, height=CHART_HEIGHT)
            view["years"] = GraphBox(type="line", title_text="Two years", labels=MONTHS,
                                     datasets=[{"label": "2025", "data": [8, 11, 9, 14, 13, 17]},
                                               {"label": "2026", "data": [10, 14, 12, 18, 21, 23], "show_points": True}],
                                     target_lines=[{"value": 20, "label": "Target"}], width=CHART_WIDTH, height=CHART_HEIGHT)
        with HGroup(hug=True, gap=8):
            SmartButton(text="Line", on_click=lambda: view["sales"].set_type("line"))
            SmartButton(text="Bars", on_click=lambda: view["sales"].set_type("bar"))
            SmartButton(text="As a table", on_click=toggle_table)
            SmartButton(text="Save a picture", tone="cyan", on_click=save_picture)
        view["chosen"] = Label(text="Click a bar.", font_size=14, text_color=TEXT_SOFT)
    view["is_table"] = False
    every(TICK_MS, tick)


def tick():
    view["tick"] += 1
    number = LIVE_POINTS + view["tick"]
    view["live"].add_value(str(number), live_value(number))


def show_month(graph, item):
    view["chosen"].text = f"{item['label']}: {item['value']:,} TL"


def toggle_table():
    view["is_table"] = not view["is_table"]
    view["sales"].set_table_view(view["is_table"])


def save_picture():
    path = save_file("sales.png", file_types=("Pictures (*.png)",))
    if path:
        view["sales"].save_image(path)
        Toast.success("Saved.")


if __name__ == "__main__":
    App(start, title="Charts", size=(920, 720)).run()
