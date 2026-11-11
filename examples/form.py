# Bismillah
"""A form: fields of text, a date, a time, a color, a number. Send checks them and shows the values as a dict."""

import datetime

from ozdenui import (App, ColorPicker, DatePicker, EmailField, HGroup, Label, NumberField, PasswordField, ScrollArea, Slider,
                     SmartButton, Stepper, TextField, TimePicker, Toast, VGroup)

PAGE_COLOR = "#F4F5F7"
CARD_COLOR = "#FFFFFF"
TEXT_SOFT = "#5A6270"
FORM_WIDTH = 520
FIRST_COLOR = "#3871E0"

view = {}


def titled(title):
    """A small title over a field that has none of its own: with titled("Date"): DatePicker(...)
    The "with" block puts the field into the group, under the title."""
    group = VGroup(hug=True, gap=6, align="left top")
    with group:
        Label(text=title, font_size=13, text_color=TEXT_SOFT)
    return group


def start(page):
    page.color = PAGE_COLOR
    next_week = datetime.date.today() + datetime.timedelta(days=7)
    with ScrollArea(align="center top", gap=16, padding=30):
        Label(text="A reservation", font_size=24, bold=True)
        with VGroup(width=FORM_WIDTH, height="auto", align="left top", gap=14, padding=20, color=CARD_COLOR, round=12):
            view["name"] = TextField(title_text="Name", placeholder="Ada", required=True, width="100%", on_enter=send)
            view["email"] = EmailField(title_text="E-mail", required=True, width="100%", on_enter=send)
            view["password"] = PasswordField(title_text="Password", min_length=6, width="100%")
            view["budget"] = NumberField(title_text="Budget", value=250, width="100%")
            with HGroup(hug=True, gap=12, wrap=True, align="left top"):
                with titled("Date"):
                    view["date"] = DatePicker(value=next_week, min_date=datetime.date.today(), width=150)
                with titled("Time"):
                    view["time"] = TimePicker(value="19:30", minute_step=15, width=120)
                with titled("Table color"):
                    view["color"] = ColorPicker(value=FIRST_COLOR, width=150)
            with titled("Guests"):
                view["guests"] = Stepper(value=2, min_value=1, max_value=12)
            with titled("How quiet"):
                view["noise"] = Slider(value=70, width=FORM_WIDTH - 40, on_change_end=show_noise)
            with HGroup(hug=True, gap=8):
                SmartButton(text="Send", tone="cyan", on_click=send)
                SmartButton(text="Clear", on_click=clear)
        view["result"] = Label(text="", font_size=13, text_color=TEXT_SOFT, width=FORM_WIDTH)


def values():
    return {
        "name": view["name"].text,
        "email": view["email"].text,
        "budget": view["budget"].value,
        "date": view["date"].value,
        "time": view["time"].value,
        "color": view["color"].value,
        "guests": view["guests"].value,
        "quiet": view["noise"].value,
    }


def show_noise(slider):
    view["result"].text = f"How quiet: {slider.value}"


def send():
    # WHY a list and not "and": every field shows its warning, not only the first one
    answers = [view[name].check() for name in ("name", "email", "password")]
    if not all(answers):
        Toast.error("Look at the marked fields.")
        return
    view["result"].text = str(values())
    Toast.success("Sent.")


def clear():
    for name in ("name", "email", "password"):
        view[name].text = ""
    view["budget"].value = None
    view["date"].value = ""
    view["result"].text = ""


if __name__ == "__main__":
    App(start, title="A form", size=(620, 720)).run()
