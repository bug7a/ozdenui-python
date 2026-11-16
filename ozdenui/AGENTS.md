# OzdenUI for Python: rules for an AI assistant

This project uses **OzdenUI** (`pip install ozdenui`): desktop windows written in plain Python. It is a new library,
so do not guess from tkinter, Qt or a web framework: there is no `mainloop()`, no `pack()` / `grid()`, no HTML, no
CSS file and no JavaScript to write. Everything below is the whole way of working.

## Where the truth is

- **The params, callbacks and methods of a class:** `python -c "import ozdenui; help(ozdenui.SelectBox)"`, or the file
  `__init__.pyi` in the installed package (`python -c "import ozdenui; print(ozdenui.__path__[0])"`). Read it before
  you use a class for the first time; never invent a param.
- **The handbook** (10 short chapters, whole programs): https://bug7a.github.io/ozdenui-python/handbook/
- **Example programs:** https://github.com/bug7a/ozdenui-python/tree/main/examples (`gallery.py` shows every component).

## A program

```python
from ozdenui import App, HGroup, Label, ScrollArea, SmartButton, TextField, Toast, VGroup

PAGE_COLOR = "#F4F5F7"
view = {}                                       # the objects the program changes later
notes = []                                      # the data of the program is plain Python

def start(page):                                # runs when the window is ready: make the objects here
    page.color = PAGE_COLOR
    with VGroup(gap=0):                         # a group is as large as its box: here the whole window
        with HGroup(height=52, padding=[16, 0], gap=10, align="left center", color="white"):
            view["name"] = TextField(placeholder="A new note", width=260, on_enter=add_note)
            SmartButton(text="Add", tone="cyan", on_click=add_note)
        with ScrollArea(padding=16, gap=10, align="left top") as view["notes"]:   # takes the room that is left
            view["empty"] = Label(text="No notes yet", font_size=15)
        view["count"] = Label(text="Notes: 0", font_size=13, height=28)

def add_note():
    typed = view["name"].text.strip()           # the state is in Python: reading asks nothing of the window
    if not typed:
        Toast.warning("Write a note first.")
        return
    notes.append(typed)
    with view["notes"]:                         # objects made later go into a box the same way
        Label(text=typed, font_size=15)
    view["empty"].visible = False
    view["name"].text = ""
    view["count"].text = f"Notes: {len(notes)}"

App(start, title="Notes", size=(480, 420)).run()   # once, at the end of the program, on the main thread
```

- `App(start, title=, size=(w, h), theme="light" | "dark" | "auto", style="" | "minimal", accent="#2A78D6")`.
  Inside the functions it is `page.app` (`page.app.close()`, `page.app.set_title()`, `page.app.theme`).
- Objects are made in `start()` or later (an event, a timer), never before `run()`.
- The app outside `start()`: `app = App(start, title=...)`, then `app.run()` on the last line; the functions use `app`.
- A class works as well as the dict: `self.name = TextField(...)`, then `App(MyApp().start).run()`.

## Objects and values

- Five plain objects: `Box`, `Label`, `Button`, `Input`, `Icon`. The rest are components (below).
- A value is a keyword when the object is made and an attribute later: `label.text = "Hi"`,
  `label.set(text="Hi", font_size=20)`. Names are snake_case (`font_size`, `text_color`, `title_text`).
- Every object: `color` (the background), `border`, `border_color`, `round`, `opacity`, `visible`, `width`, `height`,
  `css={...}`. A size is a number (px) or a text: `"100%"`, `"auto"`.
- `text` is shown exactly as written (a `<b>` stays `<b>`); HTML goes in as `html=`.
- `obj.remove()` removes it for good; to hide it for a while: `obj.visible = False`.

## Layout

- **Only a `Box` and the groups hold objects**, with a `with` block. `with Label():` is an error.
- `VGroup` (one under the other), `HGroup` (side by side), `GridGroup(columns=4)`:
  `gap`, `padding` (`20` or `[x, y]`), `align` (`"center"` is the default; `"left top"`, `"right center"`...), `wrap=True`.
- **A group is `width="100%"`, `height="100%"` by default.** A group inside another one almost always needs one of:
  `hug=True` (as large as its objects), `height="auto"` / a number, or `fill=True` (the room the others leave: the
  height in a `VGroup`, the width in an `HGroup`). Two groups of 100% in one `VGroup` squeeze each other.
- A typical window: `VGroup(gap=0)` holding a bar of a fixed height, a middle part with `fill=True` (or a
  `ScrollArea`, which takes the room by itself and scrolls), a line at the bottom.
- In a group an object needs only its size. Outside a group it has a place: `Box(20, 20, 100, 100)` is
  `left, top, width, height` (for a game or a drawing).

## Events

- `on_click=fn` when the object is made, `obj.on_click = fn` later, `obj.on("keydown", fn)` for one more handler.
- A handler takes what it needs: `fn()`, `fn(obj)` or `fn(obj, event)` (`event` is a dict: `key`, `x`, `y`, `shift`...).
- In a loop keep the value with a default: `on_click=lambda number=number: pick(number)`.
- A component tells a change with a callback param: `on_change=fn`. **A change made by the code does not call it**,
  only the user's does.
- Everything runs one at a time on one thread, so no locks; but a slow function freezes the window. Never
  `time.sleep()` in an event: `after(ms, fn)` once, `every(ms, fn)` again and again (both return a function that stops
  it), and a slow job (a download, a big file, an AI call) goes to `run_in_background(job, *args)`, which may change
  the objects directly. A thread of your own uses `call_soon(fn)`.

## Components

Each is a class of `ozdenui`; its state is read from Python (`field.text`, `select.value`, `box.checked`).

| For | Classes |
|---|---|
| Buttons | `SmartButton(text=, tone="cyan" main / "orange" delete / "accent", on_click=)`; `button.waiting = True` |
| Fields | `TextField`, `EmailField`, `PasswordField`, `NumberField`, `CurrencyField`, `PhoneField`, `UrlField`, `TextAreaField`, `SearchInput`, `TagInput` (`title_text`, `placeholder`, `required=True` then `field.check()`) |
| Choices | `CheckBox`, `Toggle`, `RadioButton` (`RadioButton.value_of(group)`), `SelectBox(options=, value=)`, `Slider`, `SliderField`, `RangeSlider`, `Stepper`, `DatePicker`, `TimePicker`, `ColorPicker` |
| Lists and tables | `ItemList(items=)`, `SortableList`, `TreeView`, `SmartTable(columns=, rows=)` (very many rows), `DataTable` |
| Areas that hold objects | `ScrollArea`, `Tabs` (`with tabs.panel("Name"):`), `Accordion` (`with acc.section("Name"):`), `Splitter` (`split.first`, `split.second`), `SidePanel` (`panel.body`) |
| Bars | `MenuBar`, `ToolBar`, `StatusBar`, `ContextMenu` |
| Messages | `Dialog`, `Toast`, `Tooltip`, `LoadingScreen`, `ProgressBar`, `StepBar` |
| Views | `GraphBox` (charts), `LogView`, `ImageView`, `MarkdownView`, `JsonView`, `JsonEditor`, `CodeEditor`, `Canvas`, `ChatView`, `WebView`, `FilePicker` |

- A dialog returns its answer, like `input()`: `if Dialog.confirm("Delete it?", danger=True):`,
  `name = Dialog.prompt("Name:")` (`None`: cancelled), `Dialog.alert(...)`, `Dialog.ask(..., buttons=[...])`.
- `Toast.success("Saved.")`, `.error()`, `.warning()`, `.info()` never wait.
- The file dialogs of the system: `open_file()`, `save_file()`, `choose_folder()` return a real path or `None`.
- A picture (`Icon(picture=)`, `ImageView`) takes a path, bytes, a Pillow image or a matplotlib figure.
- `SmartTable`: a row may carry keys that are not columns (`"id": 7`); `table.selected_row` and
  `on_select(table, row)` give them back, so find a row by its id, not by its texts. The values are shown as text:
  format the numbers in Python.
- A component of the kit without a class: `Component("Gauge", value=72)` with `App(start, components=["Gauge"])`.

## Looks

- `App(start, theme="dark")`: every component takes its dark look by itself. For your own colors use
  `page.app.theme` (`"light"` or `"dark"`): `TEXT = {"light": "#5A6270", "dark": "#9AA3B5"}[page.app.theme]`.
- `App(start, style="minimal", accent="#2A78D6")`: a small look made of lines, in one color; the main button is
  `SmartButton(tone="accent")`.
- `page.app.set_theme("dark")` changes the theme while the program runs: the page is made again and `start()` runs
  again, so every object is new and the timers set before are gone. Keep the data in variables outside `start()`,
  fill the objects from them in `start()`, and set the timers there.
- One component: `style_name="..."` (its packages are named in its docstring), or `style={"box": {"color": "#FFF"}}`.
- Keep the colors of a program as names at the top of its file.

## Mistakes to avoid

1. A param that does not exist. The terminal says it with the line of the program
   (`ozdenui: form.py:12: Label: "txet" is not a param of Label`): run the program and **read the terminal**.
2. A nested group without `hug=True`, `fill=True` or a height (see Layout).
3. Reading a value that was never given (`label.width` of an `"auto"` label) raises an error: `obj.measure("width")`
   asks the window. Keep `measure()` and `ask()` out of loops and out of `run_in_background()` jobs.
4. Putting an object into a `Label` or a button. Make it next to it, in the same box.
5. Waiting in an event (`time.sleep`, a download): the window freezes.
6. Colors written for a light window only, in a program that may open dark.
7. A callback that must answer at once (a validator that returns `False`) can not be a Python function.
8. Saying a window is right without a look at it (`python -m ozdenui look`, below).

## Running and checking

- **Look at the window you made:** `python -m ozdenui look app.py` runs the program as it is, saves a picture of its
  window as `app.png` and closes it. Read the picture: a program that runs without an error can still have a part
  covered, cut or squeezed. `python -m ozdenui look app.py dark.png --theme dark --wait 3`: another file, the dark
  window, more seconds before the picture. (On Windows it needs Pillow and the window in front.)
- `python my_program.py` opens a real window and returns when it is closed. To check a program without a person,
  close it from the code: `after(3000, page.app.close)` as the first line of `start()`, then read the terminal
  (`python -u`: the prints come at once; macOS has no `timeout` command).
- A check that plays the program from code (calls its functions after `start()`) must not reach a `Dialog`: it waits
  for a person. Give the function a way around it in the check.
- `App(start, debug=True)` gives the developer tools of the web view (right click > Inspect).
- macOS and Windows (WebView2). No browser or Jupyter mode.
