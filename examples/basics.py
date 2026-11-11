# Bismillah
"""The basic objects: a Box, an Icon, a Label, an Input and a Button, each in a place of its own.
Write a text and press the button (or Enter): the card shows the text and takes the next color."""

from ozdenui import App, Box, Button, Icon, Input, Label

PAGE_COLOR = "#F4F5F7"
CARD_COLORS = ["#5BBAC1", "#E0A038", "#E8796D", "#65A293"]
# A white circle with a check: a drawing as a text, so no picture file is needed.
PICTURE = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="white"/>'
           b'<path d="M7.5 12.5l3 3 6-7" fill="none" stroke="#2B2B2B" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')

view = {"color_number": 0}


def start(page):
    page.color = PAGE_COLOR

    # An object has a place: left, top, width, height. The objects of a "with" block are inside the Box: their place is in it.
    with Box(20, 20, 320, 110, color=CARD_COLORS[0], round=12) as view["card"]:
        view["icon"] = Icon(20, 25, 60, 60, picture=PICTURE)
        view["label"] = Label(100, 36, 200, 38, text="Hello", font_size=26, bold=True, text_color="white")

    # An event is a function: on_click runs at a click, on_enter at Enter.
    view["input"] = Input(20, 150, 200, 40, placeholder="Write a text", on_enter=change)
    view["button"] = Button(230, 150, 110, 40, text="Change", on_click=change)


def change():
    view["label"].text = view["input"].text.strip() or "Hello"
    view["color_number"] = (view["color_number"] + 1) % len(CARD_COLORS)
    view["card"].color = CARD_COLORS[view["color_number"]]


if __name__ == "__main__":
    App(start, title="The basic objects", size=(360, 260)).run()
