# 5. Components

A component is a ready part of a window, made of the objects of chapter 2: a button with a waiting clock, a field with
a title and a warning, a list with a search box, a table of 100000 rows. 53 of them have a Python class; about 35
more work through `Component("Name")`.

## How every component works

```python
remember = CheckBox(text="Remember me", checked=True, on_change=show)
```

- **Params are keywords**, in snake_case: `title_text`, `selected_keys`, `panel_height`. A short name is often there
  too: `text` for `label_text`, `icon` for `icon_file`.
- **A callback is a param**: `on_change=show`. Like an event, it takes what it needs: `show()`, `show(box)`, or more
  (`on_change(lst, selected_items)` of an `ItemList`). The docstring of each class names its arguments:
  `help(ItemList)`.
- **Its state is in Python**: `remember.checked`, `select.value`, `table.rows`. Reading it asks nothing of the page.
- **Changing it** is an attribute or a method: `remember.checked = False`, `bar.value = 40`, `lst.add_item(...)`.
  A param is changed by its name too, where the component can change it later: `field.unit_text = "kg"`.
  A change made by your code does not call the callback; only the user's does. (Two exceptions: `on_complete` of a
  `ProgressBar` runs when its value reaches `max_value`, and `increase()` / `decrease()` of a `Stepper` call `on_change`.)

## A form on two tabs

```python
from ozdenui import (App, CheckBox, HGroup, Label, RadioButton, SelectBox, Slider, SmartButton, Tabs, TextField,
                     Toast, Toggle, VGroup)

view = {}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=16, padding=24, align="left top"):
        Label(text="Settings", font_size=24, bold=True)
        with VGroup(width=460, height="auto", padding=20, gap=16, align="left top", color="white", round=12):
            tabs = Tabs(tabs=["Profile", "Sound"], panel_height=240)
            with tabs.panel("Profile"):
                with VGroup(width="100%", height="auto", gap=14, padding=[0, 16], align="left top"):
                    view["name"] = TextField(title_text="Name", required=True, width=400)
                    view["language"] = SelectBox(options=["English", "Türkçe", "Deutsch"], value="English", width=400)
                    view["news"] = CheckBox(text="Send me the news")
            with tabs.panel("Sound"):
                with VGroup(width="100%", height="auto", gap=16, padding=[0, 16], align="left top"):
                    view["volume"] = Slider(value=7, min_value=0, max_value=10, width=400)
                    with HGroup(hug=True, gap=18):
                        for quality in ("Low", "Normal", "High"):
                            RadioButton(group="quality", value=quality, text=quality, checked=(quality == "Normal"))
                    view["sounds"] = Toggle(value=True)
            SmartButton(text="Save", tone="cyan", on_click=save)

def save():
    if not view["name"].check():          # shows the warning on the field
        return
    settings = {
        "name": view["name"].text,
        "language": view["language"].value,
        "news": view["news"].checked,
        "volume": view["volume"].value,
        "quality": RadioButton.value_of("quality"),
        "sounds": view["sounds"].value,
    }
    print(settings)
    Toast.success("Saved.")

App(start, title="Settings", size=(540, 580)).run()
```

`examples/settings.py` is a longer one with three tabs.

## The components, by what they do

### Buttons

| | |
|---|---|
| `SmartButton(text="Save", tone="cyan", on_click=save)` | `tone`: `"cyan"` the main action, `"orange"` a delete, `"yellow"`, `"green"`, `"blue"`, `"white"`; `"accent"`: the main action of any window (chapter 7) |
| `SmartButton(text="", icon=svg_or_path, aria_label="More")` | an icon button: a square |
| `button.waiting = True` | a clock on it; it takes no clicks until `button.waiting = False` |
| `SmartButton(text="Delete", ask="Click again to delete.")` | the first click asks, the second one runs `on_click` |
| `button.enabled = False`, `button.text = "Saved"` | |

### Fields

| | |
|---|---|
| `TextField(title_text="Name", placeholder="Ada", on_change=fn, on_enter=fn)` | `field.text`; `on_change` at every change, `on_enter` on Enter |
| `EmailField`, `PasswordField`, `NumberField`, `TextAreaField` | the same, for an e-mail, a password, a number (`field.value`), many lines |
| `TextField(required=True)`, then `field.check()` | shows the warning on the field; `True` when there is none |
| `TextField(max_length=40)`, `PasswordField(min_length=8)` | the most and the fewest letters |
| `UrlField(title_text="Site", text="github.com")` | `field.text`: the whole address with its protocol (`https://github.com`) |
| `PhoneField(country_code="+1", unit_text="US")`, `CurrencyField(value=1234.5, unit_text="$")` | the number in its mask; the amount in groups (`field.value` is a number) |
| `SearchInput(placeholder="Find", on_change=fn)` | `fn(box)` at every change, `on_enter` on Enter; `box.text` |
| `TagInput(tags=["audio"], suggestions=[...], on_change=fn)` | `field.tags` |

`if name.check() and email.check(): save()` shows every warning of a form and tells if there is none.

### Choices

| | |
|---|---|
| `CheckBox(text="Remember me", checked=True)` | `box.checked` |
| `Toggle(value=True)` | `toggle.value` |
| `RadioButton(group="size", value="M", text="Medium")` | `RadioButton.value_of("size")` |
| `SelectBox(options=["Apple", "Pear"], value="Pear")` | `select.value` |
| `Slider(value=30, min_value=0, max_value=100, on_change_end=fn)` | `slider.value`; `on_change_end`: when the mouse lets it go |
| `SliderField(text="Volume", value=5, min_value=0, max_value=10)`, `Stepper(value=2, min_value=0, max_value=10)` | `.value` |
| `RangeSlider(low=200, high=800, max_value=1000, step=50)` | `slider.low`, `slider.high` |
| `DatePicker(value="2026-11-20")`, `TimePicker(value="19:30")`, `ColorPicker(value="#3871E0")` | `.value`; also `.date` (a `datetime.date`) and `.time` (a `datetime.time`) |

### Lists, tables and trees

```python
fruits = ItemList(items=["Apple", {"key": "p", "text": "Pear", "description": "Green"}],
                  selection="multiple", height=240, on_change=lambda lst, items: print(lst.selected_keys))
fruits.add_item({"key": "c", "text": "Cherry"})
fruits.remove_item("p")
```

- **`ItemList`**: `lst.items`, `lst.selected_keys`, `lst.selected`. A text item gets its index as its key
  (`{"key": "0", "text": "Apple"}`); `"enabled": False` can not be chosen. `layout="grid", style_name="gallery"` shows
  pictures (`examples/photos.py`).
- **`SmartTable(columns=[{"key": "name", "title": "Name"}], rows=[...], height=300, on_select=fn)`**: very many rows
  (only the rows that are seen are made), a filter box and sorting. `on_select(table, row)`.
- **`DataTable`**: a smaller table that gives the selected row back as you gave it: `table.selected_row`.
- **`TreeView(items=[{"key": "a", "text": "A", "children": ["b"]}], on_select=fn)`**: `tree.value`. A big tree is read
  when a node opens: `"has_children": True` and `on_load_children(tree, node)` (`examples/files.py`).
- **`SortableList(items=["Sales", "Stock"], on_change=fn)`**: the user changes the order (the grip at the left, or Space
  and the arrows); `lst.items` gives your items in the new order. `on_change(lst, item, from_index, to_index)`.
- **The keys of an item** are the names of the kit: `text`, `description`, `icon_file`, `enabled`... An item with no
  `text` and a key its list does not know (`"title"`) would be an empty row: the terminal tells it once, at the line of
  your program.

### Areas that hold your objects

Some components hold objects of yours. Each gives a box to a `with` block:

```python
tabs = Tabs(tabs=["Orders", "Customers"])
with tabs.panel("Orders"):
    Label(text="No orders yet")

acc = Accordion(sections=["General", "Advanced"])
with acc.section("General"):
    CheckBox(text="Start with the system")

split = Splitter(first_size=240)          # two areas, a line to drag between them
with split.first:
    Label(text="Left")
with split.second:
    Label(text="Right")

panel = SidePanel(title_text="Filters")   # slides in from the side
with panel.body:
    CheckBox(text="Only the new ones")
SmartButton(text="Filters", on_click=panel.open)
```

### The bars of a window

| | |
|---|---|
| `MenuBar(menus=[{"text": "File", "items": [{"text": "Save", "shortcut": "Ctrl+S", "on_click": save}]}])` | in the page, in the look of the window; Ctrl is Cmd on a Mac |
| `ToolBar(items=[{"key": "save", "icon": "save", "hint": "Save", "on_click": save}, "-", ...])` | `"-"` a line; `toggle=True` stays pressed; what does not fit goes into a "..." menu |
| `StatusBar(message="Ready", items=["UTF-8"])` | `bar.set_message("Saved", "success", 3000)`, `bar.set_busy(True)` |
| `ContextMenu(target=table, items=["Open", "-", {"text": "Delete", "on_click": fn}])` | a right click on the target opens it |

A window with a menu, a tool bar, a list that takes the room and a status bar is a `VGroup(gap=0)` of them, with
`fill=True` on the middle part (chapter 3).

### Progress and steps

| | |
|---|---|
| `ProgressBar(title_text="Copying", value=0)` | `bar.value = 40` |
| `LoadingScreen(title_text="My App", message_text="Reading...")` | covers the window; `loading.set_progress(0.4)`, `loading.close()` |
| `StepBar(steps=["Cart", "Address", "Payment"], step=1)` | `bar.next()`, `bar.previous()`, `bar.step` |
| `Tooltip(target=button, text="Saves the file")` | a hint under the mouse; chapter 6 has its other forms |

### Views: chapter 8

`GraphBox` (charts), `LogView`, `ImageView`, `MarkdownView`, `JsonView`, `JsonEditor`, `CodeEditor`, `Canvas`, `ChatView` and `WebView`
show data, pictures, code, a conversation and web pages (`JsonEditor` and `CodeEditor` also write them): chapter 8.

### The texts of a component

The texts a component writes itself (a warning, the buttons of a dialog, the message of an empty table) are in English.
Each one changes with a param:

```python
TextField(title_text="Name", required=True, required_text="Needed")                 # in the place of "Required"
Dialog.confirm("The file will be deleted.", title="Delete it?", confirm_text="Delete", cancel_text="Keep it", danger=True)
SmartTable(columns=columns, rows=rows, no_data_found_alert="No records", all_titles_text="ALL")
DatePicker(value="2026-11-20", language="tr")                                       # the months and the days in Turkish
JsonEditor(value=rows, texts={"add_row": "Row", "search": "Search the rows", "table": "Table"})
```

The text params of a component are seen in the default values of its source (`requiredText: "Required"`); in Python
they are written in snake_case. The texts of a `JsonEditor` are in one `texts` dict; its keys may be snake_case too
(`add_row`).

## The other components: Component("Name")

The kit has more components than classes. Any of them works with its name:

```python
from ozdenui import App, Component

def start(page):
    Component("Gauge", 20, 20, 180, 180, value=72, sub_text="Disk")

App(start, components=["Gauge"]).run()    # loads the component and what it needs
```

- `components=[...]` loads the files of the ones the page does not load by itself.
- Its params are the params of basic.js, in snake_case or camelCase; a function is a callback.
- `obj.call("setValue", 80)` calls its methods (chapter 10).
- The list: `Badge`, `Breadcrumbs`, `Filters`, `Gauge`, `HoldToConfirmButton`, `LeftMenu`, `MiniGraphBox`, `Notice`,
  `PageControl`, `TimeLine`, `TinyTable` and more; [the catalog](https://bug7a.github.io/js-components/)
  shows every one with an example.

### A box inside a component

`comp.part("content")` is a box inside a component, to put objects into: `with comp.part("content"): Label(...)`. The
classes above already give theirs (`tabs.panel()`, `split.first`).

## Next

[Chapter 6: Dialogs, messages and files](06-dialogs-and-files.md).
