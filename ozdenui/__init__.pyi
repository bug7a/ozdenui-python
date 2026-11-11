# Bismillah
"""__init__.pyi - ozdenui v0.1 (OzdenUI: basic.js for Python)
The stubs of the package for an editor: the names every class takes, so they are offered and a misspelled one is marked.
Made by make_stubs.py from the classes and the kit copy in web/: do not change it by hand.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

from typing import Any, Callable, TypeVar

_T = TypeVar("_T")

__version__: str
__all__ = ["App", "WindowClosed", "every", "after", "call_soon", "run_in_background", "open_file", "save_file", "choose_folder", "Box", "VGroup", "HGroup", "GridGroup", "ScrollArea", "Label", "Button", "Input", "Icon", "Component", "SmartButton", "CheckBox", "Toggle", "RadioButton", "SelectBox", "TextAreaField", "SliderField", "ProgressBar", "ItemList", "SmartTable", "Tabs", "Dialog", "Toast", "LogView", "ImageView", "MenuBar", "ToolBar", "StatusBar", "Splitter", "CodeEditor", "picture_address", "TextField", "EmailField", "PasswordField", "NumberField", "UrlField", "PhoneField", "CurrencyField", "Slider", "SearchInput", "GraphBox", "TreeView", "ContextMenu", "Tooltip", "DatePicker", "TimePicker", "ColorPicker", "Stepper", "FilePicker", "Accordion", "MarkdownView", "JsonView", "RangeSlider", "StepBar", "Canvas", "SidePanel", "LoadingScreen", "TagInput", "DataTable", "JsonEditor", "SortableList", "WebView", "ChatView"]


class _BasicObject:
    """The common part of every object: create, set, on, measure, remove, and "with" for a container."""
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def set(self, **props) -> Any: ...
    def measure(self, name) -> Any: ...
    def call(self, method, *args) -> Any: ...
    def ask(self, method, *args) -> Any: ...
    @property
    def js(self) -> Any: ...
    def on(self, event_name, handler) -> Any: ...
    def __enter__(self: _T) -> _T: ...
    def __exit__(self, *error: Any) -> bool: ...
    def remove(self) -> Any: ...


class _Page(_BasicObject):
    """The page of basic.js: it already exists, so it is not created. page.color = "#F4F5F7"
    page.on("resize", fn) and page.on("keydown", fn) listen to the window; page.width / page.height are current.
    """
    @property
    def app(self) -> App: ...
    def remove(self) -> Any: ...


class App:
    """A window with a basic.js page. App(start, title="Counter", size=(400, 300)).run()
    theme: "light" (default), "dark" or "auto" (what the system asks). In a dark window every component takes its dark
    look unless it is given another one, and the plain objects and the page are dark too. app.theme: "light" or "dark".
    app.set_theme("dark") draws the window again in another theme: the page is made again and start() runs again.
    style: "" (default: the usual looks) or "minimal": small and made of lines (minimal / minimalDark, by the theme), for
    the components that have it; the others keep their usual look. app.style.
    accent: a color of the minimal look ("#2A78D6"): an on toggle, a checked box, the selected tab and the main button
    (SmartButton(tone="accent")) take it; the lines and the texts stay as they are. accent_dark: its color in a dark
    window ("": the same color made lighter until it reads on the dark ground). app.accent, app.accent_dark.
    """
    style: Any
    accent: Any
    accent_dark: Any
    theme: Any
    page: Any
    basic_version: Any
    timings: Any
    started_at: Any
    def __init__(self, start: Callable[[_Page], Any], title=..., size=..., components=..., debug=..., theme=..., style=..., accent=..., accent_dark=...) -> None: ...
    def run(self) -> Any: ...
    def close(self) -> Any: ...
    def set_title(self, title) -> Any: ...
    def set_theme(self, theme) -> Any: ...
    def call_soon(self, task) -> Any: ...
    def every(self, milliseconds, task) -> Any: ...
    def after(self, milliseconds, task) -> Any: ...
    def run_in_background(self, job, *args) -> Any: ...
    def flush(self) -> Any: ...
    def evaluate(self, script) -> Any: ...
    def open_file(self, file_types=..., directory=..., multiple=...) -> Any: ...
    def save_file(self, file_name=..., file_types=..., directory=...) -> Any: ...
    def choose_folder(self, directory=...) -> Any: ...


class WindowClosed(Exception):
    """The window was closed while the code waited for an answer (a dialog)."""


class Box(_BasicObject):
    def __init__(
        self,
        *left_top_width_height: float | str,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        html: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        on_click: Any = ...,
        on_dblclick: Any = ...,
        on_mouse_enter: Any = ...,
        on_mouse_leave: Any = ...,
        on_mouse_down: Any = ...,
        on_mouse_up: Any = ...,
        on_mouse_move: Any = ...,
        on_key_down: Any = ...,
        on_key_up: Any = ...,
        on_input: Any = ...,
        on_change: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_wheel: Any = ...,
        on_context_menu: Any = ...,
        fill: Any = ...,
    ) -> None: ...


class _Group(Box):
    """The common part of VGroup and HGroup. Unlike in basic.js, a group does not cut what goes out of it: clip_content=True
    cuts. A group that scrolls (scroll_y=True at its start) cuts, as in basic.js.
    """


class VGroup(_Group):
    """Objects one under the other (flexbox). A group is 100% x 100% by default; hug=True wraps its content."""
    def __init__(
        self,
        *left_top_width_height: float | str,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        flow: Any = ...,
        align: Any = ...,
        gap: Any = ...,
        padding: Any = ...,
        wrap: Any = ...,
        justify: Any = ...,
        hug: Any = ...,
        fit: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        html: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        on_click: Any = ...,
        on_dblclick: Any = ...,
        on_mouse_enter: Any = ...,
        on_mouse_leave: Any = ...,
        on_mouse_down: Any = ...,
        on_mouse_up: Any = ...,
        on_mouse_move: Any = ...,
        on_key_down: Any = ...,
        on_key_up: Any = ...,
        on_input: Any = ...,
        on_change: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_wheel: Any = ...,
        on_context_menu: Any = ...,
        fill: Any = ...,
    ) -> None: ...


class HGroup(_Group):
    """Objects side by side (flexbox)."""
    def __init__(
        self,
        *left_top_width_height: float | str,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        flow: Any = ...,
        align: Any = ...,
        gap: Any = ...,
        padding: Any = ...,
        wrap: Any = ...,
        justify: Any = ...,
        hug: Any = ...,
        fit: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        html: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        on_click: Any = ...,
        on_dblclick: Any = ...,
        on_mouse_enter: Any = ...,
        on_mouse_leave: Any = ...,
        on_mouse_down: Any = ...,
        on_mouse_up: Any = ...,
        on_mouse_move: Any = ...,
        on_key_down: Any = ...,
        on_key_up: Any = ...,
        on_input: Any = ...,
        on_change: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_wheel: Any = ...,
        on_context_menu: Any = ...,
        fill: Any = ...,
    ) -> None: ...


class GridGroup(HGroup):
    """Objects in columns and rows: with GridGroup(columns=3, gap=8): ... They go into the cells in order, left to right.
    columns: 3 (equal columns), [120, "1fr", "auto"] (px, a part of the room, the width of its content) or a CSS text.
    rows: none (as many as the objects need, each as high as its content), or as columns: with a height, rows=4 fills it.
    gap: 8 or [column gap, row gap]. align: where each object stands in its cell ("left center"); none: it fills the cell.
    An object with a width of its own keeps it: width="100%" fills the cell. Unlike the other groups it is as high as its rows.
    grid.place(obj, column_span=2) and grid.place(obj, column=1, row=0, align="right") give an object a cell of its own (from 0).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        width: Any = ...,
        height: Any = ...,
        columns: Any = ...,
        rows: Any = ...,
        gap: Any = ...,
        align: Any = ...,
        clip_content: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        key: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        style_name: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        on_click: Any = ...,
        on_dblclick: Any = ...,
        on_mouse_enter: Any = ...,
        on_mouse_leave: Any = ...,
        on_mouse_down: Any = ...,
        on_mouse_up: Any = ...,
        on_mouse_move: Any = ...,
        on_key_down: Any = ...,
        on_key_up: Any = ...,
        on_input: Any = ...,
        on_change: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_wheel: Any = ...,
        on_context_menu: Any = ...,
        fill: Any = ...,
    ) -> None: ...
    def set(self, **props) -> Any: ...
    def place(self, obj, column=..., row=..., column_span=..., row_span=..., align=...) -> Any: ...


class Component(_BasicObject):
    """A component of basic.js (comp/): its params as keywords, a function for a callback param.
    Component("TreeView", width=300, on_select=fn) uses one without a Python class of its own.
    framed=False: no border and no rounded corners on its box (a component that fills the room between two bars); it is
    style={"box": {"border": 0, "round": 0}}, and a key of your own style wins.
    """
    def __init__(self, type_name: str, *left_top_width_height: float | str, **params: Any) -> None: ...
    def set(self, **props) -> Any: ...
    def part(self, *path) -> Any: ...


class _TypedComponent(Component):
    """The base of the components with a Python class: CheckBox(text="...")"""
    def set(self, **props) -> Any: ...


class ScrollArea(_TypedComponent):
    """A box that scrolls what is in it (comp/scroll-area.js): with ScrollArea(gap=12, padding=20): Label(...)
    The objects of its "with" block go one under the other into its content (align, gap, padding, as in a VGroup) and
    scroll when they are taller than the area. As an object of the page it is the whole window; in a group it takes the
    room the other objects leave (a VGroup with a MenuBar over it and a StatusBar under it: the height between them). A
    size of its own wins (height=300). scroll_x=True: to the side too. color, border, round: its look. The scroll bar
    of the kit: style_name "light" (default), "dark", "minimal", "minimalDark".
    area.scroll_to_top(), scroll_to_end(), scroll_to_object(obj), area.scroll_top (a question to the page),
    set_scroll_top(px), on_scroll(area). Objects added later: with area: ... (they go under the others).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        align: Any = ...,
        gap: Any = ...,
        padding: Any = ...,
        scroll_y: Any = ...,
        scroll_x: Any = ...,
        use_scroll_bar: Any = ...,
        on_scroll: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    align: Any
    gap: Any
    padding: Any
    scroll_x: Any
    scroll_y: Any
    def __enter__(self: _T) -> _T: ...
    def __exit__(self, *error: Any) -> bool: ...
    def set_align(self, value) -> Any: ...
    def set_gap(self, value) -> Any: ...
    def set_padding(self, value) -> Any: ...
    def set_scroll_x(self, value) -> Any: ...
    def set_scroll_y(self, value) -> Any: ...
    def scroll_to_top(self) -> Any: ...
    def scroll_to_end(self) -> Any: ...
    def scroll_to_object(self, obj) -> Any: ...
    @property
    def scroll_top(self) -> Any: ...
    def set_scroll_top(self, value) -> Any: ...


class Label(_BasicObject):
    """A text: Label(text="3 new"). The text is shown as it is written (a typed "<b>" stays "<b>"); html="<b>3</b> new"
    for HTML. NOTE: unlike basic.js, where text is HTML.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        html: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        on_click: Any = ...,
        on_dblclick: Any = ...,
        on_mouse_enter: Any = ...,
        on_mouse_leave: Any = ...,
        on_mouse_down: Any = ...,
        on_mouse_up: Any = ...,
        on_mouse_move: Any = ...,
        on_key_down: Any = ...,
        on_key_up: Any = ...,
        on_input: Any = ...,
        on_change: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_wheel: Any = ...,
        on_context_menu: Any = ...,
        fill: Any = ...,
    ) -> None: ...


class Button(_BasicObject):
    """The plain button of basic.js. SmartButton is the modern one. text as in a Label; html= for HTML."""
    def __init__(
        self,
        *left_top_width_height: float | str,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        html: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        on_click: Any = ...,
        on_dblclick: Any = ...,
        on_mouse_enter: Any = ...,
        on_mouse_leave: Any = ...,
        on_mouse_down: Any = ...,
        on_mouse_up: Any = ...,
        on_mouse_move: Any = ...,
        on_key_down: Any = ...,
        on_key_up: Any = ...,
        on_input: Any = ...,
        on_change: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_wheel: Any = ...,
        on_context_menu: Any = ...,
        fill: Any = ...,
    ) -> None: ...


class Input(_BasicObject):
    """A text box: Input(placeholder="A name", on_enter=fn). inp.text is always the text on the page (the page sends it
    at every change). on_enter(inp) runs on Enter; the other events of the page work as on every object (on_input...).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        on_enter: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        html: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        on_click: Any = ...,
        on_dblclick: Any = ...,
        on_mouse_enter: Any = ...,
        on_mouse_leave: Any = ...,
        on_mouse_down: Any = ...,
        on_mouse_up: Any = ...,
        on_mouse_move: Any = ...,
        on_key_down: Any = ...,
        on_key_up: Any = ...,
        on_input: Any = ...,
        on_change: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_wheel: Any = ...,
        on_context_menu: Any = ...,
        fill: Any = ...,
    ) -> None: ...
    def set(self, **props) -> Any: ...


class Icon(_BasicObject):
    """A picture: Icon(0, 0, 48, 48, picture="photo.png"). picture: a path, bytes, a Pillow image, a matplotlib figure
    or an address (see picture_address). icon.picture = "other.png" changes it. ImageView is the one with a zoom.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        picture: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        html: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        on_click: Any = ...,
        on_dblclick: Any = ...,
        on_mouse_enter: Any = ...,
        on_mouse_leave: Any = ...,
        on_mouse_down: Any = ...,
        on_mouse_up: Any = ...,
        on_mouse_move: Any = ...,
        on_key_down: Any = ...,
        on_key_up: Any = ...,
        on_input: Any = ...,
        on_change: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_wheel: Any = ...,
        on_context_menu: Any = ...,
        fill: Any = ...,
    ) -> None: ...
    def set(self, **props) -> Any: ...


class SmartButton(_TypedComponent):
    """A button: SmartButton(text="Save", tone="cyan", on_click=save). on_click(button).
    style_name: "ozden" (default), "ozden2", "ozden3", "ozden4", "pill", "outlined", "ozdenDark" ... "ozden4Dark"...
    tone: "cyan" (the main action), "orange" (a delete), "yellow", "green", "blue", "white", "ink" (the main action of
    App(style="minimal")); "cyanDark"... on a dark
    page; in a dark window (App(theme="dark")) tone="cyan" is already its dark tone.
    tone="accent": the main action of the window: the color of App(accent=...), "ink" in a minimal window without one,
    "cyan" in a usual window.
    icon: a data: address (picture_address() makes one from a file).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        text: Any = ...,
        icon: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        tone: Any = ...,
        width: Any = ...,
        height: Any = ...,
        label_text: Any = ...,
        allow_html: Any = ...,
        icon_file: Any = ...,
        icon_position: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        waiting: Any = ...,
        waiting_type: Any = ...,
        animated: Any = ...,
        ripple: Any = ...,
        ask: Any = ...,
        on_before_click: Any = ...,
        on_click: Any = ...,
        on_waiting_end: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    label_text: Any
    icon: Any
    icon_file: Any
    enabled: Any
    waiting: Any
    tone: Any
    animated: Any
    ripple: Any
    ask: Any
    style: Any
    def set_tone(self, tone) -> Any: ...
    def set_text(self, text) -> Any: ...
    def set_icon(self, file) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    def set_waiting(self, waiting) -> Any: ...
    def press(self) -> Any: ...


class CheckBox(_TypedComponent):
    """CheckBox(text="Remember me", checked=True, on_change=fn). on_change(box): read box.checked.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        text: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        checked: Any = ...,
        enabled: Any = ...,
        label_text: Any = ...,
        allow_html: Any = ...,
        label_position: Any = ...,
        wrap_label: Any = ...,
        animated: Any = ...,
        on_change: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    label_text: Any
    enabled: Any
    animated: Any
    @property
    def checked(self) -> Any: ...
    def set_checked(self, checked) -> Any: ...
    def set_text(self, text) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...


class Toggle(_TypedComponent):
    """An on / off switch: Toggle(value=True, on_change=fn). on_change(toggle): read toggle.value.
    toggle.value = True in code does not call on_change, as in every component (the silent setValue(value, 1) of the kit).
    style_name: "modern" (default), "classic", "float", "round", "slim", "outline", "square", "tick", "badge", "label".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        spacing: Any = ...,
        value: Any = ...,
        invert_color: Any = ...,
        off_button_scale: Any = ...,
        on_mark: Any = ...,
        off_mark: Any = ...,
        mark_place: Any = ...,
        animated: Any = ...,
        focus_ring_color: Any = ...,
        mark_style: Any = ...,
        on_change: Any = ...,
        background_style: Any = ...,
        button_style: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    animated: Any
    @property
    def value(self) -> Any: ...
    def set_value(self, value) -> Any: ...


class RadioButton(_TypedComponent):
    """One choice of a group: RadioButton(group="size", value="M", text="Medium", on_change=fn).
    on_change(radio) runs when it becomes checked. RadioButton.value_of("size") is the value of the checked one.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern". NOTE: the group names are shared by the whole page.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        text: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        group: Any = ...,
        value: Any = ...,
        checked: Any = ...,
        enabled: Any = ...,
        label_text: Any = ...,
        allow_html: Any = ...,
        label_position: Any = ...,
        on_change: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    label_text: Any
    enabled: Any
    @property
    def checked(self) -> Any: ...
    def set_checked(self, checked) -> Any: ...
    def set_text(self, text) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    @staticmethod
    def value_of(group) -> Any: ...


class SelectBox(_TypedComponent):
    """A drop-down list: SelectBox(options=["Apple", "Pear"], value="Pear", on_change=fn).
    An option is a text or {"value", "label", "description", "icon_file"...}. on_change(box): read box.value
    (a list with multiple=True). style_name: "light" (default; its old name "classic"), "dark" (a dark page), "ozden", "ozdenDark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        options: Any = ...,
        value: Any = ...,
        multiple: Any = ...,
        searchable: Any = ...,
        auto_search_count: Any = ...,
        clearable: Any = ...,
        close_on_select: Any = ...,
        show_select_all: Any = ...,
        placeholder: Any = ...,
        search_placeholder: Any = ...,
        empty_text: Any = ...,
        select_all_text: Any = ...,
        clear_text: Any = ...,
        more_text: Any = ...,
        field_label_count: Any = ...,
        panel_min_width: Any = ...,
        panel_max_height: Any = ...,
        max_render_count: Any = ...,
        enabled: Any = ...,
        use_scroll_bar: Any = ...,
        use_search_input: Any = ...,
        full_height_list: Any = ...,
        scale: Any = ...,
        aria_label: Any = ...,
        create_item_view: Any = ...,
        create_value_view: Any = ...,
        on_change: Any = ...,
        on_open: Any = ...,
        on_close: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    options: Any
    enabled: Any
    placeholder: Any
    full_height_list: Any
    def set_value(self, value) -> Any: ...
    def set_options(self, options) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    def set_placeholder(self, text) -> Any: ...
    def open(self) -> Any: ...
    def close(self) -> Any: ...


class _Field(_TypedComponent):
    """The common part of the fields with a title: field.text is the text on the page (field.value too, the name of the
    kit). on_change(field) runs at every change of the user, on_focus(field) and on_blur(field) when the cursor comes and
    goes.
    """
    text: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    @property
    def value(self) -> Any: ...
    def set_text(self, text) -> Any: ...
    def set_title(self, text) -> Any: ...
    def set_placeholder(self, text) -> Any: ...
    def set_max_length(self, count) -> Any: ...
    def set_required(self, value) -> Any: ...
    def set_warning_text(self, text) -> Any: ...
    def is_valid(self) -> Any: ...
    def check(self) -> Any: ...


class TextAreaField(_Field):
    """A text of more lines: TextAreaField(text="...", on_change=fn). area.text is the text on the page.
    on_change(area) runs at every change. title_text: a small title above it.
    style_name: as TextField.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        text: Any = ...,
        type: Any = ...,
        title_text: Any = ...,
        placeholder: Any = ...,
        required: Any = ...,
        min_char_count: Any = ...,
        show_count: Any = ...,
        length_text: Any = ...,
        warning_text: Any = ...,
        warning_color: Any = ...,
        max_length: Any = ...,
        height: Any = ...,
        right_padding: Any = ...,
        unit_style: Any = ...,
        scroll_bar_style: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        width: Any = ...,
        left_padding: Any = ...,
        title_font_size: Any = ...,
        input_font_size: Any = ...,
        input_height: Any = ...,
        field_padding: Any = ...,
        description_font_size: Any = ...,
        title_position: Any = ...,
        title_gap: Any = ...,
        value: Any = ...,
        show_description: Any = ...,
        description_text: Any = ...,
        allow_html: Any = ...,
        background_color: Any = ...,
        focus_background_color: Any = ...,
        hover_background_color: Any = ...,
        line_color: Any = ...,
        focus_line_color: Any = ...,
        back_border_color: Any = ...,
        focus_back_border_color: Any = ...,
        hover_back_border_color: Any = ...,
        back_border_top_round: Any = ...,
        back_border_bottom_round: Any = ...,
        title_text_color: Any = ...,
        title_bold: Any = ...,
        title_letter_spacing: Any = ...,
        input_text_color: Any = ...,
        input_color_scheme: Any = ...,
        placeholder_color: Any = ...,
        description_text_color: Any = ...,
        warning_ball_border_color: Any = ...,
        required_text: Any = ...,
        required_color: Any = ...,
        animated_warning_ball: Any = ...,
        warning_ball_type: Any = ...,
        warning_ball_size: Any = ...,
        warning_ball_border: Any = ...,
        warning_border_color: Any = ...,
        warning_icon_size: Any = ...,
        required_icon_file: Any = ...,
        warning_icon_file: Any = ...,
        required_icon_color: Any = ...,
        tooltip_style: Any = ...,
        select_style: Any = ...,
        show_left_box: Any = ...,
        show_right_box: Any = ...,
        show_unit: Any = ...,
        create_input: Any = ...,
        unit_text: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_change: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    value: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    warning_color: Any
    description_text: Any
    background_color: Any
    focus_background_color: Any
    line_color: Any
    focus_line_color: Any
    required_text: Any
    unit_text: Any


class SliderField(_TypedComponent):
    """A number on a bar: SliderField(text="Size", value=3, min_value=0, max_value=10, step=1, on_change=fn).
    on_change(slider) runs while it is dragged, on_change_end(slider) when it is let go: read slider.value.
    set_range(min_value, max_value) changes both ends. style_name: "light" (default; its old name "classic"), "dark" (a
    dark page), "modern".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        text: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        label_text: Any = ...,
        value: Any = ...,
        min_value: Any = ...,
        max_value: Any = ...,
        step: Any = ...,
        precision: Any = ...,
        unit_text: Any = ...,
        editable: Any = ...,
        show_ticks: Any = ...,
        max_ticks: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        value_format: Any = ...,
        on_change: Any = ...,
        on_change_end: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    text: Any
    label_text: Any
    enabled: Any
    min_value: Any
    max_value: Any
    step: Any
    precision: Any
    unit_text: Any
    show_ticks: Any
    def set_value(self, value) -> Any: ...
    def set_range(self, min_value, max_value) -> Any: ...
    def set_min_value(self, value) -> Any: ...
    def set_max_value(self, value) -> Any: ...
    def set_step(self, value) -> Any: ...
    def set_text(self, text) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...


class ProgressBar(_TypedComponent):
    """The progress of a job: bar = ProgressBar(title_text="Copying", max_value=100); bar.value = 40.
    It may be changed from a background job (run_in_background). status: "normal", "success", "error".
    on_complete(bar) runs once when the value reaches max_value. style_name: "light" (default), "dark" (a dark page),
    "ozden", "modern"; style={"bar": {"color": "..."}} changes the color of the bar.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        value: Any = ...,
        second_value: Any = ...,
        max_value: Any = ...,
        stripes: Any = ...,
        second_stripes: Any = ...,
        limits: Any = ...,
        dark_track: Any = ...,
        indeterminate: Any = ...,
        status: Any = ...,
        title_text: Any = ...,
        allow_html: Any = ...,
        value_position: Any = ...,
        value_format: Any = ...,
        on_change: Any = ...,
        on_complete: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    title_text: Any
    status: Any
    indeterminate: Any
    max_value: Any
    second_value: Any
    stripes: Any
    second_stripes: Any
    limits: Any
    dark_track: Any
    def set_value(self, value) -> Any: ...
    def add_value(self, step=...) -> Any: ...
    def set_title(self, text) -> Any: ...
    def set_status(self, status) -> Any: ...
    def set_indeterminate(self, indeterminate) -> Any: ...
    def set_max_value(self, value) -> Any: ...


class ItemList(_TypedComponent):
    """A list to choose from: ItemList(items=["Apple", {"key": "p", "text": "Pear", "description": "Green"}], on_change=fn).
    An item: a text or {"key", "text", "description", "icon_file", "search_text", "enabled"}; enabled=False: it can not be
    chosen. Every item gets a key: a text "Apple" becomes {"key": "0", "text": "Apple"} (its index), as the page names it.
    selection: "single" (default), "multiple", "none". on_change(lst, selected_items);
    on_item_click(lst, item, index). lst.items, lst.selected_keys and lst.selected are kept in Python.
    style_name: "ozden" (default, a gray list), "ozdenDark" (a dark page), "light" (a white box, flat rows), "dark".
    Another ground: style={"box": {"color": "white"}}.
    Pictures: ItemList(layout="grid", style_name="gallery" (a dark window takes "galleryDark"), items=[{"text": "Sea",
    "icon_file": "sea.jpg"}]): a big photo on every tile. icon_file takes a path, bytes, a Pillow image or an address.
    An item with no text and a key the list does not know ("title") is told in the terminal.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        items: Any = ...,
        layout: Any = ...,
        selection: Any = ...,
        selected_keys: Any = ...,
        scroll_to_selected: Any = ...,
        create_item_view: Any = ...,
        create_section_view: Any = ...,
        animated: Any = ...,
        show_search: Any = ...,
        search_params: Any = ...,
        empty_text: Any = ...,
        no_result_text: Any = ...,
        enabled: Any = ...,
        use_scroll_bar: Any = ...,
        aria_label: Any = ...,
        on_item_click: Any = ...,
        on_change: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    items: Any
    selected_keys: Any
    enabled: Any
    selected: Any
    layout: Any
    selection: Any
    animated: Any
    def set_items(self, items) -> Any: ...
    def add_item(self, item, index=...) -> Any: ...
    def remove_item(self, key) -> Any: ...
    def set_selected(self, keys) -> Any: ...
    def select(self, key) -> Any: ...
    def clear_selection(self) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    def scroll_to_item(self, key) -> Any: ...


class SmartTable(_TypedComponent):
    """A table for data of any size: only the rows that are seen are made, so very many rows stay fast. It has a filter
    box, sorting on its titles and the keys of a list (arrows, Page Up / Down, Home, End, Enter).

    SmartTable(columns=[{"key": "name", "title": "Name", "width": 200}], rows=[{"name": "Ada"}], height=300)
    A column: key, title (the key by default), width (px), type ("string", "integer", "boolean"), sortable (True).
    A row: a dict by the keys of the columns, or a list in the order of the columns. The values are shown as text:
    format them in Python. on_select(table, row): a click, or Enter on a row (row: the dict). table.rows is kept in
    Python; table.selected_row asks the page which row is selected now (the arrow keys move it without an event).
    height: a number or "100%": the rows fill it; none: as high as line_count rows. width: "100%" by default.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page), "green".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        columns: Any = ...,
        rows: Any = ...,
        on_select: Any = ...,
        line_count: Any = ...,
        key: Any = ...,
        title_height: Any = ...,
        item_height: Any = ...,
        info_height: Any = ...,
        item_line_count: Any = ...,
        highlight_title: Any = ...,
        highlight_line: Any = ...,
        invert_color: Any = ...,
        no_data_found_alert: Any = ...,
        search_keyword: Any = ...,
        search_title_index: Any = ...,
        show_search_title_select: Any = ...,
        wheel_scroll: Any = ...,
        allow_html: Any = ...,
        show_cell_tooltip: Any = ...,
        all_titles_text: Any = ...,
        can_select: Any = ...,
        fit_line_count: Any = ...,
        locale: Any = ...,
        sort_by_title_index: Any = ...,
        sort_direction: Any = ...,
        fill_test_data: Any = ...,
        create_cell_view: Any = ...,
        update_cell_view: Any = ...,
        title_data_list: Any = ...,
        item_data_list: Any = ...,
        scroll_bar_params: Any = ...,
        search_title_menu_params: Any = ...,
        search_input_params: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        height: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    rows: Any
    item_data_list: Any
    item_height: Any
    item_line_count: Any
    search_title_index: Any
    show_search_title_select: Any
    wheel_scroll: Any
    show_cell_tooltip: Any
    can_select: Any
    fit_line_count: Any
    locale: Any
    title_data_list: Any
    @property
    def selected_row(self) -> Any: ...
    def set_rows(self, rows) -> Any: ...
    def add_row(self, row) -> Any: ...
    def remove_row(self, row) -> Any: ...
    def clear_rows(self) -> Any: ...
    def select_row(self, index) -> Any: ...
    def clear_selection(self) -> Any: ...
    def sort_by(self, key, direction=...) -> Any: ...
    def search(self, text) -> Any: ...


class Tabs(_TypedComponent):
    """Pages in one window: tabs = Tabs(tabs=["Orders", "Customers"]); with tabs.panel("Orders"): Label(...)
    A tab is a text or {"key", "text", "icon_file", "count", "badge", "disabled"}. on_change(tabs): read
    tabs.value (the key of the open tab). panels=False makes only the bar. variant: "underline" or "pill".
    set_tabs([...]) (tabs.tabs = [...]): new tabs; their pages are made again. set_count(key, 3): the number of a tab.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        tabs: Any = ...,
        value: Any = ...,
        variant: Any = ...,
        vertical: Any = ...,
        full_width: Any = ...,
        closable: Any = ...,
        add_button: Any = ...,
        show_arrows: Any = ...,
        panels: Any = ...,
        panel_height: Any = ...,
        bar_width: Any = ...,
        scale: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        on_change: Any = ...,
        on_close: Any = ...,
        on_add: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    tabs: Any
    previous_value: Any
    enabled: Any
    def panel(self, key) -> Any: ...
    def set_value(self, key) -> Any: ...
    def set_tabs(self, tabs) -> Any: ...
    def set_count(self, key, count) -> Any: ...


class Dialog:
    """The dialogs of comp/dialog.js. Each one waits for its answer and returns it; the window keeps working
    meanwhile (other events and timers run). They work from a background job too.
    """
    @staticmethod
    def alert(message, title=..., button_text=...) -> Any: ...
    @staticmethod
    def confirm(message, title=..., confirm_text=..., cancel_text=..., danger=...) -> Any: ...
    @staticmethod
    def prompt(message=..., title=..., value=..., placeholder=..., field_text=..., required=..., confirm_text=..., cancel_text=...) -> Any: ...
    @staticmethod
    def ask(message, title=..., buttons=...) -> Any: ...


class Toast:
    """A short message in a corner: Toast.success("Saved"), Toast.error("Could not save", title="Error").
    type: "success", "error", "warning", "info". duration: milliseconds (0: it stays until closed).
    Its theme is the theme of the window (App(style="minimal"): "minimal" / "minimalDark"); Toast.THEME = "dark" chooses
    one for every toast.
    """
    THEME: Any
    @staticmethod
    def show(message, type=..., title=..., duration=...) -> Any: ...
    @staticmethod
    def success(message, title=..., duration=...) -> Any: ...
    @staticmethod
    def error(message, title=..., duration=...) -> Any: ...
    @staticmethod
    def warning(message, title=..., duration=...) -> Any: ...
    @staticmethod
    def info(message, title=..., duration=...) -> Any: ...


class _ThemedComponent(_TypedComponent):
    """The components that change their look while they are on the page: comp.theme = "dark" or comp.set_theme("dark").
    What they show stays.
    """
    theme: Any
    style_name: Any
    def set_theme(self, name) -> Any: ...


class LogView(_ThemedComponent):
    """The output of a program: colored lines that follow the last line. log = LogView(height=300); log.info("Reading")
    add_line(text, level), info(), success(), warn(), error(), debug(), clear(). A scroll up stops the following; a small
    button goes back to the end. The texts are never HTML. lines=[...]: the first lines; max_lines=1000: the oldest go.
    capture_print() sends print() into it, logging_handler() the logging module. style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        lines: Any = ...,
        max_lines: Any = ...,
        auto_scroll: Any = ...,
        show_time: Any = ...,
        show_level: Any = ...,
        wrap_lines: Any = ...,
        empty_text: Any = ...,
        new_lines_text: Any = ...,
        level_texts: Any = ...,
        aria_label: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    auto_scroll: Any
    show_time: Any
    show_level: Any
    wrap_lines: Any
    max_lines: Any
    def add_line(self, text, level=...) -> Any: ...
    def info(self, text) -> Any: ...
    def success(self, text) -> Any: ...
    def warn(self, text) -> Any: ...
    def error(self, text) -> Any: ...
    def debug(self, text) -> Any: ...
    def clear(self) -> Any: ...
    def get_text(self) -> Any: ...
    def scroll_to_end(self) -> Any: ...
    def set_levels(self, levels) -> Any: ...
    def set_auto_scroll(self, value) -> Any: ...
    def set_show_time(self, value) -> Any: ...
    def set_show_level(self, value) -> Any: ...
    def set_wrap_lines(self, value) -> Any: ...
    def set_max_lines(self, count) -> Any: ...
    def capture_print(self, errors=..., terminal=...) -> Any: ...
    def logging_handler(self, level=...) -> Any: ...


class ImageView(_ThemedComponent):
    """A place to look at a picture or a plot: the wheel and two fingers zoom, a drag moves it, a small toolbar.
    view = ImageView(height=400, image="photo.png"); view.set_image(figure)
    A picture: a path, bytes, a Pillow image, a matplotlib figure, or an address (see picture_address()). A new picture
    of the same size keeps the zoom and the place and does not blink: a program can keep drawing its plot.
    view.zoom_level, view.natural_width, view.natural_height are kept in Python. on_load(view), on_error(view),
    on_zoom_change(view). enlarge_to_fit=True: a small picture grows to the box. style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        image: Any = ...,
        alt: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        image_file: Any = ...,
        alt_text: Any = ...,
        min_zoom: Any = ...,
        max_zoom: Any = ...,
        zoom_step: Any = ...,
        enlarge_to_fit: Any = ...,
        wheel_zoom: Any = ...,
        pixelated_zoom: Any = ...,
        show_toolbar: Any = ...,
        empty_text: Any = ...,
        error_text: Any = ...,
        aria_label: Any = ...,
        button_texts: Any = ...,
        on_load: Any = ...,
        on_error: Any = ...,
        on_zoom_change: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    image: Any
    image_file: Any
    show_toolbar: Any
    zoom_level: Any
    natural_width: Any
    natural_height: Any
    def set_image(self, picture, alt_text=...) -> Any: ...
    def clear_image(self) -> Any: ...
    def zoom_in(self) -> Any: ...
    def zoom_out(self) -> Any: ...
    def zoom_to_fit(self) -> Any: ...
    def zoom_to_actual_size(self) -> Any: ...
    def set_zoom_level(self, zoom) -> Any: ...
    def set_show_toolbar(self, value) -> Any: ...


class MenuBar(_ThemedComponent):
    """The row of menus of a window, in the page (not the menu of the system):
    MenuBar(menus=[{"text": "File", "items": [{"text": "Save", "key": "save", "shortcut": "Ctrl+S", "on_click": save}, "-"]}])
    An item: text, key, shortcut, checked, enabled, items (a submenu), on_click: fn(bar, item, menu) (fn() too), or a
    text; "-" is a line. Ctrl is also Cmd on a Mac, and a shortcut runs its item. on_click=fn of the bar: every item.
    set_item_checked(key, True), set_item_enabled(key, False). style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        menus: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        on_click: Any = ...,
        on_menu_open: Any = ...,
        on_menu_close: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    menus: Any
    enabled: Any
    def set_menus(self, menus) -> Any: ...
    def set_item_checked(self, key, value) -> Any: ...
    def set_item_enabled(self, key, value) -> Any: ...
    def set_enabled(self, value) -> Any: ...
    def close_menu(self) -> Any: ...


class ToolBar(_ThemedComponent):
    """The row of small buttons of a window, under its menus:
    ToolBar(items=[{"key": "save", "icon": "save", "hint": "Save", "shortcut": "Ctrl+S", "on_click": save}, "-",
                   {"key": "bold", "icon": "bold", "hint": "Bold", "toggle": True}, " ", {"key": "run", "text": "Run"}])
    An item: key, text, icon (a name of ToolBar.ICONS or an SVG text), icon_file, hint, shortcut, toggle=True (it stays
    pressed), group="align" (one of the group stays pressed), checked, enabled, items (it opens a menu, as in MenuBar),
    on_click: fn(bar, item) (fn() too), or a text. "-" is a line; " ": the next ones stand at the right end. What does not
    fit goes into a "..." menu. on_click=fn of the bar: every item. Ctrl is also Cmd on a Mac; a key that is also in a
    MenuBar runs once. bar.checked_keys, is_checked(key), set_item_checked(key, True), set_item_enabled(key, False),
    set_item_text(key, text), set_item_hint(key, text), click_item(key). style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        shrink: Any = ...,
        items: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        more_text: Any = ...,
        on_click: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    items: Any
    enabled: Any
    ICONS: Any
    @property
    def checked_keys(self) -> Any: ...
    def is_checked(self, key) -> Any: ...
    def set_items(self, items) -> Any: ...
    def set_item_checked(self, key, value) -> Any: ...
    def set_item_enabled(self, key, value) -> Any: ...
    def set_item_text(self, key, text) -> Any: ...
    def set_item_hint(self, key, text) -> Any: ...
    def click_item(self, key) -> Any: ...
    def set_enabled(self, value) -> Any: ...
    def close_menu(self) -> Any: ...


class StatusBar(_ThemedComponent):
    """The thin bar at the bottom of a window: bar = StatusBar(message="Ready", items=["3 files", "UTF-8"])
    bar.set_message("Saved", "success", 3000): a tone ("success", "warn", "error", "info") and a time (ms), after which
    the lasting message comes back. bar.set_busy(True): a turning circle. A part: a text, or {"key", "text", "tone",
    "on_click": fn(bar, part)}. It stands at the bottom of a Box by itself; in a VGroup it takes its place.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        message: Any = ...,
        tone: Any = ...,
        key: Any = ...,
        left: Any = ...,
        width: Any = ...,
        height: Any = ...,
        message_text: Any = ...,
        message_tone: Any = ...,
        items: Any = ...,
        busy: Any = ...,
        aria_label: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    busy: Any
    items: Any
    message: Any
    message_text: Any
    def set_message(self, text, tone=..., time=...) -> Any: ...
    def set_busy(self, value) -> Any: ...
    def set_items(self, items) -> Any: ...
    def set_item_text(self, key, text) -> Any: ...
    def set_item_visible(self, key, value) -> Any: ...


class Splitter(_ThemedComponent):
    """Two areas with a line between them: a drag of the line changes their sizes.
    split = Splitter(first_size=240); with split.first: ...; with split.second: ...
    direction: "horizontal" (side by side) or "vertical". first_size or second_size: px, or a part ("30%"): a part stays
    a part when the window changes, px stay px. min_first, min_second (px). on_change_end(split): read split.first_size_now.
    set_area_visible("first", False) hides an area. Objects go one under the other in an area, as in a VGroup.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        direction: Any = ...,
        first_size: Any = ...,
        second_size: Any = ...,
        min_first: Any = ...,
        min_second: Any = ...,
        key_step: Any = ...,
        aria_label: Any = ...,
        on_change: Any = ...,
        on_change_end: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    first_size_now: Any
    first_size: Any
    @property
    def first(self) -> Any: ...
    @property
    def second(self) -> Any: ...
    def set_first_size(self, size) -> Any: ...
    def set_area_visible(self, name, value) -> Any: ...


class CodeEditor(_ThemedComponent):
    """A text editor for code: line numbers and colors: CodeEditor(value="x = 1", language="python", height=300)
    language: "python", "javascript", "json", "html", "css", "sql", "bash", "text". Tab, Shift + Tab, Enter and Ctrl + /
    edit the lines; undo takes them back. A big text stays fast (only the lines that are seen are drawn).
    editor.value asks the page for the text. editor.cursor_line, editor.cursor_column are kept in Python.
    on_change(editor), on_cursor_change(editor). change_delay (ms): on_change waits for the typing to rest.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        value: Any = ...,
        language: Any = ...,
        tab_size: Any = ...,
        read_only: Any = ...,
        show_line_numbers: Any = ...,
        placeholder: Any = ...,
        change_delay: Any = ...,
        aria_label: Any = ...,
        on_change: Any = ...,
        on_cursor_change: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    language: Any
    read_only: Any
    show_line_numbers: Any
    tab_size: Any
    cursor_line: Any
    cursor_column: Any
    @property
    def value(self) -> Any: ...
    def set_value(self, text) -> Any: ...
    def insert_text(self, text) -> Any: ...
    def get_selected_text(self) -> Any: ...
    def set_language(self, language) -> Any: ...
    def set_read_only(self, value) -> Any: ...
    def set_show_line_numbers(self, value) -> Any: ...
    def set_tab_size(self, size) -> Any: ...
    def go_to_line(self, line) -> Any: ...
    def focus(self) -> Any: ...


class TextField(_Field):
    """A text field with a title: TextField(title_text="Name", text="Ada", on_change=fn). field.text is the text on the
    page. on_change(field) runs at every change, on_enter(field) on Enter. required=True: field.check() shows the warning
    of an empty field and returns False (required_text: its text). max_length: the most letters. unit_text="kg": a unit
    at its end. description_text: a small text under it.
    style_name: "light" (default), "dark" (a dark page), "modern", "modernDark", "ozden", "ozdenDark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        on_enter: Any = ...,
        text: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        type: Any = ...,
        width: Any = ...,
        height: Any = ...,
        left_padding: Any = ...,
        right_padding: Any = ...,
        title_font_size: Any = ...,
        input_font_size: Any = ...,
        input_height: Any = ...,
        field_padding: Any = ...,
        description_font_size: Any = ...,
        title_position: Any = ...,
        title_gap: Any = ...,
        title_text: Any = ...,
        placeholder: Any = ...,
        value: Any = ...,
        max_length: Any = ...,
        show_description: Any = ...,
        description_text: Any = ...,
        allow_html: Any = ...,
        background_color: Any = ...,
        focus_background_color: Any = ...,
        hover_background_color: Any = ...,
        line_color: Any = ...,
        focus_line_color: Any = ...,
        back_border_color: Any = ...,
        focus_back_border_color: Any = ...,
        hover_back_border_color: Any = ...,
        back_border_top_round: Any = ...,
        back_border_bottom_round: Any = ...,
        title_text_color: Any = ...,
        title_bold: Any = ...,
        title_letter_spacing: Any = ...,
        input_text_color: Any = ...,
        input_color_scheme: Any = ...,
        placeholder_color: Any = ...,
        description_text_color: Any = ...,
        warning_ball_border_color: Any = ...,
        required: Any = ...,
        required_text: Any = ...,
        required_color: Any = ...,
        warning_text: Any = ...,
        warning_color: Any = ...,
        animated_warning_ball: Any = ...,
        warning_ball_type: Any = ...,
        warning_ball_size: Any = ...,
        warning_ball_border: Any = ...,
        warning_border_color: Any = ...,
        warning_icon_size: Any = ...,
        required_icon_file: Any = ...,
        warning_icon_file: Any = ...,
        required_icon_color: Any = ...,
        tooltip_style: Any = ...,
        select_style: Any = ...,
        show_left_box: Any = ...,
        show_right_box: Any = ...,
        show_unit: Any = ...,
        create_input: Any = ...,
        unit_text: Any = ...,
        unit_style: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_change: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    value: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    on_enter: Any
    description_text: Any
    background_color: Any
    focus_background_color: Any
    line_color: Any
    focus_line_color: Any
    required_text: Any
    warning_color: Any
    unit_text: Any
    def focus(self) -> Any: ...
    def select_text(self) -> Any: ...
    def set_description(self, text) -> Any: ...
    def set_unit_text(self, text) -> Any: ...


class EmailField(TextField):
    """A field for an e-mail address: EmailField(title_text="E-mail"). email.is_valid() and email.check() look at its form.
    style_name: as TextField.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        on_enter: Any = ...,
        text: Any = ...,
        required: Any = ...,
        type: Any = ...,
        title_text: Any = ...,
        placeholder: Any = ...,
        warning_text: Any = ...,
        warning_color: Any = ...,
        max_length: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        width: Any = ...,
        height: Any = ...,
        left_padding: Any = ...,
        right_padding: Any = ...,
        title_font_size: Any = ...,
        input_font_size: Any = ...,
        input_height: Any = ...,
        field_padding: Any = ...,
        description_font_size: Any = ...,
        title_position: Any = ...,
        title_gap: Any = ...,
        value: Any = ...,
        show_description: Any = ...,
        description_text: Any = ...,
        allow_html: Any = ...,
        background_color: Any = ...,
        focus_background_color: Any = ...,
        hover_background_color: Any = ...,
        line_color: Any = ...,
        focus_line_color: Any = ...,
        back_border_color: Any = ...,
        focus_back_border_color: Any = ...,
        hover_back_border_color: Any = ...,
        back_border_top_round: Any = ...,
        back_border_bottom_round: Any = ...,
        title_text_color: Any = ...,
        title_bold: Any = ...,
        title_letter_spacing: Any = ...,
        input_text_color: Any = ...,
        input_color_scheme: Any = ...,
        placeholder_color: Any = ...,
        description_text_color: Any = ...,
        warning_ball_border_color: Any = ...,
        required_text: Any = ...,
        required_color: Any = ...,
        animated_warning_ball: Any = ...,
        warning_ball_type: Any = ...,
        warning_ball_size: Any = ...,
        warning_ball_border: Any = ...,
        warning_border_color: Any = ...,
        warning_icon_size: Any = ...,
        required_icon_file: Any = ...,
        warning_icon_file: Any = ...,
        required_icon_color: Any = ...,
        tooltip_style: Any = ...,
        select_style: Any = ...,
        show_left_box: Any = ...,
        show_right_box: Any = ...,
        show_unit: Any = ...,
        create_input: Any = ...,
        unit_text: Any = ...,
        unit_style: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_change: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    value: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    on_enter: Any
    warning_color: Any
    description_text: Any
    background_color: Any
    focus_background_color: Any
    line_color: Any
    focus_line_color: Any
    required_text: Any
    unit_text: Any


class PasswordField(TextField):
    """A password with a button that shows it: PasswordField(title_text="Password"). Its rules: min_length, must_use_number,
    must_use_letter, must_use_uppercase, must_use_lowercase, must_use_special_char; field.check() shows the one that is
    not kept (min_length_warning_text: its text). style_name: as TextField.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        on_enter: Any = ...,
        text: Any = ...,
        required: Any = ...,
        required_text: Any = ...,
        type: Any = ...,
        title_text: Any = ...,
        placeholder: Any = ...,
        warning_text: Any = ...,
        warning_color: Any = ...,
        max_length: Any = ...,
        show_password: Any = ...,
        show_show_password_button: Any = ...,
        show_password_icon_file: Any = ...,
        hide_password_icon_file: Any = ...,
        eye_icon_size: Any = ...,
        show_password_hint_text: Any = ...,
        hide_password_hint_text: Any = ...,
        min_length: Any = ...,
        min_length_warning_text: Any = ...,
        must_use_number: Any = ...,
        must_use_number_warning_text: Any = ...,
        must_use_letter: Any = ...,
        must_use_letter_warning_text: Any = ...,
        must_use_uppercase: Any = ...,
        must_use_uppercase_warning_text: Any = ...,
        must_use_lowercase: Any = ...,
        must_use_lowercase_warning_text: Any = ...,
        must_use_special_char: Any = ...,
        must_use_special_char_warning_text: Any = ...,
        invert_icon_color: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        width: Any = ...,
        height: Any = ...,
        left_padding: Any = ...,
        right_padding: Any = ...,
        title_font_size: Any = ...,
        input_font_size: Any = ...,
        input_height: Any = ...,
        field_padding: Any = ...,
        description_font_size: Any = ...,
        title_position: Any = ...,
        title_gap: Any = ...,
        value: Any = ...,
        show_description: Any = ...,
        description_text: Any = ...,
        allow_html: Any = ...,
        background_color: Any = ...,
        focus_background_color: Any = ...,
        hover_background_color: Any = ...,
        line_color: Any = ...,
        focus_line_color: Any = ...,
        back_border_color: Any = ...,
        focus_back_border_color: Any = ...,
        hover_back_border_color: Any = ...,
        back_border_top_round: Any = ...,
        back_border_bottom_round: Any = ...,
        title_text_color: Any = ...,
        title_bold: Any = ...,
        title_letter_spacing: Any = ...,
        input_text_color: Any = ...,
        input_color_scheme: Any = ...,
        placeholder_color: Any = ...,
        description_text_color: Any = ...,
        warning_ball_border_color: Any = ...,
        required_color: Any = ...,
        animated_warning_ball: Any = ...,
        warning_ball_type: Any = ...,
        warning_ball_size: Any = ...,
        warning_ball_border: Any = ...,
        warning_border_color: Any = ...,
        warning_icon_size: Any = ...,
        required_icon_file: Any = ...,
        warning_icon_file: Any = ...,
        required_icon_color: Any = ...,
        tooltip_style: Any = ...,
        select_style: Any = ...,
        show_left_box: Any = ...,
        show_right_box: Any = ...,
        show_unit: Any = ...,
        create_input: Any = ...,
        unit_text: Any = ...,
        unit_style: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_change: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    value: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    on_enter: Any
    required_text: Any
    warning_color: Any
    show_password: Any
    description_text: Any
    background_color: Any
    focus_background_color: Any
    line_color: Any
    focus_line_color: Any
    unit_text: Any
    def set_show_password(self, value) -> Any: ...


class NumberField(TextField):
    """Only a number can be typed: NumberField(title_text="Count", value=3). field.value is a number, or None when the
    field is empty; field.text is what is written. allow_negative, allow_decimal (True by default), decimal_separator ("."
    or ","), max_decimal_digits (2). style_name: as TextField.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        value: Any = ...,
        on_enter: Any = ...,
        text: Any = ...,
        required: Any = ...,
        type: Any = ...,
        title_text: Any = ...,
        max_length: Any = ...,
        placeholder: Any = ...,
        allow_negative: Any = ...,
        allow_decimal: Any = ...,
        decimal_separator: Any = ...,
        max_decimal_digits: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        width: Any = ...,
        height: Any = ...,
        left_padding: Any = ...,
        right_padding: Any = ...,
        title_font_size: Any = ...,
        input_font_size: Any = ...,
        input_height: Any = ...,
        field_padding: Any = ...,
        description_font_size: Any = ...,
        title_position: Any = ...,
        title_gap: Any = ...,
        show_description: Any = ...,
        description_text: Any = ...,
        allow_html: Any = ...,
        background_color: Any = ...,
        focus_background_color: Any = ...,
        hover_background_color: Any = ...,
        line_color: Any = ...,
        focus_line_color: Any = ...,
        back_border_color: Any = ...,
        focus_back_border_color: Any = ...,
        hover_back_border_color: Any = ...,
        back_border_top_round: Any = ...,
        back_border_bottom_round: Any = ...,
        title_text_color: Any = ...,
        title_bold: Any = ...,
        title_letter_spacing: Any = ...,
        input_text_color: Any = ...,
        input_color_scheme: Any = ...,
        placeholder_color: Any = ...,
        description_text_color: Any = ...,
        warning_ball_border_color: Any = ...,
        required_text: Any = ...,
        required_color: Any = ...,
        warning_text: Any = ...,
        warning_color: Any = ...,
        animated_warning_ball: Any = ...,
        warning_ball_type: Any = ...,
        warning_ball_size: Any = ...,
        warning_ball_border: Any = ...,
        warning_border_color: Any = ...,
        warning_icon_size: Any = ...,
        required_icon_file: Any = ...,
        warning_icon_file: Any = ...,
        required_icon_color: Any = ...,
        tooltip_style: Any = ...,
        select_style: Any = ...,
        show_left_box: Any = ...,
        show_right_box: Any = ...,
        show_unit: Any = ...,
        create_input: Any = ...,
        unit_text: Any = ...,
        unit_style: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_change: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    on_enter: Any
    description_text: Any
    background_color: Any
    focus_background_color: Any
    line_color: Any
    focus_line_color: Any
    required_text: Any
    warning_color: Any
    unit_text: Any
    @property
    def value(self) -> Any: ...
    def set_value(self, value) -> Any: ...


class UrlField(TextField):
    """A web address: UrlField(title_text="Site", text="https://github.com"). The protocol is chosen at its start
    (http://, https://, http://www., https://www.); field.text is the whole address with it ("" when nothing is written).
    A text without a protocol takes the chosen one (https:// by default). on_change(field) runs at every change, also of
    the protocol. field.is_valid() and field.check() look at its form (a name with a dot, a port, a path).
    style_name: as TextField.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        on_enter: Any = ...,
        text: Any = ...,
        width: Any = ...,
        required: Any = ...,
        title_text: Any = ...,
        placeholder: Any = ...,
        warning_text: Any = ...,
        warning_color: Any = ...,
        max_length: Any = ...,
        right_padding: Any = ...,
        tiny_select_params: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        type: Any = ...,
        height: Any = ...,
        left_padding: Any = ...,
        title_font_size: Any = ...,
        input_font_size: Any = ...,
        input_height: Any = ...,
        field_padding: Any = ...,
        description_font_size: Any = ...,
        title_position: Any = ...,
        title_gap: Any = ...,
        value: Any = ...,
        show_description: Any = ...,
        description_text: Any = ...,
        allow_html: Any = ...,
        background_color: Any = ...,
        focus_background_color: Any = ...,
        hover_background_color: Any = ...,
        line_color: Any = ...,
        focus_line_color: Any = ...,
        back_border_color: Any = ...,
        focus_back_border_color: Any = ...,
        hover_back_border_color: Any = ...,
        back_border_top_round: Any = ...,
        back_border_bottom_round: Any = ...,
        title_text_color: Any = ...,
        title_bold: Any = ...,
        title_letter_spacing: Any = ...,
        input_text_color: Any = ...,
        input_color_scheme: Any = ...,
        placeholder_color: Any = ...,
        description_text_color: Any = ...,
        warning_ball_border_color: Any = ...,
        required_text: Any = ...,
        required_color: Any = ...,
        animated_warning_ball: Any = ...,
        warning_ball_type: Any = ...,
        warning_ball_size: Any = ...,
        warning_ball_border: Any = ...,
        warning_border_color: Any = ...,
        warning_icon_size: Any = ...,
        required_icon_file: Any = ...,
        warning_icon_file: Any = ...,
        required_icon_color: Any = ...,
        tooltip_style: Any = ...,
        select_style: Any = ...,
        show_left_box: Any = ...,
        show_right_box: Any = ...,
        show_unit: Any = ...,
        create_input: Any = ...,
        unit_text: Any = ...,
        unit_style: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_change: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    value: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    on_enter: Any
    warning_color: Any
    description_text: Any
    background_color: Any
    focus_background_color: Any
    line_color: Any
    focus_line_color: Any
    required_text: Any
    unit_text: Any
    def set_text(self, text) -> Any: ...


class PhoneField(TextField):
    """A phone number in its mask: PhoneField(title_text="Phone", country_code="+1", unit_text="US"). Only digits are
    typed: the country code and the marks of the mask (phone_mask=" (___) ___-____", a "_" for a digit) are written by
    the field, and a number given in code or pasted goes into it ("0555 123 45 67", "+90 555 123 45 67").
    field.text is the number in its mask ("" with no digit); field.is_valid(): every digit is written.
    set_country_code(code), set_phone_mask(mask) keep the digits. The kit's defaults: "+90", " (___) ___-____", "TR".
    style_name: as TextField.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        on_enter: Any = ...,
        text: Any = ...,
        required: Any = ...,
        title_text: Any = ...,
        placeholder: Any = ...,
        warning_text: Any = ...,
        warning_color: Any = ...,
        country_code: Any = ...,
        phone_mask: Any = ...,
        unit_text: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        type: Any = ...,
        width: Any = ...,
        height: Any = ...,
        left_padding: Any = ...,
        right_padding: Any = ...,
        title_font_size: Any = ...,
        input_font_size: Any = ...,
        input_height: Any = ...,
        field_padding: Any = ...,
        description_font_size: Any = ...,
        title_position: Any = ...,
        title_gap: Any = ...,
        value: Any = ...,
        max_length: Any = ...,
        show_description: Any = ...,
        description_text: Any = ...,
        allow_html: Any = ...,
        background_color: Any = ...,
        focus_background_color: Any = ...,
        hover_background_color: Any = ...,
        line_color: Any = ...,
        focus_line_color: Any = ...,
        back_border_color: Any = ...,
        focus_back_border_color: Any = ...,
        hover_back_border_color: Any = ...,
        back_border_top_round: Any = ...,
        back_border_bottom_round: Any = ...,
        title_text_color: Any = ...,
        title_bold: Any = ...,
        title_letter_spacing: Any = ...,
        input_text_color: Any = ...,
        input_color_scheme: Any = ...,
        placeholder_color: Any = ...,
        description_text_color: Any = ...,
        warning_ball_border_color: Any = ...,
        required_text: Any = ...,
        required_color: Any = ...,
        animated_warning_ball: Any = ...,
        warning_ball_type: Any = ...,
        warning_ball_size: Any = ...,
        warning_ball_border: Any = ...,
        warning_border_color: Any = ...,
        warning_icon_size: Any = ...,
        required_icon_file: Any = ...,
        warning_icon_file: Any = ...,
        required_icon_color: Any = ...,
        tooltip_style: Any = ...,
        select_style: Any = ...,
        show_left_box: Any = ...,
        show_right_box: Any = ...,
        show_unit: Any = ...,
        create_input: Any = ...,
        unit_style: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_change: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    value: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    on_enter: Any
    country_code: Any
    phone_mask: Any
    warning_color: Any
    unit_text: Any
    description_text: Any
    background_color: Any
    focus_background_color: Any
    line_color: Any
    focus_line_color: Any
    required_text: Any
    def set_text(self, text) -> Any: ...
    def set_country_code(self, code) -> Any: ...
    def set_phone_mask(self, mask) -> Any: ...


class CurrencyField(TextField):
    """An amount of money, written in groups of three: CurrencyField(title_text="Price", value=1234.5, unit_text="$")
    shows "1,234.5". field.value is a number (int or float; None when empty), field.text is what is written.
    allow_negative (True), allow_decimal (True), decimal_separator ("." or ","), group_separator (","),
    max_decimal_digits (2: more digits are cut, as the page does when they are typed). The kit's unit is "TL".
    style_name: as TextField.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        value: Any = ...,
        on_enter: Any = ...,
        text: Any = ...,
        required: Any = ...,
        title_text: Any = ...,
        placeholder: Any = ...,
        max_length: Any = ...,
        allow_negative: Any = ...,
        allow_decimal: Any = ...,
        decimal_separator: Any = ...,
        max_decimal_digits: Any = ...,
        group_separator: Any = ...,
        unit_text: Any = ...,
        key: Any = ...,
        style_name: Any = ...,
        type: Any = ...,
        width: Any = ...,
        height: Any = ...,
        left_padding: Any = ...,
        right_padding: Any = ...,
        title_font_size: Any = ...,
        input_font_size: Any = ...,
        input_height: Any = ...,
        field_padding: Any = ...,
        description_font_size: Any = ...,
        title_position: Any = ...,
        title_gap: Any = ...,
        show_description: Any = ...,
        description_text: Any = ...,
        allow_html: Any = ...,
        background_color: Any = ...,
        focus_background_color: Any = ...,
        hover_background_color: Any = ...,
        line_color: Any = ...,
        focus_line_color: Any = ...,
        back_border_color: Any = ...,
        focus_back_border_color: Any = ...,
        hover_back_border_color: Any = ...,
        back_border_top_round: Any = ...,
        back_border_bottom_round: Any = ...,
        title_text_color: Any = ...,
        title_bold: Any = ...,
        title_letter_spacing: Any = ...,
        input_text_color: Any = ...,
        input_color_scheme: Any = ...,
        placeholder_color: Any = ...,
        description_text_color: Any = ...,
        warning_ball_border_color: Any = ...,
        required_text: Any = ...,
        required_color: Any = ...,
        warning_text: Any = ...,
        warning_color: Any = ...,
        animated_warning_ball: Any = ...,
        warning_ball_type: Any = ...,
        warning_ball_size: Any = ...,
        warning_ball_border: Any = ...,
        warning_border_color: Any = ...,
        warning_icon_size: Any = ...,
        required_icon_file: Any = ...,
        warning_icon_file: Any = ...,
        required_icon_color: Any = ...,
        tooltip_style: Any = ...,
        select_style: Any = ...,
        show_left_box: Any = ...,
        show_right_box: Any = ...,
        show_unit: Any = ...,
        create_input: Any = ...,
        unit_style: Any = ...,
        on_focus: Any = ...,
        on_blur: Any = ...,
        on_change: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    title_text: Any
    placeholder: Any
    max_length: Any
    required: Any
    warning_text: Any
    on_enter: Any
    unit_text: Any
    description_text: Any
    background_color: Any
    focus_background_color: Any
    line_color: Any
    focus_line_color: Any
    required_text: Any
    warning_color: Any
    @property
    def value(self) -> Any: ...
    def set_value(self, value) -> Any: ...


class Slider(_TypedComponent):
    """A number on a thin bar: Slider(value=30, min_value=0, max_value=100, step=1, width=280, on_change_end=fn).
    on_change(slider) runs while it is dragged, on_change_end(slider) when it is let go (a key and a click on the bar too),
    on_change_start(slider) when it is taken: read slider.value. Its title and its number are yours (SliderField has
    them inside). style_name: "round" (default), "roundDark" (a dark page), "split", "splitDark" (split on a dark page).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        value: Any = ...,
        min_value: Any = ...,
        max_value: Any = ...,
        step: Any = ...,
        min_thumb_height: Any = ...,
        thumb_color: Any = ...,
        track_height: Any = ...,
        track_color: Any = ...,
        track_background_color: Any = ...,
        on_change_start: Any = ...,
        on_change: Any = ...,
        on_change_end: Any = ...,
        show_value_at_start: Any = ...,
        show_value_on_set: Any = ...,
        show_value_on_drag: Any = ...,
        aria_label: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        height: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    min_value: Any
    max_value: Any
    step: Any
    thumb_color: Any
    track_color: Any
    track_background_color: Any
    def set_value(self, value) -> Any: ...
    def set_min_value(self, value) -> Any: ...
    def set_max_value(self, value) -> Any: ...
    def set_step(self, value) -> Any: ...


class SearchInput(_TypedComponent):
    """A search box: SearchInput(placeholder="Search", on_change=fn). on_change(box) runs at every change (typed, pasted,
    cleared), on_enter(box) on Enter and after the clear icon: read box.text. show_clear_icon=False: no clear icon.
    style_name: "ozden" (default), "ozdenDark" (a dark page), "light", "original".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        text: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        search_icon_file: Any = ...,
        clear_icon_file: Any = ...,
        search_icon_size: Any = ...,
        search_icon_left: Any = ...,
        search_icon_gap: Any = ...,
        clear_icon_right: Any = ...,
        text_end_space: Any = ...,
        show_clear_icon: Any = ...,
        clear_icon_min_text_width: Any = ...,
        text_fade_width: Any = ...,
        clear_on_escape: Any = ...,
        value: Any = ...,
        placeholder: Any = ...,
        color: Any = ...,
        text_color: Any = ...,
        placeholder_color: Any = ...,
        search_icon_opacity: Any = ...,
        clear_icon_opacity: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        border_bottom_style: Any = ...,
        focus_border_color: Any = ...,
        focus_border_width: Any = ...,
        round: Any = ...,
        font_size: Any = ...,
        text_offset_y: Any = ...,
        clear_icon_offset_y: Any = ...,
        search_icon_offset_y: Any = ...,
        invert_icon_color: Any = ...,
        invert_search_icon_color: Any = ...,
        invert_clear_icon_color: Any = ...,
        animated: Any = ...,
        hover_ring_color: Any = ...,
        focus_ring_color: Any = ...,
        on_change: Any = ...,
        on_enter: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        key: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    placeholder: Any
    clear_icon_right: Any
    value: Any
    animated: Any
    def set_text(self, text) -> Any: ...
    def clear(self) -> Any: ...
    def set_placeholder(self, text) -> Any: ...
    def focus(self) -> Any: ...


class GraphBox(_TypedComponent):
    """A chart, drawn by the page with no other library: GraphBox(type="bar", labels=["Jan", "Feb"], values=[12, 19]).
    type: "line", "area", "bar", "pie", "doughnut", "radar", "scatter", "bubble". More lines or bars: datasets=[{"label":
    "2026", "data": [12, 19]}, ...]; a dataset also takes color, fill, dashed, curve, show_points. The values may be numpy
    arrays or a pandas Series. Scatter: data=[{"x": 1, "y": 2}, ...].
    format_value="{:,.0f} TL": the numbers of the axis and the tooltip, a text and not a function (the page needs them at
    once); format_x for the x axis of a scatter. title_text, subtitle_text, legend ("auto", "top", "none"...), stacked,
    horizontal, show_values, curve ("linear", "smooth"), target_lines=[{"value": 90, "label": "Target"}], max_count (a live
    chart: the oldest value goes). on_click(graph, item): item has label, value, dataset_label...
    graph.save_image("chart.png") writes a picture of it. theme: "light", "dark", "auto".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        type: Any = ...,
        theme: Any = ...,
        title_text: Any = ...,
        subtitle_text: Any = ...,
        labels: Any = ...,
        values: Any = ...,
        datasets: Any = ...,
        data: Any = ...,
        legend: Any = ...,
        stacked: Any = ...,
        horizontal: Any = ...,
        total_text: Any = ...,
        target_lines: Any = ...,
        max_slices: Any = ...,
        other_text: Any = ...,
        center_text: Any = ...,
        center_sub_text: Any = ...,
        begin_at_zero: Any = ...,
        min_value: Any = ...,
        max_value: Any = ...,
        soft_min_value: Any = ...,
        soft_max_value: Any = ...,
        value_step: Any = ...,
        min_x: Any = ...,
        max_x: Any = ...,
        size_text: Any = ...,
        x_axis_text: Any = ...,
        y_axis_text: Any = ...,
        show_values: Any = ...,
        table_view: Any = ...,
        table_head_text: Any = ...,
        max_labels: Any = ...,
        curve: Any = ...,
        show_points: Any = ...,
        format_value: Any = ...,
        format_x: Any = ...,
        locale: Any = ...,
        max_count: Any = ...,
        empty_text: Any = ...,
        animated: Any = ...,
        on_click: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style_name: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    labels: Any
    values: Any
    datasets: Any
    type: Any
    title_text: Any
    subtitle_text: Any
    theme: Any
    legend: Any
    show_values: Any
    table_view: Any
    stacked: Any
    horizontal: Any
    curve: Any
    target_lines: Any
    format_value: Any
    format_x: Any
    center_text: Any
    data: Any
    max_slices: Any
    value_step: Any
    animated: Any
    style: Any
    def set_labels(self, labels) -> Any: ...
    def set_values(self, values, dataset_index=...) -> Any: ...
    def set_datasets(self, datasets) -> Any: ...
    def set_data(self, labels, datasets) -> Any: ...
    def add_value(self, label, values) -> Any: ...
    def add_point(self, point, dataset_index=...) -> Any: ...
    def add_dataset(self, dataset) -> Any: ...
    def remove_dataset(self, position) -> Any: ...
    def set_dataset_visible(self, position, value) -> Any: ...
    def set_type(self, type_name) -> Any: ...
    def set_title(self, text) -> Any: ...
    def set_subtitle(self, text) -> Any: ...
    def set_center_text(self, text) -> Any: ...
    def set_legend(self, legend) -> Any: ...
    def set_show_values(self, value) -> Any: ...
    def set_table_view(self, value) -> Any: ...
    def set_stacked(self, value) -> Any: ...
    def set_horizontal(self, value) -> Any: ...
    def set_curve(self, curve) -> Any: ...
    def set_target_lines(self, lines) -> Any: ...
    def set_value_limits(self, minimum, maximum) -> Any: ...
    def set_format_value(self, text) -> Any: ...
    def set_format_x(self, text) -> Any: ...
    def set_theme(self, name) -> Any: ...
    def get_table_data(self) -> Any: ...
    def save_image(self, path, scale=...) -> Any: ...


class TreeView(_TypedComponent):
    """A tree: TreeView(items=[{"key": "src", "text": "src", "children": ["a.py", "b.py"]}, "readme"], height=300, on_select=fn).
    A node: a text or {"key", "text", "children", "expanded", "has_children", "description", "description_color", "tag",
    "tag_color", "text_color", "icon_file", "enabled", "data"}; enabled=False: it can not be selected or opened.
    on_select(tree, node) runs for a click and the arrow keys: tree.value is the key of the selected node.
    on_activate(tree, node): a double click or Enter. on_toggle(tree, node): it opened or closed.
    A branch made when it opens: {"key": "photos", "text": "photos", "has_children": True}, then on_load_children(tree, node)
    gives its nodes: tree.set_children(node["key"], [...]). style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        items: Any = ...,
        value: Any = ...,
        empty_text: Any = ...,
        type_ahead: Any = ...,
        use_scroll_bar: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        on_select: Any = ...,
        on_activate: Any = ...,
        toggle_on_double_click: Any = ...,
        on_toggle: Any = ...,
        on_hover: Any = ...,
        on_load_children: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    items: Any
    enabled: Any
    empty_text: Any
    previous_value: Any
    def set_items(self, items) -> Any: ...
    def set_value(self, key) -> Any: ...
    @property
    def selected_node(self) -> Any: ...
    def get_node(self, key) -> Any: ...
    def get_path(self, key) -> Any: ...
    def set_children(self, key, children) -> Any: ...
    def add_node(self, parent_key, node, position=...) -> Any: ...
    def remove_node(self, key) -> Any: ...
    def update_node(self, key, **values) -> Any: ...
    def expand(self, key) -> Any: ...
    def collapse(self, key) -> Any: ...
    def toggle(self, key) -> Any: ...
    def expand_all(self) -> Any: ...
    def collapse_all(self) -> Any: ...
    def reveal(self, key) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    def set_empty_text(self, text) -> Any: ...
    def focus(self) -> Any: ...


class ContextMenu(_TypedComponent):
    """A menu that opens at the mouse: ContextMenu(target=table, items=["Open", "-", {"text": "Delete", "key": "delete",
    "on_click": fn}], on_click=fn). An item: a text or {"text", "key", "icon", "icon_file", "items" (a submenu), "shortcut",
    "checked", "enabled", "data", "on_click"}; "-" is a line. A right click on the target opens it; trigger="click": a click.
    fn(menu, item, index) (fn() too). on_click=fn of the menu: every item. menu.open_at(x, y), menu.open_below(obj), menu.close().
    style_name: "light" (default; its old name "classic"), "dark" (a dark page).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        items: Any = ...,
        target: Any = ...,
        trigger: Any = ...,
        min_width: Any = ...,
        max_width: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        on_click: Any = ...,
        on_open: Any = ...,
        on_close: Any = ...,
        on_side_key: Any = ...,
        parent_menu: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        height: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    items: Any
    enabled: Any
    def set_items(self, items) -> Any: ...
    def attach_to(self, obj, trigger=...) -> Any: ...
    def detach(self, obj) -> Any: ...
    def open_at(self, x, y) -> Any: ...
    def open_below(self, obj) -> Any: ...
    def close(self) -> Any: ...
    def is_open(self) -> Any: ...
    def set_item_enabled(self, key, value) -> Any: ...
    def set_item_checked(self, key, value) -> Any: ...
    def set_enabled(self, value) -> Any: ...


class Tooltip(_TypedComponent):
    """A hint under the mouse: Tooltip(target=button, text="Save the file"). position: "top" (default), "bottom", "left",
    "right". look={"arrow": 10, "color": "#222", "text_color": "white"}: its look (shadow, padding, round, border, border_color...).
    Tooltip.show(button, "Saved.", time=2000): a bubble at the object, not under the mouse; bubble.remove() takes it away.
    Tooltip.popover(button, make_content): a click on the button opens a bubble that stays; make_content() makes its objects.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        text: Any = ...,
        position: Any = ...,
        target: Any = ...,
        hint_text: Any = ...,
        hint_position: Any = ...,
        content: Any = ...,
        trigger: Any = ...,
        look: Any = ...,
        style_name: Any = ...,
        scale: Any = ...,
        visible: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        height: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        key: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        width: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    text: Any
    hint_text: Any
    def set_text(self, text) -> Any: ...
    @staticmethod
    def show(target, text, side=..., look=..., time=...) -> Any: ...
    @staticmethod
    def popover(target, content, side=..., look=..., on_close=...) -> Any: ...
    @staticmethod
    def close_popover() -> Any: ...


class _Picker(_TypedComponent):
    """The common part of a field that opens a panel (a date, a time, a color). inline=True: the panel stays in its place.
    on_change(picker) runs when it changes: read picker.value. "" is no value.
    """
    value: Any
    enabled: Any
    def open(self) -> Any: ...
    def close(self) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...


class DatePicker(_Picker):
    """A date: a field that opens a calendar: DatePicker(value="2026-11-20", on_change=fn). inline=True: a calendar that stays.
    picker.value is a text ("2026-11-20", "": none), picker.date a datetime.date or None; a date may be given as either.
    min_date, max_date, format ("DD.MM.YYYY"), language ("en", "tr"), first_day_of_week (1: Monday).
    style_name: "light" (default; its old name "classic"), "dark" (a dark page).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        value: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        date: Any = ...,
        min_date: Any = ...,
        max_date: Any = ...,
        format: Any = ...,
        language: Any = ...,
        first_day_of_week: Any = ...,
        placeholder: Any = ...,
        inline: Any = ...,
        scale: Any = ...,
        enabled: Any = ...,
        close_on_select: Any = ...,
        show_today_button: Any = ...,
        show_clear_button: Any = ...,
        on_change: Any = ...,
        on_open: Any = ...,
        on_close: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    enabled: Any
    min_date: Any
    max_date: Any
    @property
    def date(self) -> Any: ...
    def set_value(self, value) -> Any: ...
    def set_min_date(self, value) -> Any: ...
    def set_max_date(self, value) -> Any: ...


class TimePicker(_Picker):
    """A time: a field that opens two columns: TimePicker(value="19:30", on_change=fn). inline=True: the columns stay.
    picker.value is a text ("19:30", "": none), picker.time a datetime.time or None; a time may be given as either.
    min_time, max_time, minute_step (5), language ("en", "tr"). style_name: "light" (default; its old name "classic"), "dark" (a dark page).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        value: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        time: Any = ...,
        min_time: Any = ...,
        max_time: Any = ...,
        minute_step: Any = ...,
        format: Any = ...,
        language: Any = ...,
        placeholder: Any = ...,
        inline: Any = ...,
        enabled: Any = ...,
        close_on_select: Any = ...,
        use_scroll_bar: Any = ...,
        show_now_button: Any = ...,
        show_clear_button: Any = ...,
        on_change: Any = ...,
        on_open: Any = ...,
        on_close: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    enabled: Any
    min_time: Any
    max_time: Any
    minute_step: Any
    @property
    def time(self) -> Any: ...
    def set_value(self, value) -> Any: ...
    def set_min_time(self, value) -> Any: ...
    def set_max_time(self, value) -> Any: ...
    def set_minute_step(self, step) -> Any: ...


class ColorPicker(_Picker):
    """A color: a field that opens a palette: ColorPicker(value="#3871E0", on_change=fn). inline=True: a palette that stays.
    picker.value is the color ("#3871E0", "": none). colors=[...]: your own palette, columns: how many in a row.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        value: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        selected_color: Any = ...,
        colors: Any = ...,
        columns: Any = ...,
        show_text: Any = ...,
        placeholder: Any = ...,
        inline: Any = ...,
        enabled: Any = ...,
        close_on_select: Any = ...,
        on_change: Any = ...,
        on_open: Any = ...,
        on_close: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    enabled: Any
    selected_color: Any
    colors: Any
    def set_value(self, color) -> Any: ...
    def set_colors(self, colors) -> Any: ...


class Stepper(_TypedComponent):
    """A number with - and + buttons: Stepper(value=2, min_value=0, max_value=10, step=1, on_change=fn). on_change(stepper):
    read stepper.value. A click on the number types it (editable=False: no); a button that is held keeps counting.
    precision: its decimals. unit_text=" kg". value_format="{:,.1f} kg": its text. wrap=True: after max_value comes
    min_value.
    layout: "horizontal" or "compact". style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern", "ozden",
    "ozdenDark" (ozden on a dark page).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        value: Any = ...,
        min_value: Any = ...,
        max_value: Any = ...,
        step: Any = ...,
        precision: Any = ...,
        unit_text: Any = ...,
        editable: Any = ...,
        wrap: Any = ...,
        hold_to_repeat: Any = ...,
        layout: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        value_format: Any = ...,
        on_change: Any = ...,
        on_min_reached: Any = ...,
        on_max_reached: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    value: Any
    enabled: Any
    unit_text: Any
    step: Any
    precision: Any
    min_value: Any
    max_value: Any
    def set_value(self, value) -> Any: ...
    def increase(self) -> Any: ...
    def decrease(self) -> Any: ...
    def set_min_value(self, value) -> Any: ...
    def set_max_value(self, value) -> Any: ...
    def set_range(self, min_value, max_value) -> Any: ...
    def set_step(self, step) -> Any: ...
    def set_precision(self, digits) -> Any: ...
    def set_unit_text(self, text) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    def focus(self) -> Any: ...


class FilePicker(_TypedComponent):
    """A place for files: a file dropped on it, or chosen in the file dialog of the system after a click:
    FilePicker(accept=".csv,.txt", multiple=True, on_change=fn). on_change(picker) runs when the list changes.
    picker.files: [{"name", "path", "size", "size_text", "type", "extension", "last_modified"}]: "path" is the real path on
    this computer, so open(file["path"]) reads it. picker.paths: only the paths.
    accept: ".pdf,.txt", "image/*"; max_size (bytes), max_files: what does not pass goes to on_error(picker, errors).
    multiple=True adds to the list; without it a new file takes the place of the old one. directory=True: a click chooses a
    folder, and the list holds its files. picker.add_paths([...]), picker.remove_file(0), picker.clear(), picker.open().
    title_text, description_text: its texts. icon_file: a picture of yours in the place of its icon (a path, bytes, a
    Pillow image or an address; set_icon() changes it). NOTE: a folder dropped on it is not read.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        on_change: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        zone_height: Any = ...,
        multiple: Any = ...,
        directory: Any = ...,
        accept: Any = ...,
        max_size: Any = ...,
        max_files: Any = ...,
        enabled: Any = ...,
        show_icon: Any = ...,
        icon_svg: Any = ...,
        icon_file: Any = ...,
        animated: Any = ...,
        show_list: Any = ...,
        show_preview: Any = ...,
        prevent_page_drop: Any = ...,
        title_text: Any = ...,
        description_text: Any = ...,
        hint_text: Any = ...,
        drop_text: Any = ...,
        allow_html: Any = ...,
        on_error: Any = ...,
        on_open_dialog: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    enabled: Any
    title_text: Any
    description_text: Any
    icon_file: Any
    on_change: Any
    icon_svg: Any
    animated: Any
    @property
    def files(self) -> Any: ...
    @property
    def paths(self) -> Any: ...
    def set_on_change(self, handler) -> Any: ...
    def add_paths(self, paths) -> Any: ...
    def open(self) -> Any: ...
    def remove_file(self, index) -> Any: ...
    def clear(self) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    def set_title_text(self, text) -> Any: ...
    def set_description_text(self, text) -> Any: ...
    def set_icon(self, picture) -> Any: ...


class Accordion(_ThemedComponent):
    """Sections that fold: acc = Accordion(sections=["General", {"key": "more", "text": "Advanced", "opened": True}]);
    with acc.section("General"): Label(...). Objects go one under the other, also while a section is closed.
    A section: a text (its key too) or {"key", "text", "description", "icon_file", "icon", "opened", "enabled", "data"};
    description: a soft text at the end of its row, enabled=False: it does not open or close.
    multiple=False: a section that opens closes the others. on_toggle(acc, section): read section["key"], section["opened"],
    or acc.open_keys. height: none: it grows with its sections; a number or "100%": they scroll inside it. animated=True: the
    arrow turns and the objects fade in. arrow_side: "right" or "left". style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        sections: Any = ...,
        multiple: Any = ...,
        arrow_side: Any = ...,
        enabled: Any = ...,
        animated: Any = ...,
        use_scroll_bar: Any = ...,
        on_toggle: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    sections: Any
    enabled: Any
    animated: Any
    @property
    def open_keys(self) -> Any: ...
    def section(self, key) -> Any: ...
    def open(self, key) -> Any: ...
    def close(self, key) -> Any: ...
    def toggle(self, key) -> Any: ...
    def is_open(self, key) -> Any: ...
    def open_all(self) -> Any: ...
    def close_all(self) -> Any: ...
    def add_section(self, section) -> Any: ...
    def remove_section(self, key) -> Any: ...
    def set_sections(self, sections) -> Any: ...
    def set_section_text(self, key, text) -> Any: ...
    def set_section_description(self, key, text) -> Any: ...
    def set_section_enabled(self, key, value) -> Any: ...
    def set_enabled(self, value) -> Any: ...
    def set_animated(self, value) -> Any: ...
    def focus(self, key=...) -> Any: ...


class MarkdownView(_ThemedComponent):
    """A text written in Markdown, drawn on the page: a report, the answer of an AI:
        MarkdownView(text="# A title

    Some **bold** words"). Headings, lists, check marks, quotes, tables, links, pictures,
        code with colors and a button that copies it. A text is never read as HTML, and no script of it runs.
        view.text, set_text(text), clear(), load_file("report.md"). append_text(piece): a text that comes piece by piece, from
        a background job too: what is above stays, and the view follows the end until the reader scrolls up.
        A picture: ![A plot](plot.png), a file in picture_folder (default: the folder the program runs in) or next to the file
        of load_file(); a matplotlib figure: f"![A plot]({picture_address(figure)})". A picture with an http address stays a
        link, because its address can carry data and its server sees that the text was opened: a text you trust: remote_pictures=True.
        on_link_click(view, address): a link comes to you; without it the browser of the computer opens it. A link to
        "#a-heading" goes to that heading. view.headings, scroll_to_heading(id), scroll_to_top(), scroll_to_end().
        height: none: it fills its group; a number; "auto": it grows with its text. empty_text. style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        picture_folder: Any = ...,
        text: Any = ...,
        theme: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        markdown_text: Any = ...,
        empty_text: Any = ...,
        auto_scroll: Any = ...,
        remote_pictures: Any = ...,
        use_scroll_bar: Any = ...,
        aria_label: Any = ...,
        copy_text: Any = ...,
        copied_text: Any = ...,
        on_link_click: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    markdown_text: Any
    empty_text: Any
    auto_scroll: Any
    @property
    def text(self) -> Any: ...
    def set_text(self, text) -> Any: ...
    def append_text(self, piece) -> Any: ...
    def clear(self) -> Any: ...
    def load_file(self, path) -> Any: ...
    @property
    def headings(self) -> Any: ...
    def scroll_to_heading(self, heading_id) -> Any: ...
    def scroll_to_top(self) -> Any: ...
    def scroll_to_end(self) -> Any: ...
    def set_empty_text(self, text) -> Any: ...
    def set_auto_scroll(self, value) -> Any: ...


class JsonView(_ThemedComponent):
    """A value as a tree: the answer of a server, a dictionary of your program: JsonView(value={"name": "Ada", "tags": ["a"]}).
    Keys and values in colors. A branch is made when it opens and a long list comes in pages, so a list of a million items
    opens at once. A date, a set or an object of yours is shown as its text. expand_level: how many levels are open at the start.
    on_select(view, entry): a row was clicked: entry["pathText"] (users[0].name), entry["path"], entry["kind"], entry["value"]
    (None for a branch: a dict, a list, or a page of one longer than page_size, 100; the page does not send them).
    view.selected_value is the value of the selected row, a branch too (a page: the whole dict or list it is part of);
    view.selected_path, selected_path_text. select_path(["users", 0, "name"]) opens the rows down to it.
    Right click or Ctrl+C: its value or its path goes to the clipboard; on_copy(view, text). set_json_text(text): a text that
    is not JSON shows its error and returns False. expand_all(), collapse_all(). height: none: it fills its group; a number;
    "auto": it grows with its rows. style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        value: Any = ...,
        expand_level: Any = ...,
        page_size: Any = ...,
        empty_text: Any = ...,
        copy_value_text: Any = ...,
        copy_path_text: Any = ...,
        use_scroll_bar: Any = ...,
        aria_label: Any = ...,
        on_select: Any = ...,
        on_copy: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    @property
    def value(self) -> Any: ...
    def set_value(self, value) -> Any: ...
    def set_json_text(self, text) -> Any: ...
    @property
    def selected_path(self) -> Any: ...
    @property
    def selected_path_text(self) -> Any: ...
    @property
    def selected_value(self) -> Any: ...
    def select_path(self, path) -> Any: ...
    def expand_all(self) -> Any: ...
    def collapse_all(self) -> Any: ...


class RangeSlider(_ThemedComponent):
    """A range of values on a thin bar, with two knobs: RangeSlider(low=200, high=800, min_value=0, max_value=1000, step=50,
    width=280, on_change_end=fn). on_change(slider) runs while it moves, on_change_end(slider) when it is let go (a key and a click on
    the bar too): read slider.low, slider.high, slider.values. min_gap: the smallest distance between them.
    value_format="{:,.0f} TL": the text of its bubble. set_values(low, high). style_name / theme: "round" (default), "roundDark" (a dark page).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        low: Any = ...,
        high: Any = ...,
        value_format: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        min_value: Any = ...,
        max_value: Any = ...,
        step: Any = ...,
        low_value: Any = ...,
        high_value: Any = ...,
        min_gap: Any = ...,
        show_value_on_move: Any = ...,
        format_value: Any = ...,
        enabled: Any = ...,
        low_aria_label: Any = ...,
        high_aria_label: Any = ...,
        on_change: Any = ...,
        on_change_end: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    low: Any
    low_value: Any
    high: Any
    high_value: Any
    min_value: Any
    max_value: Any
    step: Any
    min_gap: Any
    enabled: Any
    @property
    def values(self) -> Any: ...
    def set_values(self, low=..., high=...) -> Any: ...
    def set_low(self, value) -> Any: ...
    def set_high(self, value) -> Any: ...
    def set_min_value(self, value) -> Any: ...
    def set_max_value(self, value) -> Any: ...
    def set_step(self, value) -> Any: ...
    def set_min_gap(self, value) -> Any: ...
    def set_enabled(self, value) -> Any: ...


class StepBar(_ThemedComponent):
    """The steps of a job in a row: StepBar(steps=["Cart", "Address", {"text": "Payment", "description": "Card or cash"}, "Done"],
    step=1). A step: a text or {"key", "text", "description"}.
    A step behind has a check mark; on_step_click(bar, index) runs for a click on it (the page goes there with set_step()).
    can_go_back=False: no step can be clicked. bar.step, set_step(index), next(), previous(), set_steps([...]).
    show_titles=False: only the circles. style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        step: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        steps: Any = ...,
        current_step: Any = ...,
        can_go_back: Any = ...,
        show_titles: Any = ...,
        aria_label: Any = ...,
        on_step_click: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    step: Any
    current_step: Any
    steps: Any
    def set_step(self, index) -> Any: ...
    def next(self) -> Any: ...
    def previous(self) -> Any: ...
    def set_steps(self, steps) -> Any: ...


class Canvas(_ThemedComponent):
    """A place to draw on: canvas = Canvas(width=600, height=400); canvas.line(20, 20, 200, 120, color="tomato", line_width=4)
    Shapes: line(x1, y1, x2, y2), rect(x, y, width, height, round=), circle(x, y, radius), ellipse(x, y, radius_x, radius_y),
    polyline(points), polygon(points), text(x, y, text, font_size=, bold=, align=), image(x, y, width, height, picture).
    The look: color (the line), fill, line_width, dash=[6, 4], opacity, draggable=True. Each returns the key of the shape.
    update_shape(key, x=..., fill=...), move_shape(key, dx, dy), remove_shape(key), bring_to_front(key), clear().
    canvas.shapes (copies) and canvas.shape(key) are kept in Python. on_click(canvas, x, y, shape): shape is None on an
    empty place. drawing=True: the mouse draws free lines with the pen (set_pen(color, width)); on_draw_end(canvas, shape).
    A draggable shape is moved by the page: on_shape_move(canvas, shape) at the end (a move of the mouse is not sent).
    save_image("drawing.png"). style_name / theme: "light", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        theme: Any = ...,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        shapes: Any = ...,
        drawing: Any = ...,
        pen_color: Any = ...,
        pen_width: Any = ...,
        aria_label: Any = ...,
        on_click: Any = ...,
        on_shape_move: Any = ...,
        on_draw_end: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    drawing: Any
    @property
    def shapes(self) -> Any: ...
    def shape(self, key) -> Any: ...
    def add_shape(self, shape) -> Any: ...
    def line(self, x1, y1, x2, y2, **look) -> Any: ...
    def rect(self, x, y, width, height, **look) -> Any: ...
    def circle(self, x, y, radius, **look) -> Any: ...
    def ellipse(self, x, y, radius_x, radius_y, **look) -> Any: ...
    def polyline(self, points, **look) -> Any: ...
    def polygon(self, points, **look) -> Any: ...
    def text(self, x, y, text, **look) -> Any: ...
    def image(self, x, y, width, height, picture, **look) -> Any: ...
    def update_shape(self, key, **changes) -> Any: ...
    def move_shape(self, key, dx, dy) -> Any: ...
    def remove_shape(self, key) -> Any: ...
    def bring_to_front(self, key) -> Any: ...
    def set_shapes(self, shapes) -> Any: ...
    def clear(self) -> Any: ...
    def set_drawing(self, is_on) -> Any: ...
    def set_pen(self, color=..., width=...) -> Any: ...
    def save_image(self, path) -> Any: ...


class SidePanel(_TypedComponent):
    """A panel that slides in from a side of the window, over the page: panel = SidePanel(title_text="Filters");
    with panel.body: CheckBox(...); then panel.open() and panel.close(). side: "right" (default), "left", "top", "bottom";
    panel_size: px. It is made on the page, wherever the code makes it. A click on its cover or Escape closes it, so
    panel.is_open is kept in Python. on_open(panel), on_close(panel).
    style_name: "light" (default), "modern", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        side: Any = ...,
        container: Any = ...,
        panel_size: Any = ...,
        screen_margin: Any = ...,
        duration: Any = ...,
        fade: Any = ...,
        title_text: Any = ...,
        allow_html: Any = ...,
        show_header: Any = ...,
        show_close_button: Any = ...,
        show_backdrop: Any = ...,
        close_on_backdrop: Any = ...,
        close_on_escape: Any = ...,
        exclusive: Any = ...,
        opened: Any = ...,
        aria_label: Any = ...,
        on_open: Any = ...,
        on_close: Any = ...,
        on_before_close: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        height: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    title_text: Any
    is_opened: Any
    panel_size: Any
    @property
    def body(self) -> Any: ...
    @property
    def is_open(self) -> Any: ...
    def open(self) -> Any: ...
    def close(self) -> Any: ...
    def toggle(self) -> Any: ...
    def set_title(self, text) -> Any: ...


class LoadingScreen(_TypedComponent):
    """A cover while the app gets ready: loading = LoadingScreen(title_text="My App", message_text="Reading the files...");
    later loading.close(): it fades out (after min_duration ms at least, so a fast job does not blink). It covers the
    window (cover=box: that box). loading.set_message(text), loading.set_progress(0.4) (a bar; -1 hides it),
    loading.open() shows it again. spinner_type: "clock" (default), "ring", "dots", "none". remove_on_close=True: it
    goes away for good. on_close(loading) after it has faded out. style_name: "light" (default), "dark", "ozden".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        cover: Any = ...,
        title: Any = ...,
        message: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        style_name: Any = ...,
        icon_file: Any = ...,
        icon_svg: Any = ...,
        title_text: Any = ...,
        allow_html: Any = ...,
        message_text: Any = ...,
        spinner_type: Any = ...,
        progress: Any = ...,
        opened: Any = ...,
        min_duration: Any = ...,
        fade_duration: Any = ...,
        remove_on_close: Any = ...,
        on_close: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        key: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    title_text: Any
    message_text: Any
    progress: Any
    def open(self) -> Any: ...
    def close(self) -> Any: ...
    def set_title(self, text) -> Any: ...
    def set_message(self, text) -> Any: ...
    def set_progress(self, value) -> Any: ...


class TagInput(_TypedComponent):
    """Tags in a field: TagInput(tags=["audio"], suggestions=["audio", "fitness", "guide"], on_change=fn).
    on_change(field): read field.tags (a list of texts, kept in Python). Enter or a comma ends a tag, a pasted list is
    split. allow_custom=False: only the suggestions; max_tags; lowercase=True; placeholder. In code (not calling
    on_change): field.tags = [...], field.add_tag(tag), field.remove_tag(tag), field.clear().
    style_name: "light" (default), "modern", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        tags: Any = ...,
        suggestions: Any = ...,
        allow_custom: Any = ...,
        show_suggestions_on_focus: Any = ...,
        max_suggestions: Any = ...,
        max_tags: Any = ...,
        min_length: Any = ...,
        max_length: Any = ...,
        lowercase: Any = ...,
        separators: Any = ...,
        placeholder: Any = ...,
        empty_text: Any = ...,
        enabled: Any = ...,
        aria_label: Any = ...,
        validate: Any = ...,
        on_change: Any = ...,
        on_add: Any = ...,
        on_remove: Any = ...,
        on_reject: Any = ...,
        messages: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    suggestions: Any
    enabled: Any
    placeholder: Any
    max_tags: Any
    @property
    def tags(self) -> Any: ...
    def set_tags(self, tags) -> Any: ...
    def add_tag(self, tag) -> Any: ...
    def remove_tag(self, tag) -> Any: ...
    def clear(self) -> Any: ...
    def set_suggestions(self, suggestions) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    def set_placeholder(self, text) -> Any: ...


class DataTable(_TypedComponent):
    """A table that fits its texts, for up to a few hundred rows: DataTable(columns=[{"key": "name", "title": "Name"}],
    rows=[...], on_select=fn). A row is a dict (by the keys of the columns, with an "id") or a list in their order (the
    id first). on_select(table, row): the row as it was given, or None; on_row_click(table, row): a click or Enter.
    table.selected_row is kept in Python. A column: key, title, width, align, type ("number"), sortable. show_search=True:
    a search box in its head; sort_key, sort_direction. Very many rows: SmartTable.
    style_name: "light" (default), "plain", "dark".
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        on_select: Any = ...,
        on_row_click: Any = ...,
        width: Any = ...,
        height: Any = ...,
        columns: Any = ...,
        rows: Any = ...,
        id_index: Any = ...,
        id_key: Any = ...,
        sort_key: Any = ...,
        sort_direction: Any = ...,
        can_select: Any = ...,
        row_height: Any = ...,
        title_text: Any = ...,
        show_search: Any = ...,
        search_params: Any = ...,
        empty_text: Any = ...,
        no_result_text: Any = ...,
        sort_icon_file: Any = ...,
        use_scroll_bar: Any = ...,
        on_sort: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        key: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    rows: Any
    title_text: Any
    @property
    def selected_row(self) -> Any: ...
    def set_rows(self, rows) -> Any: ...
    def add_row(self, row) -> Any: ...
    def remove_row(self, row_id) -> Any: ...
    def select(self, row_id) -> Any: ...
    def clear_selection(self) -> Any: ...
    def sort_by(self, key, direction=...) -> Any: ...


class JsonEditor(_TypedComponent):
    """A list or a dict of JSON written in a table: the items of a menu, the products of a shop, the settings of a program:
    JsonEditor(value=[{"name": "Apple", "price": 1.2, "in_stock": True}], height=360, on_change=fn).
    + adds a row, a click on a cell writes in it, a title sorts, the dots of a row drag it. A dict is a table of names and
    values; a cell that holds a list or a dict opens as a table of its own. The kind of a column comes from its values and
    its name (a text, a number, on / off, a color, a picture); columns=[{"key": "unit", "options": ["kg", "piece"]}] gives the
    choices of a cell (a column: key, kind, options, note, columns). Rows pasted from a spreadsheet or as a JSON list, its own
    undo (Cmd/Ctrl+Z), a search, a JSON view (Table | JSON). texts={"add_row": "Satır"}: its own texts.
    value: a list or a dict, or its JSON text; JSON data only (a date is refused: it would come back as a text). A whole
    number bigger than 2**53 goes as its text. on_change(editor, value): a change in the table, with the whole value (not
    at create time, not with set_value()). editor.value asks the page: a cell being written is written first; None: the table
    can not make a value now (a name used twice), editor.error_text says why. set_value(), set_json_text(text) (False: not
    JSON, its error is on the editor), get_json_text(), editor.view = "json" ("table"), undo(), redo(), has_changes(),
    set_title_text(title_text, note_text), focus(). style_name: "light", "dark", "minimal", "minimalDark".
    JsonEditor.open(value=..., on_apply=fn): the editor in a window over the page, with Cancel and Apply.
    NOTE: color_of, options_of, on_pick_color and on_pick_picture take a function of the page, not a Python function.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        left: Any = ...,
        top: Any = ...,
        width: Any = ...,
        height: Any = ...,
        value: Any = ...,
        title_text: Any = ...,
        note_text: Any = ...,
        columns: Any = ...,
        show_title_bar: Any = ...,
        show_hint: Any = ...,
        picture_base: Any = ...,
        aria_label: Any = ...,
        texts: Any = ...,
        on_change: Any = ...,
        on_pick_color: Any = ...,
        on_pick_picture: Any = ...,
        color_of: Any = ...,
        options_of: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    title_text: Any
    note_text: Any
    @property
    def value(self) -> Any: ...
    @property
    def error_text(self) -> Any: ...
    def set_value(self, value) -> Any: ...
    def set_json_text(self, text) -> Any: ...
    def get_json_text(self) -> Any: ...
    @property
    def view(self) -> Any: ...
    def set_view(self, view) -> Any: ...
    def undo(self) -> Any: ...
    def redo(self) -> Any: ...
    def has_changes(self) -> Any: ...
    def set_title_text(self, title_text, note_text=...) -> Any: ...
    def focus(self) -> Any: ...
    @staticmethod
    def open(**params) -> Any: ...


class SortableList(_TypedComponent):
    """A list whose order the user changes: SortableList(items=["Sales", "Stock", {"key": "home", "text": "Home",
    "description": "The first page", "locked": True}], on_change=fn). The grip at the left drags a row (drag_by="row":
    the whole row); with the keys: the arrows move the focus, Space grabs and drops a row, Alt + an arrow moves it at once.
    lst.items: your items (the same texts and dicts) in the order on the page; lst.keys: their keys (a dict's "key", else
    its text). on_change(lst, item, from_index, to_index) after a move of the user. removable=True: an x button and the
    Delete key, on_remove(lst, item, index). on_item_click(lst, item, index), on_drag_start(lst, item, index),
    on_drag_end(lst, item, index). An item: a text or {"key", "text", "description", "locked"}; locked=True: it does not
    move, and the user can not move a row past it. show_buttons=True: up / down buttons; show_numbers=False: no numbers;
    height="auto": it grows with its rows. In code: move_item(from_index, to_index), add_item(item, index=-1),
    remove_item(index), set_items(items), index_of(key), focus_item(index), set_enabled(); they do not call on_change or
    on_remove. style_name: "light" (default), "dark" (a dark page), "modern".
    NOTE: create_item_view takes a function of the page, not a Python function: the page draws a row at once.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        items: Any = ...,
        drag_by: Any = ...,
        show_handle: Any = ...,
        show_numbers: Any = ...,
        show_buttons: Any = ...,
        removable: Any = ...,
        enabled: Any = ...,
        row_gap: Any = ...,
        empty_text: Any = ...,
        use_scroll_bar: Any = ...,
        aria_label: Any = ...,
        create_item_view: Any = ...,
        texts: Any = ...,
        on_change: Any = ...,
        on_remove: Any = ...,
        on_item_click: Any = ...,
        on_drag_start: Any = ...,
        on_drag_end: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    enabled: Any
    order: Any
    @property
    def items(self) -> Any: ...
    @property
    def keys(self) -> Any: ...
    def index_of(self, key) -> Any: ...
    def set(self, **props) -> Any: ...
    def set_items(self, items) -> Any: ...
    def move_item(self, from_index, to_index) -> Any: ...
    def add_item(self, item, index=...) -> Any: ...
    def remove_item(self, index) -> Any: ...
    def set_enabled(self, enabled) -> Any: ...
    def focus_item(self, index=...) -> Any: ...


class WebView(_TypedComponent):
    """A web page or an HTML text in a box: WebView(url="https://example.com", height=400), WebView(html=fig.to_html()).
    The HTML of other libraries runs in it with its scripts: a plotly chart (fig.to_html()), a folium map
    (m.get_root().render()), a pandas table (df.to_html()); a script or a picture from the internet needs a connection.
    url: a web address, or a path of this computer (its text is shown: a picture or a style next to the file is not
    loaded; give them as https:// or data: addresses). load(address), load_html(html), load_file(path), reload(), clear().
    on_load(view). on_error(view): a page that is not there. load_timeout=15 (seconds), on_timeout(view): a page that does
    not come. on_message(view, data): the page sends with window.parent.postMessage(data, "*"); post_message(data) sends
    to it. auto_height=True: the box grows with the page (an HTML text). scale=0.5: a smaller copy; interactive=False:
    the page can not be clicked, on_click(view) runs instead. toolbar=True: the address, reload and "open in the browser".
    A site may refuse to be shown in a frame (its own rule). It has one look, also in a dark window.
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        html: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        url: Any = ...,
        html_text: Any = ...,
        aria_label: Any = ...,
        sandbox: Any = ...,
        allow: Any = ...,
        referrer_policy: Any = ...,
        lazy: Any = ...,
        scale: Any = ...,
        interactive: Any = ...,
        auto_height: Any = ...,
        toolbar: Any = ...,
        show_loading: Any = ...,
        empty_text: Any = ...,
        load_timeout: Any = ...,
        on_load: Any = ...,
        on_error: Any = ...,
        on_timeout: Any = ...,
        on_message: Any = ...,
        on_click: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        placeholder: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        style_name: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    url: Any
    html_text: Any
    html: Any
    scale: Any
    interactive: Any
    auto_height: Any
    def load(self, address) -> Any: ...
    def load_html(self, html) -> Any: ...
    def load_file(self, path) -> Any: ...
    def reload(self) -> Any: ...
    def clear(self) -> Any: ...
    def post_message(self, data) -> Any: ...
    def set_scale(self, scale) -> Any: ...
    def set_interactive(self, interactive) -> Any: ...
    def set_auto_height(self, auto_height) -> Any: ...
    def show_error(self, text) -> Any: ...
    def hide_error(self) -> Any: ...


class ChatView(_ThemedComponent):
    """A conversation with an AI: ChatView(height=500, empty_text="Ask something", on_send=answer). The messages of the
    user are bubbles on the right; an answer is Markdown (headings, lists, tables, code with a button that copies it).
    on_send(chat, text): the user sent a text (Enter; Shift+Enter makes a new line): its message is on the view already.
    Answer it piece by piece, from a background job too:

        def answer(chat, text):
            key = chat.add_message(role="assistant")
            chat.busy = True  # three dots until the first words, and Stop in the place of Send
            run_in_background(write_answer, chat, key, text)  # chat.append_text(key, piece)..., then chat.busy = False

    on_stop(chat): Stop was pressed (chat.busy is False already): stop your answer. A message: {"key", "role", "text"},
    role "user", "assistant" (default) or "system" (a soft line in the middle). chat.messages: copies, kept in Python.
    add_message(text="", role="assistant", key=None) returns its key; append_text(key, piece), set_message_text(key, text),
    message_text(key), remove_message(key), clear(), set_messages([...]). send() sends the text of the field,
    chat.input_text asks the page for it, set_input_text(), focus(). show_input=False: only the messages.
    A picture of an answer: as in a MarkdownView (picture_folder). style_name / theme: "light", "dark", "minimal",
    "minimalDark" (a minimal window takes them: small, made of lines).
    """
    def __init__(
        self,
        *left_top_width_height: float | str,
        picture_folder: Any = ...,
        theme: Any = ...,
        key: Any = ...,
        width: Any = ...,
        height: Any = ...,
        messages: Any = ...,
        placeholder: Any = ...,
        empty_text: Any = ...,
        send_text: Any = ...,
        stop_text: Any = ...,
        show_input: Any = ...,
        send_on_enter: Any = ...,
        max_input_lines: Any = ...,
        busy: Any = ...,
        auto_scroll: Any = ...,
        remote_pictures: Any = ...,
        aria_label: Any = ...,
        copy_text: Any = ...,
        copied_text: Any = ...,
        on_send: Any = ...,
        on_stop: Any = ...,
        on_link_click: Any = ...,
        style_name: Any = ...,
        style: Any = ...,
        alt: Any = ...,
        aria: Any = ...,
        auto_size: Any = ...,
        bold: Any = ...,
        border: Any = ...,
        border_color: Any = ...,
        bottom: Any = ...,
        box_shadow: Any = ...,
        clickable: Any = ...,
        clip_content: Any = ...,
        color: Any = ...,
        css: Any = ...,
        cursor: Any = ...,
        ellipsis: Any = ...,
        enabled: Any = ...,
        font_family: Any = ...,
        font_size: Any = ...,
        grow: Any = ...,
        image_fit: Any = ...,
        input_type: Any = ...,
        italic: Any = ...,
        left: Any = ...,
        line_height: Any = ...,
        loop: Any = ...,
        max_length: Any = ...,
        minimal: Any = ...,
        opacity: Any = ...,
        padding: Any = ...,
        plain_text: Any = ...,
        position: Any = ...,
        read_only: Any = ...,
        right: Any = ...,
        role: Any = ...,
        rotate: Any = ...,
        round: Any = ...,
        scroll_x: Any = ...,
        scroll_y: Any = ...,
        selectable: Any = ...,
        shrink: Any = ...,
        space: Any = ...,
        space_x: Any = ...,
        space_y: Any = ...,
        tab_index: Any = ...,
        text_align: Any = ...,
        text_color: Any = ...,
        text_size: Any = ...,
        title: Any = ...,
        top: Any = ...,
        value: Any = ...,
        visible: Any = ...,
        z_index: Any = ...,
        zoom: Any = ...,
        fill: Any = ...,
        framed: Any = ...,
    ) -> None: ...
    theme: Any
    style_name: Any
    busy: Any
    empty_text: Any
    placeholder: Any
    show_input: Any
    @property
    def messages(self) -> Any: ...
    def message_text(self, key) -> Any: ...
    def add_message(self, text=..., role=..., key=...) -> Any: ...
    def append_text(self, key, piece) -> Any: ...
    def set_message_text(self, key, text) -> Any: ...
    def remove_message(self, key) -> Any: ...
    def clear(self) -> Any: ...
    def set_messages(self, messages) -> Any: ...
    def set_busy(self, value) -> Any: ...
    def send(self) -> Any: ...
    def stop(self) -> Any: ...
    @property
    def input_text(self) -> Any: ...
    def set_input_text(self, text) -> Any: ...
    def focus(self) -> Any: ...
    def set_placeholder(self, text) -> Any: ...
    def set_empty_text(self, text) -> Any: ...
    def set_show_input(self, value) -> Any: ...
    def scroll_to_end(self) -> Any: ...
    def scroll_to_top(self) -> Any: ...


def every(milliseconds: float, task: Callable[..., Any]) -> Callable[[], None]:
    """Runs task() again and again (the loop() of basic.js). Returns a function that stops it."""
    ...


def after(milliseconds: float, task: Callable[..., Any]) -> Callable[[], None]:
    """Runs task() once, after a time. Returns a function that cancels it."""
    ...


def call_soon(task: Callable[..., Any]) -> None:
    """Runs task() on the app thread, after the task that runs now. Any thread may call it."""
    ...


def run_in_background(job: Callable[..., Any], *args: Any) -> Any:
    """Runs job(*args) on a thread of its own, so the window does not wait for it (see App.run_in_background).
    Returns the thread.
    """
    ...


def open_file(file_types=..., directory=..., multiple=...) -> Any:
    """The path of the chosen file (a list with multiple=True), or None. file_types: ("Images (*.png;*.jpg)", ...)"""
    ...


def save_file(file_name=..., file_types=..., directory=...) -> str | None:
    """The path to save to, or None."""
    ...


def choose_folder(directory=...) -> str | None:
    """The path of the chosen folder, or None."""
    ...


def picture_address(picture: Any) -> str:
    """A picture as an address the page can show: a path (str or pathlib), bytes, a Pillow image, a matplotlib figure,
    or an address (http://, https://, data:). "" or None: no picture.

    WHY a data: address for what is on this computer: the web view refuses a file:// picture outside the folder of the
    page (WKWebView, measured 2026-11-05), and a data: address is fast enough: 8 MB in 150 ms, 32 MB in 0.7 s.
    """
    ...
