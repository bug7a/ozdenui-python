# Bismillah
"""Every component with a Python class, on one page. The line at the bottom says what was changed last.
python gallery.py dark: the same page in a dark window (App(theme="dark")). The Dark / Light button of the ToolBar
draws it again in the other theme (page.app.set_theme()).
"""

import sys

from ozdenui import (Accordion, App, Box, Canvas, ChatView, CheckBox, CodeEditor, ColorPicker, ContextMenu, CurrencyField, DatePicker, Dialog,
                     EmailField, FilePicker, GraphBox, GridGroup, HGroup, ImageView, ItemList, JsonEditor, JsonView, Label, LogView, MarkdownView,
                     MenuBar, NumberField, PasswordField, PhoneField, ProgressBar, RadioButton, RangeSlider, ScrollArea, SearchInput,
                     SelectBox, Slider, SliderField, SmartButton, SmartTable, SortableList, Splitter, StatusBar, StepBar, Stepper, Tabs,
                     TextAreaField, TextField, TimePicker, Toast, Toggle, ToolBar, Tooltip, TreeView, UrlField, VGroup, WebView)

# The colors of this page, for the two themes. (The components take their look from the theme of the window.)
COLORS = {
    "light": {"page": "#F4F5F7", "card": "#FFFFFF", "soft": "#5A6270", "line": "#E1E3E6"},
    "dark": {"page": "#141413", "card": "#232322", "soft": "rgba(255, 255, 255, 0.6)", "line": "rgba(255, 255, 255, 0.12)"},
}
THEME_BUTTON_TEXTS = {"light": "Dark", "dark": "Light"}  # the button of the ToolBar names the other theme
CARD_WIDTH = 440

PEOPLE = [
    {"id": 1, "name": "Ayşe Yılmaz", "city": "İstanbul", "age": 34},
    {"id": 2, "name": "Mehmet Kaya", "city": "Ankara", "age": 41},
    {"id": 3, "name": "Zeynep Demir", "city": "İzmir", "age": 28},
    {"id": 4, "name": "Can Öztürk", "city": "Bursa", "age": 52},
]
COLUMNS = [
    {"key": "name", "title": "Name", "width": 180, "sortable": True},
    {"key": "city", "title": "City", "width": 120, "sortable": True},
    {"key": "age", "title": "Age", "width": 70, "type": "number", "align": "right", "sortable": True},
]


PICTURE = (b'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200"><rect width="320" height="200" fill="#DCEFF1"/>'
           b'<circle cx="160" cy="100" r="60" fill="#5BBAC1"/></svg>')


def picture_of(ground, sun):
    """A small picture made here (an SVG): a ground and a sun. ItemList takes a file path or a Pillow image too."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect width="200" height="200" fill="{ground}"/>'
            f'<circle cx="100" cy="90" r="46" fill="{sun}"/><rect y="150" width="200" height="50" fill="{sun}" opacity="0.5"/></svg>').encode()


PICTURES = [{"key": "sea", "text": "Sea", "icon_file": picture_of("#DCEFF1", "#3F8D94")},
            {"key": "sun", "text": "Sun", "icon_file": picture_of("#FBEBD3", "#E0913A")},
            {"key": "wood", "text": "Wood", "icon_file": picture_of("#E3EEDC", "#5E8C4A")}]
CODE = 'def hello(name):\n    print("Hello", name)  # a comment\n\nhello("world")\n'
PRODUCTS = [{"name": "Honey", "price": 150, "in_stock": True}, {"name": "Olive oil", "price": 420, "in_stock": False},
            {"name": "Tea", "price": 95, "in_stock": True}]
# A page of HTML with its own script: a click sends a message to Python (on_message of the WebView)
WEB_PAGE = """<body style="margin: 16px; font: 15px -apple-system, 'Segoe UI', sans-serif">
<p style="margin: 0 0 12px">An HTML page with its own script.</p><button id="send">Send to Python</button>
<script>let count = 0; send.onclick = function () { parent.postMessage({count: ++count}, "*"); };</script></body>"""

view = {}


MARKDOWN_NOTE = """### A small report

The **sales** went up. Read the [notes](https://example.com/notes).

| Product | Total |
|:---|---:|
| Honey | 3,150 TL |

- [x] Write it
- [ ] Send it

```python
total = sum(rows)
```
"""


def card(title):
    """A white card with a title; the objects of its "with" block go under the title."""
    group = VGroup(width=CARD_WIDTH, height="auto", align="left top", gap=14, padding=20, color=view["colors"]["card"], round=12)
    with group:
        Label(text=title, font_size=13, bold=True, text_color=view["colors"]["soft"])
    return group


def tell(text):
    view["status"].set_message(text)


def start(page):
    view["colors"] = COLORS[page.app.theme]
    view["app"] = page.app
    page.color = view["colors"]["page"]
    with VGroup(gap=0, align="left top"):
        MenuBar(menus=[
            {"text": "File", "items": [{"text": "New", "shortcut": "Ctrl+N", "on_click": lambda: tell("New was chosen.")}, "-",
                                       {"text": "Recent", "items": ["a.txt", "b.txt"]}]},
            {"text": "View", "items": [{"text": "Word wrap", "key": "wrap", "checked": True, "on_click": toggle_wrap}]},
            {"text": "Help", "items": [{"text": "About", "on_click": lambda: tell("About was chosen.")}]},
        ])
        ToolBar(on_click=tell_tool, items=[
            {"key": "new", "icon": "new", "hint": "New"},
            {"key": "save", "icon": "save", "hint": "Save"},
            "-",
            {"key": "bold", "icon": "bold", "hint": "Bold", "toggle": True},
            {"key": "left", "icon": "align_left", "hint": "Align left", "group": "align", "checked": True},
            {"key": "right", "icon": "align_right", "hint": "Align right", "group": "align"},
            "-",
            {"key": "insert", "text": "Insert", "items": ["A picture", "A table"]},
            " ",
            {"key": "theme", "text": THEME_BUTTON_TEXTS[page.app.theme]},
            {"key": "run", "icon": "play", "text": "Run", "shortcut": "F9"},
        ])
        with ScrollArea(align="center top", gap=20, padding=30):
            draw_cards()
        view["status"] = StatusBar(message="Change something.", items=["UTF-8", {"key": "count", "text": "53 classes"}])


def tell_tool(bar, item):
    if item.get("key") == "theme":  # WHY get: an item of the Insert menu has no key
        switch_theme()
        return
    tell(f"{item.get('hint') or item.get('text')}, pressed: {bar.checked_keys}")


def switch_theme():
    """The other theme: the page is drawn again, start() runs again with the new page.app.theme."""
    app = view["app"]
    app.set_theme("light" if app.theme == "dark" else "dark")


def toggle_wrap(bar, item):
    view["log"].wrap_lines = not item["checked"]
    bar.set_item_checked("wrap", not item["checked"])
    tell(f"Word wrap: {not item['checked']}")


def draw_cards():
    """The cards, one under the other in the ScrollArea."""
    Label(text="OzdenUI: the components", font_size=24, bold=True)

    # WHY one row of two columns: a new row started under the taller column and left an empty area beside the shorter one.
    # A new card goes into the shorter column.
    with HGroup(width="auto", height="auto", align="left top", gap=20):
        with VGroup(width=CARD_WIDTH, height="auto", align="left top", gap=20):
            with card("SmartButton"):
                with HGroup(hug=True, gap=8):
                    SmartButton(text="Save", tone="cyan", on_click=lambda: Toast.success("Saved."))
                    SmartButton(text="Cancel", on_click=lambda: tell("Cancel was clicked."))
                    SmartButton(text="Delete", tone="orange", on_click=lambda: ask_delete(tell))

            with card("CheckBox, Toggle, RadioButton"):
                CheckBox(text="Remember me", checked=True,
                         on_change=lambda box: tell(f"Remember me: {box.checked}"))
                with HGroup(hug=True, gap=10, align="left center"):
                    Toggle(value=True, on_change=lambda toggle: tell(f"Notifications: {toggle.value}"))
                    Label(text="Notifications", font_size=15)
                with HGroup(hug=True, gap=18):
                    for size in ("S", "M", "L"):
                        RadioButton(group="size", value=size, text=size, checked=(size == "M"),
                                    on_change=lambda radio: tell(f"Size: {RadioButton.value_of('size')}"))

            with card("SelectBox, SliderField"):
                SelectBox(options=["İstanbul", "Ankara", "İzmir", "Bursa"], value="Ankara", width="100%",
                          on_change=lambda box: tell(f"City: {box.value}"))
                SliderField(text="Volume", value=6, min_value=0, max_value=10, width="100%",
                            on_change_end=lambda slider: tell(f"Volume: {slider.value}"))

            with card("ProgressBar"):
                bar = ProgressBar(title_text="Uploading", value=40, width="100%")
                with HGroup(hug=True, gap=8):
                    SmartButton(text="+10", on_click=lambda: bar.add_value(10))
                    SmartButton(text="Reset", on_click=lambda: bar.set_value(0))

            with card("LogView"):
                view["log"] = LogView(height=170, lines=[{"text": "Started", "level": "info"},
                                                         {"text": "14 files found", "level": "success"},
                                                         {"text": "A file is very large", "level": "warn"},
                                                         {"text": "A file can not be read", "level": "error"}])
                SmartButton(text="Write a line", on_click=lambda: view["log"].info("A new line"))

            with card("Splitter"):
                with Box(width="100%", height=120, color="transparent", border=1, border_color=view["colors"]["line"], round=8):
                    split = Splitter(first_size="40%")
                    with split.first:
                        Label(text="Drag the line", font_size=14, text_color=view["colors"]["soft"], padding=10)
                    with split.second:
                        Label(text="The other area", font_size=14, text_color=view["colors"]["soft"], padding=10)

            with card("Tabs"):
                tabs = Tabs(tabs=["General", "Advanced"], on_change=lambda t: tell(f"Tab: {t.value}"))
                with tabs.panel("General"):
                    Label(text="The general settings.", font_size=14)
                with tabs.panel("Advanced"):
                    Label(text="The advanced settings.", font_size=14)

            with card("TextField, EmailField, PasswordField, NumberField"):
                TextField(title_text="Name", placeholder="Ada", width="100%", on_change=lambda field: tell(f"Name: {field.text}"))
                EmailField(title_text="E-mail", width="100%")
                PasswordField(title_text="Password", width="100%")
                NumberField(title_text="Count", value=3, width="100%", on_change=lambda field: tell(f"Count: {field.value}"))

            with card("SearchInput, Slider, Stepper"):
                SearchInput(width="100%", on_change=lambda search: tell(f"Search: {search.text}"))
                Slider(value=30, width="100%", on_change_end=lambda slider: tell(f"Slider: {slider.value}"))
                Stepper(value=2, min_value=0, max_value=10, on_change=lambda stepper: tell(f"Stepper: {stepper.value}"))

            with card("StepBar"):
                StepBar(steps=["Cart", "Address", "Payment"], step=1, on_step_click=lambda bar, index: (bar.set_step(index), tell(f"Step: {index + 1}")))

            with card("RangeSlider"):
                RangeSlider(low=200, high=800, max_value=1000, step=50, width="100%", value_format="{:,.0f} TL",
                            on_change_end=lambda slider: tell(f"Range: {slider.low} - {slider.high}"))

            with card("DatePicker, TimePicker, ColorPicker"):
                with HGroup(hug=True, gap=10):
                    DatePicker(value="2026-11-20", width=140, on_change=lambda picker: tell(f"Date: {picker.date}"))
                    TimePicker(value="19:30", width=110, on_change=lambda picker: tell(f"Time: {picker.value}"))
                    ColorPicker(value="#3871E0", width=130, on_change=lambda picker: tell(f"Color: {picker.value}"))

            with card("GridGroup"):
                with GridGroup(columns=3, gap=8) as grid:
                    for number in range(1, 7):
                        button = SmartButton(text=f"Cell {number}", width="100%", on_click=lambda: tell("A cell was clicked."))
                        if number == 4:
                            grid.place(button, column_span=2)

            with card("UrlField, PhoneField, CurrencyField"):
                UrlField(title_text="Site", width="100%", on_change=lambda field: tell(f"Site: {field.text}"))
                PhoneField(title_text="Phone", width="100%", on_change=lambda field: tell(f"Phone: {field.text}"))
                CurrencyField(title_text="Price", unit_text="$", width="100%", on_change=lambda field: tell(f"Price: {field.value}"))

            with card("SortableList"):
                SortableList(items=["Sales", "Stock", {"key": "pay", "text": "Payments", "description": "Every Monday"}],
                             width="100%", height="auto", on_change=lambda lst, item, a, b: tell(f"Order: {lst.keys}"))

            with card("WebView"):
                WebView(html=WEB_PAGE, width="100%", height=110, on_message=lambda v, data: tell(f"WebView: {data['count']}"))

            with card("ChatView"):
                ChatView(width="100%", height=300, messages=[{"role": "user", "text": "Hello!"}, "Hi! **How** can I help?"],
                         on_send=lambda chat, text: chat.add_message(f"You wrote: {text}"))

        with VGroup(width=CARD_WIDTH, height="auto", align="left top", gap=20):
            with card("TextAreaField"):
                note = TextAreaField(title_text="Note", placeholder="Write something...", width="100%",
                                     height=110, on_change=lambda: tell(f"Note: {len(note.text)} letters"))

            with card("ItemList"):
                ItemList(items=[{"key": "a", "text": "Apples", "description": "Red"},
                                {"key": "p", "text": "Pears", "description": "Green"},
                                {"key": "g", "text": "Grapes", "description": "Purple"}],
                         width="100%", height=170,
                         on_change=lambda lst, items: tell(f"Fruit: {lst.selected_keys}"))

            with card("ItemList: pictures"):
                ItemList(items=PICTURES, layout="grid", width="100%", height="auto", selected_keys=["sun"],
                         style_name="gallery",  # WHY no "galleryDark": a dark window takes it
                         style={"tile": {"width": 120, "iconSize": 104}},  # WHY: three in the row of this card
                         on_change=lambda lst, items: tell(f"Picture: {lst.selected_keys}"))

            with card("Canvas"):
                board = Canvas(width="100%", height=170, on_shape_move=lambda c, shape: tell(f"Moved: {shape['key']}"),
                               on_click=lambda c, x, y, shape: tell(f"Canvas: {shape['key'] if shape else 'empty'}"))
                board.rect(0, 125, CARD_WIDTH, 45, fill="#E3EEDC", key="ground")
                board.polygon([[20, 125], [80, 55], [140, 125]], fill="#9DBE8C", key="hill")
                board.line(170, 150, 330, 150, color="#5E8C4A", line_width=3, dash=[8, 5], key="path")
                board.circle(300, 55, 24, fill="#E0913A", draggable=True, key="sun")
                board.text(16, 12, "Drag the sun", font_size=15, bold=True, key="title")

            with card("SmartTable"):
                SmartTable(columns=COLUMNS, rows=PEOPLE, width="100%", height=230,
                           on_select=lambda table, row: tell(f"Row: {row['name']}"))

            with card("ImageView"):
                ImageView(height=170, image=PICTURE, enlarge_to_fit=True, alt="A circle on a square")

            with card("CodeEditor"):
                CodeEditor(height=150, language="python", value=CODE)

            with card("GraphBox"):
                GraphBox(type="bar", labels=["Jan", "Feb", "Mar", "Apr"], values=[1200, 1900, 700, 1500], width="100%", height=210,
                         format_value="{:,.0f} TL", on_click=lambda graph, item: tell(f"Bar: {item['label']}"))

            with card("TreeView, ContextMenu"):
                tree = TreeView(items=[{"key": "photos", "text": "photos", "expanded": True, "children": ["sea.jpg", "hill.jpg"]},
                                       {"key": "notes", "text": "notes.txt", "description": "4 KB"}],
                                width="100%", height=130, on_select=lambda t, node: tell(f"Node: {node['text']}"))
                ContextMenu(target=tree, items=[{"text": "Open them all", "on_click": tree.expand_all}, "-",
                                                {"text": "Close them all", "on_click": tree.collapse_all}])

            with card("Tooltip"):
                with HGroup(hug=True, gap=8):
                    hint_button = SmartButton(text="A hint")
                    Tooltip(target=hint_button, text="A hint on the button")
                    bubble_button = SmartButton(text="A bubble", on_click=lambda: Tooltip.show(bubble_button, "It goes by itself.", time=1500))
                    popover_button = SmartButton(text="A popover")
                    Tooltip.popover(popover_button, lambda: Label(text="It stays, and holds objects.", font_size=14))

            with card("Accordion"):
                folds = Accordion(sections=[{"key": "more", "text": "More settings", "description": "2", "opened": True}, "Closed at the start"],
                                  on_toggle=lambda a, section: tell(f"Open: {a.open_keys}"))
                with folds.section("more"):
                    CheckBox(text="Save it by itself", checked=True)
                with folds.section("Closed at the start"):
                    Label(text="It was made while it was closed.", font_size=14, text_color=view["colors"]["soft"])

            with card("MarkdownView"):
                MarkdownView(height=250, text=MARKDOWN_NOTE, on_link_click=lambda v, address: tell(f"Link: {address}"),
                             style={"box": {"color": "transparent"}, "page": {"padding": [0, 0]}})

            with card("JsonView"):
                JsonView(height=170, value={"status": "ok", "count": 2, "users": [{"name": "Ada", "active": True}]}, expand_level=2,
                         on_select=lambda v, entry: tell(f"Path: {entry['pathText']}"), style={"box": {"color": "transparent"}})

            with card("JsonEditor"):
                JsonEditor(height=340, value=PRODUCTS, title_text="Products", on_change=count_products)

            with card("FilePicker"):
                FilePicker(width="100%", zone_height=110, multiple=True,
                           on_change=lambda picker: tell(f"Files: {len(picker.files)}"))


def count_products(editor, products):
    """on_change of the JsonEditor: the whole value, as a list of dicts."""
    in_stock = sum(1 for product in products if product.get("in_stock"))
    tell(f"Products: {len(products)}, {in_stock} in stock")


def ask_delete(tell):
    if Dialog.confirm("The file will be deleted.", title="Delete it?", confirm_text="Delete", danger=True):
        tell("Deleted.")
    else:
        tell("Not deleted.")


if __name__ == "__main__":
    App(start, title="OzdenUI gallery", size=(1000, 820), theme=sys.argv[1] if len(sys.argv) > 1 else "light").run()
