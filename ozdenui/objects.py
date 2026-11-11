# Bismillah
"""objects.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The basic.js objects on the Python side.

An object here is a proxy: it keeps an id and the values it was given, and sends commands to the page, where the
real basic.js object lives. Reading a value it was given needs no question to the page (label.text).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import difflib
import itertools
import sys

from . import _kit
from . import app as _app
from .values import (call_with_count, camel_case, event_name_of, number_format, picture_address, positional_count, snake_case,
                     source_line, to_page)

_POSITION_NAMES = ("left", "top", "width", "height")
_next_number = itertools.count(1)
_warned_names = set()  # (the type, the name, the line of the program) already told in the terminal


def _warn_about_unknown_names(type_name, names):
    """Tells once in the terminal, at the line of the program, about a name an object does not have.
    WHY: the page kept a misspelled name as a property of its own, without a word: Label(txet="Hi") showed nothing."""
    known = _kit.known_names(type_name)
    if known is None:
        return  # a component the list of the kit does not know: its params are not known either
    for name in names:
        if camel_case(name) in known:
            continue
        place = source_line()
        if (type_name, name, place) in _warned_names:
            continue
        _warned_names.add((type_name, name, place))
        # WHY only the names Python can send: a name of the kit with an underscore (lbl_arrow of Tooltip) goes as lblArrow
        reachable = [known_name for known_name in known if camel_case(snake_case(known_name)) == known_name]
        guess = difflib.get_close_matches(camel_case(name), reachable, n=1)
        hint = f' (did you mean "{snake_case(guess[0])}"?)' if guess else ""
        print(f'ozdenui: {place}: {type_name}: "{name}" is not a param of {type_name}{hint}', file=sys.stderr)


def _warn_about_camel_names(type_name, names):
    """Tells once in the terminal, at the line of the program, about a name of the kit a class got in camelCase.
    WHY: a class reads its params and gives its defaults by their Python names, so a camelCase name could go under them
    without a word: TextField(titleText="Name") had no title, CheckBox(onChange=fn) never called fn. Its value still
    goes to the page; Component("Name") takes both ways."""
    known = _kit.known_names(type_name) or frozenset()
    for name in names:
        python_name = snake_case(name)
        is_reachable = (camel_case(python_name) == camel_case(name))
        if python_name == name or camel_case(name) not in known or not is_reachable:
            continue  # a Python name, or one the warning of unknown names tells
        place = source_line()
        if (type_name, name, place) in _warned_names:
            continue
        _warned_names.add((type_name, name, place))
        print(f'ozdenui: {place}: {type_name}: "{name}" is written "{python_name}" in Python '
              f"(a class reads its params by their Python names)", file=sys.stderr)


def _new_id():
    return "o" + str(next(_next_number))


def _listen_for_enter(obj, handler):
    """Runs handler on Enter (the on_enter of an Input and of the fields): handler() or handler(obj). A new one replaces
    the one given before, None takes it away. WHY its own place: as a value of the page, inp.on_enter = fn listened to an
    "enter" event, which the page does not have."""
    if handler is None:
        obj._set_dom_handler("keydown", None, slot="enter")
        return
    count = positional_count(handler)

    def on_key(_obj, event):
        if event.get("key") == "Enter":
            call_with_count(handler, count, [obj])

    obj._set_dom_handler("keydown", on_key, slot="enter")


class BasicObject:
    """The common part of every object: create, set, on, measure, remove, and "with" for a container."""

    _type = "Box"  # the basic.js function that makes it
    _is_container = False
    _built_in_events = ()  # DOM events the page always sends (an Input sends its text)
    _state = {}  # values the page sends back with every event, kept in Python: {"checked": "checked"} reads a
    #              property, {"selectedKeys": "getSelectedKeys()"} calls a method
    _callback_params = False  # components: on_change=fn is the onChange param (a callback), not a DOM event
    _has_own_place = False  # the object knows its place without one (StatusBar: at the bottom of a Box)
    _dark_values = {}  # its values in a dark window (App(theme="dark")), unless they are given
    _text_is_plain = False  # Label, Button: text is shown as it is written (plainText of basic.js); html= is HTML
    _whole_args = {}  # callback params whose values at these places are JSON data that comes whole: {"onChange": (1,)}

    def __init__(self, *position, **props):
        if len(position) not in (0, 4):
            raise TypeError(f"{type(self).__name__}() takes no position or all four: left, top, width, height")
        app = _app.current_app()
        self._init_proxy(app, _new_id(), dict(zip(_POSITION_NAMES, position)), self._built_in_events)

        if not position and not self._has_own_place and self._is_free_place(app._objects.get(app._container_id())):
            # WHY: basic.js puts an object without a place at -1000, -1000 (out of sight until it is placed). Outside
            #      a group, Python gives it the top left corner: the commands go together, so nothing is seen early.
            props.setdefault("left", 0)
            props.setdefault("top", 0)
        self._take_fill(props, app)
        dom_handlers = self._take_dom_handlers(props)
        _warn_about_unknown_names(self._type, props)
        values = {camel_case(name): value for name, value in props.items()}
        values = {**self._first_values(values), **values}
        if app.theme == "dark":
            for key, value in self._dark_values.items():
                values.setdefault(key, value)
        page_values = self._page_values(values, f"{type(self).__name__}()")
        self._keep_values(values)

        app._register(self)
        app._send({
            "op": "create",
            "id": self._id,
            "type": self._type,
            "args": list(position),
            "props": page_values,
            "parent": app._container_id(),
            "state": dict(self._state),
            "src": source_line(),
        })
        for event_name in self._built_in_events:
            app._send({"op": "listen", "id": self._id, "event": event_name})
        for event_name, handler in dom_handlers.items():
            self._set_dom_handler(event_name, handler)

    def _init_proxy(self, app, object_id, values, listened=()):
        object.__setattr__(self, "_app", app)
        object.__setattr__(self, "_id", object_id)
        object.__setattr__(self, "_handlers", {})
        object.__setattr__(self, "_listened", set(listened))
        object.__setattr__(self, "_values", values)
        object.__setattr__(self, "_prop_handlers", {})  # event -> the remover of the handler given as on_x=fn
        object.__setattr__(self, "_param_callbacks", {})  # param -> the ids of the functions given to it (also in its items)

    def _first_values(self, values):
        """Values Python gives before the values of the code, which win (a group: clipContent 0)."""
        return {}

    def _take_fill(self, props, app):
        """fill=True: the object takes the room the other objects of its group leave: the height that is left in a
        VGroup, the width that is left in an HGroup. (A grow of flexbox that may also shrink.)"""
        if not props.pop("fill", False):
            return
        parent = app._objects.get(app._container_id())
        is_in_row = isinstance(parent, HGroup) and not isinstance(parent, GridGroup)
        look = _FILL_IN_ROW if is_in_row else _FILL_IN_COLUMN
        for name, value in look["props"].items():
            props.setdefault(name, value)
        # WHY the basis and the minimum: a flex item is as large as its content unless it may shrink (no scroll bar came)
        props["css"] = dict(look["css"], **props.get("css", {}))

    def _take_dom_handlers(self, props):
        """on_click=fn of an object (not of a component, where it is a param): {"click": fn}, out of props. None takes
        the handler away."""
        if self._callback_params:
            return {}
        names = [name for name in props if name.startswith("on_") and (callable(props[name]) or props[name] is None)]
        return {event_name_of(name): props.pop(name) for name in names}

    def _page_values(self, values, where):
        """The values as they go to the page. The functions given to a param replace the ones given before.
        None in a callback param of a component is the default of the component (see _no_function)."""
        page_values = {}
        for key, value in values.items():
            if _is_style_param(key):
                value = _style_keys_for_page(value)
            if value is None and self._callback_params and _is_callback_param(key):
                value = self._no_function(key)
            page_key = self._page_key(key)
            callback_ids = []
            page_values[page_key] = to_page(value, self._app, self._id, where, callback_ids)
            self._replace_callbacks(key, callback_ids)
            is_function = callable(value) and not hasattr(value, "_id")
            if is_function and key in self._whole_args:
                page_values[page_key]["wholeArgs"] = list(self._whole_args[key])
        return page_values

    def _no_function(self, key):
        """WHY: on_change=None (a function of the program that may be None) went to the page as null, and the
        component called it: an error of the page at every click."""
        return _kit.no_function(self._type, key)

    def _replace_callbacks(self, slot, callback_ids):
        """The functions of a param (or of the items of a list) in the place of the ones given to it before, which are
        forgotten. WHY: every set(on_change=fn) kept a new function for ever, and so did every set_items() whose items
        had an on_click (with what each function held)."""
        for callback_id in self._param_callbacks.pop(slot, ()):
            self._app._forget_callback(callback_id)
        if callback_ids:
            self._param_callbacks[slot] = callback_ids

    def _page_key(self, key):
        """WHY plainText: the text of basic.js is HTML, so a typed "<b>" became bold and a "<img onerror=...>" ran.
        In Python, text is the text as it is written; html= is the HTML.
        WHY text for html: a Label and a Button of basic.js have no html (only a Box has one): their text is the HTML.
        Sent as html it was a property nobody reads: Label(html="<b>3</b> new") showed nothing."""
        if self._text_is_plain and key == "text":
            return "plainText"
        if self._text_is_plain and key == "html":
            return "text"
        return key

    def _python_key(self, key):
        """The name a value is kept under: a Label given plain_text reads it back as label.text."""
        if self._text_is_plain and key == "plainText":
            return "text"
        return key

    def _keep_values(self, values):
        """The values given (not the functions), kept to be read back without a question to the page."""
        for key, value in values.items():
            if callable(value):
                continue
            key = self._python_key(key)
            if self._text_is_plain and key in ("text", "html"):
                # WHY: after one of them, the other one is not what the object shows
                self._values.pop("html" if key == "text" else "text", None)
            self._values[key] = value

    def _set_dom_handler(self, event_name, handler, slot=None):
        """The handler given as a value (on_click=fn, obj.on_click = fn): a new one replaces it, None takes it away; the
        handlers of on() stay. slot: its own place when two of them listen to one event (on_enter: a keydown).
        WHY: obj.on_click = fn went to the page as a param, and nothing listened to the click."""
        slot = slot or event_name
        old_remover = self._prop_handlers.pop(slot, None)
        if old_remover:
            old_remover()
        if handler is not None:
            self._prop_handlers[slot] = self.on(event_name, handler)

    @staticmethod
    def _is_free_place(container):
        """The page or a Box: its objects have a place of their own (in a group, the group places them)."""
        if isinstance(container, Page):
            return True
        if container is None or isinstance(container, (VGroup, HGroup, Part)):
            return False  # WHY Part: the boxes of components to put objects into are groups (a tab, a dialog)
        return isinstance(container, Box)

    # *** VALUES:

    def __getattr__(self, name):
        # WHY: only called for names that are not attributes of the proxy: they are the values of the object.
        if name.startswith("_"):
            raise AttributeError(name)
        values = object.__getattribute__(self, "_values")
        key = self._python_key(camel_case(name))
        if key in values:
            return values[key]
        raise AttributeError(
            f"{type(self).__name__}.{name} was not given: read it from the page with .measure(\"{name}\")"
        )

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        self.set(**{name: value})

    def set(self, **props):
        """Changes values: label.set(text="Hi", font_size=20). label.text = "Hi" does the same."""
        for event_name, handler in self._take_dom_handlers(props).items():
            self._set_dom_handler(event_name, handler)
        if not props:
            return self
        _warn_about_unknown_names(self._type, props)
        values = {camel_case(name): value for name, value in props.items()}
        page_values = self._page_values(values, f"{type(self).__name__}.set()")
        self._keep_values(values)
        self._app._send({"op": "set", "id": self._id, "props": page_values, "src": source_line()})
        return self

    def measure(self, name):
        """The value as basic.js reads it on the page now (a size of "auto", the text of an Input...)."""
        return self._app._read(self._id, self._page_key(camel_case(name)))

    def call(self, method, *args):
        """Calls a method of the basic.js object: box.call("setMotion", "left 0.3s"). Its result is not waited for."""
        return self._send_call(method, args, f"{type(self).__name__}.call(\"{method}\")")

    def _call_and_refresh(self, method, *args):
        """call(), and the page sends the state back after it (the value as the component keeps it)."""
        return self._send_call(method, args, f"{type(self).__name__}.{method}()", refresh=True)

    def _call_with_items(self, slot, method, *args):
        """call() that gives the object new items for its param slot ("items", "menus"): the functions of the old items
        are forgotten (see _replace_callbacks)."""
        return self._send_call(method, args, f"{type(self).__name__}.{method}()", slot=slot)

    def _send_call(self, method, args, where, refresh=False, slot=None):
        callback_ids = []
        page_args = [to_page(value, self._app, self._id, where, callback_ids) for value in args]
        if slot is not None:
            self._replace_callbacks(slot, callback_ids)
        command = {"op": "call", "id": self._id, "method": method, "args": page_args, "src": source_line()}
        if refresh:
            command["refresh"] = 1
        self._app._send(command)
        return self

    def ask(self, method, *args):
        """Calls a method of the basic.js object and returns its result (a question to the page)."""
        where = f"{type(self).__name__}.ask(\"{method}\")"
        page_args = [to_page(value, self._app, self._id, where) for value in args]
        return self._app._ask(self._id, method, page_args)

    @property
    def js(self):
        """The object in JavaScript, for app.evaluate(): app.evaluate(f"{label.js}.elem.offsetWidth")"""
        return f"__bp.objectOf('{self._id}')"

    # *** EVENTS (of the DOM: click, input, keydown, mouseenter...):

    def on(self, event_name, handler):
        """handler(), handler(obj) or handler(obj, event). Returns a function that removes it."""
        entry = (handler, positional_count(handler))
        self._handlers.setdefault(event_name, []).append(entry)
        if event_name not in self._listened:
            self._listened.add(event_name)
            self._app._send({"op": "listen", "id": self._id, "event": event_name, "src": source_line()})

        def remove_handler():
            handlers = self._handlers.get(event_name, [])
            if entry in handlers:
                handlers.remove(entry)

        return remove_handler

    def _receive(self, event_name, data):
        if "text" in data:
            self._values["text"] = data["text"]
        if data.get("state"):
            self._values.update(data["state"])
        for handler, count in list(self._handlers.get(event_name, [])):
            call_with_count(handler, count, [self, data])

    # *** CONTAINER: "with box:" makes the objects of the block inside it.

    def __enter__(self):
        if not self._is_container:
            raise TypeError(f"A {type(self).__name__} can not hold other objects: only a Box or a group can.")
        self._app._open_container(self._id)
        return self

    def __exit__(self, *error):
        self._app._close_container(self._id)
        return False

    # *** REMOVE:

    def remove(self):
        """Removes the object and every object inside it."""
        self._app._send({"op": "remove", "id": self._id, "src": source_line()})

    def __repr__(self):
        return f"<{type(self).__name__} {self._id}>"


# The keys of a style go to the page in camelCase, also when the code writes them in snake_case (selected_color).
# WHY the prefixes: the kit names a few families of keys with a prefix and an underscore (the params of a ScrollBar:
#      bar_color, bar_width...): they stay as they are.
_KIT_KEY_PREFIXES = ("bar_", "lbl_", "tab_", "input_")


def _is_style_param(key):
    """style, look, buttonStyle, searchParams...: a param of looks, not of data (the rows of a table keep their keys)."""
    return key in ("style", "look") or key.endswith("Style") or key.endswith("Params")


def _is_callback_param(key):
    """onChange, onClick...: a param of a component that takes a function."""
    return key.startswith("on") and key[2:3].isupper()


def _style_keys_for_page(value):
    if isinstance(value, dict):
        return {_style_key_for_page(key): _style_keys_for_page(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_style_keys_for_page(item) for item in value]
    return value


def _style_key_for_page(key):
    if not isinstance(key, str) or "_" not in key or key.startswith(_KIT_KEY_PREFIXES):
        return key
    return camel_case(key)


_DARK_TEXT = "rgba(255, 255, 255, 0.86)"
_FILL_IN_COLUMN = {"props": {"width": "100%", "height": "auto", "grow": 1}, "css": {"flexBasis": "0", "minHeight": "0"}}
_FILL_IN_ROW = {"props": {"width": "auto", "height": "100%", "grow": 1}, "css": {"flexBasis": "0", "minWidth": "0"}}


class Box(BasicObject):
    _type = "Box"
    _is_container = True
    _dark_values = {"color": "#232322", "textColor": _DARK_TEXT}


class _Group(Box):
    """The common part of VGroup and HGroup. Unlike in basic.js, a group does not cut what goes out of it: clip_content=True
    cuts. A group that scrolls (scroll_y=True at its start) cuts, as in basic.js."""
    _dark_values = {}  # WHY: a group has no ground of its own

    def _first_values(self, values):
        # WHY: a group of basic.js cut a button that grew, a focus ring or a shadow at its edge, so nearly every group
        #      of a program said clip_content=0.
        # WHY first: clipContent sets the overflow of both sides, so after a scrollY it would take the scroll bar away.
        if values.get("scrollY") or values.get("scrollX"):
            return {}
        return {"clipContent": 0}


class VGroup(_Group):
    """Objects one under the other (flexbox). A group is 100% x 100% by default; hug=True wraps its content."""
    _type = "VGroup"


class HGroup(_Group):
    """Objects side by side (flexbox)."""
    _type = "HGroup"


class GridGroup(HGroup):
    """Objects in columns and rows: with GridGroup(columns=3, gap=8): ... They go into the cells in order, left to right.
    columns: 3 (equal columns), [120, "1fr", "auto"] (px, a part of the room, the width of its content) or a CSS text.
    rows: none (as many as the objects need, each as high as its content), or as columns: with a height, rows=4 fills it.
    gap: 8 or [column gap, row gap]. align: where each object stands in its cell ("left center"); none: it fills the cell.
    An object with a width of its own keeps it: width="100%" fills the cell. Unlike the other groups it is as high as its rows.
    grid.place(obj, column_span=2) and grid.place(obj, column=1, row=0, align="right") give an object a cell of its own (from 0)."""
    _type = "GridGroup"
    _METHODS = {"columns": "setColumns", "rows": "setRows", "gap": "setGap", "align": "setAlign"}

    def __init__(self, *position, **props):
        # WHY in the props: a component of comp/ takes one params object, not (left, top, width, height).
        super().__init__(**dict(zip(_POSITION_NAMES, position)), **props)

    def set(self, **props):
        # WHY methods: as plain values they would not reach the CSS of the grid.
        for name, method in self._METHODS.items():
            if name in props:
                self._values[name] = props[name]
                self.call(method, props.pop(name))
        return super().set(**props)

    def place(self, obj, column=None, row=None, column_span=None, row_span=None, align=None):
        """Returns the object."""
        where = {"column": column, "row": row, "columnSpan": column_span, "rowSpan": row_span, "align": align}
        self.call("place", obj, {name: value for name, value in where.items() if value is not None})
        return obj


class Label(BasicObject):
    """A text: Label(text="3 new"). The text is shown as it is written (a typed "<b>" stays "<b>"); html="<b>3</b> new"
    for HTML. NOTE: unlike basic.js, where text is HTML."""
    _type = "Label"
    _dark_values = {"textColor": _DARK_TEXT}
    _text_is_plain = True


class Button(BasicObject):
    """The plain button of basic.js. SmartButton is the modern one. text as in a Label; html= for HTML."""
    _type = "Button"
    _text_is_plain = True


class Input(BasicObject):
    """A text box: Input(placeholder="A name", on_enter=fn). inp.text is always the text on the page (the page sends it
    at every change). on_enter(inp) runs on Enter; the other events of the page work as on every object (on_input...)."""
    _type = "Input"
    _built_in_events = ("input",)
    _dark_values = {"color": "#2A2A29", "textColor": _DARK_TEXT, "borderColor": "rgba(255, 255, 255, 0.2)"}

    def __init__(self, *position, on_enter=None, **props):
        super().__init__(*position, **props)
        if on_enter is not None:
            _listen_for_enter(self, on_enter)

    def set(self, **props):
        if "on_enter" in props:
            _listen_for_enter(self, props.pop("on_enter"))
        return super().set(**props)


class Icon(BasicObject):
    """A picture: Icon(0, 0, 48, 48, picture="photo.png"). picture: a path, bytes, a Pillow image, a matplotlib figure
    or an address (see picture_address). icon.picture = "other.png" changes it. ImageView is the one with a zoom."""
    _type = "Icon"

    def __init__(self, *position, picture=None, **props):
        super().__init__(*position, **props)
        if picture is not None:
            self.set(picture=picture)

    def set(self, **props):
        # WHY a method and not a value: an Icon loads its file with load(); a value named picture did nothing.
        if "picture" in props:
            self._values["picture"] = props["picture"]
            self.call("load", picture_address(props.pop("picture")))
        return super().set(**props)


class Part(BasicObject):
    """A box inside a component (the panel of a tab, the content of a dialog): objects go into it with "with"."""

    _is_container = True

    def __init__(self, owner, path):
        app = owner._app
        self._init_proxy(app, _new_id(), {})
        app._register(self)
        app._send({"op": "part", "id": self._id, "of": owner._id, "path": list(path), "src": source_line()})


class Page(BasicObject):
    """The page of basic.js: it already exists, so it is not created. page.color = "#F4F5F7"
    page.on("resize", fn) and page.on("keydown", fn) listen to the window; page.width / page.height are current."""

    _is_container = True

    def __init__(self, app, width=0, height=0):
        self._init_proxy(app, "page", {"width": width, "height": height}, ("resize",))
        app._register(self)
        # WHY always: page.width / page.height came only with an event of the page, so without a handler of the
        #      user they kept the size of the start
        app._send({"op": "listen", "id": "page", "event": "resize"})

    @property
    def app(self):
        """The App of the window: page.app.theme, page.app.close()... (every(), open_file() and the others are also
        functions of ozdenui)."""
        return self._app

    def remove(self):
        raise TypeError("The page can not be removed: close the window with app.close().")


# The dark look of the components that have one, for a dark window (App(theme="dark")). The others keep their look.
# WHY these names: the rule of the kit for a new dark page (CLAUDE.md of the repository): "dark" for the fields of text,
# "ozdenDark" for the buttons, the lists and the search box.
DARK_STYLE_NAMES = {
    "SmartButton": "ozdenDark", "TextField": "dark", "EmailField": "dark", "PhoneField": "dark",
    "PasswordField": "dark", "UrlField": "dark", "NumberField": "dark", "CurrencyField": "dark",
    "TextAreaField": "dark", "ItemList": "ozdenDark", "SearchInput": "ozdenDark", "ProgressBar": "dark",
    "Dialog": "ozdenDark", "LoadingScreen": "ozdenDark", "Slider": "roundDark", "RangeSlider": "roundDark", "StepBar": "dark",
    "CheckBox": "dark", "RadioButton": "dark", "Toggle": "ozdenDark", "SelectBox": "dark", "SliderField": "dark", "Tabs": "dark",
    "SmartTable": "dark", "LogView": "dark", "ImageView": "dark", "MenuBar": "dark", "StatusBar": "dark", "Splitter": "dark",
    "FilePicker": "dark", "Accordion": "dark", "ToolBar": "dark", "MarkdownView": "dark", "JsonView": "dark",
    "JsonEditor": "dark", "CodeEditor": "dark", "ContextMenu": "dark", "DataTable": "dark", "FullScreenSelect": "dark", "Gauge": "dark",
    "LabelEditor": "dark", "LeftMenu": "dark", "NumericKeyboard": "dark", "RichTextEditor": "dark", "SearchResults": "dark",
    "ColorPicker": "dark", "DatePicker": "dark", "TimePicker": "dark", "SidePanel": "dark", "SortableList": "dark",
    "Stepper": "dark", "TagInput": "dark", "TinyTable": "dark", "TreeView": "dark", "Canvas": "dark", "ScrollArea": "dark",
    "ChatView": "dark",
}
# The components that have the minimal look (App(style="minimal")): (light window, dark window)
_MINIMAL_PAIR = ("minimal", "minimalDark")
MINIMAL_STYLE_NAMES = {name: _MINIMAL_PAIR for name in (
    "SmartButton", "CheckBox", "RadioButton", "Toggle", "SearchInput", "SelectBox", "ItemList", "Slider", "ProgressBar",
    "Tabs", "Stepper", "TextField", "EmailField", "PhoneField", "PasswordField", "UrlField", "NumberField",
    "CurrencyField", "TextAreaField", "ContextMenu", "Tooltip", "TreeView", "SmartTable", "RangeSlider", "MenuBar", "ToolBar",
    "StatusBar", "Dialog", "DataTable", "DatePicker", "TimePicker", "ColorPicker", "FilePicker", "Accordion", "SliderField",
    "StepBar", "TagInput", "Splitter", "SidePanel", "LoadingScreen", "ScrollArea", "JsonEditor", "ChatView",
)}
# The packages of App(accent=...): MinimalAccent (comp/minimal-accent.js) makes them on the page from the minimal ones,
# for the same components. A SmartButton tone of the same name: the main action in the color (tone="accent").
ACCENT_STYLE_NAME = "minimalAccent"
_ACCENT_PAIR = (ACCENT_STYLE_NAME, ACCENT_STYLE_NAME + "Dark")
# A light package the code names, and its dark twin: a dark window takes the twin (ItemList(style_name="gallery")).
DARK_TWIN_STYLE_NAMES = {"ItemList": {"gallery": "galleryDark"}, "SmartButton": {"minimalDanger": "minimalDangerDark"}}
_THEME_PARAM = ("GraphBox",)  # it takes theme="dark" (or "minimal", "minimalDark"), not a package


def _unframed_style(style):
    """The style of a component without its frame: no border and no rounded corners on its box. The keys of the code win.
    WHY a param of Python: seven examples wrote style={"box": {"border": 0, "round": 0}} for a component that fills the
    room between two bars; the frame of a component is on the box of its style in the kit."""
    style = dict(style or {})
    box = dict(style.get("box") or {})
    box.setdefault("border", 0)
    box.setdefault("round", 0)
    style["box"] = box
    return style


class Component(BasicObject):
    """A component of basic.js (comp/): its params as keywords, a function for a callback param.
    Component("TreeView", width=300, on_select=fn) uses one without a Python class of its own.
    framed=False: no border and no rounded corners on its box (a component that fills the room between two bars); it is
    style={"box": {"border": 0, "round": 0}}, and a key of your own style wins."""

    _callback_params = True

    def __init__(self, type_name, *position, **params):
        if len(position) not in (0, 4):
            raise TypeError(f"{type_name}() takes no position or all four: left, top, width, height")
        # WHY: a component takes one params object, not (left, top, width, height): the position goes into it
        params = dict(dict(zip(_POSITION_NAMES, position)), **params)
        if not params.pop("framed", True):
            params["style"] = _unframed_style(params.get("style"))
        self._take_window_theme(type_name, params)
        object.__setattr__(self, "_type", type_name)
        super().__init__(**params)

    @staticmethod
    def _take_window_theme(type_name, params):
        """A minimal window: the minimal look; a dark window: the dark look; unless the code chose one.
        A chosen light package with a dark twin (DARK_TWIN_STYLE_NAMES) becomes the twin in a dark window."""
        is_dark = (_app.current_app().theme == "dark")
        for name in ("style_name", "styleName"):
            if is_dark and name in params:
                params[name] = DARK_TWIN_STYLE_NAMES.get(type_name, {}).get(params[name], params[name])
        if "style_name" in params or "styleName" in params:
            return
        if type_name in _THEME_PARAM:
            _take_window_theme_param(params, is_dark)
            return
        if _takes_minimal_look(type_name):
            params["style_name"] = minimal_style_name(type_name, is_dark)
            return
        if is_dark and type_name in DARK_STYLE_NAMES:
            params["style_name"] = DARK_STYLE_NAMES[type_name]

    def set(self, **props):
        """Changes values: comp.set(unit_text="lb"); comp.unit_text = "lb" does the same. A param the component has a
        method for (the setUnitText of the kit) is changed with it: the component draws it again, and its callback is
        not called. Any other value goes to the page as it is.
        WHY: sent as a value, such a param changed nothing, without a word (field.unit_text, table.rows of a DataTable)."""
        methods = _kit.component_setters(self._type)
        for name in [name for name in props if camel_case(name) in methods]:
            self._set_with_method(name, props.pop(name))
        return super().set(**props)

    def _set_with_method(self, name, value):
        key = camel_case(name)
        method, takes_silent = _kit.component_setters(self._type)[key]
        values = {key: value}
        page_value = self._page_values(values, f"{type(self).__name__}.set()")[self._page_key(key)]
        self._keep_values(values)
        arguments = [page_value, 1] if takes_silent else [page_value]
        command = {"op": "call", "id": self._id, "method": method, "args": arguments, "src": source_line()}
        if self._state:
            command["refresh"] = 1  # WHY: the method may change the state too (new rows: no row is selected)
        self._app._send(command)

    def part(self, *path):
        """A box inside the component, to put objects into: with comp.part("content"): Label(...)
        A step may call a method: {"call": "getPanel", "args": ["Details"]}."""
        return Part(self, path)


def _take_window_theme_param(params, is_dark):
    """GraphBox: the look of the window as its theme param, unless the code chose a theme."""
    if getattr(_app.current_app(), "style", "") == "minimal":
        params.setdefault("theme", "minimalDark" if is_dark else "minimal")
    elif is_dark:
        params.setdefault("theme", "dark")


def _takes_minimal_look(type_name):
    return getattr(_app.current_app(), "style", "") == "minimal" and type_name in MINIMAL_STYLE_NAMES


def minimal_style_name(type_name, is_dark):
    """The minimal package of a component in this window: minimal / minimalDark, or the ones of App(accent=...)."""
    pair = _ACCENT_PAIR if getattr(_app.current_app(), "accent", "") else MINIMAL_STYLE_NAMES.get(type_name, _MINIMAL_PAIR)
    return pair[1 if is_dark else 0]


def _keep_state():
    """The callback of a component that only keeps its state in Python (the page sends it with every call)."""


class TypedComponent(Component):
    """The base of the components with a Python class: CheckBox(text="...")"""

    _defaults = {}  # params given unless the user gives them (Ex: the modern look)
    _aliases = {}  # short Python names of params: {"text": "label_text"}
    _setters = {}  # obj.name = value calls a method of the class: {"checked": "set_checked"}
    _sync_callbacks = ()  # callbacks always given to the page, so the state stays current: ("on_change",)
    _state_defaults = {}  # the state before the first event, unless a param gave it: {"selectedKeys": []}
    _data_params = ("value", "options", "items", "rows", "columns", "tabs", "selectedKeys", "group", "itemDataList", "titleDataList")  # True stays True
    _format_params = ()  # params that take a text like "{:,.0f} TL": it works on the page ("formatValue")

    def __init__(self, *position, **params):
        _warn_about_camel_names(self._type, params)
        given = {}
        for name, value in list(params.items()):
            if name in self._aliases:
                given[name] = value
                params[self._aliases[name]] = params.pop(name)
        is_dark_window = _app.current_app().theme == "dark" and self._type in DARK_STYLE_NAMES
        is_minimal_look = _takes_minimal_look(self._type)
        is_window_look = is_dark_window or is_minimal_look
        for name, value in self._defaults.items():
            if name == "style_name" and is_window_look:
                continue  # WHY: the look of a light window; Component chooses the dark or the minimal one.
            params.setdefault(name, value)
        for name in self._sync_callbacks:
            params.setdefault(name, _keep_state)
        self._prepare_params(params)
        super().__init__(self._type, *position, **params)
        for name, value in given.items():
            if not callable(value):
                self._values[camel_case(name)] = value
        for key, value in self._state_defaults.items():
            self._values.setdefault(key, value)

    def set(self, **props):
        _warn_about_camel_names(self._type, props)
        plain = {}
        for name, value in props.items():
            if name in self._setters:
                getattr(self, self._setters[name])(value)
                continue
            plain[self._aliases.get(name, name)] = value
            if name in self._aliases and not callable(value):
                self._values[camel_case(name)] = value  # WHY: read by its short name, it was the value of the start
        self._prepare_params(plain)
        if plain:
            super().set(**plain)
        return self

    def _prepare_params(self, params):
        self._flags_as_numbers(params)
        for name, value in params.items():
            if camel_case(name) in self._format_params:
                params[name] = self._format_of(name, value)

    def _no_function(self, key):
        # WHY: the state of the component comes back with this one (on_change=None: box.checked stayed as it was)
        if snake_case(key) in self._sync_callbacks:
            return _keep_state
        return super()._no_function(key)

    def _format_of(self, name, value):
        where = f"{type(self).__name__}({name}=...)"
        if value is None:
            return None
        if callable(value):
            raise TypeError(f'{where}: it is a text like "{{:,.0f}} TL": a Python function can not answer the page at once')
        return number_format(value, where)

    def _flags_as_numbers(self, params):
        """True / False -> 1 / 0, as basic.js takes them (a Toggle compares value === 1). The data params stay.
        WHY set() too: only the params of the start were changed, so set(enabled=False) sent false."""
        for name, value in params.items():
            if isinstance(value, bool) and camel_case(name) not in self._data_params:
                params[name] = int(value)

    def _keep(self, name, value):
        """Keeps a value in Python after a method changed it on the page."""
        self._values[camel_case(name)] = value

    def _state_changed(self):
        """Called after the page sent a new state (RadioButton unchecks the others of its group)."""
