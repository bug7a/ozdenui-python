# 1. The first window

## Install

```
pip install ozdenui
```

It needs Python 3.9 or newer. It brings [pywebview](https://pywebview.flowrl.com/), which opens the window. On a Mac
with the Python of the system, upgrade pip first (`python3 -m pip install --upgrade pip`): its old pip tries to build a
part of pywebview from source and fails. On Windows the window needs the WebView2 runtime, which most computers have.

## A window with a counter

```python
from ozdenui import App, HGroup, Label, SmartButton, VGroup

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=16):
        count = Label(text="0", font_size=64, bold=True)
        with HGroup(hug=True, gap=12):
            SmartButton(text="−", on_click=lambda: change(count, -1))
            SmartButton(text="+", tone="cyan", on_click=lambda: change(count, +1))

def change(count, step):
    count.text = str(int(count.text) + step)

App(start, title="Counter", size=(400, 320)).run()
```

Read it from the bottom:

- **`App(start, title=..., size=...)`** is the window. `.run()` opens it and returns when it is closed; call it once, at
  the end of your program, from the main thread.
- **`start(page)`** runs when the window is ready. It makes the objects. `page` is the ground of the window: it has a
  `color`, a `width` and a `height`, and every object without a box of its own is on it.
- **`with VGroup(gap=16):`** opens a group: the objects made inside the block go into it, one under the other, 16 px
  apart. The `HGroup` inside it puts the two buttons side by side; `hug=True` makes it only as large as its buttons.
- **`Label(text="0", font_size=64, bold=True)`** is a text. Its values are keywords.
- **`on_click=lambda: change(count, -1)`** is the event: a click runs the function.
- **`count.text = ...`** changes the label. `count.text` also reads it back, without asking the window.

The window is shown when the first drawing of `start()` is ready, so it never opens empty.

## How it works

The window is the web view of the system (WebKit on a Mac, WebView2 on Windows). The page in it holds basic.js and its
components; the package carries them, so no internet is needed.

```
your Python code ──commands──▶ the page (basic.js objects) ──▶ what you see
        ▲                                     │
        └──────────── events (a click) ◀──────┘
```

- Every object in Python is a small object that sends commands to the page. All the commands of one function
  (`start`, an event, a timer) go together, in one call: 1000 objects take about 50 ms on a Mac.
- A click on the page calls your Python function; its changes are on the screen about 3 ms later.
- Your code runs in Python, with every library you like: files, databases, `requests`, `numpy`, an AI client.

## The App

```python
App(start,
    title="Notes",          # the title of the window
    size=(800, 600),        # width and height in px
    theme="light",          # "light", "dark" or "auto" (what the system asks): chapter 7
    style="",               # "" or "minimal": chapter 7
    components=(),          # more components to load: chapter 5
    debug=False)            # True: the developer tools of the web view (right click > Inspect)
```

`page.app` is the same `App` inside your functions:

```python
page.app.set_title("Notes — saved")
page.app.close()            # closes the window; run() returns
page.app.theme              # "light" or "dark"
page.app.set_theme("dark")  # the window again in another theme: chapter 7
```

## A program in more than one function

Most programs keep the objects they change later. A dict at the top of the file is the simplest place:

```python
from ozdenui import App, Label, SmartButton, TextField, VGroup

view = {}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=14, padding=40):
        view["name"] = TextField(title_text="What is your name?", placeholder="Ada", width=300, on_enter=greet)
        SmartButton(text="Greet", tone="cyan", on_click=greet)
        view["answer"] = Label(text="", font_size=18)

def greet():
    typed = view["name"].text.strip()
    view["answer"].text = f"Hello, {typed}!" if typed else "Write your name first."

App(start, title="Greeting", size=(420, 320)).run()
```

`view["name"].text` is always the text in the field: the page sends it with every key. A `Label` shows a typed text
as it is (a `<b>` stays `<b>`).

A class works just as well (`self.name = TextField(...)`, then `App(TodoApp().start)`): `examples/todo.py` of the package is
written that way, and chapter 9 makes a component of yours with a class.

## When the page is loaded again

With `debug=True`, a reload of the page (right click > Reload) makes the objects again: `start()` runs again and the
timers stop. A program that keeps its data in Python (a list, a file) shows it again; nothing else is needed.

## Next

[Chapter 2: Objects](02-objects.md): the five plain objects and their values.
