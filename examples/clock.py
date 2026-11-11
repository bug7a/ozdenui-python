# Bismillah
"""A clock and a stopwatch: every() runs a function again and again (the loop() of basic.js)."""

import time

from ozdenui import App, HGroup, Label, SmartButton, VGroup, every

PAGE_COLOR = "#1E2230"
TEXT_LIGHT = "#F4F5F7"
TEXT_SOFT = "#9AA3B5"
STOPWATCH_STEP_MS = 100

view = {}
stopwatch = {"started_at": None, "total": 0.0, "stop": None}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=10, padding=30):
        view["clock"] = Label(text=time.strftime("%H:%M:%S"), font_size=72, bold=True, text_color=TEXT_LIGHT)
        view["date"] = Label(text=time.strftime("%A, %d %B %Y"), font_size=16, text_color=TEXT_SOFT)
        view["watch"] = Label(text="0.0 s", font_size=28, text_color=TEXT_LIGHT)
        with HGroup(hug=True, gap=8):
            view["start"] = SmartButton(text="Start", style_name="ozdenDark", on_click=toggle)
            SmartButton(text="Reset", style_name="ozdenDark", on_click=reset)
    every(1000, show_time)


def show_time():
    view["clock"].text = time.strftime("%H:%M:%S")


def elapsed():
    running = time.perf_counter() - stopwatch["started_at"] if stopwatch["started_at"] else 0
    return stopwatch["total"] + running


def show_watch():
    view["watch"].text = f"{elapsed():.1f} s"


def toggle():
    if stopwatch["started_at"] is None:
        stopwatch["started_at"] = time.perf_counter()
        stopwatch["stop"] = every(STOPWATCH_STEP_MS, show_watch)
        view["start"].text = "Stop"
        return
    stopwatch["total"] = elapsed()
    stopwatch["started_at"] = None
    stopwatch["stop"]()
    view["start"].text = "Start"
    show_watch()


def reset():
    stopwatch["total"] = 0.0
    if stopwatch["started_at"] is not None:
        stopwatch["started_at"] = time.perf_counter()
    show_watch()


if __name__ == "__main__":
    App(start, title="Clock", size=(460, 340)).run()
