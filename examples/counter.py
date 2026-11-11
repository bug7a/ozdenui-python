# Bismillah
"""A counter: two buttons change a number."""

from ozdenui import App, HGroup, Label, SmartButton, VGroup

PAGE_COLOR = "#F4F5F7"
TEXT_SOFT = "#5A6270"


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=16, padding=40):
        Label(text="Counter", font_size=22, text_color=TEXT_SOFT)
        count = Label(text="0", font_size=64, bold=True)
        with HGroup(hug=True, gap=12):
            SmartButton(text="−", width=64, height=44, on_click=lambda: change(count, -1))
            SmartButton(text="+", width=64, height=44, tone="cyan", on_click=lambda: change(count, +1))


def change(count, step):
    count.text = str(int(count.text) + step)


if __name__ == "__main__":
    App(start, title="Counter", size=(400, 320)).run()
