# Bismillah
"""A TextField read in Python: view["name"].text is always the text on the page. Enter or the button greets."""

from ozdenui import App, Label, SmartButton, TextField, VGroup

PAGE_COLOR = "#F4F5F7"

view = {}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=14, padding=40):
        view["name"] = TextField(title_text="What is your name?", placeholder="Ada", width=300, on_enter=greet)
        SmartButton(text="Greet", tone="cyan", on_click=greet)
        view["answer"] = Label(text="", font_size=18)


def greet():
    typed = view["name"].text.strip()
    view["answer"].text = f"Hello, {typed}!" if typed else "Write your name first."


if __name__ == "__main__":
    App(start, title="Greeting", size=(420, 320)).run()
