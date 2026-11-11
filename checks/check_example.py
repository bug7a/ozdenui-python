# Bismillah
"""check_example.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Runs an example in its real window and plays it as a user would: clicks, typing, keys. Then it checks the page and
the values in Python, takes a picture of the window and closes it.

Usage: .venv/bin/python checks/check_example.py counter [picture.png] [theme]
Exit code 0: passed. The last line is the result as JSON (checks/run_all.py reads it).
A problem names the line of the play that made it ("play_todo line 40: ..."); a message of the page in the terminal
names the step it came after.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import datetime
import json
import os
import sys
import tempfile
import threading
import time
import traceback

from webview.dom import _dnd_state

from ozdenui import (Accordion, App, Canvas, ChatView, CodeEditor, CurrencyField, DatePicker, GraphBox, GridGroup, ImageView, ItemList, JsonEditor, JsonView, Label, LogView, MarkdownView,
                     MenuBar, NumberField, PhoneField, RangeSlider, SearchInput, SelectBox, Slider, SliderField, SmartButton, SmartTable,
                     SortableList, StepBar, Stepper, TextField, Toggle, ToolBar, Tooltip, TreeView, UrlField, WebView)
from ozdenui.objects import DARK_STYLE_NAMES
from window_check import HERE, TerminalProblems, bring_to_front, can_drop_natively, drop_file_natively, load_example, snapshot_window

STEP_SECONDS = 0.35  # after an action: the event goes to Python and the answer comes back
ANSWER_SECONDS = 10
WAIT_SECONDS = 8
MENU_TRIES = 3
MENU_WAIT_SECONDS = 3
DROP_TRIES = 2
DROP_WAIT_SECONDS = 3
TIMEOUT_SECONDS = 60
SIZES = {"gallery": (1000, 820), "gallery-styled": (1000, 820), "csv_viewer": (900, 640), "settings": (580, 560), "todo": (540, 560),
         "image_viewer": (760, 560), "job_log": (680, 520), "editor": (760, 600), "markdown_editor": (960, 640), "json_viewer": (720, 560),
         "json_editor": (820, 600), "photos": (980, 640), "paint": (900, 620), "greeting": (420, 320), "form": (620, 720),
         "charts": (920, 720), "files": (960, 620), "basics": (360, 260), "calculator": (320, 410), "minimal_theme": (1000, 820),
         "minimal_accent": (860, 600)}
DEFAULT_SIZE = (720, 560)
# What the page says when a menu did not open: its focus, whether it is seen, the elements with the text of the title,
# the menus that are seen
_MENU_REPORT_JS = """JSON.stringify({ focus: document.hasFocus(), seen: document.visibilityState,
    titles: __check.visible("body *").filter(function (el) { return el.children.length === 0 && el.textContent.trim() === %s; }).length,
    menus: __check.visible("[role=menu]").length, active: (document.activeElement || {}).className || "" })"""

# The helpers on the page: the last visible element with a text (a dialog is made after the page, so its button is
# the last "Delete"), typing into the last visible input, a key on the focused element.
HELPERS_JS = r"""
window.__check = {
    visible: function (selector) {
        return Array.from(document.querySelectorAll(selector)).filter(function (el) {
            return el.getClientRects().length > 0;
        });
    },
    find: function (text) {
        const found = this.visible("body *").filter(function (el) {
            return el.children.length === 0 && el.textContent.trim() === text;
        });
        return found[found.length - 1] || null;
    },
    click: function (text) {
        const el = this.find(text);
        if (!el) return "not found: " + text;
        el.click();
        return "ok";
    },
    type: function (text, selector) {
        const inputs = this.visible(selector || "input");
        const input = inputs[inputs.length - 1];
        if (!input) return "no " + (selector || "input");
        input.focus();
        input.value = "";
        Array.from(text).forEach(function (letter) {
            input.value += letter;
            input.dispatchEvent(new Event("input", { bubbles: true }));
        });
        return "ok";
    },
    typeIn: function (owner, text) {
        const input = owner.querySelector("input, textarea");
        if (!input) return "no input in it";
        input.focus();
        input.value = "";
        Array.from(text).forEach(function (letter) {
            input.value += letter;
            input.dispatchEvent(new Event("input", { bubbles: true }));
        });
        if (!text) input.dispatchEvent(new Event("input", { bubbles: true }));
        return "ok";
    },
    dropFile: function (owner, name, text) {
        const files = new DataTransfer();
        files.items.add(new File([text], name, { type: "text/plain" }));
        owner.dispatchEvent(new DragEvent("drop", { bubbles: true, cancelable: true, dataTransfer: files }));
        return "ok";
    },
    key: function (key) {
        const target = document.activeElement || document.body;
        // WHY cancelable: as a real key. The second of two bars with one shortcut knows from preventDefault() that it has run.
        target.dispatchEvent(new KeyboardEvent("keydown", { key: key, bubbles: true, cancelable: true }));
        return "ok";
    },
    text: function () {
        return document.body.innerText;
    },
};
"ok"
"""


def place_in_play():
    """The play and its line that runs now (Ex: "play_todo line 40"); "" outside a play."""
    frame = sys._getframe(1)
    while frame is not None:
        name = frame.f_code.co_name
        if name.startswith("play_"):
            return f"{name} line {frame.f_lineno}"
        frame = frame.f_back
    return ""


class Player:
    """Plays the example from a thread of its own; every action runs on the app thread."""

    def __init__(self, app, example, terminal=None):
        self.app = app
        self.example = example
        self.problems = []
        self.terminal = terminal  # a TerminalProblems: it is told the step that runs now

    def on_app(self, func, what=""):
        self._name_step(what)
        done = threading.Event()
        box = {}

        def run():
            try:
                box["value"] = func()
            except Exception as error:
                box["error"] = error
            finally:
                done.set()

        self.app.call_soon(run)
        if not done.wait(ANSWER_SECONDS):
            raise TimeoutError("the app thread did not answer")
        if "error" in box:
            raise box["error"]
        return box.get("value")

    def _name_step(self, what):
        if self.terminal is None:
            return
        place = place_in_play() or "before the play"
        self.terminal.set_step(f"{place}: {what}" if what else place)

    def problem(self, message):
        """A problem of the play, with the line of the play that found it."""
        place = place_in_play()
        self.problems.append(f"{place}: {message}" if place else message)

    def js(self, script, what=""):
        return self.on_app(lambda: self.app.evaluate(script), what)

    def act(self, script, what):
        result = self.js(script, what)
        if result != "ok":
            self.problem(f"{what}: {result}")
        time.sleep(STEP_SECONDS)

    def click(self, text):
        self.act(f"__check.click({json.dumps(text)})", f"click {text!r}")

    def type(self, text, selector="input"):
        self.act(f"__check.type({json.dumps(text)}, {json.dumps(selector)})", f"type {text!r}")

    def type_in(self, obj, text):
        """Types into the field of an object, letter by letter."""
        self.act(f"__check.typeIn({obj.js}.elem, {json.dumps(text)})", f"type {text!r} in {obj!r}")

    def key(self, key):
        self.act(f"__check.key({json.dumps(key)})", f"key {key}")

    def click_object(self, obj):
        self.act(f"({obj.js}.elem.click(), 'ok')", f"click {obj!r}")

    def press_tool(self, bar, name):
        """A button of a ToolBar, by its name: an icon button has no text to find."""
        selector = json.dumps(f'button[aria-label="{name}"]')
        self.act(f"({bar.js}.elem.querySelector({selector}).click(), 'ok')", f"press {name!r}")

    def page_text(self):
        return self.js("__check.text()")

    def expect(self, is_true, message):
        if not is_true:
            self.problem(message)

    def wait_for_text(self, text, seconds=WAIT_SECONDS):
        """Waits until an element with this text is on the page."""
        deadline = time.time() + seconds
        while time.time() < deadline:
            if self.js(f"__check.find({json.dumps(text)}) ? 'ok' : 'no'") == "ok":
                return
            time.sleep(STEP_SECONDS / 2)
        self.problem(f"no element with the text {text!r} after {seconds} s")

    def expect_text(self, text):
        shown = self.page_text()
        self.expect(text in shown, f"the page does not show {text!r}")

    def open_menu(self, title, item):
        """Opens a menu of a MenuBar and waits for its item, as a person would: the window in front, and one more click
        when the menu went away. WHY: a ContextMenu closes when the window loses the focus (a computer in use, the
        activation of the window coming late), so in a long check a menu was gone before its item was clicked."""
        for _ in range(MENU_TRIES):
            if not self.come_to_front():
                return False
            self.click(title)
            if self._is_found_within(item, MENU_WAIT_SECONDS):
                return True
        self.problem(f"the menu {title!r} did not show {item!r}: {self.js(_MENU_REPORT_JS % json.dumps(title))}")
        return False

    def _is_found_within(self, text, seconds):
        deadline = time.time() + seconds
        while time.time() < deadline:
            if self.js(f"__check.find({json.dumps(text)}) ? 'ok' : 'no'") == "ok":
                return True
            time.sleep(STEP_SECONDS / 2)
        return False

    def come_to_front(self):
        """WHY a problem and not a skip: a part of the check that did not run must not look like a part that passed."""
        if bring_to_front(self.app, self.js):
            return True
        self.problem("the window could not come to the front (another program holds it): run this check again")
        return False

    def first(self, kind, **values):
        """The first object of a kind with these values (Ex: the Label with font_size 64)."""
        for obj in list(self.app._objects.values()):
            if isinstance(obj, kind) and all(obj._values.get(key) == value for key, value in values.items()):
                return obj
        raise LookupError(f"no {kind.__name__} with {values}")


# *** THE PLAYS:

def play_counter(p):
    for text in ["+", "+", "+", "−"]:
        p.click(text)
    count = p.first(Label, fontSize=64)
    p.expect(count.text == "2", f"the count is {count.text!r} in Python")
    on_page = p.on_app(lambda: count.measure("text"))
    p.expect(on_page == "2", f"the count is {on_page!r} on the page")
    if can_drop_natively() and p.come_to_front():
        stray = os.path.join(tempfile.mkdtemp(), "stray.txt")
        with open(stray, "w", encoding="utf-8") as file:
            file.write("a stray file")
        drop_file_natively(p.app, stray, 100, 100)
        time.sleep(STEP_SECONDS)
        p.expect(p.js("location.href").endswith("index.html"), "a file dropped on the window took the place of the program")


def play_greeting(p):
    p.type("Ayşe")
    p.click("Greet")
    p.expect_text("Hello, Ayşe!")
    p.type("Can <b>")
    p.key("Enter")
    p.expect_text("Hello, Can <b>!")


def play_calculator(p):
    view = p.example.view
    screen = view["screen"]

    def shown():
        return screen._values.get("text")

    for key in "12+7=":
        p.click(key)
    p.expect(shown() == "19", f"12 + 7 = {shown()}")
    p.click("×")
    p.click("2")
    p.click("=")
    p.expect(shown() == "38", f"19 x 2 = {shown()}")
    p.click("C")
    p.expect(shown() == "0", f"C: {shown()}")
    for key in ["1", "÷", "0", "="]:
        p.click(key)
    p.expect(shown() == "Error", f"1 / 0: {shown()}")
    p.click("C")
    for key in [".", "5", "+", ".", "2", "5", "="]:
        p.click(key)
    p.expect(shown() == "0.75", f".5 + .25 = {shown()}")
    p.click("C")
    for key in ["9", "*", "3", "Enter"]:
        p.key(key)
    p.expect(shown() == "27", f"the keyboard: 9 * 3 = {shown()}")
    # The wide keys take their cells: C three of them, 0 two of them.
    width_of = "__check.find('%s').closest('.basic-focus-ring').getBoundingClientRect().width"  # WHY: the box of the button itself
    one = p.js(width_of % "7")
    p.expect(abs(p.js(width_of % "0") - (2 * one + 8)) < 2, "the 0 takes two cells")
    p.expect(abs(p.js(width_of % "C") - (3 * one + 16)) < 2, "the C takes three cells")


def play_basics(p):
    """WHY all of this here: this is the one example that uses Input and Button."""
    view = p.example.view
    first_ground = p.js(f"getComputedStyle({view['card'].js}.elem).backgroundColor")
    p.expect(p.js(f"{view['icon'].js}.elem.naturalWidth > 0"), "the picture of the Icon is not drawn")
    p.type("Ada <b>")
    p.expect(view["input"].text == "Ada <b>", f"the text of the Input in Python: {view['input'].text!r}")
    p.click_object(view["button"])
    p.expect_text("Ada <b>")
    second_ground = p.js(f"getComputedStyle({view['card'].js}.elem).backgroundColor")
    p.expect(second_ground != first_ground, f"the Box keeps its color: {second_ground}")
    p.type("Can")
    p.key("Enter")
    p.expect_text("Can")
    p.on_app(lambda: view["input"].set(text="From Python"))
    time.sleep(STEP_SECONDS)
    p.expect(p.on_app(lambda: view["input"].measure("text")) == "From Python", "the text of an Input from Python")
    p.on_app(lambda: view["button"].set(text="Changed"))
    time.sleep(STEP_SECONDS)
    p.expect(p.on_app(lambda: view["button"].measure("text")) == "Changed", "the text of a Button from Python")


def play_gallery(p):
    """gallery and gallery-styled (the same page): every component, then the theme button."""
    play_gallery_steps(p)
    play_the_theme_switch(p)  # WHY last: the page is made again, the steps of the gallery would start over


def play_gallery_steps(p):
    if not p.come_to_front():  # WHY: it opens menus and popups
        return
    p.click("Remember me")
    p.expect_text("Remember me: False")
    p.click_object(p.first(Toggle))
    p.expect_text("Notifications: False")
    p.click("L")
    p.expect_text("Size: L")
    p.on_app(lambda: p.first(SelectBox).open())  # WHY open(): "Ankara" is in the table too
    time.sleep(STEP_SECONDS)
    p.click("İzmir")  # the last one: the list of the SelectBox is made on the page when it opens
    p.expect_text("City: İzmir")
    slider = p.first(SliderField)
    p.js(f"({slider.js}.focus(), 'ok')")
    p.key("ArrowRight")
    p.expect_text("Volume: 7")
    p.expect(slider.value == 7, f"the slider is {slider.value} in Python")
    p.click("+10")
    p.expect_text("50%")
    p.type("Hi", "textarea:not(.code-editor-textarea):not(.chat-view-field)")  # WHY: a CodeEditor and a ChatView have one too
    p.expect_text("Note: 2 letters")
    p.click("Pears")
    p.expect_text("Fruit: ['p']")
    p.click("Mehmet Kaya")
    p.expect_text("Row: Mehmet Kaya")
    p.click("Write a line")
    p.expect_text("A new line")
    if p.open_menu("View", "Word wrap"):
        p.click("Word wrap")
        p.expect_text("Word wrap: False")
    if p.open_menu("Help", "About"):
        p.click("About")
        p.expect_text("About was chosen.")
    p.expect_text("Drag the line")
    editor = p.first(CodeEditor)
    p.expect("hello" in p.on_app(lambda: editor.value), "the text of the CodeEditor")
    p.click("Advanced")
    p.expect_text("Tab: Advanced")
    p.expect_text("The advanced settings.")
    p.click("Save")
    p.expect_text("Saved.")
    p.click("Delete")
    p.click("Delete")  # the button of the dialog
    p.expect_text("Deleted.")
    play_gallery_new_classes(p)


def play_the_url_phone_and_currency_fields(p):
    url = p.first(UrlField)
    p.type_in(url, "python.org")
    p.expect_text("Site: https://python.org")
    p.act(f"({url.js}.tinySelect.setSelectedIndex(0), 'ok')", "choose http://")  # WHY: the kit calls onChange for it now
    p.expect_text("Site: http://python.org")
    phone = p.first(PhoneField)
    p.type_in(phone, "5551234567")
    p.expect_text("Phone: +90 (555) 123-4567")
    p.on_app(lambda: phone.set_text("0555 987 65 43"))
    time.sleep(STEP_SECONDS)
    on_page = p.js(f"{phone.js}.getValue()")
    p.expect(on_page == phone.text == "+90 (555) 987-6543", f"a number given in code is in the mask: {on_page!r}, {phone.text!r}")
    price = p.first(CurrencyField)
    p.type_in(price, "1234.5")
    p.expect_text("Price: 1234.5")
    p.expect(p.js(f"{price.js}.getValue()") == "1,234.5", "the groups of a CurrencyField")


def play_the_sortable_list(p):
    """A row moved with the keys, as a person without a mouse does: Space grabs it, ArrowDown moves it, Space drops it."""
    lst = p.first(SortableList)
    p.act(f"({lst.js}.focusItem(0), 'ok')", "the focus on the first row")
    for key in (" ", "ArrowDown", " "):
        p.key(key)
    p.expect_text("Order: ['Stock', 'Sales', 'pay']")
    p.expect(lst.items[:2] == ["Stock", "Sales"], f"the items in Python: {lst.items}")


def play_the_web_view(p):
    """The script of the HTML runs in the frame, and its message reaches Python."""
    web = p.first(WebView)
    deadline = time.time() + WAIT_SECONDS
    while p.js(f"{web.js}.isLoaded") != 1 and time.time() < deadline:
        time.sleep(STEP_SECONDS / 2)
    p.act(f"({web.js}.getDocument().getElementById('send').click(), 'ok')", "click the button of the page in the WebView")
    p.wait_for_text("WebView: 1")


def send_in_chat(p, chat, text):
    """Types into the field of a ChatView and presses Enter, as a person does."""
    p.type_in(chat, text)
    p.key("Enter")


def play_the_chat_view(p):
    chat = p.first(ChatView)
    send_in_chat(p, chat, "Hi")
    p.wait_for_text("You wrote: Hi")
    texts = [message["text"] for message in chat.messages]
    p.expect(texts[-2:] == ["Hi", "You wrote: Hi"], f"the messages in Python: {texts}")


def play_chat(p):
    """The answer comes word by word from a background job; Stop ends one; New chat starts again."""
    chat = p.first(ChatView)
    send_in_chat(p, chat, "my week")
    p.expect(p.js(f"{chat.js}.dotsRow.visible") == 1, "the dots while the first words are waited for")
    p.wait_for_text("Ask again if something is not clear.", seconds=10)
    time.sleep(STEP_SECONDS)
    full = p.example.ANSWER.format(topic="my week")
    messages = chat.messages
    p.expect([m["role"] for m in messages] == ["system", "user", "assistant"], f"the roles: {[m['role'] for m in messages]}")
    p.expect(messages[-1]["text"] == full, "the whole answer in Python")
    p.expect(chat.busy == 0 and p.js(f"{chat.js}.busy") == 0, "not busy after the answer")
    p.expect(p.js(f"{chat.js}.messageGroup.elem.querySelectorAll('table td').length") == 4, "the answer is Markdown (its table)")
    send_in_chat(p, chat, "a garden")
    time.sleep(1.2)  # WHY: some words of the answer, not all of them
    p.act(f"({chat.js}.btnSend.elem.click(), 'ok')", "press Stop")
    time.sleep(0.6)
    stopped = chat.messages[-1]["text"]
    p.expect(chat.busy == 0 and 0 < len(stopped) < len(p.example.ANSWER), f"Stop ends the answer: {len(stopped)} letters, busy {chat.busy}")
    p.click("New chat")
    p.expect(len(chat.messages) == 1 and p.js(f"{chat.js}.getMessages().length") == 1, "New chat starts again")


def play_gallery_new_classes(p):
    grid = p.first(GridGroup)
    p.expect(p.js(f"getComputedStyle({grid.js}.elem).display") == "grid", "a GridGroup is a grid on the page")
    p.expect(p.js(f"getComputedStyle({grid.js}.elem).gridTemplateColumns.split(' ').length") == 3, "its three columns")
    name_field = p.first(TextField, titleText="Name")
    p.type_in(name_field, "Ada")
    p.expect_text("Name: Ada")
    count_field = p.first(NumberField)
    p.type_in(count_field, "12")
    p.expect_text("Count: 12")
    p.type_in(p.first(SearchInput), "sea")
    p.expect_text("Search: sea")
    p.on_app(lambda: p.first(Stepper).increase())
    time.sleep(STEP_SECONDS)
    p.expect_text("Stepper: 3")
    p.on_app(lambda: p.first(DatePicker).open())
    time.sleep(STEP_SECONDS)
    p.click("25")
    p.expect_text("Date: 2026-11-25")
    tree = p.first(TreeView)
    p.click("sea.jpg")
    p.expect_text("Node: sea.jpg")
    p.expect(tree.value is not None, "the value of the TreeView")
    bars = text_of_chart(p, p.first(GraphBox))
    p.expect("TL" in bars and "undefined" not in bars, "the axis of the GraphBox: " + bars)
    play_the_accordion(p)
    play_the_tool_bar(p)
    play_the_markdown_view(p)
    play_the_json_view(p)
    play_the_json_editor(p)
    play_the_range_slider(p)
    play_the_list_ground(p)
    play_the_picture_list(p)
    play_the_canvas(p)
    play_the_step_bar(p)
    play_the_url_phone_and_currency_fields(p)
    play_the_sortable_list(p)
    play_the_web_view(p)
    play_the_chat_view(p)
    p.click("A bubble")
    p.wait_for_text("It goes by itself.")
    p.click("A popover")
    p.wait_for_text("It stays, and holds objects.")
    p.key("Escape")
    p.expect("It stays" not in p.page_text(), "Escape closes the popover")


def play_the_accordion(p):
    folds = p.first(Accordion)
    made_while_closed = p.js("__check.find('It was made while it was closed.').offsetHeight")
    frame = f"{folds.js}.getContent('Closed at the start').elem.parentElement"
    p.expect(made_while_closed > 0, "the object of a closed section has no size")
    p.expect(p.js(f"{frame}.offsetHeight") == 0, "a closed section is seen")
    p.click("Closed at the start")
    p.expect_text("Open: ['more', 'Closed at the start']")
    p.expect(p.js(f"{frame}.offsetHeight") > 0, "an open section is not seen")
    p.on_app(lambda: folds.close("Closed at the start"))
    time.sleep(STEP_SECONDS)
    p.expect(folds.open_keys == ["more"], f"the open sections in Python: {folds.open_keys}")
    p.expect(p.js(f"{frame}.offsetHeight") == 0, "close() does not close it")


def play_the_tool_bar(p):
    tools = p.first(ToolBar)
    p.press_tool(tools, "Bold")
    p.expect_text("Bold, pressed: ['bold', 'left']")
    p.press_tool(tools, "Align right")
    p.press_tool(tools, "Align right")
    p.expect_text("Align right, pressed: ['bold', 'right']")
    p.on_app(lambda: tools.set_item_checked("bold", False))
    time.sleep(STEP_SECONDS)
    p.expect(tools.checked_keys == ["right"], f"the pressed buttons in Python: {tools.checked_keys}")
    p.expect(p.js(f"{tools.js}.elem.querySelector('button[aria-label=\"Bold\"]').getAttribute('aria-pressed')") == "false", "set_item_checked on the page")
    p.click("Insert")
    p.click("A table")
    p.expect_text("A table, pressed: ['right']")
    p.key("F9")
    p.expect_text("Run, pressed: ['right']")
    p.press_tool(tools, "New")
    p.expect_text("New, pressed: ['right']")
    p.on_app(lambda: setattr(tools, "width", 170))
    time.sleep(STEP_SECONDS)
    p.press_tool(tools, "More")
    p.click("Run")  # WHY it is in the menu now: the button of the row is hidden
    p.expect_text("Run, pressed: ['right']")
    p.on_app(lambda: setattr(tools, "width", "100%"))
    time.sleep(STEP_SECONDS)
    is_hidden = p.js(f"{tools.js}.elem.querySelector('button[aria-label=\"More\"]').getClientRects().length === 0")
    p.expect(is_hidden, "the \"...\" button when everything fits")


def play_the_markdown_view(p):
    markdown_view = p.first(MarkdownView)
    p.expect(p.js(f"{markdown_view.js}.elem.querySelectorAll('table td').length") == 2, "the table of a MarkdownView")
    p.expect(p.js(f"{markdown_view.js}.elem.querySelectorAll('.markdown-view-check-on').length") == 1, "the check mark of a MarkdownView")
    p.click("notes")
    p.expect_text("Link: https://example.com/notes")


def play_the_json_view(p):
    json_view = p.first(JsonView)
    p.expect(p.js(f"{json_view.js}.tree.getRowElem('users[0].name').textContent") == 'name"Ada"', "a row of a JsonView")
    p.act(f"({json_view.js}.tree.getRowElem('users[0].name').click(), 'ok')", "click a row of a JsonView")
    p.expect_text("Path: users[0].name")
    p.expect(json_view.selected_value == "Ada", f"the selected value in Python: {json_view.selected_value!r}")


def play_the_json_editor(p):
    editor = p.first(JsonEditor)
    click_json_cell(p, editor, 1, "in_stock")  # Olive oil: False -> True
    p.expect_text("Products: 3, 3 in stock")
    p.expect(p.on_app(lambda: editor.value)[1] == {"name": "Olive oil", "price": 420, "in_stock": True}, "editor.value in the gallery")


def play_the_range_slider(p):
    slider = p.first(RangeSlider)
    p.expect(p.js(f"{slider.js}.lowKnob.elem.getAttribute('aria-valuetext')") == "200 TL", "the format of a RangeSlider on the page")
    p.js(f"({slider.js}.lowKnob.elem.focus(), 'ok')")
    p.key("ArrowRight")
    p.expect_text("Range: 250 - 800")
    p.expect(slider.values == (250, 800), f"the values in Python: {slider.values}")
    p.on_app(lambda: slider.set_values(900, 100))
    time.sleep(STEP_SECONDS)
    p.expect(p.js(f"{slider.js}.getValues().join()") == "100,900", "set_values on the page")
    p.expect(slider.values == (100, 900), f"set_values in Python: {slider.values}")


def play_the_step_bar(p):
    bar = p.first(StepBar)
    p.expect(p.js(f"{bar.js}.row.elem.children[1].getAttribute('aria-current')") == "step", "the step of now")
    p.act(f"({bar.js}.row.elem.children[0].click(), 'ok')", "click a step behind")
    p.expect_text("Step: 1")
    time.sleep(STEP_SECONDS)
    p.expect(bar.step == 0, f"the step in Python: {bar.step}")


def play_the_theme_switch(p):
    """The Dark / Light button of the ToolBar draws the page again in the other theme (app.set_theme()): the theme of
    the app, the ground of the page, the package of the fruit list (chosen by the code: LOOKS; or the dark look of the
    window) and the button itself."""
    other = "light" if p.app.theme == "dark" else "dark"
    old_page = p.app.page
    p.click(p.example.THEME_BUTTON_TEXTS[p.app.theme])
    # WHY from Python: a question to the page while it is loaded again waits for the new page (pywebview), and on
    #      Windows its answer never came. The app makes a new page object when the new page is ready.
    deadline = time.time() + WAIT_SECONDS
    while time.time() < deadline and p.app.page is old_page:
        time.sleep(STEP_SECONDS / 2)
    if p.app.page is old_page:
        p.problem(f"the page was not made again (loading: {p.app._is_loading_for_theme}, "
                  f"loaded: {p.app._window.events.loaded.is_set()})")
        return
    p.on_app(lambda: None)  # WHY: it runs after start() and its drawing on the new page
    p.js(HELPERS_JS)  # WHY again: they were on the old page
    p.wait_for_text(p.example.THEME_BUTTON_TEXTS[other])
    p.expect(p.app.theme == other, f"the theme after the button: {p.app.theme}")
    ground = p.js("page.color")
    p.expect(ground == p.example.COLORS[other]["page"], f"the ground of the new page: {ground}")
    looks = getattr(p.example, "LOOKS", None)
    window_look = DARK_STYLE_NAMES["ItemList"] if other == "dark" else None
    expected_list = looks[other]["list"] if looks else window_look
    fruit_list = p.on_app(lambda: p.first(ItemList)._values.get("styleName"))
    p.expect(fruit_list == expected_list, f"the fruit list on the new page: {fruit_list} ({expected_list} expected)")


def play_the_list_ground(p):
    item_list = p.first(ItemList)
    expected = "rgb(26, 26, 25)" if p.app.theme == "dark" else "rgb(245, 245, 245)"
    # WHY: gallery-styled chose the light package of the kit, and its dark twin in a dark window
    chosen_grounds = {"light": "rgb(255, 255, 255)", "dark": "rgb(35, 35, 34)"}
    expected = chosen_grounds.get(item_list._values.get("styleName"), expected)
    ground = p.js(f"getComputedStyle({item_list.js}.elem).backgroundColor")
    p.expect(ground == expected, f"the ground of an ItemList: {ground}")


def play_the_picture_list(p):
    pictures = p.first(ItemList, layout="grid")
    fits = p.js(f"Array.from({pictures.js}.elem.querySelectorAll('img')).map(function (img) {{ return getComputedStyle(img).objectFit; }}).join()")
    p.expect(fits == "cover,cover,cover", f"the pictures fill their squares: {fits}")
    tops = p.js(f"new Set(Array.from({pictures.js}.elem.querySelectorAll('img')).map(function (img) {{ return Math.round(img.getBoundingClientRect().top); }})).size")
    p.expect(tops == 1, f"three pictures in a row: {tops} rows")
    p.click("Wood")
    p.expect_text("Picture: ['wood']")


def play_the_canvas(p):
    canvas = p.first(Canvas)
    press_on_canvas(p, canvas, [[80, 110]])
    p.expect_text("Canvas: hill")
    press_on_canvas(p, canvas, [[300, 55], [280, 70], [260, 80]])
    p.expect_text("Moved: sun")
    p.expect(canvas.shape("sun")["x"] == 260, f"the sun in Python: {canvas.shape('sun')['x']}")


def text_of_chart(p, graph):
    return p.js(f"Array.from({graph.js}.elem.querySelectorAll('svg text')).map(function (text) {{ return text.textContent; }}).join('|')")


def play_form(p):
    view = p.example.view
    p.click("Send")
    p.expect_text("Look at the marked fields.")
    p.type_in(view["name"], "Ada")
    p.expect(view["name"].text == "Ada", f"the name in Python: {view['name'].text!r}")
    p.type_in(view["email"], "not an address")
    p.expect(p.on_app(view["email"].is_valid) is False, "a wrong address is not valid")
    p.expect(p.on_app(view["email"].check) is False, "a wrong address does not pass")
    p.type_in(view["email"], "ada@example.com")
    p.expect(p.on_app(view["email"].check) is True, "a right address passes")
    p.type_in(view["password"], "abc")
    p.expect(p.on_app(view["password"].check) is False, "a short password does not pass")
    p.type_in(view["password"], "secret1")
    p.type_in(view["budget"], "12a5")
    p.expect(view["budget"].text == "125", f"letters do not go into a number: {view['budget'].text!r}")
    p.expect(view["budget"].value == 125, f"the number in Python: {view['budget'].value!r}")
    p.on_app(lambda: view["date"].set_value(datetime.date(2031, 3, 14)))
    time.sleep(STEP_SECONDS)
    p.expect(view["date"].value == "2031-03-14", f"the date in Python: {view['date'].value!r}")
    p.expect(view["date"].date == datetime.date(2031, 3, 14), f"the date as a date: {view['date'].date!r}")
    p.on_app(lambda: view["date"].set_value("2001-01-01"))  # before min_date: not taken
    time.sleep(STEP_SECONDS)
    p.expect(view["date"].value == "2031-03-14", f"a date out of its limits: {view['date'].value!r}")
    p.on_app(lambda: view["time"].set_value(datetime.time(20, 45)))
    time.sleep(STEP_SECONDS)
    p.expect(view["time"].value == "20:45", f"the time in Python: {view['time'].value!r}")
    p.on_app(lambda: view["color"].set_value("#ff0000"))
    time.sleep(STEP_SECONDS)
    p.expect(view["color"].value.upper() == "#FF0000", f"the color in Python: {view['color'].value!r}")
    p.on_app(view["guests"].increase)
    time.sleep(STEP_SECONDS)
    p.expect(view["guests"].value == 3, f"the guests in Python: {view['guests'].value}")
    p.js(f"({view['noise'].js}.elem.focus(), 'ok')")
    p.key("ArrowRight")
    p.expect(view["noise"].value == 71, f"the slider after a key: {view['noise'].value}")
    p.expect_text("How quiet: 71")
    p.click("Send")
    p.expect_text("Sent.")
    for part in ("'name': 'Ada'", "'budget': 125", "'date': '2031-03-14'", "'time': '20:45'", "'guests': 3", "'quiet': 71"):
        p.expect_text(part)
    p.click("Clear")
    p.expect(view["budget"].value is None, "an empty number is None")
    p.expect(view["date"].value == "" and view["date"].date is None, f"an empty date: {view['date'].value!r}")


def play_charts(p):
    view = p.example.view
    sales = view["sales"]
    labels = text_of_chart(p, sales)
    p.expect("2,000 TL" in labels or "2,500 TL" in labels, "the format on the page: " + labels)
    p.expect("undefined" not in labels, "undefined on the axis: " + labels)
    p.expect("°" in text_of_chart(p, view["live"]), "the format of the live chart")
    last_number = LAST_LABEL_JS % view["live"].js
    first_labels = p.js(last_number)
    time.sleep(2.2)
    p.expect(p.js(last_number) != first_labels, "the live chart did not move")
    click_on_chart(p, sales, 0.2)
    p.wait_for_text("Jan: 1,200 TL")
    click_on_chart(p, sales, 0.95)
    p.wait_for_text("Jun: 1,800 TL")
    p.click("As a table")
    p.expect_text("1,900 TL")
    p.click("As a table")
    p.click("Line")
    p.expect(sales.type == "line", f"the type in Python: {sales.type}")
    p.click("Bars")
    path = os.path.join(tempfile.mkdtemp(), "chart.png")
    p.on_app(lambda: sales.save_image(path))
    with open(path, "rb") as file:
        p.expect(file.read(4) == b"\x89PNG", "save_image() writes a PNG")


def click_on_chart(p, graph, part_of_width):
    """The mouse comes over the chart and clicks there. WHY not the keyboard: a window in the back gets no focus event."""
    p.act(f"""(function () {{
        const plot = {graph.js}.plot.elem;
        const box = plot.getBoundingClientRect();
        const place = {{ bubbles: true, clientX: box.left + box.width * {part_of_width}, clientY: box.top + box.height * 0.6 }};
        plot.dispatchEvent(new PointerEvent("pointermove", place));
        plot.dispatchEvent(new MouseEvent("click", place));
        return "ok";
    }})()""", "click on the chart")


LAST_LABEL_JS = "Array.from(%s.elem.querySelectorAll('svg text')).map(function (text) { return text.textContent; }).join('|')"


def play_files(p):
    view = p.example.view
    tree = view["tree"]
    folder = os.path.join(p.example.ROOT, "ozdenui")
    p.on_app(lambda: tree.expand(folder))
    p.wait_for_text("app.py")  # WHY wait: the branch is made by Python, after the page asked
    p.click("app.py")
    app_file = os.path.join(folder, "app.py")
    p.expect(tree.value == app_file, f"the value of the tree: {tree.value!r}")
    p.expect(p.on_app(lambda: tree.selected_node)["key"] == app_file, "the selected node")
    p.expect(p.on_app(lambda: tree.get_path(app_file)) == [folder, app_file], "the path of a node")
    p.expect_text(app_file)

    if not p.come_to_front():
        return
    p.on_app(lambda: view["menu"].open_at(120, 120))
    time.sleep(STEP_SECONDS)
    p.click("Its size")
    p.wait_for_text("app.py: " + f"{os.path.getsize(app_file) / 1024:.1f} KB")

    readme = os.path.abspath(os.path.join(p.example.ROOT, "README.md"))
    p.on_app(lambda: view["drop"].add_paths(readme))
    time.sleep(STEP_SECONDS)
    p.expect(view["drop"].paths == [readme], f"the paths of a file from Python: {view['drop'].paths}")
    p.wait_for_text("README.md")

    # WHY not on Windows: WebView2 takes only a file of the disk in a drop (pywebview sends the files to learn their
    #      paths), and the drop of this play is made in the page; a real drag from Explorer is tried by hand there.
    if sys.platform != "win32":
        dropped = os.path.join(tempfile.mkdtemp(), "dropped note.txt")
        with open(dropped, "w", encoding="utf-8") as file:
            file.write("hello")
        p.expect(drop_until_it_arrives(p, view["drop"], dropped), f"the real path of a dropped file: {view['drop'].files}")
        p.expect(len(_dnd_state["paths"]) == 0, "pywebview gave the path it had")
        p.wait_for_text(dropped)
        p.expect(len(view["table"].rows) == 2, f"the rows of the table: {len(view['table'].rows)}")
    p.type_in(view["search"], "values.py")
    p.expect(p.on_app(lambda: tree.get_node(os.path.join(folder, "values.py"))) is not None, "a search finds a file in a folder")
    p.expect(p.on_app(lambda: tree.get_node(folder)) is None, "the search shows only what it found")
    p.type_in(view["search"], "")
    p.expect(p.on_app(lambda: tree.get_node(folder)) is not None, "an empty search brings the tree back")
    p.click("About")
    p.expect_text("A tree, a menu and a place to drop files.")
    p.expect(view["about"].is_open is True, "the popover is open")
    p.click("Close")
    p.expect(view["about"].is_open is False, "a button in the popover closes it")
    p.expect("A tree, a menu" not in p.page_text(), "the popover is gone")
    p.click("About")
    p.expect(view["about"].is_open is True, "it opens again")
    p.click("About")
    p.expect(view["about"].is_open is False, "a second click on its button closes it")
    p.click("Clear")
    p.expect(view["drop"].files == [], f"Clear: {view['drop'].files}")


def drop_until_it_arrives(p, picker, path):
    """WHY tries: on a busy computer the page can miss a drop made so fast; a person's drag takes much longer."""
    for _ in range(DROP_TRIES):
        _dnd_state["paths"].clear()
        if p.come_to_front():
            drop_a_file(p, picker, path)
        deadline = time.time() + DROP_WAIT_SECONDS
        while time.time() < deadline:
            if path in picker.paths:
                return True
            time.sleep(STEP_SECONDS / 2)
    return False


def drop_a_file(p, picker, path):
    """A drop on a FilePicker. Another system: pywebview gets the path by hand and the page a file (WHY: no drag without a
    person there); a real drag is still to be tried on Windows."""
    zone = picker.js + ".zone.elem"
    if can_drop_natively():
        place = p.js(f"(function () {{ const box = {zone}.getBoundingClientRect(); return [box.left + box.width / 2, box.top + box.height / 2]; }})()")
        drop_file_natively(p.app, path, place[0], place[1])
        return
    name = os.path.basename(path)
    _dnd_state["paths"].append((name, path))
    p.act(f"__check.dropFile({zone}, {json.dumps(name)}, 'hello')", "drop a file")


def play_file_tool(p):
    readme = os.path.join(HERE, "..", "README.md")
    p.on_app(lambda: p.example.count_file(readme))
    time.sleep(1.5)
    view = p.example.view
    p.expect("lines" in view["result"]._values.get("text", ""), "no result")
    p.expect(view["bar"].value == 100, f"the bar is {view['bar'].value}")
    p.expect_text("Counted.")


def play_csv_viewer(p):
    p.wait_for_text("Berlin")  # WHY: the rows of a SmartTable come after its first size (a moment later on Chromium)
    p.click("Berlin")
    p.expect_text("city: Berlin")
    p.click("100000 rows")
    p.wait_for_text("7")  # WHY: the rows go to the page, and the table sorts them
    p.click("7")
    p.expect_text("number: 7")
    table = p.first(SmartTable)
    p.expect(len(table.rows) == 100000, f"the table has {len(table.rows)} rows in Python")
    p.expect(p.on_app(lambda: table.selected_row)["number"] == 7, "the selected row of the table")


def play_image_viewer(p):
    image = p.first(ImageView)
    time.sleep(STEP_SECONDS)
    p.expect(image.natural_width == 640, f"the width of the plot: {image.natural_width}")
    p.expect_text("640 x 400 at")
    p.on_app(lambda: image.set_zoom_level(2))
    time.sleep(STEP_SECONDS)
    p.expect(image.zoom_level == 2, f"the zoom in Python: {image.zoom_level}")
    p.click("Draw the plot again")
    p.expect_text("Drawn again")
    p.expect(image.zoom_level == 2, "the zoom stays when the plot is drawn again")


def play_job_log(p):
    p.click("Run the job")
    time.sleep(1.6)
    text = p.on_app(lambda: p.first(LogView).get_text())
    p.expect("The job started" in text, "print() in the LogView: " + text[:200])
    p.expect("Copied photo.jpg" in text, "the logging module in the LogView")
    p.expect("ERROR disk.bin can not be read" in text, "an error of logging is an error of the LogView: " + text[:300])
    p.expect("WARN  backup.zip is very large" in text, "a warning of logging is a warning of the LogView")
    p.expect_text("6 files")
    p.click("Only warnings and errors")
    only = p.on_app(lambda: p.first(LogView).get_text())
    p.expect("Copied" not in only and "disk.bin" in only, "the levels of the LogView: " + only[:200])


def play_editor(p):
    editor = p.first(CodeEditor)
    p.expect("Press F5" in p.on_app(lambda: editor.value), "the first text")
    p.key("F5")
    time.sleep(1.5)  # WHY: a new Python starts and runs the program
    text = p.on_app(lambda: p.first(LogView).get_text())
    p.expect(text.count("1 Ada") == 1 and text.count("The program ended") == 1, "the output of the program, once: " + text[:300])
    tools = p.first(ToolBar)
    p.press_tool(tools, "Clear the output")
    p.expect(p.on_app(lambda: p.first(LogView).get_text()) == "", "a button of the ToolBar clears the output")
    p.on_app(lambda: setattr(editor, "value", "print(1 / 0)"))
    time.sleep(STEP_SECONDS)
    if not p.come_to_front():  # WHY: the next step opens a menu
        return
    # WHY by its object: the text "Run" of the ToolBar is found first.
    p.act(f"({p.first(MenuBar).js}.menuList[1].title.elem.click(), 'ok')", "open the menu Run")
    p.click("Run the program")
    time.sleep(1.5)
    text = p.on_app(lambda: p.first(LogView).get_text())
    p.expect("ZeroDivisionError" in text and "ended with the code 1" in text, "an error of the program: " + text[:300])
    p.press_tool(tools, "Clear the output")
    p.press_tool(tools, "Run")
    time.sleep(1.5)
    text = p.on_app(lambda: p.first(LogView).get_text())
    p.expect(text.count("ZeroDivisionError") >= 1 and text.count("ended with the code 1") == 1, "a button of the ToolBar runs it: " + text[:300])
    p.on_app(lambda: editor.go_to_line(1))
    time.sleep(STEP_SECONDS)
    p.expect_text("Line 1, column 1")
    if not p.open_menu("View", "Dark theme"):  # WHY open_menu: a menu closes when the window loses the focus (run_all)
        return
    p.click("Dark theme")
    ground = p.js(f"getComputedStyle({editor.js}.elem).backgroundColor")
    p.expect(ground == "rgb(28, 28, 27)", f"the dark theme of the CodeEditor: {ground}")
    ground = p.js(f"getComputedStyle({tools.js}.elem).backgroundColor")
    p.expect(ground == "rgb(35, 35, 34)", f"the dark theme of the ToolBar: {ground}")


def play_markdown_editor(p):
    editor = p.first(CodeEditor)
    markdown_view = p.first(MarkdownView)
    in_view = f"{markdown_view.js}.elem"
    p.expect("A small report" in p.js(f"{in_view}.querySelector('[role=heading]').textContent"), "the first text in the view")
    p.expect(p.js(f"{in_view}.querySelectorAll('.markdown-view-code .code-editor-keyword').length") > 0, "the colors of the code")
    typed = '# A typed title\n\n<img src=x onerror="document.title=1"> [a link](https://example.com/x) [not](javascript:document.title=1)'
    p.type_in(editor, typed)
    time.sleep(0.4)  # WHY: on_change waits for the typing to rest
    p.expect(p.js(f"{in_view}.querySelector('[role=heading]').textContent") == "A typed title", "the typed text in the view")
    p.expect(markdown_view.text == typed, f"the text in Python: {markdown_view.text!r}")
    p.expect(p.js(f"{in_view}.querySelectorAll('img').length") == 0, "a typed HTML picture is only a text")
    p.expect("<img src=x" in p.js(f"{in_view}.textContent"), "the typed HTML is shown as it is")
    p.expect(p.js(f"{in_view}.querySelectorAll('a').length") == 1, "the address that is not safe is not a link")
    p.expect_text("10 words")
    p.click("a link")
    p.expect_text("Link: https://example.com/x")
    p.on_app(lambda: markdown_view.append_text("\n\nThe **end**"))
    time.sleep(STEP_SECONDS)
    p.expect("The end" in p.js(f"{in_view}.textContent"), "append_text on the page")
    p.expect(markdown_view.text.endswith("The **end**"), "append_text in Python")
    headings = p.on_app(lambda: markdown_view.headings)
    p.expect(headings == [{"id": "a-typed-title", "level": 1, "text": "A typed title"}], f"the headings: {headings}")
    p.click("Dark theme")
    ground = p.js(f"getComputedStyle({in_view}).backgroundColor")
    p.expect(ground == "rgb(28, 28, 27)", f"the dark theme of the MarkdownView: {ground}")


def press_on_canvas(p, canvas, places):
    """A press of the mouse at the first place, moves to the others, and its end at the last (the places of the canvas)."""
    script = (f"(function () {{ const elem = {canvas.js}.elem.querySelector('canvas'); const rect = elem.getBoundingClientRect();"
              f" const places = {json.dumps(places)};"
              " const send = function (type, place) { elem.dispatchEvent(new PointerEvent(type, { clientX: rect.left + place[0],"
              " clientY: rect.top + place[1], button: 0, pointerId: 9, bubbles: true })); };"
              " send('pointerdown', places[0]); places.slice(1).forEach(function (place) { send('pointermove', place); });"
              " send('pointerup', places[places.length - 1]); return 'ok'; })()")
    p.act(script, f"a press on the canvas at {places[0]}")


def play_paint(p):
    canvas = p.first(Canvas)
    tools = p.first(ToolBar)
    p.press_tool(tools, "The pen: Cyan")  # (its text is also its hint: the color of the line below tells that it ran)
    p.press_tool(tools, "Width 8")
    p.expect_text("The width: 8")
    press_on_canvas(p, canvas, [[100, 100], [140, 120], [200, 160], [260, 150]])
    time.sleep(STEP_SECONDS)  # WHY: the end of the line goes to Python and its count comes back: two ways, not one
    p.expect_text("1 shapes")
    line = canvas.shapes[0]
    p.expect(line["type"] == "polyline" and len(line["points"]) == 4, f"the line in Python: {line}")
    p.expect(line["color"] == "#3F8D94" and line["line_width"] == 8, f"the pen of the line (Cyan, 8): {line['color']}, {line['line_width']}")
    p.click("Shape")
    p.expect_text("2 shapes")
    shape = canvas.shapes[-1]
    middle = [shape["x"], shape["y"]] if shape["type"] == "circle" else [shape["x"] + 30, shape["y"] + 30]
    press_on_canvas(p, canvas, [middle, [middle[0] + 20, middle[1] + 10], [middle[0] + 40, middle[1] + 20]])
    p.expect_text("A shape was moved")
    moved = canvas.shape(shape["key"])
    p.expect(moved["x"] == shape["x"] + 40 and moved["y"] == shape["y"] + 20, f"the new place in Python: {moved['x']}, {moved['y']}")
    p.on_app(lambda: p.example.view["tools"].click_item("undo"))
    time.sleep(STEP_SECONDS)
    p.expect_text("1 shapes")
    picture = os.path.join(tempfile.mkdtemp(), "drawing.png")
    p.on_app(lambda: canvas.save_image(picture))
    with open(picture, "rb") as file:
        p.expect(file.read(8) == b"\x89PNG\r\n\x1a\n", "the drawing is saved as a PNG")


def play_photos(p):
    image = p.first(ImageView)
    p.expect_text("6 pictures")
    p.expect(p.js(f"{image.js}.altText") == "Sea", "the first picture is open")
    p.click("Sunset")
    p.expect_text("Sunset")
    time.sleep(STEP_SECONDS)
    p.expect(p.js(f"{image.js}.altText") == "Sunset", "a click opens the picture large")
    p.expect(image.natural_width == 480, f"its size in Python: {image.natural_width}")
    p.expect(p.on_app(lambda: p.example.view["list"].selected_keys) == ["sunset"], "the chosen picture in Python")


def play_json_viewer(p):
    json_view = p.first(JsonView)
    row_text = lambda key: p.js(f"{json_view.js}.tree.getRowElem({json.dumps(key)}).textContent")
    p.expect(row_text("users[0].name") == 'name"Ada Yılmaz"', "the rows that are open at the start")
    p.expect(p.js(f"{json_view.js}.tree.getRowElem('users[0].address') !== null"), "the second level is open")
    p.expect(p.js(f"{json_view.js}.tree.getNode('users[0].address.city') === null"), "the third level is made when it opens")
    p.act(f"({json_view.js}.tree.getRowElem('users[1].email').click(), 'ok')", "click a row")
    p.expect_text("users[1].email (string)")
    p.expect(json_view.selected_path == ["users", 1, "email"], f"the path in Python: {json_view.selected_path}")
    p.expect(json_view.selected_value == "can@example.com", f"the value in Python: {json_view.selected_value!r}")
    p.click("Open all")
    p.expect(row_text("users[0].address.city") == 'city"İzmir"', "Open all opens the third level")
    p.click("Close all")
    p.expect(p.js(f"{json_view.js}.tree.getRowElem('users').getAttribute('aria-expanded')") == "false", "Close all")
    p.on_app(lambda: json_view.select_path(["users", 0, "roles", 1]))
    time.sleep(STEP_SECONDS)
    p.expect(json_view.selected_path_text == "users[0].roles[1]", f"select_path: {json_view.selected_path_text}")
    p.expect(json_view.selected_value == "editor", f"select_path, its value: {json_view.selected_value!r}")
    values = {"when": datetime.date(2026, 11, 7), "not a number": float("nan"), "big": 2 ** 60, "items": list(range(100000)), "<b>html</b>": "<img src=x>"}
    p.on_app(lambda: json_view.set_value(values))
    time.sleep(STEP_SECONDS)
    p.expect(row_text("when") == 'when"2026-11-07"', "a date is its text")
    p.expect(row_text('["not a number"]') == "not a numberNaN", "a float that is not a number")
    p.expect(row_text("big") == f'big"{2 ** 60}"', "a big number is not rounded")
    p.expect(p.js(f"{json_view.js}.elem.querySelectorAll('img, b').length") == 0, "a value is not read as HTML")
    p.expect(p.js(f"{json_view.js}.elem.querySelectorAll('[role=treeitem]').length") < 200, "a long list comes in pages")
    p.on_app(lambda: json_view.select_path(["items", 76543]))
    time.sleep(STEP_SECONDS)
    p.expect(json_view.selected_value == 76543, f"through the pages: {json_view.selected_value!r}")
    p.expect(p.on_app(lambda: json_view.set_json_text("{ not json")) is False, "set_json_text of a broken text")
    time.sleep(STEP_SECONDS)
    error = p.js(f"{json_view.js}.tree.lblEmpty.elem.getBoundingClientRect().left >= 0 && {json_view.js}.errorText.length > 0")
    p.expect(error, "the error of a broken text is seen")


# A click on a cell of a JsonEditor, as the tests of the kit click it: its row (from 0) and the title of its column
JSON_CELL_CLICK_JS = r"""(function (editor, rowIndex, title) {
    const content = editor.elem.querySelector("div.json-editor-scroll").firstElementChild;
    const titleLabel = Array.from(editor.elem.querySelectorAll("*")).find(function (el) {
        const isTitle = (el.childElementCount === 0 && el.textContent.trim().replace(/ [↑↓]$/, "") === title);
        return isTitle && !el.closest("div.json-editor-scroll") && !editor.titleBar.elem.contains(el);
    });
    if (!titleLabel) return "no column " + title;
    const cell = titleLabel.parentElement.getBoundingClientRect();
    const top = content.getBoundingClientRect().top;
    const point = { clientX: cell.left + 20, clientY: top + (rowIndex + 0.5) * editor.style.rowHeight, bubbles: true, cancelable: true };
    content.dispatchEvent(new MouseEvent("click", point));
    return "ok";
})(%s, %d, %s)"""
# A key in the field of the cell that is being written (text: written into it first; null: as it is)
JSON_CELL_KEY_JS = r"""(function (editor, text, keyName) {
    const field = editor.elem.querySelector("textarea");
    if (text !== null) field.value = text;
    field.dispatchEvent(new KeyboardEvent("keydown", { key: keyName, bubbles: true, cancelable: true }));
    return "ok";
})(%s, %s, %s)"""
# Deeper than the bridge sends a value of an event as it is (5 levels): it comes whole as a JSON text
DEEP_ROWS = [{"name": "Deep", "in_stock": False, "a": {"b": {"c": {"d": {"e": {"f": 1}}}}}}]


def click_json_cell(p, editor, row_index, title):
    p.act(JSON_CELL_CLICK_JS % (editor.js, row_index, json.dumps(title)), f"click the cell {title!r} of row {row_index}")


def press_in_json_cell(p, editor, key, text=None):
    p.act(JSON_CELL_KEY_JS % (editor.js, json.dumps(text), json.dumps(key)), f"{key} in the cell")


def play_json_editor(p):
    editor = p.first(JsonEditor)
    seen = []
    count_products = p.example.count_products
    p.on_app(lambda: editor.set(on_change=lambda e, value: (seen.append(value), count_products(e, value))))
    p.on_app(lambda: editor.set_value(DEEP_ROWS))
    time.sleep(STEP_SECONDS)
    click_json_cell(p, editor, 0, "in_stock")
    deep = [dict(DEEP_ROWS[0], in_stock=True)]
    p.expect(seen[-1:] == [deep], f"on_change gets the whole value: {seen[-1:]!r}")
    p.expect(p.on_app(lambda: editor.value) == deep, "editor.value is the whole value")
    products = p.example.PRODUCTS
    p.on_app(lambda: editor.set_value(products))
    time.sleep(STEP_SECONDS)
    click_json_cell(p, editor, 2, "in_stock")
    # WHY counted from the list: the example may have more products (the slides of the site)
    in_stock = sum(1 for product in products if product["in_stock"]) + (-1 if products[2]["in_stock"] else 1)
    p.expect_text(f"{len(products)} products, {in_stock} in stock")
    click_json_cell(p, editor, 0, "name")
    press_in_json_cell(p, editor, "Enter", "Green apple")
    press_in_json_cell(p, editor, "Escape")  # WHY: Enter opens the cell of the next row
    p.expect(seen[-1][0]["name"] == "Green apple", f"a written cell: {seen[-1][0]!r}")
    p.expect(p.on_app(lambda: editor.value)[0]["name"] == "Green apple", "editor.value after a written cell")
    p.expect(p.on_app(lambda: editor.set_view("json")) is True and p.on_app(lambda: editor.view) == "json", "the JSON view")
    p.expect(p.js(f"{editor.js}.elem.querySelectorAll('textarea')[1].value.indexOf('Green apple') !== -1"), "the JSON text")
    p.expect(p.on_app(lambda: editor.set_view("table")) is True, "back to the table")
    p.expect(p.on_app(lambda: editor.set_json_text("{ not json")) is False, "set_json_text of a broken text")
    p.expect(p.on_app(lambda: editor.error_text).startswith("Not JSON"), "its error")
    p.expect_text(f"{len(products)} rows")  # the table stays
    p.click("Settings...")
    p.wait_for_text("Apply")
    window_editor = [obj for obj in list(p.app._objects.values()) if isinstance(obj, JsonEditor)][-1]
    p.expect(window_editor is not editor, "the editor of the window is a Python object")
    click_json_cell(p, window_editor, 2, "value")  # show_prices: True -> False
    p.click("Apply")
    p.expect(p.example.view["settings"].get("show_prices") is False, f"on_apply: {p.example.view['settings']!r}")
    p.expect(p.example.view["settings"]["address"] == {"city": "İzmir", "zip": "35000"}, "the dict in a cell came back")
    p.expect_text("Settings of Fresh Fruit: 6 names")
    p.expect(p.js("__check.find('Apply') ? 'open' : 'closed'") == "closed", "Apply closes the window")


def play_todo(p):
    tasks = p.first(ItemList)  # WHY first(): the example is a class (TodoApp), it keeps no view dict
    p.type("Test the app")
    p.click("Add")
    p.expect_text("4 tasks, 0 done")
    p.click("Buy bread")
    p.expect_text("4 tasks, 1 done")
    p.click("Delete the done ones")
    p.click("Delete")  # the button of the dialog
    p.expect_text("3 tasks, 0 done")
    p.expect("Buy bread" not in p.page_text(), "Buy bread is still on the page")
    p.expect(len(tasks.items) == 3, f"{len(tasks.items)} items in Python")


def play_settings(p):
    view = p.example.view
    p.click("Sound")
    p.click("High")
    p.click("Notifications")
    p.click("SMS")
    p.click("Save")
    saved = view["saved"]._values.get("text", "")
    for part in ("'sms': True", "'quality': 'High'", "'volume': 7", "'name': 'Ada'", "'language': 'English'"):
        p.expect(part in saved, f"{part} is not in {saved!r}")
    p.click("Reset")
    p.expect(view["sms"].checked is False, "sms is still checked after Reset")


def play_dialogs(p):
    p.click("Confirm")
    p.click("Replace")
    p.expect_text("True")
    p.click("Prompt")
    p.type("Docs")
    p.click("OK")
    p.expect_text("'Docs'")
    p.click("Prompt")
    p.key("Escape")
    p.expect_text("None")
    p.click("Ask")
    p.click("Don't save")
    p.expect_text("\"Don't save\"")
    p.click("Alert")
    p.click("OK")
    p.expect_text("'closed'")


def play_clock(p):
    view = p.example.view
    first = view["clock"].text
    time.sleep(2.2)
    p.expect(view["clock"].text != first, "the clock did not move")
    p.click("Start")
    time.sleep(0.8)
    p.click("Stop")
    shown = float(view["watch"].text.split()[0])
    p.expect(0.5 <= shown <= 2.0, f"the stopwatch shows {shown}")


def play_game(p):
    view = p.example.view
    started = time.perf_counter()
    p.click("Play")
    start_left = view["player"].left
    for _ in range(3):
        p.key("ArrowRight")
    moved = view["player"].left - start_left
    p.expect(moved == 3 * p.example.STEP, f"the player moved {moved} px in Python")
    on_page = p.on_app(lambda: view["player"].measure("left"))
    p.expect(on_page == view["player"].left, f"the player is at {on_page} on the page")
    time.sleep(1.3)
    shown = view["time"].text
    seconds = int(time.perf_counter() - started)
    # WHY from the time that passed: a busy computer took more than 2 s from Play to here ("Time: 27" failed)
    fewest_left = p.example.GAME_SECONDS - seconds
    allowed = [f"Time: {left}" for left in range(fewest_left, p.example.GAME_SECONDS)]
    p.expect(shown in allowed, f"the time is {shown!r} after {seconds} s")


def play_minimal_theme(p):
    if not p.come_to_front():  # WHY: it opens a dialog
        return
    p.click("Remember me")
    p.expect_text("Remember me: False")
    p.click("Yearly")
    p.expect_text("Plan: Yearly")
    p.click("Sound")
    p.expect_text("Tab: Sound")
    p.click("README.md")
    p.expect_text("File: README.md")
    chat = p.first(ChatView)
    p.expect(p.js(f"{chat.js}.styleName").startswith("minimal"), "the minimal look of the ChatView")
    send_in_chat(p, chat, "Hi")
    p.wait_for_text("You wrote: Hi")
    p.click("A dialog")
    p.click("Delete")  # the button of the dialog: it is made after the page
    p.expect_text("The file is deleted.")


def play_minimal_accent(p):
    if not p.come_to_front():  # WHY: it opens a dialog
        return
    p.click("Remember me")
    p.expect_text("Remember me: False")
    p.click("Sound")
    p.expect_text("Tab: Sound")
    p.click("A dialog")
    p.click("Yes, send")  # the button of the dialog: it is made after the page
    p.expect_text("The report is sent.")


PLAYS = {name[len("play_"):]: func for name, func in globals().items() if name.startswith("play_")}
PLAYS["gallery-styled"] = play_gallery  # WHY: the same page, only some looks and a color are chosen by its code


# *** RUN:

def main():
    name = sys.argv[1]
    picture_file = sys.argv[2] if len(sys.argv) > 2 else ""
    theme = sys.argv[3] if len(sys.argv) > 3 else "light"
    example = load_example(name)
    result = {"example": name if theme == "light" else f"{name} {theme}", "problems": [], "picture": None}
    stderr = TerminalProblems(sys.stderr)
    stderr.set_step("the window opens: start()")
    sys.stderr = stderr

    def play():
        player = Player(app, example, stderr)
        try:
            player.js(HELPERS_JS)
            time.sleep(STEP_SECONDS)
            PLAYS[name](player)
        except Exception:
            player.problems.append(traceback.format_exc(limit=3))
        stderr.set_step("after the play: the picture, the window closes")
        result["problems"] = player.problems
        if not picture_file:
            app.close()
            return

        def after_picture(error):
            result["picture"] = error or picture_file
            app.close()

        app.call_soon(lambda: snapshot_window(app, picture_file, after_picture))

    def start(page):
        try:
            example.start(page)
        finally:
            threading.Thread(target=play, daemon=True).start()

    # WHY STYLE and COMPONENTS of the example: its own window is not opened, so this one takes its look and its components
    app = App(start, title=name, size=SIZES.get(name, DEFAULT_SIZE), theme=theme, style=getattr(example, "STYLE", ""),
              accent=getattr(example, "ACCENT", ""), components=getattr(example, "COMPONENTS", ()))
    # WHY here and not in start(): a page that does not get ready never calls start().
    closer = threading.Timer(TIMEOUT_SECONDS, app.close)
    closer.daemon = True
    closer.start()
    app.run()
    result["terminal_problems"] = stderr.lines
    result["passed"] = not result["problems"] and not stderr.lines
    sys.stderr = stderr.stream
    print(json.dumps(result))  # WHY ASCII: the console of Windows can not print every letter of a message
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
