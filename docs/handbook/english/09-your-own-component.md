# 9. Your own component

A part you need more than once (a card, a row of a form, a rating) becomes a class of yours. It makes its objects in a
`with` block, keeps the ones it changes, and has methods. No JavaScript is needed.

## A card

```python
from ozdenui import App, HGroup, Label, SmartButton, VGroup

CARD_LOOK = dict(width=220, height="auto", align="left top", padding=16, gap=8, color="white", round=12)

class Card:
    """A card: a title, a text and a button. on_open(card) runs when its button is clicked."""

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
            Card(name, "Updated today.", on_open=lambda card: card.set_title("Opened"))

App(start, title="Cards", size=(760, 240)).run()
```

- **A plain class, not a subclass of `Box`.** The class keeps its objects (`self.box`, `self.title`). A name set on a
  ozdenui object goes to the page as one of its values: `box.title = ...` changes the box, it keeps nothing.
- **Methods change it** (`set_title()`), as the methods of the components do.
- **Its objects are ordinary objects:** `card.box.remove()` removes the card and everything in it;
  `card.box.on("mouseenter", fn)` and `card.title.measure("width")` work as on any object.
- **Share it as a file:** put it in `card.py`, then `from card import Card` in every program that needs it.

## State and a callback of its own

A component of yours keeps its state in Python and tells the program when the user changes it:

```python
from functools import partial
from ozdenui import App, HGroup, Label, VGroup

STAR_ON = "#E0A038"
STAR_OFF = "#C9CDD4"

class Rating:
    """Five stars: rating.value (0 to 5); on_change(rating) when the user clicks a star."""

    def __init__(self, value=0, on_change=None):
        self.value = value
        self.on_change = on_change
        with HGroup(hug=True, gap=4) as self.box:
            self.stars = [Label(text="★", font_size=28, on_click=partial(self.click, number)) for number in range(1, 6)]
        self.show()

    def set_value(self, value):
        """From code: it does not call on_change, as the components do."""
        self.value = value
        self.show()

    def click(self, number):
        self.set_value(number)
        if self.on_change:
            self.on_change(self)

    def show(self):
        for number, star in enumerate(self.stars, start=1):
            star.text_color = STAR_ON if number <= self.value else STAR_OFF

def start(page):
    with VGroup(gap=12):
        said = Label(text="Rate it", font_size=16)
        Rating(value=3, on_change=lambda rating: said.set(text=f"{rating.value} stars"))

App(start, title="Rating", size=(320, 200)).run()
```

`partial(self.click, number)` gives each star its number (`lambda number=number: self.click(number)` does too).

## A component that holds objects

Give the box it holds objects in a name, as `Tabs` gives `tabs.panel()`:

```python
class Section:
    """A titled part of a form: section = Section("Sound"); with section.body: ..."""

    def __init__(self, title):
        with VGroup(width="100%", height="auto", gap=8, align="left top") as self.box:
            Label(text=title.upper(), font_size=11, bold=True, text_color="#5A6270")
            self.body = VGroup(width="100%", height="auto", gap=10, align="left top")

sound = Section("Sound")
with sound.body:
    CheckBox(text="Play a sound")
    Slider(value=7, min_value=0, max_value=10)
```

## What belongs to Python, what to the page

**"A click, then a change" belongs to Python.** Your function runs, the page shows the change about 3 ms later.

**"Every frame, every mouse move" belongs to the page.** A motion made of many steps sent from Python would stutter.
Tell the page how to move, then give the end:

```python
ball.call("setMotion", "left 0.3s, opacity 0.2s")   # these values now change smoothly
ball.left = 300                                      # the page moves it there in 0.3 s
```

A `Canvas` does so by itself: the page draws the free lines and moves the dragged shapes, Python hears only their ends.

### A callback that must answer at once

Some callbacks of basic.js components must return an answer at once (a function that draws a row of a list, a check
that stops a click). Python's answer comes a little later, so such a callback can not be a Python function: format the
values in Python before they go to the page instead, and use the params the components give (chapter 10 lists them).

## Next

[Chapter 10: Going further](10-going-further.md).
