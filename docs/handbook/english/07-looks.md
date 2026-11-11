# 7. Looks

Three levels, from the widest to the smallest: the **theme** of the window (light or dark), the **style** of the window
(the usual look or the minimal one, in your color), and the **look of one component** (its package and its colors).
A look your code gives always wins over the one of the window.

## A dark window

```python
App(start, theme="dark").run()     # "light" (the default), "dark", or "auto": what the system asks
```

- Every component takes its dark look; the dialogs and the toasts too.
- The page, a `Label`, a `Box` and an `Input` follow: a dark ground, a light text.
- A `tone` of a `SmartButton` becomes its dark tone (`"cyan"` → `"cyanDark"`).
- `page.app.theme` is `"light"` or `"dark"` (also after `"auto"`): use it for the colors of your own objects.

```python
TEXT_SOFT = {"light": "#5A6270", "dark": "#9AA3B5"}
Label(text="Updated today", text_color=TEXT_SOFT[page.app.theme])
```

Fifteen components change their theme while they are on the page (`log.set_theme("dark")`, also `log.theme = "dark"`):
`LogView`, `ImageView`, `MarkdownView`, `JsonView`, `ChatView`, `RangeSlider`, `StepBar`, `Canvas`, `MenuBar`, `ToolBar`,
`StatusBar`, `Splitter`, `CodeEditor`, `Accordion` and `GraphBox`. The others take their look when they are made, so a
whole window changes its theme by making its page again:

```python
page.app.set_theme("dark")    # "light", "dark" or "auto": the page is made again and start() runs again
```

What your program keeps in its own variables stays; the objects start again (a text typed in a field is gone).
`examples/gallery.py` and `gallery-styled.py` have a Dark / Light button for it in their ToolBar.

## The minimal look, in your color

```python
App(start, style="minimal").run()                          # small and made of lines; theme="dark" works too
App(start, style="minimal", accent="#2A78D6").run()        # the same, in your color
```

**`style="minimal"`** gives about 40 components their minimal look: 28 px controls, a 13 px text, no fill and no shadow
of their own, so they take the ground of the window. A tool, an editor, a panel of settings look calm in it.

**`accent`** gives the minimal look one color. It goes where the look draws its ink: an on toggle, a checked box, the
fill of a slider and of a progress bar, the selected tab, row and step, the edge of a field while typing, and the main
button. The lines, the texts and the focus ring stay as they are.

```python
from ozdenui import App, CheckBox, HGroup, Label, ProgressBar, SmartButton, Tabs, Toggle, VGroup

THEME = "light"            # "dark", or "auto": what the system asks
ACCENT = "#2A78D6"         # a color that reads on white: it is the text of a selected tab too
GROUND = {"light": "#FFFFFF", "dark": "#1A1A19"}

def start(page):
    page.color = GROUND[page.app.theme]
    with VGroup(gap=14, padding=30, align="left top"):
        Label(text="Account", font_size=18, bold=True)
        Tabs(tabs=["General", "Privacy", "Advanced"], panels=False, width=300)
        CheckBox(text="Remember me", checked=True)
        with HGroup(hug=True, gap=10):
            Toggle(value=True)
            Label(text="Sounds", font_size=13)
        ProgressBar(title_text="Uploading", value=62, width=260)
        with HGroup(hug=True, gap=8):
            SmartButton(text="Cancel")
            SmartButton(text="Save", tone="accent")
            SmartButton(text="Delete", style_name="minimalDanger")

App(start, title="Minimal", size=(420, 380), theme=THEME, style="minimal", accent=ACCENT).run()
```

- **`tone="accent"`** is the main action of any window: the accent color here, the ink of the minimal look without an
  accent, `"cyan"` in the usual look.
- **`style_name="minimalDanger"`**: a delete in the minimal look (in a dark window its dark twin).
- **In a dark window** the color is made lighter until it reads on the dark ground. `accent_dark="#7FB6DE"` chooses it.
- **The text on the color** (a selected day, the main button) is white or dark, the one that reads better.
- A component without a minimal look keeps its usual one. `examples/minimal_theme.py` shows all of them,
  `examples/minimal_accent.py` the accent.

## The look of one component

### A package: style_name

Most components have a few looks, called packages. The docstring of a class names them:

```python
CheckBox(text="Remember me", style_name="modern")
ItemList(items=photos, layout="grid", style_name="gallery")
SmartButton(text="Next", style_name="pill", tone="blue")
```

A package you name stays in every window; in a dark window a light package with a dark twin takes the twin
(`"gallery"` → `"galleryDark"`, `"minimalDanger"` → `"minimalDangerDark"`).

### Your colors: style

`style` changes the parts of a component. Its keys may be written in snake_case, like every param:

```python
SmartButton(text="Go", style={"box": {"color": "#2A78D6"}, "hover": {"color": "#2367BA"},
                              "label": {"text_color": "white"}})
ItemList(items=fruits, style={"box": {"color": "white"}})
Toggle(value=True, background_style={"selected_color": "#6AC966"})
```

- `style={...}` goes over the package: what you give wins, the rest stays.
- The names of the parts (`box`, `hover`, `label`...) are the ones of the component in basic.js; the
  [catalog](https://bug7a.github.io/js-components/) shows the code of every component.
- A param that ends in `_style` (`background_style`, `button_style`) is a style too.
- `framed=False` takes the frame of a component (no border, no rounded corners on its box): a `LogView` or a `CodeEditor`
  that fills the room between two bars. It is `style={"box": {"border": 0, "round": 0}}` in one word.

### Plain objects

A `Box`, a `Label`, a group take their colors from their values (`color`, `text_color`, `border_color`): chapter 2.
Keep the colors of a program at the top of its file, as names, so a change is one line:

```python
PAGE_COLOR = "#F4F5F7"
CARD_COLOR = "#FFFFFF"
TEXT_SOFT = "#5A6270"
```

## Next

[Chapter 8: Data and pictures](08-data-and-pictures.md).
