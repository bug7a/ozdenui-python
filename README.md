# OzdenUI

A small, modern window of its own in Python, made of [basic.js](https://bug7a.github.io/basic.js/) objects and components.
Only Python: no JavaScript, no HTML, no browser tab, no server. Your Python code makes the objects, and a window shows them.

```python
from ozdenui import App, HGroup, Label, SmartButton, VGroup

def start(page):
    with VGroup(gap=16):
        count = Label(text="0", font_size=64, bold=True)
        with HGroup(hug=True, gap=12):
            SmartButton(text="−", on_click=lambda: change(count, -1))
            SmartButton(text="+", tone="cyan", on_click=lambda: change(count, +1))

def change(count, step):
    count.text = str(int(count.text) + step)

App(start, title="Counter", size=(400, 320)).run()
```

```
pip install ozdenui
```

On a Mac with the Python of the system, upgrade pip first (`python3 -m pip install --upgrade pip`): its old pip tries to
build a part of pywebview from source and fails.

**Learn it step by step:** [the handbook](https://github.com/bug7a/ozdenui-python/blob/main/handbook/README.md), ten short chapters for people who know Python and have
never written a web page (the first window, objects, layout, events, components, dialogs, looks, data, your own
component, going further). Every program in it is run by the tests. In Turkish:
[OzdenUI — El Kitabı](https://github.com/bug7a/ozdenui-python/blob/main/handbook/turkce/README.md).

**Status: v0.1, experimental.** Tested on macOS (Python 3.9, pywebview 6.2), in the web view of the system (WebKit) and in
Chromium, the engine of WebView2. Windows itself is checked by the tests of this repository (GitHub Actions); it needs the
[WebView2 runtime](https://developer.microsoft.com/microsoft-edge/webview2/), which most Windows computers have. Linux needs
the GTK or Qt web view of [pywebview](https://pywebview.flowrl.com/).

## How it works

- The window is the web view of the system (WebKit on macOS, WebView2 on Windows), opened by pywebview. The page in
  it holds basic.js and its components; the package carries them (about 3 MB, no internet needed).
- Your code runs in Python. Every object is a small Python object that sends commands to the page; all the commands
  of a function (start, an event, a timer) go together, in one call.
- On a Mac: 1000 objects in about 50 ms, a click → your Python function → the screen in about 3 ms, the window shows
  in about 0.5 s.

## Objects

| Python | basic.js |
|---|---|
| `Box`, `VGroup`, `HGroup`, `GridGroup`, `Label`, `Button`, `Input`, `Icon` (`examples/basics.py`) | the same names |
| `Box(20, 20, 100, 100, color="red")` | `Box(20, 20, 100, 100, { color: "red" })` |
| `font_size=20` (or `fontSize=20`) | `fontSize: 20` |
| `with VGroup(gap=10):` ... | `VGroup({ gap: 10 })` ... `endGroup()` |
| `label.text = "Hi"` or `label.set(text="Hi", bold=True)` | `label.text = "Hi"` |
| `on_click=fn` or `obj.on("click", fn)` | `obj.on("click", fn)` |
| `obj.remove()` | `obj.remove()` (the objects inside it too) |

- **Groups place their objects.** `VGroup` puts them one under the other, `HGroup` side by side (`gap`, `padding`,
  `align="left top"`, `hug=True` to wrap the content). A group is 100% x 100% by default.
- **`fill=True`** makes an object take the room the others leave: the height that is left in a `VGroup` (a list between
  a tool bar and a status bar), the width that is left in an `HGroup`. Any object takes it: `LogView(fill=True)`,
  `Splitter(fill=True)`. **`ScrollArea()`** does so and scrolls what is in it, one under the other:
  `with ScrollArea(gap=12, padding=16): ...` (as an object of the page: the whole window; the scroll bar of the kit).
- **`GridGroup`** puts its objects in columns and rows, in order: `with GridGroup(columns=3, gap=8):`. `columns` is a number (equal
  columns), a list (`[120, "1fr", "auto"]`) or a CSS text. An object fills its cell (`width="100%"` for one with a width of its own), or
  `align="left center"` puts it in its cell. `grid.place(button, column_span=2)` gives it more cells. See `examples/calculator.py`.
- **Outside a group** an object has a place of its own: `Box(left, top, width, height)`. Without one it starts at the
  top left corner (basic.js itself puts it out of sight until it is placed).
- **Only a Box or a group holds other objects:** `with Label():` is an error.
- **Values:** a value you gave is read back without asking the page (`count.text`). A value of the page is asked with
  `obj.measure("width")`. Every text is shown as it is written (a typed `<b>` stays `<b>`): the `text` of a `Label`
  or a `Button` and the texts of the components. HTML of your own: `html="<b>3</b> new"` on a Label or a Button,
  `allow_html=True` on a component. (In basic.js the `text` of a Label is HTML.)
- **A misspelled name** (`Label(txet="Hi")`) is told in the terminal once, at its line, with the name it may be; so
  is a name of the kit written in camelCase to a class (`TextField(titleText=...)`: write `title_text`). An editor
  (VS Code, PyCharm) offers the params of every class and marks such a name before the program runs (the stubs of
  the package, `ozdenui/__init__.pyi`).
- **Events:** a handler takes what it needs: `fn()`, `fn(obj)` or `fn(obj, event)`; `event` is a dict
  (`key`, `x`, `y`, `text`...). `obj.on_click = fn` replaces the handler given before; `obj.on("click", fn)` adds
  one more. The text of an `Input` is always current in Python: `name.text`; `Input(on_enter=fn)` runs `fn` on Enter, as a
  `TextField` does. The values of the event go only to the
  parameters without a default, so a value of a loop stays: `lambda number=number: pick(number)`.
- **The page:** `page.color = "#F4F5F7"`, `page.width` and `page.height` (always current),
  `page.on("resize", fn)`, `page.on("keydown", fn)`.
- **More of basic.js:** `obj.call("setMotion", "left 0.3s")` calls a method, `obj.ask("getValue")` returns its
  result, `app.evaluate(f"{obj.js}.elem.offsetWidth")` runs JavaScript.

## Components

A component takes its params by their names in snake_case, and a Python function for a callback. Its state is kept
in Python (`box.checked`, `select.value`...). Setting it in code does not call the handler, except the `on_complete` of a
`ProgressBar` (it runs when the value reaches `max_value`), `increase()` and `decrease()` of a `Stepper`, and `add_paths()` of a
`FilePicker`. The names are the names of the kit in snake_case
(`TextField`, `min_value`, `max_value`, `description`...). A param is changed later by its name too, where the
component can change it: `field.unit_text = "kg"`.

| Component | Example | State |
|---|---|---|
| `SmartButton` | `SmartButton(text="Save", tone="cyan", on_click=save)` | `button.waiting = True` shows a clock |
| `TextField` | `TextField(title_text="Name", on_change=fn, on_enter=fn)` | `field.text`, `field.check()` |
| `EmailField`, `PasswordField` | `EmailField(title_text="E-mail", required=True)` | `field.text`, `field.check()` |
| `NumberField` | `NumberField(title_text="Count", value=3)` | `field.value` (a number or `None`), `field.text` |
| `UrlField` | `UrlField(title_text="Site", text="github.com")` | `field.text`: the whole address, with the protocol chosen at its start (`https://github.com`) |
| `PhoneField` | `PhoneField(title_text="Phone", country_code="+1", unit_text="US")` | `field.text`: the number in its mask (`+1 (555) 123-4567`), `field.is_valid()` |
| `CurrencyField` | `CurrencyField(title_text="Price", value=1234.5, unit_text="$")` | `field.value` (a number or `None`), `field.text` (`1,234.5`) |
| `TextAreaField` | `TextAreaField(title_text="Note", height=120, on_change=fn)` | `area.text` |
| `SearchInput` | `SearchInput(placeholder="Find", on_change=fn, on_enter=fn)` | `box.text` |
| `CheckBox` | `CheckBox(text="Remember me", checked=True, on_change=fn)` | `box.checked` |
| `Toggle` | `Toggle(value=True, on_change=fn)` | `toggle.value` |
| `RadioButton` | `RadioButton(group="size", value="M", text="Medium")` | `RadioButton.value_of("size")` |
| `SelectBox` | `SelectBox(options=["Apple", "Pear"], value="Pear", on_change=fn)` | `select.value` |
| `Slider` | `Slider(value=30, min_value=0, max_value=100, width=280, on_change_end=fn)` | `slider.value` |
| `SliderField` | `SliderField(text="Volume", value=5, min_value=0, max_value=10, on_change_end=fn)` | `slider.value` |
| `Stepper` | `Stepper(value=2, min_value=0, max_value=10, on_change=fn)` | `stepper.value` |
| `DatePicker` | `DatePicker(value="2026-11-20", on_change=fn)` | `picker.value`, `picker.date` (a `datetime.date`) |
| `TimePicker` | `TimePicker(value="19:30", on_change=fn)` | `picker.value`, `picker.time` (a `datetime.time`) |
| `ColorPicker` | `ColorPicker(value="#3871E0", on_change=fn)` | `picker.value` |
| `FilePicker` | `FilePicker(accept=".csv,.txt", multiple=True, on_change=fn)` | `picker.files`, `picker.paths` |
| `ProgressBar` | `bar = ProgressBar(title_text="Copying", max_value=100); bar.value = 40` | `bar.value` |
| `SortableList` | `SortableList(items=["Sales", "Stock", {"key": "home", "text": "Home", "locked": True}], on_change=fn)` | `lst.items` (your items in the new order), `lst.keys`; `move_item()`, `add_item()`, `remove_item()` |
| `ItemList` | `ItemList(items=["Apple", {"key": "p", "text": "Pear", "description": "Green"}], on_change=fn)` | `lst.items`, `lst.selected_keys`, `lst.selected` (a text item becomes `{"key": "0", "text": "Apple"}`; `"enabled": False` can not be chosen). Pictures: `layout="grid", style_name="gallery"` (a dark window takes `"galleryDark"`), an item `{"text": "Sea", "icon_file": "sea.jpg"}` (a path, bytes, a Pillow image or an address) |
| `SmartTable` | `SmartTable(columns=[{"key": "name", "title": "Name"}], rows=[...], height=300, on_select=fn)` | `table.rows`, `table.selected_row` |
| `TreeView` | `TreeView(items=[{"key": "a", "text": "A", "children": ["b"]}], height=300, on_select=fn)` | `tree.value`, `tree.selected_node` |
| `Tabs` | `tabs = Tabs(tabs=["A", "B"])`, then `with tabs.panel("A"): ...` | `tabs.value` |
| `Accordion` | `acc = Accordion(sections=["A", "B"])`, then `with acc.section("A"): ...` | `acc.open_keys` |
| `GraphBox` | `GraphBox(type="bar", labels=["Jan", "Feb"], values=[12, 19], format_value="{:,.0f} TL")` | `graph.set_values([...])`, `graph.save_image("chart.png")` |
| `LogView` | `log = LogView(height=300); log.info("Reading"); log.error("Failed")` | `log.get_text()` |
| `ImageView` | `view = ImageView(height=400); view.set_image(figure)` | `view.zoom_level`, `view.natural_width` |
| `Canvas` | `canvas = Canvas(height=400); canvas.circle(100, 80, 30, fill="orange", draggable=True)` | `canvas.shapes`, `canvas.shape(key)`; `line()`, `rect()`, `polygon()`, `text()`, `image()`, `update_shape()`, `move_shape()`, `save_image()`; `drawing=True`: a pen (`on_draw_end`) |
| `StepBar` | `StepBar(steps=["Cart", "Address", "Payment"], step=1, on_step_click=fn)` | `bar.step`, `next()`, `previous()` |
| `RangeSlider` | `RangeSlider(low=200, high=800, max_value=1000, step=50, width=280, on_change_end=fn)` | `slider.low`, `slider.high`, `set_values(100, 500)` |
| `MarkdownView` | `view = MarkdownView(text="# A report\n\nSome **bold** words"); view.append_text("More")` | `view.text`, `view.headings` |
| `ChatView` | `ChatView(empty_text="Ask something", on_send=answer)`; in `answer`: `key = chat.add_message(role="assistant")`, then `chat.append_text(key, piece)` | `chat.messages`, `chat.busy` (the dots, Stop) |
| `JsonView` | `JsonView(value=answer, height=400, on_select=fn)` | `view.selected_path`, `view.selected_value` |
| `JsonEditor` | `JsonEditor(value=products, height=360, on_change=fn)` | `editor.value` (asks the page), `editor.set_value([...])`; `JsonEditor.open(value=settings, on_apply=fn)` is a window |
| `MenuBar` | `MenuBar(menus=[{"text": "File", "items": [{"text": "Save", "shortcut": "Ctrl+S", "on_click": save}]}])` | `set_item_checked(key, True)` |
| `ToolBar` | `ToolBar(items=[{"key": "save", "icon": "save", "hint": "Save", "on_click": save}, "-", {"key": "bold", "icon": "bold", "toggle": True}])` | `bar.checked_keys`, `set_item_enabled(key, False)` |
| `ContextMenu` | `ContextMenu(target=tree, items=["Open", "-", {"text": "Delete", "on_click": fn}])` | `menu.open_at(x, y)` |
| `StatusBar` | `bar = StatusBar(message="Ready", items=["UTF-8"]); bar.set_message("Saved", "success", 3000)` | `set_busy(True)` shows a circle |
| `Splitter` | `split = Splitter(first_size=240)`, then `with split.first: ...` and `with split.second: ...` | `split.first_size_now` |
| `CodeEditor` | `CodeEditor(value="x = 1", language="python", height=300, on_change=fn)` | `editor.value`, `editor.cursor_line` |
| `Tooltip` | `Tooltip(target=button, text="Saves the file")` | `Tooltip.show(button, "Saved.", time=2000)` |
| `SidePanel` | `panel = SidePanel(title_text="Filters")`, then `with panel.body: ...` and `panel.open()` | `panel.is_open` (also after its cover or Escape closed it) |
| `LoadingScreen` | `loading = LoadingScreen(title_text="My App", message_text="Reading...")`, later `loading.close()` | `set_message()`, `set_progress(0.4)`; it covers the window (`cover=box`: a box) |
| `TagInput` | `TagInput(tags=["audio"], suggestions=["audio", "fitness"], on_change=fn)` | `field.tags` |
| `DataTable` | `DataTable(columns=[{"key": "name", "title": "Name"}], rows=[...], on_select=fn)` | `table.selected_row` (the row as it was given) |
| `WebView` | `WebView(html=figure.to_html(), height=400)`, `WebView(url="https://example.com")` | `view.load(address)`, `load_html()`, `load_file()`, `post_message(data)`; `on_message(view, data)` |

- **`TextField`** and the fields made from it: `required=True` and the rules of a field show a warning on the field. `if name.check() and
  email.check(): save()` shows every warning and tells if there is none. `on_change` runs at every change, `on_enter` on Enter.
  `max_length` and `min_length` (a `PasswordField`) count the letters. A `PhoneField` writes the country code and the marks of
  its mask (`phone_mask=" (___) ___-____"`) by itself, and a number given in code or pasted goes into it (`"0555 123 45 67"`);
  the defaults of the kit are `"+90"` and `"TR"`. A `CurrencyField` writes its number in groups (`group_separator`,
  `decimal_separator`, `max_decimal_digits`). A `UrlField` starts with `https://` (the kit: `https://www.`); a change of its
  protocol calls `on_change` too.
- **`SortableList`**: the user changes the order: the grip at the left drags a row (`drag_by="row"`: the whole row), and with the
  keys Space grabs a row, the arrows move it and Space drops it. `lst.items` gives back your own items (the same texts and dicts)
  in the new order. `on_change(lst, item, from_index, to_index)`; `removable=True` adds an x button (`on_remove`),
  `show_buttons=True` up and down buttons; an item with `"locked": True` does not move. A change in code is silent.
- **`FilePicker`** gives real paths: a file dropped on it or chosen after a click (the file dialog of the system) reaches Python as
  `{"name", "path", "size", "size_text", "type", "extension", "last_modified"}`, so `open(file["path"])` reads it. `picker.add_paths()`
  adds files from code. A folder dropped on it is not read; `directory=True` chooses a folder with a click. `icon_file`: a
  picture of yours in the place of its icon.
- **`GraphBox`**: line, area, bar, pie, doughnut, radar, scatter, bubble; no other library is needed. The values may be numpy arrays or a
  pandas Series. `format_value` is a text and not a function, because the page needs the text of a number while it draws:
  `{}`, `{:.2f}`, `{:,}`, `{:,.0f} TL`, `{:d}`, `{:.1%}`.
- **`TreeView`** reads a folder only when it opens: a node with `"has_children": True` and no children calls
  `on_load_children(tree, node)`, which answers with `tree.set_children(node["key"], [...])`. See `examples/files.py`.
  A node: `key`, `text`, `description` (a soft text at its end, Ex: a size), `tag`, `icon_file`, `enabled`, `children`.
- **`Accordion`**: sections that fold. `multiple=False` keeps one open. A closed section keeps its objects, and objects can be made in it
  while it is closed. A section: a text, or `{"key", "text", "description", "opened", "enabled"}`.
- **The items of a list** (an `ItemList`, a `TreeView`, a `StepBar`, an `Accordion`, `Tabs`, a `StatusBar`, a `ToolBar`, a `SortableList`)
  take the keys of the kit. An item with no `text` and a key its list does not know (`"title"`) would be an empty row:
  the terminal tells it once, at the line of the program:
  `ozdenui: shop.py:12: ItemList: an item has no "text"; "title" is not a key of its items (key, text, description, ...)`.
- **`Tooltip`** has three forms: a hint under the mouse, `Tooltip.show()` a bubble at an object, and
  `Tooltip.popover(button, make_content)`, a bubble that stays and holds objects: `make_content()` makes them when it opens.
- **`SmartTable`** makes only the rows that are seen: 100000 rows reach it in about 2 s on a Mac, and then it stays fast.
  A row is a dict by the keys of the columns, or a list in their order.
- **`LogView`** takes the output of your program: `log.capture_print()` sends `print()` into it (and the errors, as
  errors), `logging.getLogger().addHandler(log.logging_handler())` the `logging` module.
- **`ImageView`** and `Icon(picture=...)` take a path, bytes, a Pillow image, a matplotlib figure or an address
  (`picture_address()` makes the address). A new picture of the same size keeps the zoom and does not blink, so a
  program can keep drawing its plot. A picture goes to the page as a `data:` address: 8 MB in about 150 ms, 32 MB in
  about 0.7 s on a Mac. (The web view of macOS refuses a `file://` picture outside the folder of the page.)
- **`MarkdownView`**: a report, or the answer of an AI as it comes (`append_text()`: what is above stays, and the view follows the end
  until the reader scrolls up). A text is never read as HTML and no script of it runs. `![A plot](plot.png)` reads a file of this
  computer (`picture_folder=`, or next to the file of `load_file()`); a matplotlib figure: `f"![A plot]({picture_address(figure)})"`.
  A picture with an `http` address stays a link, because its address can carry data (the answer of an AI); a text you trust: `remote_pictures=True`. `on_link_click(view, address)`
  takes the links; without it the browser of the computer opens them.
- **`ChatView`**: a conversation with an AI. The user writes at the bottom (Enter sends, Shift+Enter makes a new line) and
  `on_send(chat, text)` gets the text when its bubble is on the view already. An answer is Markdown: `key =
  chat.add_message(role="assistant")`, `chat.busy = True` (three dots until the first words, Stop in the place of Send),
  then `chat.append_text(key, piece)` for every piece, from a background job too (`run_in_background`), and `chat.busy =
  False`. Stop calls `on_stop(chat)`: stop your answer there. `chat.messages` keeps the conversation (`{"key", "role",
  "text"}`), `set_messages()` starts another one. `examples/chat.py` writes its answers itself, word by word: your AI
  goes in its place.
- **`JsonView`** shows any value, also a date, a set or an object of yours (as its text). A branch is made when it opens and a long list
  comes in pages, so a list of a million items opens at once. A click tells the path of a row (`users[0].name`); right click or Ctrl+C copies.
- **`JsonEditor`** writes a list or a dict of JSON in a table: a click on a cell writes in it, a title sorts, rows come pasted
  from a spreadsheet or as a JSON list, and a cell that holds a list or a dict opens as a table of its own. `on_change(editor,
  value)` gets the whole value at every change; `editor.value` asks the page (`None`, and `editor.error_text`, while the table
  can not make one: a name used twice). Only JSON data goes in: a date is refused, as `json` does (it would come back as a text).
  `columns=[{"key": "unit", "options": ["kg", "box"]}]` gives the choices of a cell; `texts={"add_row": "Satır"}` its own texts.
  `JsonEditor.open(...)` is the editor in a window with Cancel and Apply: `on_apply(value)`.
- **`WebView`** shows a web page or an HTML text, with its scripts: a plotly chart (`fig.to_html()`), a folium map
  (`m.get_root().render()`), a table of pandas (`df.to_html()`). A script, a map tile or a picture from the internet needs a
  connection; `fig.to_html()` carries plotly in it (3.5 MB arrive in about 0.25 s). A path of this computer (`url="report.html"`,
  `load_file()`) shows the text of the file: a picture or a style next to it is not loaded, because the web view opens no file
  outside the folder of the package. `on_message(view, data)` gets `window.parent.postMessage(data, "*")` of the page;
  `post_message(data)` sends to it. `auto_height=True` grows the box with its page. A site may refuse to be shown in a frame.
- **`MenuBar`** is in the page, in the look of the window: it is not the menu bar of the system.
- **`ToolBar`**: the row of buttons under the menus. An icon is a name of `ToolBar.ICONS` or your own SVG text; `"-"` is a line, `" "`
  sends the next ones to the right end, `toggle=True` and `group="align"` stay pressed, `items` opens a menu. What does not fit goes
  into a "..." menu and comes back when there is room. A key that is also in a `MenuBar` runs once.
- **`CodeEditor`**: Python, JavaScript, JSON, HTML, CSS, SQL and Bash; only the lines that are seen are drawn. Typing is
  the text box of the web view, so undo, selection and the input of every language work.
- **`framed=False`** takes the frame of a component: no border and no rounded corners on its box, for one that fills the
  room between two bars (a `LogView`, a `CodeEditor`, an `ImageView`, a `Canvas`, a `JsonEditor`). It is
  `style={"box": {"border": 0, "round": 0}}` in one word; a key of your own `style` wins. See `examples/editor.py`.

The other components of basic.js (about 40 in the package) work without a Python class of their own:

```python
from ozdenui import App, Component

def start(page):
    Component("Gauge", 20, 20, 180, 180, value=72, sub_text="Disk")

App(start, components=["Gauge"]).run()  # loads the component and what it needs
```

## Your own component

A component of your own is a Python class that makes its objects in a `with` block. No JavaScript is needed:

```python
from ozdenui import App, HGroup, Label, SmartButton, VGroup

CARD_LOOK = dict(width=220, height="auto", align="left top",
                 padding=16, gap=8, color="white", round=12)

class Card:
    """A card: a title, a text and a button."""

    def __init__(self, title, text, on_open=None):
        self.on_open = on_open
        with VGroup(**CARD_LOOK) as self.box:
            self.title = Label(text=title, font_size=18, bold=True)
            Label(text=text, text_color="#5A6270")
            SmartButton(text="Open", on_click=self.open)

    def open(self):
        if self.on_open:
            self.on_open(self)

    def set_title(self, title):
        self.title.text = title

def start(page):
    page.color = "#F4F5F7"
    with HGroup(gap=16, padding=24, wrap=True):
        for name in ["Sales", "Stock", "Orders"]:
            Card(name, "Updated today.",
                 on_open=lambda card: card.set_title("Opened"))

App(start, title="Cards", size=(760, 240)).run()
```

- **A plain class, not a subclass of `Box`:** the class keeps its objects (`self.box`, `self.title`). A name set on
  a basic.js object goes to the page as one of its values (`box.title = ...` changes the box, it keeps no label).
- **Methods change it** (`set_title()`), as the `setX()` methods of the components of basic.js do.
- **Share it as a file:** put it in `card.py`, then `from card import Card` in every program that needs it.
- Its objects are ordinary objects: `card.box.remove()` removes the card with the objects inside it,
  `card.box.on("click", fn)` and `card.title.measure("width")` work as on any other object.
- **The rule of thumb:** "a click, then a change" belongs to Python; "every frame, every mouse move" belongs to the page.
- **A callback that must answer at once** can not be a Python function, Ex: the function that draws a row of a list
  (`createItemView`). See "Limits of v0.1".
- **A fast, continuous event** (dragging, following the mouse) sends every move to Python and stutters: give the motion
  to the page instead (`obj.call("setMotion", "left 0.3s")`, then `obj.left = 200`: the page moves it smoothly).
  A `Canvas` does so by itself: the page draws the free lines and the drags, Python hears only their ends.

## Light and dark

One word makes the whole window dark: every component takes its dark look, the dialogs and the toasts too, and the page,
a `Label`, a `Box` and an `Input` follow. A `tone` of a `SmartButton` becomes its dark tone.

```python
App(start, theme="dark").run()       # "light" (default), "dark", or "auto": what the system asks
page.app.theme                       # "light" or "dark": for the colors of your own objects
page.app.set_theme("dark")           # the window again in another theme: its page is made again, start() runs again
```

A look you give stays: `CheckBox(style_name="modern")`, `Label(text_color="red")`. A component without a dark look keeps
its light one (`Component("Filters")`).

`LogView`, `ImageView`, `MarkdownView`, `JsonView`, `ChatView`, `RangeSlider`, `StepBar`, `Canvas`, `MenuBar`, `ToolBar`, `StatusBar`, `Splitter`, `CodeEditor`, `Accordion` and `GraphBox` also change their theme while they are
on the page; what they show stays:

```python
log.set_theme("dark")                # log.theme = "dark" does the same
page.color = "#1C1C1B"               # the page is yours
```

The other components take their look when they are made.

## Minimal

`App(style="minimal")` gives the components their minimal look: small (28 px controls, 13 px text) and made of lines,
with no fill and no shadow of their own, so they take the ground of the window; with `theme="dark"` the minimalDark
look. About 40 components have it (the fields, the choices, the pickers, the lists, the tables, the bars, the dialogs, a
`GraphBox`...); the others keep their usual look.

```python
App(start, style="minimal").run()                         # also theme="dark"
SmartButton(text="Send", tone="ink")                      # the main action: the one filled button
SmartButton(text="Delete", style_name="minimalDanger")    # a delete (minimalDangerDark in a dark window)
```

`examples/minimal_theme.py` shows every one of them (`python minimal_theme.py dark`: in a dark window).

**In a color:** `accent` gives the minimal look one color of yours. It goes where the look draws its ink: an on toggle,
a checked box, the fill of a slider and of a progress bar, the selected tab, row and step, the edge of a field while
typing, and the main button (`tone="accent"`). The lines, the texts and the focus ring stay as they are.

```python
App(start, style="minimal", accent="#2A78D6").run()       # choose a color that reads on white
App(start, style="minimal", accent="#2A78D6", accent_dark="#7FB6DE", theme="dark").run()
SmartButton(text="Send", tone="accent")                   # the main action of any window ("ink" without an accent)
```

In a dark window the color is made lighter until it reads on the dark ground, unless `accent_dark` gives it. The text
on the color is white or dark, the one that reads better. Any other color of a component can still be given with its
`style`. `examples/minimal_accent.py` shows it (`python minimal_accent.py dark`).

## Dialogs and messages

Each dialog returns its answer; the window keeps working while your code waits:

```python
from ozdenui import Dialog, Toast

if Dialog.confirm("The file will be deleted.", title="Delete it?", confirm_text="Delete", danger=True):
    ...
name = Dialog.prompt("A name for the folder:", value="Photos")      # the text, or None
choice = Dialog.ask("Save the changes?", buttons=["Save", "Don't save", "Cancel"])
Dialog.alert("Done.")
Toast.success("Saved.")       # also Toast.error / warning / info
```

## The app

```python
app = App(start, title="Tool", size=(800, 600), components=())   # page.app is the same App
app.run()                       # opens the window; returns when it is closed (call it from the main thread)
app.set_title("New title"); app.close()

from ozdenui import every, after, run_in_background, call_soon, open_file, save_file, choose_folder

every(1000, tick)           # again and again (the loop() of basic.js); returns a function that stops it
after(500, later)           # once; returns a function that cancels it
run_in_background(job, x)   # a job on a thread of its own; it may change objects (a progress bar)
call_soon(task)             # task() on the app thread, from any thread
open_file(file_types=("Images (*.png;*.jpg)",))   # also save_file(), choose_folder(): a path or None
```

They work in any function of the program, so a button gives its function nothing: `SmartButton(text="Open",
on_click=open_picture)`. The app has them too (`app.every(...)`).

**Threads:** `start`, the events and the timers run one at a time, on one thread: no locks are needed. A job of
`run_in_background` may change objects; it may not `measure()` (that is refused with a clear message).

**A dialog in `start()`** works: the window is shown first. If the page is loaded again (the reload of
`debug=True`), the timers stop and `start()` runs again.

## Examples

In the `examples/` folder of the source: `basics` (a Box, an Icon, a Label, an Input and a Button, each in a place of its own), `calculator` (a GridGroup), `counter`,
`greeting` (a TextField), `gallery` (every component; its Dark / Light button: `page.app.set_theme()`), `gallery-styled` (the gallery with some looks and a color chosen by the code: `style_name`, `style`, `track_color`), `form` (fields, a date, a time,
a color, a number), `charts` (a live line, bars, a doughnut), `files` (a tree, a menu and files dropped with their paths),
`file_tool` (a file dialog, a background job and a progress bar), `csv_viewer` (a CSV in a SmartTable, 100000 rows too),
`todo` (an ItemList; the program is a class), `settings` (Tabs with a form), `dialogs`, `clock` (timers), `game` (places of their own and keys),
`image_viewer` (a plot drawn again and again), `job_log` (`print()` and `logging` in a LogView) `editor` (a small code
editor that runs its Python) `markdown_editor` (write on the left, read on the right), `json_viewer` (the path of a row, right click to copy),
`json_editor` (the products of a shop in a JsonEditor, the settings in its window), `chat` (a ChatView whose answer comes word by
word from a background job, with Stop), `photos`
(the pictures of a folder in an ItemList gallery, one of them large in an ImageView), `paint` (a Canvas: a pen, a shape to drag, the drawing saved as a picture)
`minimal_theme` (every component in its minimal look: `App(style="minimal")`) and `minimal_accent` (the minimal look
in one color: `App(style="minimal", accent="#2A78D6")`).

## Limits of v0.1

- Tested only on macOS. Windows and Linux are not tested yet.
- A callback that must answer at once can not be a Python function, because the answer comes later: the
  `on_before_click` of a SmartButton, an `on_close` of Tabs that returns `False`, the `validate` of a TagInput, and functions
  that build objects inside a component (`createItemView` of a list, `createCellView`). Format the values of a SmartTable in Python;
  a number of a `GraphBox` or a `Stepper` takes a format text. The same for the `color_of` and `options_of` of a JsonEditor
  (its `columns` give the choices), and its `on_pick_color` and `on_pick_picture`: their cell is written with a function of
  the page. Without them a color cell opens the color picker of the web view, and a picture cell takes its address as a text.
- `set_theme()` is in fifteen components (see "Light and dark"); the others take their look when they are made, so
  `page.app.set_theme()` changes a whole window by making its page again: its objects start again (a text typed in a
  field is gone), what the program keeps in its own variables stays.
- No browser or Jupyter mode yet.

## Development

```
python3 -m venv .venv && .venv/bin/python -m pip install --upgrade pip && .venv/bin/python -m pip install -e . pytest build pillow mypy
.venv/bin/python -m pytest tests          # the Python side, without a window
.venv/bin/python checks/run_all.py        # every example in its real window, played as a user would; a problem names
                                          # its line of the play (a page error: the step it came after)
.venv/bin/python checks/check_handbook.py pictures   # every program of the handbook in its window; pictures/sheet.png
.venv/bin/python checks/look.py gallery chat.png 1.5 1000 860 --run "scroll_to(first(ChatView))" --clip "first(ChatView)"
                                          # a picture of an example: --run code before it (first(), scroll_to(), click(),
                                          # js()), --clip only the part of these objects
.venv/bin/python bench/bench.py           # the measurements (bench/results.json)
BASIC_REPO=path/to/js-components ./update-web.sh    # copies basic.js and comp/ from that repository again
./update-web.sh --commit HEAD                       # the same, as they are in a commit (not the changes of the folder)
.venv/bin/python make_stubs.py            # ozdenui/__init__.pyi again (update-web.sh runs it)
PYWEBVIEW_GUI=qt python checks/run_all.py # the same check in Chromium, on a Mac (needs PyQt6, PyQt6-WebEngine, qtpy)
```

After a new copy of the kit, `tests/test_kit_names.py` names every param, method, state and key of an item that the kit
does not have any more: the page takes a name it does not know without a word. `ozdenui/__init__.pyi` (the stubs) gives
an editor the params of every class, from the same lists: `tests/test_stubs.py` fails while it is old.
`tests/test_types.py` reads the examples and the handbook with mypy and the stubs, as an editor would (skipped without
mypy). `tests/test_headers.py`: every code file
has its header (Bismillah, its name and version, the license block); an example has only Bismillah.

On Windows, `checks\run_windows.bat` makes the environment and runs all of it; its result is in `checks\windows-result.txt`.

## License

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0 (see `LICENSE` and `NOTICE`), the same as basic.js.

Developed with the help of Claude Code (Anthropic).
