# Bismillah
"""The minimal look in a color: App(style="minimal", accent="#2A78D6").
The color goes where the minimal look draws its ink: an on toggle, a checked box, the fill of a slider and of a
progress bar, the selected tab, row and step, the edge of a field while typing; the main button takes it with
tone="accent". The lines and the texts stay as they are. Any color works: change ACCENT.
python minimal_accent.py dark: the same page in a dark window. The color is made lighter there until it reads on the
dark ground; App(accent_dark="#7FB6DE") chooses it.
"""

import sys

from ozdenui import (App, CheckBox, DatePicker, Dialog, HGroup, ItemList, Label, ProgressBar, RadioButton, ScrollArea,
                     SelectBox, Slider, SmartButton, StatusBar, StepBar, Tabs, TextField, Toast, Toggle, VGroup)

# The look of the window (checks/check_example.py reads them too)
STYLE = "minimal"
ACCENT = "#2A78D6"  # it reads on white (4.5:1): it is the text of a selected tab too

# The colors of this page, for the two themes. (The components take their look from the window.)
COLORS = {
    "light": {"ground": "#FFFFFF", "caption": "rgba(0, 0, 0, 0.45)", "text": "rgba(0, 0, 0, 0.85)"},
    "dark": {"ground": "#1A1A19", "caption": "rgba(255, 255, 255, 0.45)", "text": "rgba(255, 255, 255, 0.88)"},
}
COLUMN_WIDTH = 340
FIELD_WIDTH = 260
FRUITS = ["Apple", "Banana", "Cherry", "Grape"]
FOLDERS = [{"key": "p", "text": "Projects"}, {"key": "d", "text": "Designs"}, {"key": "a", "text": "Archive"}]
STEPS = ["Cart", "Address", "Payment", "Done"]

view = {}


def caption(text):
    """The small title over a part of the page."""
    return Label(text=text, font_size=11, bold=True, text_color=view["colors"]["caption"])


def tell(text):
    view["status"].set_message(text)


def start(page):
    view["colors"] = COLORS[page.app.theme]
    page.color = view["colors"]["ground"]
    with VGroup(gap=0, align="left top"):
        with ScrollArea():
            with HGroup(width="100%", height="auto", align="center top", gap=40, padding=30, wrap=True):
                with VGroup(width=COLUMN_WIDTH, height="auto", align="left top", gap=14):
                    draw_buttons()
                    draw_choices()
                    draw_fields()
                with VGroup(width=COLUMN_WIDTH, height="auto", align="left top", gap=14):
                    draw_list_and_progress()
                    draw_tabs_and_steps()
        view["status"] = StatusBar(message="Change something.")


def draw_buttons():
    caption("BUTTONS")
    with HGroup(hug=True, align="left center", gap=8, wrap=True):
        SmartButton(text="Cancel", on_click=lambda: tell("Cancel was clicked."))
        SmartButton(text="Send", tone="accent", on_click=lambda: Toast.success("Sent."))
        SmartButton(text="A dialog", on_click=ask_send)


def draw_choices():
    caption("CHOICES")
    with HGroup(hug=True, align="left center", gap=20):
        CheckBox(text="Remember me", checked=True, on_change=lambda box: tell(f"Remember me: {box.checked}"))
        CheckBox(text="Send the news", on_change=lambda box: tell(f"Send the news: {box.checked}"))
    with HGroup(hug=True, align="left center", gap=20):
        RadioButton(group="plan", value="Monthly", text="Monthly", checked=True,
                    on_change=lambda radio: tell(f"Plan: {RadioButton.value_of('plan')}"))
        RadioButton(group="plan", value="Yearly", text="Yearly",
                    on_change=lambda radio: tell(f"Plan: {RadioButton.value_of('plan')}"))
    with HGroup(hug=True, align="left center", gap=10):
        Toggle(value=True, on_change=lambda toggle: tell(f"Sounds: {toggle.value}"))
        Label(text="Sounds", font_size=13, text_color=view["colors"]["text"])


def draw_fields():
    caption("FIELDS")
    TextField(title_text="Name", placeholder="Your name", width=FIELD_WIDTH)
    SelectBox(options=FRUITS, value="Cherry", width=FIELD_WIDTH, on_change=lambda box: tell(f"Fruit: {box.value}"))
    DatePicker(value="2026-11-12", width=140, on_change=lambda picker: tell(f"Date: {picker.value}"))


def draw_list_and_progress():
    caption("LIST, SLIDER, PROGRESS")
    ItemList(items=FOLDERS, selected_keys=["d"], width=FIELD_WIDTH, height="auto",
             on_change=lambda folders: tell(f"Folder: {folders.selected_keys}"))
    Slider(value=40, min_value=0, max_value=100, width=FIELD_WIDTH, on_change_end=lambda slider: tell(f"Slider: {slider.value}"))
    ProgressBar(title_text="Uploading files", value=62, width=FIELD_WIDTH)


def draw_tabs_and_steps():
    caption("TABS, STEPS")
    Tabs(tabs=["General", "Sound", "Advanced"], panels=False, width=300, on_change=lambda tabs: tell(f"Tab: {tabs.value}"))
    StepBar(steps=STEPS, step=2, width="100%", on_step_click=lambda bar, index: tell(f"Back to step {index + 1}"))


def ask_send():
    if Dialog.confirm("It goes to the three people of the team.", title="Send the report?", confirm_text="Yes, send"):
        tell("The report is sent.")


if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else "light"
    App(start, title="OzdenUI minimal accent", size=(860, 600), theme=theme, style=STYLE, accent=ACCENT).run()
