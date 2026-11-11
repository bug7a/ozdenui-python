# Bismillah
"""The minimal look of every component that has it, on one page: App(style="minimal").
Small (28 px controls, 13 px text) and made of lines: a component has no fill of its own, it takes the ground of the
window. The main action is the only filled button (tone="ink"). The line at the bottom says what was changed last.
python minimal_theme.py dark: the same page in a dark window (the minimalDark looks).
"""

import sys
from urllib.parse import quote

from ozdenui import (Accordion, App, Box, ChatView, CheckBox, ColorPicker, DataTable, DatePicker, Dialog, EmailField, FilePicker, GraphBox,
                     HGroup, ItemList, Label, LoadingScreen, MenuBar, PasswordField, ProgressBar, RadioButton, RangeSlider, ScrollArea,
                     SearchInput, SelectBox, SidePanel, Slider, SliderField, SmartButton, SmartTable, Splitter, StatusBar, StepBar,
                     Stepper, Tabs, TagInput, TextAreaField, TimePicker, Toast, Toggle, ToolBar, Tooltip, TreeView, VGroup)

# The colors of this page, for the two themes. (The components take their look from the window.)
COLORS = {
    "light": {"ground": "#FFFFFF", "caption": "rgba(0, 0, 0, 0.45)", "text": "rgba(0, 0, 0, 0.85)", "line": "rgba(0, 0, 0, 0.2)"},
    "dark": {"ground": "#1A1A19", "caption": "rgba(255, 255, 255, 0.45)", "text": "rgba(255, 255, 255, 0.88)", "line": "rgba(255, 255, 255, 0.18)"},
}
# The look of the window (checks/check_example.py reads it too)
STYLE = "minimal"

COLUMN_WIDTH = 420
FIELD_WIDTH = 260
LOADING_TIME = 1500  # ms: the loading screen of this page stays this long
CHAT_MESSAGES = [
    {"role": "user", "text": "How do I count the lines of a file?"},
    "Read the file and count its lines:\n\n```python\nlines = open(\"notes.txt\").read().splitlines()\nprint(len(lines))\n```",
]


def line_icon(paths):
    """A line icon (24 x 24) as a data: address; SmartButton draws it white in a dark window."""
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" '
           f'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')
    return "data:image/svg+xml;utf8," + quote(svg)


ICON_SAVE = line_icon('<path d="M5 4h11l3 3v13H5z"/><path d="M8 4v5h7V4M8 20v-6h8v6"/>')
ICON_MORE = line_icon('<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>')

FRUITS = ["Apple", "Banana", "Cherry", "Grape"]
MENUS = [
    {"text": "File", "items": [{"text": "Open", "shortcut": "Ctrl+O"}, {"text": "Save", "shortcut": "Ctrl+S"}, "-",
                               {"text": "Quit", "enabled": False}]},
    {"text": "Edit", "items": ["Undo", "Redo", "-", {"text": "Transform", "items": ["Upper case", "Lower case"]}]},
    {"text": "View", "items": [{"text": "Word wrap", "checked": True}]},
]
TOOLS = [
    {"key": "new", "icon": "new", "hint": "New"},
    {"key": "save", "icon": "save", "hint": "Save", "shortcut": "Ctrl+S"},
    "-",
    {"key": "bold", "icon": "bold", "hint": "Bold", "toggle": True, "checked": True},
    {"key": "left", "icon": "align_left", "hint": "Left", "group": "align", "checked": True},
    {"key": "right", "icon": "align_right", "hint": "Right", "group": "align"},
]
FILES = [
    {"key": "src", "text": "src", "expanded": True, "children": [{"key": "app", "text": "app.py", "description": "4 KB"}, "lib"]},
    {"key": "readme", "text": "README.md", "tag": "new"},
]
PEOPLE = [
    {"name": "Ada Lovelace", "city": "London", "orders": 12},
    {"name": "Alan Turing", "city": "Manchester", "orders": 7},
    {"name": "Grace Hopper", "city": "New York", "orders": 21},
]
PEOPLE_COLUMNS = [
    {"key": "name", "title": "Name", "width": 150},
    {"key": "city", "title": "City", "width": 120},
    {"key": "orders", "title": "Orders", "width": 80, "align": "right", "type": "number"},
]
TAGS = ["audio", "fitness", "guide", "travel"]
SECTIONS = [
    {"key": "general", "text": "General", "description": "3 settings", "opened": True},
    {"key": "advanced", "text": "Advanced"},
    {"key": "locked", "text": "Locked", "enabled": False},
]
MONTHS = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
VISITS = [{"label": "2026", "data": [12, 19, 7, 15, 22, 18]}, {"label": "2025", "data": [8, 11, 9, 12, 14, 13]}]

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
        MenuBar(menus=MENUS)
        ToolBar(items=TOOLS, on_click=lambda bar, item: tell(f"{item['hint']}, pressed: {bar.checked_keys}"))
        with ScrollArea():
            with HGroup(width="100%", height="auto", align="center top", gap=40, padding=30, wrap=True):
                with VGroup(width=COLUMN_WIDTH, height="auto", align="left top", gap=14):
                    draw_buttons()
                    draw_choices()
                    draw_fields()
                    draw_lists()
                    draw_conversation()
                with VGroup(width=COLUMN_WIDTH, height="auto", align="left top", gap=14):
                    draw_pickers()
                    draw_steps_and_areas()
                    draw_tree_and_tables()
                    draw_chart()
                    draw_over_the_page()
        view["status"] = StatusBar(message="Change something.", items=["UTF-8", "100%"])


def draw_buttons():
    caption("BUTTONS")
    with HGroup(hug=True, align="left center", gap=8):
        SmartButton(text="Save", icon=ICON_SAVE, on_click=lambda: tell("Save was clicked."))
        SmartButton(text="Send", tone="ink", on_click=lambda: Toast.success("Sent."))
        SmartButton(text="Delete", style_name="minimalDanger", ask="Click again to delete.",
                    on_click=lambda: tell("Deleted."))
        SmartButton(text="", icon=ICON_MORE, aria_label="More", on_click=lambda: tell("More was clicked."))
    with HGroup(hug=True, align="left center", gap=8):
        SmartButton(text="Disabled", enabled=False)
        SmartButton(text="Waiting", waiting=True)


def draw_choices():
    caption("CHOICES")
    with HGroup(hug=True, align="left center", gap=20):
        CheckBox(text="Remember me", checked=True, on_change=lambda box: tell(f"Remember me: {box.checked}"))
        CheckBox(text="Send the news", on_change=lambda box: tell(f"Send the news: {box.checked}"))
    with HGroup(hug=True, align="left center", gap=20):
        for plan in ("Monthly", "Yearly"):
            RadioButton(group="plan", value=plan, text=plan, checked=(plan == "Monthly"),
                        on_change=lambda radio: tell(f"Plan: {RadioButton.value_of('plan')}"))
    with HGroup(hug=True, align="left center", gap=10):
        Toggle(value=True, on_change=lambda toggle: tell(f"Sounds: {toggle.value}"))
        Label(text="Sounds", font_size=13, text_color=view["colors"]["text"])


def draw_fields():
    caption("FIELDS")
    EmailField(title_text="E-mail", placeholder="name@mail.com", width=FIELD_WIDTH)
    PasswordField(title_text="Password", text="secret", width=FIELD_WIDTH)
    TextAreaField(title_text="Note", placeholder="A few words", width=FIELD_WIDTH, height=96,
                  on_change=lambda area: tell(f"Note: {len(area.text)} letters"))
    SearchInput(placeholder="Search", width=FIELD_WIDTH, on_change=lambda search: tell(f"Search: {search.text}"))
    SelectBox(options=FRUITS, value="Apple", width=FIELD_WIDTH, on_change=lambda box: tell(f"Fruit: {box.value}"))
    Stepper(value=3, min_value=0, max_value=10, on_change=lambda stepper: tell(f"Count: {stepper.value}"))


def draw_lists():
    caption("LIST, SLIDER, PROGRESS, TABS")
    ItemList(items=[{"key": "p", "text": "Projects"}, {"key": "d", "text": "Designs"}, {"key": "a", "text": "Archive"}],
             selected_keys=["d"], width=FIELD_WIDTH, height="auto", on_change=lambda lst: tell(f"Folder: {lst.selected_keys}"))
    Slider(value=40, min_value=0, max_value=100, width=FIELD_WIDTH, on_change_end=lambda slider: tell(f"Slider: {slider.value}"))
    ProgressBar(title_text="Uploading files", value=62, width=FIELD_WIDTH)
    Tabs(tabs=["General", "Sound", "Advanced"], panels=False, width=300, on_change=lambda tabs: tell(f"Tab: {tabs.value}"))


def draw_pickers():
    caption("PICKERS, FIELDS")
    with HGroup(width="100%", height="auto", align="left center", gap=8, wrap=True):
        DatePicker(value="2026-11-12", width=140, on_change=lambda picker: tell(f"Date: {picker.value}"))
        TimePicker(value="14:30", width=100, on_change=lambda picker: tell(f"Time: {picker.value}"))
        ColorPicker(value="#3871E0", width=130, on_change=lambda picker: tell(f"Color: {picker.value}"))
    SliderField(text="Size", value=40, min_value=0, max_value=100, unit_text=" px", width=FIELD_WIDTH,
                on_change_end=lambda slider: tell(f"Size: {slider.value}"))
    TagInput(width="100%", tags=["audio", "guide"], suggestions=TAGS, on_change=lambda field: tell(f"Tags: {field.tags}"))
    FilePicker(multiple=True, width="100%", on_change=lambda picker: tell(f"Files: {len(picker.files)}"))


def draw_steps_and_areas():
    caption("STEPS, SECTIONS, AREAS")
    StepBar(steps=["Cart", "Address", "Payment", "Done"], step=2, width="100%",
            on_step_click=lambda bar, index: tell(f"Back to step {index + 1}"))
    settings = Accordion(sections=SECTIONS, width="100%", height="auto")
    with settings.section("general"):
        CheckBox(text="Open with the system")
        CheckBox(text="Look for updates", checked=True)
    with Box(width="100%", height=80, color="transparent", border=1, border_color=view["colors"]["line"], round=4):
        Splitter(first_size=160, on_change_end=lambda split: tell("The line was moved."))


def draw_conversation():
    caption("CONVERSATION")
    ChatView(messages=CHAT_MESSAGES, width="100%", height=300, on_send=lambda chat, text: chat.add_message(f"You wrote: {text}"))


def draw_tree_and_tables():
    caption("TREE, TABLES, RANGE")
    TreeView(items=FILES, value="app", width=FIELD_WIDTH, height="auto", on_select=lambda tree, node: tell(f"File: {node['text']}"))
    SmartTable(columns=PEOPLE_COLUMNS, rows=PEOPLE, line_count=3, width="100%",
               on_select=lambda table, row: tell(f"Row: {row['name']}"))
    DataTable(columns=PEOPLE_COLUMNS, rows=PEOPLE, width="100%", height=124,
              on_select=lambda table, row: tell(f"Person: {row['name']}" if row else "No person"))
    RangeSlider(low=20, high=70, width=FIELD_WIDTH, on_change_end=lambda slider: tell(f"Range: {slider.low} - {slider.high}"))


def draw_chart():
    caption("CHART")
    GraphBox(type="line", title_text="Visits", labels=MONTHS, datasets=VISITS, width="100%", height=220)


def draw_over_the_page():
    caption("OVER THE PAGE")
    side_panel = SidePanel(side="right", panel_size=300, title_text="Filters")
    with side_panel.body:
        CheckBox(text="Only the new ones", checked=True)
        CheckBox(text="With a picture")
    with HGroup(width="100%", height="auto", align="left center", gap=8, wrap=True):
        hint = SmartButton(text="A hint")
        Tooltip(target=hint, text="Save the file (Ctrl+S)")
        SmartButton(text="A dialog", on_click=ask_delete)
        SmartButton(text="A toast", on_click=lambda: Toast.success("report.pdf is saved.", title="Saved"))
        SmartButton(text="A side panel", on_click=side_panel.open)
        SmartButton(text="Loading", on_click=show_loading)


def ask_delete():
    if Dialog.confirm("report.pdf goes to the trash.", title="Delete the file?", confirm_text="Delete", danger=True):
        tell("The file is deleted.")


def show_loading():
    """A loading screen over the whole window; close() lets it go after LOADING_TIME."""
    loading = LoadingScreen(title_text="My App", message_text="Loading the data...", min_duration=LOADING_TIME, remove_on_close=True)
    loading.close()


if __name__ == "__main__":
    App(start, title="OzdenUI minimal", size=(1000, 820), theme=sys.argv[1] if len(sys.argv) > 1 else "light", style=STYLE).run()
