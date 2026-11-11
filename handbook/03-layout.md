# 3. Layout

A place of its own (`Box(20, 20, 100, 100)`) is good for a game or a drawing. A window of a program is easier with
**groups**: they place their objects and place them again when the window changes its size.

## VGroup and HGroup

```python
with VGroup(gap=10, padding=20, align="left top"):
    Label(text="One")
    Label(text="Two")          # under "One", 10 px lower
    with HGroup(hug=True, gap=8):
        SmartButton(text="Yes")
        SmartButton(text="No")  # next to "Yes"
```

- `VGroup` puts its objects one under the other, `HGroup` side by side.
- A group is as large as its box: `width="100%"`, `height="100%"`. `hug=True` makes it only as large as its objects.
- `gap`: the space between the objects. `padding`: the space inside its edge: `20`, or `[x, y]` (`[30, 12]`).
- `align`: where the objects stand: `"center"` (the default), `"left top"`, `"right center"`, `"center bottom"`...
- `wrap=True`: the objects go on to the next line when there is no room (cards, tags).
- A group is a `Box`: `color`, `round`, `border` work on it too.

In a group an object needs only its size: `Label(text="One", width=200)`. Without a size it is as large as its content.

**More than fits:** a group with more than its box can hold squeezes its objects, and one can cover another (a title
under a card). Give the window more room, or put the content in a `ScrollArea` (below).

## Taking the room that is left: fill=True

A typical window: a bar on top, a part in the middle that takes all the room, a line at the bottom.

```python
from ozdenui import App, HGroup, Label, ScrollArea, SmartButton, VGroup

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=0):
        with HGroup(height=52, padding=[16, 0], gap=10, align="left center", color="white"):
            Label(text="Notes", font_size=18, bold=True)
            SmartButton(text="New", tone="cyan")
        with HGroup(gap=0, fill=True):
            with VGroup(width=180, height="100%", padding=16, gap=8, align="left top", color="#E9EBEF"):
                for folder in ("All", "Work", "Home"):
                    Label(text=folder, font_size=15)
            with ScrollArea(padding=16, gap=12):
                for number in range(1, 41):
                    Label(text=f"Note {number}", font_size=15)
        Label(text="40 notes", font_size=13, text_color="#5A6270", height=28)

App(start, title="Notes", size=(640, 420)).run()
```

- `fill=True` gives an object the room the others leave: **the height** that is left in a `VGroup` (the middle row
  between the bar and the bottom line), **the width** that is left in an `HGroup` (the notes next to the folders).
  Any object takes it: `HGroup(fill=True)`, `LogView(fill=True)`, `Splitter(fill=True)`.
- `ScrollArea()` takes the room the others leave, as `fill=True`, and scrolls what is in it. As an object of the page
  (not in a group) it is the whole window.
- Its objects go one under the other, as in a `VGroup`: give it `align`, `gap` and `padding` (the padding scrolls with
  them). `scroll_x=True` scrolls to the side too. It is the `ScrollArea` of the kit, with the scroll bar of the kit
  (light, or `style_name="dark"`: a dark window chooses it by itself).

## GridGroup: columns and rows

```python
from ozdenui import App, GridGroup, SmartButton

def start(page):
    with GridGroup(columns=4, gap=8, padding=16) as grid:
        for key in "789/456*123-0.=+":
            SmartButton(text=key)
        grid.place(SmartButton(text="Clear"), column_span=4)

App(start, title="Keys", size=(320, 300)).run()
```

- The objects go into the cells in order, left to right, row by row.
- `columns=4`: equal columns. `columns=[120, "1fr", "auto"]`: 120 px, the rest, as wide as its content.
- An object fills its cell; `align="left center"` on the grid puts each one in its cell instead.
- `grid.place(obj, column_span=2)`, `grid.place(obj, column=1, row=0)`: a cell of its own (counted from 0).
- Unlike the other groups, a grid is as high as its rows. `examples/calculator.py` is a whole calculator.

## Things that go out of a group

A group does not cut what goes out of its edge: a button's focus ring, a shadow or a button that grows under the mouse
shows whole, also in a small group:

```python
with HGroup(hug=True, gap=8):
    SmartButton(text="Save", tone="cyan")
    SmartButton(text="Cancel")
```

`clip_content=True` cuts, where cutting is the point (a picture in a frame). A group that scrolls (`scroll_y=True` at its
start) and a `ScrollArea` cut by themselves.

Two defaults are not the ones of basic.js, so that a program says less:

- A `VGroup` / `HGroup` of basic.js cuts its content (`clipContent: 1`); in Python it does not.
- `MenuBar`, `ToolBar`, `StatusBar` and `SearchInput` do not shrink in a group (`shrink=0`): they keep their height while
  a `ScrollArea` or a `fill=True` object takes the rest. `shrink=1` lets them.

## A place of its own

Outside a group, in a `Box` or on the page, an object stands where you put it: `left`, `top`, `width`, `height`. It is
the way for a game, a drawing or an overlay:

```python
with Box(0, 0, 400, 300, color="#1E2230") as board:
    player = Box(180, 130, 40, 40, color="#5BBAC1", round=8)
player.left += 20      # moves it 20 px to the right
```

`examples/game.py` moves a box with the keys. A size may be a text: `Box(0, 0, "100%", "100%")` fills its box.

## When the window changes its size

Groups place their objects again by themselves. For your own sums, `page.width` and `page.height` are always current,
and `page.on("resize", fn)` tells you:

```python
page.on("resize", lambda: print(page.width, page.height))
```

## Next

[Chapter 4: Events and time](04-events-and-time.md): clicks, keys, timers and long jobs.
