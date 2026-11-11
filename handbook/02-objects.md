# 2. Objects

Five plain objects make every window: `Box`, `Label`, `Button`, `Input` and `Icon`. The components of chapter 5 are
made of them.

| Object | What it is | Its own values |
|---|---|---|
| `Box` | a rectangle; the only object that holds other objects | `color`, `border`, `round`, `scroll_y` |
| `Label` | a text | `text`, `html`, `font_size`, `bold`, `text_color`, `text_align` |
| `Button` | a plain button of the system (the nicer one is `SmartButton`) | `text` |
| `Input` | a one-line text field | `text`, `placeholder`, `on_enter` |
| `Icon` | a picture | `picture` (a path, bytes, a Pillow image, a matplotlib figure) |

## A place and a size

An object outside a group has a place of its own: `left`, `top`, `width`, `height`, in px. Give them first, in this
order, or as keywords:

```python
Box(20, 20, 100, 100, color="orangered")
Box(left=20, top=20, width=100, height=100, color="orangered")    # the same
```

A size may also be a text: `width="100%"` (of the box it is in), `height="auto"` (as high as its content). An object
without a place starts at the top left corner of its box.

## Values

A value is a keyword when the object is made, and an attribute later:

```python
title = Label(text="Report", font_size=24, bold=True, text_color="#2B2B2B")
title.text = "Monthly report"           # changes it on the screen
title.set(text="Yearly report", font_size=28, bold=False)   # more than one at once
print(title.text)                        # "Yearly report": read back from Python, no question to the page
```

- **Names:** Python writes `font_size`, basic.js `fontSize`; both are accepted.
- **Numbers and flags:** a size in px is a number; `bold=True` and `bold=True` are the same.
- **Colors:** any CSS color: `"red"`, `"#2A78D6"`, `"rgba(0, 0, 0, 0.5)"`.

The values every object has:

| Value | Example |
|---|---|
| `color` | the background: `color="#FFFFFF"`, `color="transparent"` |
| `border`, `border_color` | `border=1, border_color="#DDD"` |
| `round` | the corners: `round=8`; `round=100` makes a circle of a square |
| `opacity` | `opacity=0.5` |
| `visible` | `visible=False` hides it; in a group the others close the gap |
| `clickable` | an object that listens to the mouse takes clicks by itself; `clickable=False` lets them pass through |
| `css` | anything else of CSS: `css={"cursor": "pointer"}` |

### A value you did not give

`title.text` answers from Python because your code gave it. A value the page decides, like the width of a label of
`width="auto"`, is asked with `measure()`:

```python
width = title.measure("width")      # the width on the screen now, in px
```

Reading a value that was never given raises an error that names `measure()`. `measure()` waits for the page, so use it
when you need it, not in a loop.

### Text and HTML

The `text` of a `Label` or a `Button` is shown exactly as it is written, so a text typed by a user or read from a file
goes in as it is (a `<b>` stays `<b>`). HTML goes in as `html`:

```python
note.text = typed_text
title.html = "<b>3</b> new"
```

In basic.js `text` is HTML; in Python it is the `plainText` of basic.js (`plain_text` works too). The texts of the
components are shown as they are written too (`SmartButton(text=typed)`); `allow_html=True` makes them HTML.

## Objects inside a Box

`with box:` makes the objects of the block inside the box. Their place is counted from the box's corner:

```python
from ozdenui import App, Box, Icon, Input, Label, Button

CHECK = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="white"/>'
         b'<path d="M7.5 12.5l3 3 6-7" fill="none" stroke="#2B2B2B" stroke-width="2.4"/></svg>')

view = {}

def start(page):
    page.color = "#F4F5F7"
    with Box(20, 20, 320, 110, color="#5BBAC1", round=12) as view["card"]:
        Icon(20, 25, 60, 60, picture=CHECK)
        view["label"] = Label(100, 36, 200, 38, text="Hello", font_size=26, bold=True, text_color="white")
    view["input"] = Input(20, 150, 200, 40, placeholder="Write a text", on_enter=change)
    Button(230, 150, 110, 40, text="Change", on_click=change)

def change():
    view["label"].text = view["input"].text.strip() or "Hello"

App(start, title="A card", size=(360, 220)).run()
```

- `with Box(...) as view["card"]:` keeps the box and opens it in one line.
- **Only a `Box` (and the groups, which are boxes) holds objects.** `with Label():` raises an error. To put something
  over a button, make it next to the button in the same box, at the same place.
- `Icon(picture=...)` takes the bytes of an SVG here; a file path, a Pillow image or a matplotlib figure work the same.
- `on_enter=change`: Enter in the field does what the button does.

## Removing

```python
view["card"].remove()       # the card and every object inside it
```

A removed object is gone: make a new one to show it again. To hide something for a while, use `visible=False`.

## When a box has more than it can show

`scroll_y=True` makes a box scroll its content up and down (`scroll_x=True` sideways). Inside a group, `ScrollArea()` of
chapter 3 does the same and takes the room it is given.

## Next

[Chapter 3: Layout](03-layout.md): groups place the objects for you.
