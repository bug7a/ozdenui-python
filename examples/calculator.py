# Bismillah
"""A calculator: the keys stand in a GridGroup. The keys of the keyboard work too: 12 + 7, then Enter."""

from ozdenui import App, GridGroup, Label, SmartButton, VGroup

PAGE_COLOR = "#F4F5F7"
SCREEN_COLOR = "#FFFFFF"
ERROR_TEXT = "Error"
MOST_DIGITS = 12
KEYS = ["C", "÷", "7", "8", "9", "×", "4", "5", "6", "−", "1", "2", "3", "+", "0", ".", "="]
WIDE_KEYS = {"C": 3, "0": 2}  # how many cells a key takes
KEYBOARD_NAMES = {"*": "×", "/": "÷", "-": "−", "Enter": "=", "Escape": "C", "c": "C"}
OPERATIONS = {"+": lambda a, b: a + b, "−": lambda a, b: a - b, "×": lambda a, b: a * b, "÷": lambda a, b: a / b}

view = {"typed": "0", "left": None, "operation": None, "is_new": True}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=10, padding=16, align="left top"):
        view["screen"] = Label(text="0", width="100%", font_size=34, bold=True, text_align="right", color=SCREEN_COLOR, round=10,
                               padding=[14, 8], shrink=0)
        with GridGroup(columns=4, gap=8) as grid:
            for key in KEYS:
                tone = "cyan" if key == "=" else "white"
                button = SmartButton(text=key, width="100%", tone=tone, on_click=lambda key=key: press(key))
                if key in WIDE_KEYS:
                    grid.place(button, column_span=WIDE_KEYS[key])
    page.on("keydown", lambda obj, event: press_on_keyboard(event.get("key")))


def press_on_keyboard(name):
    key = KEYBOARD_NAMES.get(name, name)
    if key in KEYS:
        press(key)


def press(key):
    if key == "C":
        clear()
    elif key == "=":
        calculate()
    elif key in OPERATIONS:
        choose_operation(key)
    else:
        write(key)


def show(text):
    view["screen"].text = text


def clear():
    view.update(typed="0", left=None, operation=None, is_new=True)
    show("0")


def write(key):
    typed = "" if view["is_new"] else view["typed"]
    if key == "." and "." in typed:
        return
    if key == "." and typed == "":
        typed = "0"
    typed = (typed + key).lstrip("0") or "0"
    if typed.startswith("."):
        typed = "0" + typed
    view.update(typed=typed[:MOST_DIGITS], is_new=False)
    show(view["typed"])


def choose_operation(key):
    if view["operation"] and not view["is_new"]:
        calculate()
    view.update(left=float(view["typed"]), operation=key, is_new=True)


def calculate():
    if not view["operation"]:
        return
    try:
        number = OPERATIONS[view["operation"]](view["left"], float(view["typed"]))
    except (ZeroDivisionError, ValueError):
        clear()
        show(ERROR_TEXT)
        return
    view.update(typed=text_of(number), left=None, operation=None, is_new=True)
    show(view["typed"])


def text_of(number):
    return f"{number:.10g}"


if __name__ == "__main__":
    App(start, title="Calculator", size=(320, 410)).run()
