# OzdenUI — The Handbook

Build a desktop window in plain Python: objects, groups and ready components. Only Python: no JavaScript, no HTML, no
browser tab, no server. This handbook teaches it step by step, for people who know Python and have never written a web page.


```python
from ozdenui import App, Label, SmartButton, VGroup

def start(page):
    with VGroup(gap=12):
        Label(text="Hello from Python", font_size=24, bold=True)
        SmartButton(text="Close", on_click=page.app.close)

App(start, title="Hello", size=(360, 200)).run()
```

## The chapters

| | Chapter | You learn |
|---|---|---|
| 1 | [The first window](01-first-window.md) | install, `App`, `start(page)`, how the window and your code talk |
| 2 | [Objects](02-objects.md) | `Box`, `Label`, `Button`, `Input`, `Icon`; values you set and read; removing |
| 3 | [Layout](03-layout.md) | `VGroup`, `HGroup`, `GridGroup`, `fill=True`, `ScrollArea`, a place of its own |
| 4 | [Events and time](04-events-and-time.md) | clicks and keys, the event dict, timers, a job in the background |
| 5 | [Components](05-components.md) | the ready parts: buttons, fields, choices, lists, tables, tabs, bars |
| 6 | [Dialogs, messages and files](06-dialogs-and-files.md) | `Dialog.confirm()`, `Toast`, bubbles, the file dialogs, files dropped on a `FilePicker` |
| 7 | [Looks](07-looks.md) | dark windows, the minimal look in your color, the colors of one component |
| 8 | [Data and pictures](08-data-and-pictures.md) | charts, big tables, plots, logs, Markdown, JSON, code |
| 9 | [Your own component](09-your-own-component.md) | a class of yours made of objects, shared as a module |
| 10 | [Going further](10-going-further.md) | basic.js from Python, speed, threads, limits, finding a mistake |

Read 1 to 4 in order: they are the whole idea. Then take the chapters you need.

## How to read it

- Every program that imports `ozdenui` and ends with `App(...).run()` is complete: copy it into a file
  and run it with `python file.py`. The tests of the package run every one of them, so they stay true.
- The examples of the package (the `examples/` folder of its source) are longer programs: a to-do list, a file tool,
  a CSV viewer, a paint program. The chapters name them where they fit.
- A name in `code` is a name in Python. The page of the window is made with [basic.js](https://bug7a.github.io/basic.js/),
  a small JavaScript library; you never need to write JavaScript, but chapter 10 shows how to reach it.

## In one minute

- `App(start).run()` opens a window. `start(page)` makes its objects; `page` is the window's ground.
- An object is made where it is written: inside a `with` block it goes into that box or group.
- A group places its objects: `VGroup` one under the other, `HGroup` side by side.
- A value is a keyword (`font_size=20`) and an attribute (`label.text = "Hi"`).
- An event is a function: `on_click=save`. It may take nothing, the object, or the object and the event.
- Components keep their state in Python: `box.checked`, `select.value`, `table.rows`.
- Your code runs on one thread: an event, a timer and `start()` never run at the same time.
