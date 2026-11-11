# 4. Events and time

## An event is a function

```python
Button(text="Save", on_click=save)          # when it is made
button.on_click = save                      # later: it takes the place of the one before
remove = button.on("click", log_click)      # one more handler; remove() takes it away
```

Any event of the page works: `on_click`, `on_dblclick`, `on_mouse_enter`, `on_mouse_leave`,
`on_key_down`, `on_input`, `on_focus`, `on_blur`... In `on()` it is written as the page writes it: `"click"`,
`"mouseenter"`, `"keydown"`.

### The handler takes what it needs

```python
def save(): ...                     # nothing
def save(button): ...               # the object
def save(button, event): ...        # the object and the event: a dict
```

The values of the event go only to the parameters without a default value. **In a loop, a default value keeps the
value**, as in other toolkits:

```python
for number in range(1, 6):
    SmartButton(text=str(number), on_click=lambda number=number: pick(number))
```

`functools.partial(pick, number)` does the same.

The event dict has what the event knows:

| Key | When |
|---|---|
| `key`, `code` | a key: `"Enter"`, `"a"`, `"ArrowLeft"`; `code` is the place on the keyboard (`"KeyA"`) |
| `shift`, `ctrl`, `alt`, `meta` | a key: `True` while held (`meta` is Cmd on a Mac) |
| `x`, `y` | the mouse, in px from the window's corner |
| `text` | an `Input`: its text |

```python
from ozdenui import App, Box, Label, VGroup

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=14):
        pressed = Label(text="Press a key", font_size=28, bold=True)
        spot = Box(width=160, height=60, color="#5BBAC1", round=10)
        where = Label(text="", font_size=14, text_color="#5A6270")

    page.on("keydown", lambda page_, event: show_key(pressed, event))
    spot.on("mouseenter", lambda: spot.set(color="#E0A038"))
    spot.on("mouseleave", lambda: spot.set(color="#5BBAC1"))
    spot.on("click", lambda box, event: where.set(text=f"Clicked at {event['x']}, {event['y']}"))

def show_key(label, event):
    held = [name for name in ("ctrl", "alt", "shift", "meta") if event.get(name)]
    label.text = " + ".join(held + [event["key"]])

App(start, title="Events", size=(420, 300)).run()
```

`page.on("keydown", ...)` hears every key of the window; a field that has the focus hears its own keys too.

## One thread: no locks

`start()`, every event and every timer run **one at a time, on one thread** (the app thread). Two clicks never run at
the same time, and a value you read is the value of now. You need no locks.

The other side of it: while one function runs, the window waits. A function that takes 3 seconds freezes the window
for 3 seconds. A slow job goes to the background (below).

## Time: every() and after()

```python
import time
from ozdenui import App, Label, SmartButton, VGroup, after, every

view = {}

def start(page):
    with VGroup(gap=12):
        view["clock"] = Label(text=time.strftime("%H:%M:%S"), font_size=48, bold=True)
        SmartButton(text="Stop the clock", on_click=stop_clock)
    view["stop"] = every(1000, tick)          # again and again, every 1000 ms
    after(5000, lambda: print("5 s passed"))  # once

def tick():
    view["clock"].text = time.strftime("%H:%M:%S")

def stop_clock():
    view["stop"]()

App(start, title="Clock", size=(360, 220)).run()
```

- `every(ms, fn)` returns a function that stops it; `after(ms, fn)` one that cancels it.
- They and the other functions of the window (`run_in_background()` below, `open_file()` of chapter 6) come from
  `ozdenui` and work in any function of the program. The app has them too: `page.app.every(1000, tick)`.
- A timer is an event too: it runs on the app thread, between the clicks.
- `examples/clock.py` adds a stopwatch.

## A slow job: run_in_background()

```python
import time
from ozdenui import App, Label, ProgressBar, SmartButton, VGroup, run_in_background

view = {}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=14):
        view["bar"] = ProgressBar(title_text="Working", value=0, width=320)
        view["button"] = SmartButton(text="Start", tone="cyan", on_click=begin)
        view["result"] = Label(text="", font_size=16)

def begin():
    view["button"].waiting = True        # a clock on the button: it does not take clicks now
    run_in_background(work, 100)

def work(steps):
    for step in range(1, steps + 1):
        time.sleep(0.03)                   # the slow part: a big file, a download, a model
        view["bar"].value = step
    view["button"].waiting = False
    view["result"].text = "Done."

App(start, title="A slow job", size=(420, 260)).run()
```

- `run_in_background(job, *args)` runs `job(*args)` on a thread of its own; the window keeps working.
- The job may change objects (the bar above) and wait for a dialog (`Dialog.confirm()` of chapter 6).
- It may not ask the page (`measure()`, `ask()`): give it what it needs before it starts.
- `examples/file_tool.py` counts the words of a big file this way.

### A thread of your own

A thread you started yourself (a server, a socket) gives its changes to the app thread with `call_soon()`:

```python
call_soon(lambda: status.set(text="A message came"))
```

## The order of events

Events reach Python in the order they happened, also when many come at once (fast typing). A fast and continuous one
(the mouse moving, a drag) sends every move to Python: let the page do those (chapter 9 shows how), and listen to the
start and the end.

## Next

[Chapter 5: Components](05-components.md): the ready parts of a window.
