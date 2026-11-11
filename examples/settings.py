# Bismillah
"""Settings on three tabs. Save shows them as a dict (also in the terminal)."""

from ozdenui import (App, CheckBox, HGroup, Label, RadioButton, SelectBox, Slider, SmartButton, Tabs, TextField,
                     Toast, Toggle, VGroup)

PAGE_COLOR = "#F4F5F7"
CARD_COLOR = "#FFFFFF"
TEXT_SOFT = "#5A6270"
FORM_WIDTH = 460
PANEL_HEIGHT = 250

view = {}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=16, padding=30, align="left top"):
        Label(text="Settings", font_size=24, bold=True)
        with VGroup(width=FORM_WIDTH + 40, height="auto", align="left top", gap=16, padding=20, color=CARD_COLOR,
                    round=12):
            tabs = Tabs(tabs=["General", "Notifications", "Sound"], panel_height=PANEL_HEIGHT)
            with tabs.panel("General"):
                with VGroup(width="100%", height="auto", align="left top", gap=14, padding=[0, 16]):
                    view["name"] = TextField(title_text="Name", text="Ada", width=FORM_WIDTH)
                    Label(text="Language", font_size=13, text_color=TEXT_SOFT)
                    view["language"] = SelectBox(options=["English", "Türkçe", "Deutsch"], value="English",
                                                 width=FORM_WIDTH)
            with tabs.panel("Notifications"):
                with VGroup(width="100%", height="auto", align="left top", gap=16, padding=[0, 16]):
                    view["email"] = CheckBox(text="E-mail", checked=True)
                    view["sms"] = CheckBox(text="SMS")
                    with HGroup(hug=True, gap=12, align="left center"):
                        view["sounds"] = Toggle(value=True)
                        Label(text="Play a sound", font_size=15)
            with tabs.panel("Sound"):
                with VGroup(width="100%", height="auto", align="left top", gap=16, padding=[0, 16]):
                    Label(text="Volume", font_size=13, text_color=TEXT_SOFT)
                    view["volume"] = Slider(value=7, min_value=0, max_value=10, width=FORM_WIDTH)
                    with HGroup(hug=True, gap=18):
                        for quality in ("Low", "Normal", "High"):
                            RadioButton(group="quality", value=quality, text=quality, checked=(quality == "Normal"))
            with HGroup(hug=True, gap=10):
                SmartButton(text="Save", tone="cyan", on_click=save)
                SmartButton(text="Reset", on_click=reset)
        view["saved"] = Label(text="", font_size=13, text_color=TEXT_SOFT)


def values():
    return {
        "name": view["name"].text,
        "language": view["language"].value,
        "email": view["email"].checked,
        "sms": view["sms"].checked,
        "sounds": view["sounds"].value,
        "volume": view["volume"].value,
        "quality": RadioButton.value_of("quality"),
    }


def save():
    settings = values()
    print("saved:", settings)
    view["saved"].text = str(settings)
    Toast.success("The settings are saved.")


def reset():
    view["name"].text = "Ada"
    view["language"].value = "English"
    view["email"].checked = True
    view["sms"].checked = False
    view["sounds"].value = True
    view["volume"].value = 7
    view["saved"].text = ""


if __name__ == "__main__":
    App(start, title="Settings", size=(580, 560)).run()
