# Bismillah
"""test_ozdenui.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The Python side of OzdenUI, without a window: a fake window keeps what would go to the page.
Usage: .venv/bin/python -m pytest tests

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import base64
import dataclasses
import datetime
import json
import os
import re
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

import ozdenui
from ozdenui import (App, Box, Button, CheckBox, Component, Dialog, HGroup, Label, RadioButton, SmartButton, Tabs,
                     Toggle, VGroup, WindowClosed)
from ozdenui import app as app_module
from ozdenui.objects import Page, Part
from ozdenui.values import camel_case, event_name_of


class FakeWindow:
    """Keeps the scripts; answers __bp.apply() as the page does when nothing fails."""

    def __init__(self):
        self.scripts = []
        self.shown = 0
        self.loaded = []  # the addresses of load_url()
        self.failing_types = set()  # the page can not make these (Ex: {"Dialog"})
        self.drop_handlers = []
        self.dom = SimpleNamespace(document=SimpleNamespace(on=lambda event, handler: self.drop_handlers.append((event, handler))))

    def show(self):
        self.shown += 1

    def load_url(self, url):
        self.loaded.append(url)

    def evaluate_js(self, script, callback=None):
        self.scripts.append(script)
        if script.startswith("__bp.apply("):
            sent = json.loads(script[len("__bp.apply("):-1])
            errors = [{"op": "create", "id": c["id"], "src": c.get("src", ""), "message": "it failed"}
                      for c in sent if c["op"] == "create" and c["type"] in self.failing_types]
            return {"errors": errors, "removed": [], "ms": 0}
        return None

    def applied_commands(self):
        commands = []
        for script in self.scripts:
            if script.startswith("__bp.apply("):
                commands.extend(json.loads(script[len("__bp.apply("):-1]))
        return commands


@pytest.fixture
def app():
    application = App(lambda page: None)
    application._window = FakeWindow()
    application._app_thread_id = threading.get_ident()
    app_module._current = application
    application.page = Page(application, 800, 600)
    yield application
    app_module._current = None


@pytest.fixture
def dark_app():
    application = App(lambda page: None, theme="dark")
    application._window = FakeWindow()
    application._app_thread_id = threading.get_ident()
    app_module._current = application
    application._make_page()
    yield application
    app_module._current = None


def created(app, obj):
    return next(c for c in app._commands if c["op"] == "create" and c["id"] == obj._id)


def commands(app, op):
    return [c for c in app._commands if c["op"] == op]


def run_queued_tasks(app):
    while not app._tasks.empty():
        app._run_task(app._tasks.get())


# *** NAMES

def test_names():
    assert camel_case("font_size") == "fontSize"
    assert camel_case("fontSize") == "fontSize"
    assert camel_case("scroll_y") == "scrollY"
    assert event_name_of("on_click") == "click"
    assert event_name_of("on_mouse_enter") == "mouseenter"


# *** OBJECTS

def test_an_object_is_one_create_command(app):
    label = Label(text="Hi", font_size=20)
    command = created(app, label)
    assert command["type"] == "Label"
    assert command["props"]["plainText"] == "Hi"  # WHY plainText: the text of Python is shown as it is written
    assert command["props"]["fontSize"] == 20
    assert command["parent"] == "page"
    assert command["src"].startswith("test_ozdenui.py:")


def test_outside_a_group_an_object_starts_at_the_top_left(app):
    label = Label(text="free")
    assert created(app, label)["props"]["left"] == 0
    with VGroup() as group:
        in_group = Label(text="placed by the group")
        in_tab = Part(group, ["wrapper"])
        with in_tab:
            in_part = Label(text="placed by the part")
    assert "left" not in created(app, in_group)["props"]
    assert "left" not in created(app, in_part)["props"]
    with Box(0, 0, 100, 100):
        in_box = Label(text="in a box")
    assert created(app, in_box)["props"]["top"] == 0


def test_with_gives_the_parent(app):
    with VGroup() as outer:
        with HGroup() as inner:
            deep = Label(text="deep")
        beside = Label(text="beside")
    after = Label(text="after")
    assert created(app, inner)["parent"] == outer._id
    assert created(app, deep)["parent"] == inner._id
    assert created(app, beside)["parent"] == outer._id
    assert created(app, after)["parent"] == "page"


def test_only_a_box_holds_objects(app):
    with pytest.raises(TypeError, match="can not hold other objects"):
        with Label(text="x"):
            pass


def test_a_place_needs_all_four_values(app):
    with pytest.raises(TypeError, match="all four"):
        Box(10, 20)


def test_values_are_kept_in_python(app):
    label = Label(text="Hi")
    assert label.text == "Hi"
    label.text = "Yo"
    assert label.text == "Yo"
    assert commands(app, "set")[-1]["props"] == {"plainText": "Yo"}
    with pytest.raises(AttributeError, match="measure"):
        _ = label.color


def test_a_value_the_page_can_not_take_fails_at_its_line(app):
    with pytest.raises(TypeError, match=r"Label\(\): a object can not go to the page"):
        Label(text=object())


def test_dom_events_reach_the_handler_with_the_values_it_takes(app):
    calls = []
    button = Button(text="Go", on_click=lambda: calls.append("none"))
    button.on("click", lambda obj: calls.append(obj))
    button.on("click", lambda obj, event: calls.append(event["x"]))
    listens = [c for c in commands(app, "listen") if c["id"] == button._id]
    assert [c["event"] for c in listens] == ["click"]
    app._dispatch(button._id, "click", {"x": 12})
    assert calls == ["none", button, 12]


def test_the_text_of_an_input_is_kept_from_its_events(app):
    field = ozdenui.Input(width=200, height=40)
    app._dispatch(field._id, "input", {"text": "typed"})
    assert field.text == "typed"


def test_flush_sends_the_commands_in_one_call(app):
    for number in range(3):
        Label(text=str(number))
    app.flush()
    applies = [s for s in app._window.scripts if s.startswith("__bp.apply(")]
    assert len(applies) == 1
    assert len([c for c in app._window.applied_commands() if c["op"] == "create"]) == 3
    assert app._commands == []


# *** COMPONENTS

def test_a_component_takes_its_place_as_params(app):
    gauge = Component("Gauge", 1, 2, 3, 4, value=5)
    command = created(app, gauge)
    assert command["args"] == []
    assert command["props"] == {"left": 1, "top": 2, "width": 3, "height": 4, "value": 5}


def test_an_object_given_to_a_component_is_a_reference(app):
    button = Button(text="Go")
    tip = Component("Tooltip", target=button, hint_text="Click")
    assert created(app, tip)["props"]["target"] == {"__bpObject": button._id}


def test_a_callback_param_keeps_the_state(app):
    seen = []
    box = CheckBox(text="Remember", on_change=lambda checkbox: seen.append(checkbox.checked))
    props = created(app, box)["props"]
    assert props["labelText"] == "Remember"
    assert "styleName" not in props  # the default of the component: "classic"
    assert created(app, box)["state"] == {"checked": "checked"}
    callback_id = props["onChange"]["__bpCallback"]
    app._dispatch(callback_id, "callback", {"args": [{"__bpObject": box._id}], "state": {"checked": 1}})
    assert seen == [True]
    assert box.checked is True


def test_setting_a_value_calls_the_method_silently(app):
    box = CheckBox(text="Remember")
    box.checked = True
    assert commands(app, "call")[-1]["method"] == "setChecked"
    assert commands(app, "call")[-1]["args"] == [1, 1]
    assert box.checked is True


def test_a_short_name_and_its_setter(app):
    button = SmartButton(text="Go")
    assert created(app, button)["props"]["labelText"] == "Go"
    assert "text" not in created(app, button)["props"]  # WHY: text is a setter of basic.js (the inner HTML)
    assert button.text == "Go"
    button.text = "Stop"
    assert commands(app, "call")[-1] == {**commands(app, "call")[-1], "method": "setLabelText", "args": ["Stop"]}
    assert button.text == "Stop"


def test_the_placeholder_and_the_length_of_a_textarea(app):
    area = ozdenui.TextAreaField(title_text="Note")
    area.placeholder = "Write a note"
    area.max_length = 500
    methods = [(c["method"], c["args"]) for c in commands(app, "call")]
    assert methods == [("setPlaceholder", ["Write a note"]), ("setMaxLength", [500])]
    assert area.placeholder == "Write a note" and area.max_length == 500


def test_true_and_false_go_as_one_and_zero(app):
    toggle = Toggle(value=True)
    assert created(app, toggle)["props"]["value"] == 1
    assert toggle.value is True


def test_a_radio_unchecks_the_others_of_its_group(app):
    radios = [RadioButton(group="size", value=size, text=size, checked=(size == "S")) for size in "SML"]
    callback_id = created(app, radios[1])["props"]["onChange"]["__bpCallback"]
    app._dispatch(callback_id, "callback", {"args": [], "state": {"checked": 1}})
    assert [radio.checked for radio in radios] == [False, True, False]
    assert RadioButton.value_of("size") == "M"


def test_the_panel_of_a_tab_is_made_once(app):
    tabs = Tabs(tabs=["A", "B"])
    panel = tabs.panel("A")
    assert tabs.panel("A") is panel
    calls = commands(app, "call")
    assert len(calls) == 1
    assert calls[0]["method"] == "setPanelContent" and calls[0]["args"] == ["A", {"__bpNoop": 1}]
    part = commands(app, "part")[0]
    assert part["path"] == [{"call": "getPanel", "args": ["A"]}, "wrapper"]
    assert tabs.value == "A"


def test_a_row_of_a_component_comes_as_its_id_and_data(app):
    value = app._python_value({"__bpObject": None, "id": 3, "data": {"name": "Ada"}})
    assert value == {"id": 3, "data": {"name": "Ada"}}
    assert app._python_value({"__bpObject": None}) is None


# *** THREADS, ORDER, WAITING

def test_the_events_run_in_the_order_of_the_page():
    delivered = []
    order = app_module._EventOrder(delivered.append)
    order.add(2, "second")
    assert delivered == []
    order.add(1, "first")
    order.add(3, "third")
    assert delivered == ["first", "second", "third"]


# *** THE FINDINGS OF THE REVIEW (2026-11-03)

def test_1_a_dialog_in_start_shows_the_window_first(app):
    helper = threading.Thread(target=answer_when_sent, args=(app, False))
    helper.start()
    Dialog.confirm("Load the last file?")
    helper.join()
    assert app._window.shown == 1


def test_2_a_task_that_runs_while_another_waits_has_its_own_with_blocks(app):
    made = {}
    with VGroup():
        app._run_task(lambda: made.setdefault("label", Label(text="tick")))
    command = next(c for c in app._window.applied_commands() if c.get("id") == made["label"]._id)
    assert command["parent"] == "page"
    assert command["props"]["left"] == 0


def test_3_a_slider_and_a_bar_keep_their_value_inside_its_range(app):
    slider = ozdenui.SliderField(min_value=0, max_value=10)
    slider.value = 15
    assert slider.value == 10
    assert commands(app, "call")[-1]["refresh"] == 1
    app._dispatch(slider._id, "__state", {"state": {"value": 9}})
    assert slider.value == 9  # the page says the last word
    bar = ozdenui.ProgressBar(max_value=100)
    bar.value = 150
    assert bar.value == 100


def test_4_the_items_of_a_list_have_the_keys_of_the_page(app):
    lst = ozdenui.ItemList(items=["A", "B", "C"])
    assert [item["key"] for item in lst.items] == ["0", "1", "2"]
    lst.add_item("K", 0)
    assert lst.items[0] == {"key": "3", "text": "K"}
    lst.remove_item("0")
    assert [item["text"] for item in lst.items] == ["K", "B", "C"]
    lst.add_item({"key": "a", "text": "Apple"})
    with pytest.raises(ValueError, match="already"):
        lst.add_item({"key": "a", "text": "Another"})


def test_4_a_picture_of_an_item_is_given_with_its_python_name(app, tmp_path):
    photo = tmp_path / "sea.png"
    photo.write_bytes(b"\x89PNG\r\n\x1a\n")
    lst = ozdenui.ItemList(layout="grid", style_name="gallery",
                           items=[{"text": "Sea", "icon_file": photo, "search_text": "deniz"},
                                  {"text": "Web", "iconFile": "https://example.com/a.png"}])
    sea, web = lst.items
    assert sea["iconFile"].startswith("data:image/png;base64,") and "icon_file" not in sea and sea["searchText"] == "deniz"
    assert web["iconFile"] == "https://example.com/a.png"  # the name of the page goes as it is
    lst.add_item({"text": "Bytes", "icon_file": b"<svg xmlns='http://www.w3.org/2000/svg'/>"})
    assert commands(app, "call")[-1]["args"][0]["iconFile"].startswith("data:")


def test_5_the_rows_of_a_table_are_kept_in_python(app):
    table = ozdenui.SmartTable(columns=[{"key": "name"}, {"key": "age"}], rows=[{"name": "Ada", "age": 36}, ["Can", 7]])
    assert table.rows == [{"name": "Ada", "age": 36}, {"name": "Can", "age": 7}]  # a list is a row by the columns
    table.add_row(["Cem", 8])
    table.remove_row({"name": "Ada", "age": 36})
    assert [row["name"] for row in table.rows] == ["Can", "Cem"]
    last_call = commands(app, "call")[-1]
    assert last_call["method"] == "setItemDataList" and last_call["args"][0] == table.rows
    table.clear_rows()
    assert table.rows == []


def test_a_smart_table_names_its_columns_and_its_size_as_the_page_does(app):
    table = ozdenui.SmartTable(10, 20, "50%", 300, style={"round": 4}, line_count=7, columns=[
        {"key": "name", "title": "Name", "width": 200, "sortable": False}, {"key": "age", "type": "integer"}])
    props = created(app, table)["props"]
    assert props["titleDataList"] == [
        {"dataTitle": "name", "name": "Name", "dataType": "string", "width": 200, "sortable": 0},
        {"dataTitle": "age", "name": "age", "dataType": "integer", "sortable": 1},
    ]
    assert props["style"] == {"round": 4, "width": "50%", "height": 300}
    assert (props["left"], props["top"], props["fitLineCount"], props["itemLineCount"]) == (10, 20, 1, 7)
    assert "width" not in props and "height" not in props
    plain = ozdenui.SmartTable(columns=[{"key": "a"}])
    plain_props = created(app, plain)["props"]
    assert plain_props["style"] == {"width": "100%", "height": "auto"} and plain_props["fitLineCount"] == 0


def test_on_select_of_a_smart_table_gives_the_table_first(app):
    seen = []
    table = ozdenui.SmartTable(columns=[{"key": "a"}], on_select=lambda t, row: seen.append((t, row)))
    only_row = ozdenui.SmartTable(columns=[{"key": "a"}], on_select=lambda: seen.append("none"))
    callback = created(app, table)["props"]["onSelect"]["__bpCallback"]
    app._dispatch(callback, "callback", {"args": [{"__bpObject": table._id}, {"a": 1}], "state": None})
    only_row_callback = created(app, only_row)["props"]["onSelect"]["__bpCallback"]
    app._dispatch(only_row_callback, "callback", {"args": [{"__bpObject": only_row._id}, {"a": 2}], "state": None})
    assert seen == [(table, {"a": 1}), "none"]


def test_a_log_view_writes_and_asks(app):
    log = ozdenui.LogView(max_lines=50)
    log.info("One")
    log.warn(404)  # not a text: it becomes one
    log.add_line("Two", "debug")
    log.clear()
    log.set_levels(("warn", "error"))
    log.wrap_lines = False
    calls = [(c["method"], c["args"]) for c in commands(app, "call")]
    assert calls == [("addLine", ["One", "info"]), ("addLine", ["404", "warn"]), ("addLine", ["Two", "debug"]),
                     ("clearLines", []), ("setLevels", [["warn", "error"]]), ("setWrapLines", [0])]
    log.get_text()
    assert app._window.scripts[-1].startswith("__bp.ask(") and "getText" in app._window.scripts[-1]


def test_capture_print_writes_whole_lines_and_gives_back_the_terminal(app, capsys):
    import sys

    log = ozdenui.LogView()
    old_out = sys.stdout
    stop = log.capture_print()
    print("first")
    print("sec", end="")
    print("ond")
    sys.stderr.write("broken\n")
    stop()
    assert sys.stdout is old_out
    lines = [c["args"] for c in commands(app, "call") if c["method"] == "addLine"]
    assert lines == [["first", "info"], ["second", "info"], ["broken", "error"]]
    assert "first" in capsys.readouterr().out  # the terminal has it too
    silent = log.capture_print(errors=False, terminal=False)
    print("only in the window")
    silent()
    assert "only in the window" not in capsys.readouterr().out


def test_the_logging_module_goes_by_its_levels(app):
    import logging

    log = ozdenui.LogView()
    logger = logging.getLogger("ozdenui-test")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    handler = log.logging_handler(logging.DEBUG)
    logger.addHandler(handler)
    logger.debug("a")
    logger.info("b")
    logger.warning("c")
    logger.error("d")
    logger.critical("e")
    logger.removeHandler(handler)
    lines = [c["args"] for c in commands(app, "call") if c["method"] == "addLine"]
    assert lines == [["a", "debug"], ["b", "info"], ["c", "warn"], ["d", "error"], ["e", "error"]]


# *** THE THEME OF THE WINDOW

def test_the_theme_of_a_window_is_a_known_one():
    assert App(lambda page: None).theme == "light"
    assert App(lambda page: None, theme="dark").theme == "dark"
    with pytest.raises(ValueError, match="light"):
        App(lambda page: None, theme="blue")


def test_set_theme_draws_the_page_again_in_the_other_theme(app, capsys):
    # WHY a new page: a component takes its look when it is made; start() makes it again in the new theme
    themes = []

    def start(page):
        themes.append(app.theme)
        ozdenui.ItemList()

    app._start = start
    app._ready.set()
    stop_tick = app.every(1000, lambda: None)
    app.set_theme("dark")
    assert app.theme == "light"  # after the task that runs now
    run_queued_tasks(app)
    assert app.theme == "dark" and app._window.loaded == [app_module._page_address()]
    assert 'window.name = "ozdenui-page-color:#1C1C1B"' in app._window.scripts
    assert not app._timers  # WHY: a tick sent its commands to the page that was being loaded
    scripts = len(app._window.scripts)
    Label(text="for the old page")
    app.flush()
    assert len(app._window.scripts) == scripts  # nothing goes to a page that is being loaded
    app._on_page_ready("26.11.10", 800, 600)
    run_queued_tasks(app)
    assert themes == ["dark"]
    item_list = next(obj for obj in app._objects.values() if isinstance(obj, ozdenui.ItemList))
    made = next(c for c in app._window.applied_commands() if c["op"] == "create" and c["id"] == item_list._id)
    assert made["props"]["styleName"] == "ozdenDark"
    assert "loaded again" not in capsys.readouterr().err  # the program asked for it
    stop_tick()


def test_set_theme_auto_follows_the_system_and_the_same_theme_changes_nothing(app):
    app._on_page_ready("26.11.10", 800, 600, True)  # the system asks for dark; the window stays light
    assert app.theme == "light"
    app.set_theme("light")
    run_queued_tasks(app)
    assert app._window.loaded == []
    app.set_theme("auto")
    run_queued_tasks(app)
    assert app.theme == "dark" and len(app._window.loaded) == 1
    with pytest.raises(ValueError, match="light"):
        app.set_theme("blue")


def test_auto_asks_the_page_before_start():
    follows = App(lambda page: None, theme="auto")
    assert follows.theme == "light"
    follows._on_page_ready("26.11", 800, 600, True)
    assert follows.theme == "dark"
    light = App(lambda page: None, theme="light")
    light._on_page_ready("26.11", 800, 600, True)  # WHY: only "auto" follows the system
    assert light.theme == "light"


def test_every_class_takes_its_dark_look_in_a_dark_window(dark_app):
    columns = [{"key": "a"}]
    expected = [
        (ozdenui.SmartButton(text="A"), "ozdenDark"), (CheckBox(), "dark"), (RadioButton(group="g"), "dark"),
        (Toggle(), "ozdenDark"), (ozdenui.SelectBox(), "dark"), (ozdenui.TextAreaField(), "dark"), (ozdenui.SliderField(), "dark"),
        (ozdenui.ProgressBar(), "dark"), (ozdenui.ItemList(), "ozdenDark"), (ozdenui.SmartTable(columns=columns), "dark"),
        (Tabs(tabs=["A"]), "dark"), (ozdenui.LogView(), "dark"), (ozdenui.ImageView(), "dark"), (ozdenui.MenuBar(), "dark"),
        (ozdenui.StatusBar(), "dark"), (ozdenui.Splitter(), "dark"), (ozdenui.CodeEditor(), "dark"),
        (Component("TreeView"), "dark"), (Component("EmailField"), "dark"), (Component("UrlField"), "dark"),
        (ozdenui.TextField(), "dark"), (ozdenui.EmailField(), "dark"), (ozdenui.PasswordField(), "dark"),
        (ozdenui.NumberField(), "dark"), (ozdenui.Slider(), "roundDark"), (ozdenui.SearchInput(), "ozdenDark"),
        (ozdenui.TreeView(), "dark"), (ozdenui.ContextMenu(), "dark"), (ozdenui.DatePicker(), "dark"), (ozdenui.TimePicker(), "dark"),
        (ozdenui.ColorPicker(), "dark"), (ozdenui.Stepper(), "dark"), (ozdenui.FilePicker(), "dark"), (ozdenui.Accordion(), "dark"),
        (ozdenui.ToolBar(), "dark"), (ozdenui.MarkdownView(), "dark"), (ozdenui.JsonView(), "dark"), (ozdenui.RangeSlider(), "roundDark"), (ozdenui.StepBar(), "dark"), (ozdenui.Canvas(), "dark"),
        (ozdenui.JsonEditor(), "dark"), (ozdenui.UrlField(), "dark"), (ozdenui.PhoneField(), "dark"),
        (ozdenui.CurrencyField(), "dark"), (ozdenui.SortableList(), "dark"),
    ]
    for obj, style_name in expected:
        assert created(dark_app, obj)["props"].get("styleName") == style_name, obj
    # A component with no dark look keeps its look; two take a theme, not a package.
    assert "styleName" not in created(dark_app, Component("Filters"))["props"]
    graph = created(dark_app, Component("GraphBox"))["props"]
    assert graph["theme"] == "dark" and "styleName" not in graph
    graph = created(dark_app, ozdenui.GraphBox())["props"]
    assert graph["theme"] == "dark" and "styleName" not in graph


def test_a_look_given_by_the_code_stays_in_a_dark_window(dark_app):
    assert created(dark_app, CheckBox(style_name="modern"))["props"]["styleName"] == "modern"
    assert created(dark_app, ozdenui.LogView(theme="light"))["props"]["styleName"] == "light"
    assert created(dark_app, Component("TreeView", styleName="classic"))["props"]["styleName"] == "classic"
    named = ozdenui.SmartButton(text="A", style_name="ozden3", tone="cyan")
    assert created(dark_app, named)["props"]["tone"] == "cyan"  # a page that names its template has chosen its colors


def test_a_light_package_with_a_dark_twin_turns_dark(dark_app):
    assert created(dark_app, ozdenui.ItemList(layout="grid", style_name="gallery"))["props"]["styleName"] == "galleryDark"
    assert created(dark_app, ozdenui.ItemList(style_name="light"))["props"]["styleName"] == "light"  # no twin: it stays


def test_a_light_window_changes_nothing(app):
    assert "styleName" not in created(app, CheckBox())["props"]
    assert "styleName" not in created(app, ozdenui.ProgressBar())["props"]  # the default of the kit: light
    assert created(app, ozdenui.SmartButton(text="A", tone="cyan"))["props"]["tone"] == "cyan"
    assert "textColor" not in created(app, Label(text="A"))["props"]
    assert "color" not in created(app, Box(0, 0, 10, 10))["props"]
    assert not [c for c in app._commands if c["op"] == "set" and c["id"] == "page"]


def make_minimal_app(theme, **options):
    application = App(lambda page: None, theme=theme, style="minimal", **options)
    application._window = FakeWindow()
    application._app_thread_id = threading.get_ident()
    app_module._current = application
    application._make_page()
    return application


def test_a_minimal_window_gives_the_minimal_looks():
    with pytest.raises(ValueError, match="minimal"):
        App(lambda page: None, style="thin")
    try:
        light = make_minimal_app("light")
        assert created(light, ozdenui.SmartButton(text="A"))["props"]["styleName"] == "minimal"
        assert created(light, CheckBox())["props"]["styleName"] == "minimal"
        assert created(light, RadioButton(group="g"))["props"]["styleName"] == "minimal"
        assert created(light, Toggle())["props"]["styleName"] == "minimal"
        assert created(light, ozdenui.ProgressBar())["props"]["styleName"] == "minimal"
        assert "style" not in created(light, ozdenui.ProgressBar())["props"]  # the ink of the package
        assert created(light, ozdenui.TextField())["props"]["styleName"] == "minimal"
        assert created(light, ozdenui.TextAreaField())["props"]["styleName"] == "minimal"
        assert created(light, ozdenui.TreeView())["props"]["styleName"] == "minimal"
        assert created(light, ozdenui.JsonEditor())["props"]["styleName"] == "minimal"
        assert created(light, ozdenui.ChatView())["props"]["styleName"] == "minimal"
        assert created(light, ozdenui.GraphBox())["props"]["theme"] == "minimal"
        assert created(light, Component("TagInput"))["props"]["styleName"] == "minimal"
        assert created(light, CheckBox(style_name="modern"))["props"]["styleName"] == "modern"  # the code chose
        assert created(light, ozdenui.SmartButton(text="B", tone="ink"))["props"]["tone"] == "ink"
        dark = make_minimal_app("dark")
        assert created(dark, ozdenui.SmartButton(text="A", tone="ink"))["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.SmartButton(text="B", tone="ink"))["props"]["tone"] == "inkDark"
        assert created(dark, Toggle())["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.Slider())["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.RangeSlider())["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.TreeView())["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.JsonEditor())["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.ChatView())["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.MenuBar())["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.GraphBox())["props"]["theme"] == "minimalDark"  # a theme param, not a package
        assert created(dark, ozdenui.GraphBox(theme="light"))["props"]["theme"] == "light"  # the code chose
        assert created(dark, ozdenui.Accordion())["props"]["styleName"] == "minimalDark"
        assert created(dark, ozdenui.SmartButton(text="Delete", style_name="minimalDanger"))["props"]["styleName"] == "minimalDangerDark"
        assert created(dark, Component("DatePicker"))["props"]["styleName"] == "minimalDark"
        assert created(dark, Component("LoadingScreen"))["props"]["styleName"] == "minimalDark"
        ozdenui.Toast.show("Saved")
        toast = [c for c in dark._commands if c.get("op") == "static" or c.get("method") == "show"][-1]
        assert "minimalDark" in json.dumps(toast)
    finally:
        app_module._current = None


def test_an_accent_gives_the_minimal_packages_of_its_color():
    with pytest.raises(ValueError, match="minimal"):
        App(lambda page: None, accent="#2A78D6")
    with pytest.raises(ValueError, match="accent"):
        App(lambda page: None, style="minimal", accent_dark="#7FB6DE")
    with pytest.raises(TypeError, match="color"):
        App(lambda page: None, style="minimal", accent=(42, 120, 214))
    try:
        light = make_minimal_app("light", accent="#2A78D6")
        light._add_accent_packages()
        made = [c for c in light._commands if c["op"] == "static" and c["target"] == "MinimalAccent"]
        assert made[0]["method"] == "addPackages" and made[0]["args"] == ["minimalAccent", "#2A78D6", ""]
        assert created(light, Toggle())["props"]["styleName"] == "minimalAccent"
        assert created(light, ozdenui.SmartButton(text="A"))["props"]["styleName"] == "minimalAccent"
        assert created(light, ozdenui.SmartButton(text="Send", tone="accent"))["props"]["tone"] == "minimalAccent"
        assert created(light, ozdenui.SmartButton(text="B", tone="ink"))["props"]["tone"] == "ink"  # the code chose
        delete = ozdenui.SmartButton(text="Delete", style_name="minimalDanger")
        assert created(light, delete)["props"]["styleName"] == "minimalDanger"
        assert created(light, ozdenui.GraphBox())["props"]["theme"] == "minimal"  # its series have their own colors
        ozdenui.Toast.show("Saved")
        assert "minimalAccent" in json.dumps(light._commands[-1])
        dark = make_minimal_app("dark", accent="#2A78D6", accent_dark="#7FB6DE")
        dark._add_accent_packages()
        made = [c for c in dark._commands if c["op"] == "static" and c["target"] == "MinimalAccent"]
        assert made[0]["args"] == ["minimalAccent", "#2A78D6", "#7FB6DE"]
        assert created(dark, Toggle())["props"]["styleName"] == "minimalAccentDark"
        assert created(dark, ozdenui.SmartButton(text="Send", tone="accent"))["props"]["tone"] == "minimalAccentDark"
        plain = make_minimal_app("light")
        plain._add_accent_packages()
        assert not [c for c in plain._commands if c["op"] == "static"]  # no accent: nothing to make
        assert created(plain, ozdenui.SmartButton(text="Send", tone="accent"))["props"]["tone"] == "ink"
    finally:
        app_module._current = None


def test_tone_accent_is_the_main_action_of_a_usual_window(dark_app):
    assert created(dark_app, ozdenui.SmartButton(text="Send", tone="accent"))["props"]["tone"] == "cyanDark"
    button = ozdenui.SmartButton(text="Send", style_name="ozden2", tone="accent")
    assert created(dark_app, button)["props"]["tone"] == "cyanDark"  # accent is not a tone of the page: it becomes one


def test_the_tones_of_a_button_turn_dark(dark_app):
    button = ozdenui.SmartButton(text="A", tone="cyan")
    assert created(dark_app, button)["props"]["tone"] == "cyanDark"
    white = ozdenui.SmartButton(text="B", tone="white")
    assert created(dark_app, white)["props"]["tone"] == "white"  # it has no dark one
    button.tone = "orange"
    assert commands(dark_app, "call")[-1]["method"] == "setTone" and commands(dark_app, "call")[-1]["args"] == ["orangeDark"]
    assert button.tone == "orange"  # as the code wrote it


def test_the_plain_objects_and_the_page_are_dark_too(dark_app):
    assert [c["props"] for c in dark_app._commands if c["op"] == "set" and c["id"] == "page"] == [{"color": "#1C1C1B"}]
    assert created(dark_app, Label(text="A"))["props"]["textColor"].startswith("rgba(255")
    assert created(dark_app, Label(text="B", text_color="red"))["props"]["textColor"] == "red"
    assert created(dark_app, Box(0, 0, 10, 10))["props"]["color"] == "#232322"
    assert created(dark_app, Box(0, 0, 10, 10, color="transparent"))["props"]["color"] == "transparent"
    assert "color" not in created(dark_app, VGroup())["props"]  # a group has no ground of its own
    assert "color" not in created(dark_app, HGroup())["props"]
    assert created(dark_app, ozdenui.Input())["props"]["color"] == "#2A2A29"


def test_the_dialogs_and_the_toasts_are_dark_too(dark_app):
    ozdenui.Toast.success("Saved")
    toast = commands(dark_app, "static")[-1]
    assert toast["args"][0]["theme"] == "dark"
    ozdenui.Toast.THEME = "light"
    try:
        ozdenui.Toast.info("A")
        assert commands(dark_app, "static")[-1]["args"][0]["theme"] == "light"
    finally:
        ozdenui.Toast.THEME = None
    answers = []

    def fake_call_static(target, method, page_args, wait_for_answer=False):
        answers.append((target, method, page_args[0]))

    dark_app._call_static = fake_call_static
    Dialog.confirm("Sure?")
    Dialog.alert("Done")
    assert [a[2]["styleName"] for a in answers] == ["ozdenDark", "ozdenDark"]


def test_an_icon_loads_its_picture(app):
    icon = ozdenui.Icon(0, 0, 48, 48, picture=b"\x89PNG")
    icon.picture = "https://a.com/b.png"
    calls = commands(app, "call")
    assert [c["method"] for c in calls] == ["load", "load"]
    assert calls[0]["args"][0].startswith("data:image/png;base64,") and calls[1]["args"] == ["https://a.com/b.png"]
    assert "picture" not in created(app, icon)["props"] and not commands(app, "set")
    assert icon.picture == "https://a.com/b.png"


def test_a_picture_becomes_an_address(tmp_path):
    from ozdenui import picture_address

    png = b"\x89PNG\r\n\x1a\nrest"
    file = tmp_path / "photo.png"
    file.write_bytes(png)
    encoded = base64.b64encode(png).decode("ascii")
    assert picture_address(str(file)) == "data:image/png;base64," + encoded
    assert picture_address(file) == "data:image/png;base64," + encoded  # pathlib
    assert picture_address(png) == "data:image/png;base64," + encoded
    assert picture_address(b"\xff\xd8abc").startswith("data:image/jpeg;base64,")
    assert picture_address(b"<svg></svg>").startswith("data:image/svg+xml;base64,")
    assert picture_address("https://a.com/b.png") == "https://a.com/b.png"
    assert picture_address("data:image/png;base64,AA") == "data:image/png;base64,AA"
    assert picture_address("") == "" and picture_address(None) == ""
    with pytest.raises(FileNotFoundError):
        picture_address(str(tmp_path / "no.png"))

    class Figure:
        def savefig(self, buffer, format, bbox_inches):
            buffer.write(b"figure-" + format.encode("ascii"))

    class PillowImage:
        mode = "RGB"

        def save(self, buffer, format):
            buffer.write(b"pillow-" + format.encode("ascii"))

    assert base64.b64decode(picture_address(Figure()).split(",")[1]) == b"figure-png"
    assert base64.b64decode(picture_address(PillowImage()).split(",")[1]) == b"pillow-PNG"


def test_an_image_view_sends_an_address_and_keeps_its_zoom(app):
    view = ozdenui.ImageView(image=b"\x89PNG", alt="A plot")
    props = created(app, view)["props"]
    assert props["imageFile"].startswith("data:image/png;base64,") and props["altText"] == "A plot"
    callback = props["onZoomChange"]["__bpCallback"]
    app._dispatch(callback, "callback", {"args": [{"__bpObject": view._id}], "state": {"zoomLevel": 2.5, "naturalWidth": 64, "naturalHeight": 48}})
    assert (view.zoom_level, view.natural_width, view.natural_height) == (2.5, 64, 48)
    view.set_image(b"\xff\xd8")
    view.image = b"\x89PNG"
    view.set_zoom_level(3)
    calls = [c for c in commands(app, "call")]
    assert calls[0]["method"] == "setImage" and calls[0]["args"][0].startswith("data:image/jpeg")
    assert calls[1]["method"] == "setImage" and calls[1]["args"][0].startswith("data:image/png")
    assert calls[2]["method"] == "setZoomLevel" and calls[2]["refresh"] == 1


def test_a_menu_bar_names_the_keys_of_its_items_at_every_level(app):
    clicks = []
    bar = ozdenui.MenuBar(menus=[{"text": "File", "items": [
        {"text": "Save", "key": "save", "on_click": lambda: clicks.append("save")},
        "-",
        {"text": "Recent", "icon_file": "x.png", "items": [{"text": "a", "on_click": lambda b, item: clicks.append((b, item["text"]))}]},
    ]}])
    menu = created(app, bar)["props"]["menus"][0]
    save = menu["items"][0]
    assert "on_click" not in save and "__bpCallback" in save["onClick"] and menu["items"][1] == "-"
    recent = menu["items"][2]
    assert recent["iconFile"] == "x.png"
    app._dispatch(save["onClick"]["__bpCallback"], "callback", {"args": [{"__bpObject": bar._id}, {"text": "Save"}, {}], "state": None})
    app._dispatch(recent["items"][0]["onClick"]["__bpCallback"], "callback", {"args": [{"__bpObject": bar._id}, {"text": "a"}, {}], "state": None})
    assert clicks == ["save", (bar, "a")]
    bar.set_item_checked("x", True)
    bar.set_menus([{"text": "New", "items": [{"text": "b", "on_click": lambda: None}]}])
    calls = commands(app, "call")
    assert calls[0]["args"] == ["x", 1]
    assert "onClick" in calls[1]["args"][0][0]["items"][0]


def test_a_status_bar_keeps_its_own_place(app):
    bar = ozdenui.StatusBar(message="Ready", items=["UTF-8", {"key": "z", "text": "1", "on_click": lambda: None}])
    props = created(app, bar)["props"]
    assert "top" not in props and props["messageText"] == "Ready"  # WHY: a top would hold it at the top of a Box
    assert props["items"][0] == "UTF-8" and "onClick" in props["items"][1]
    box_in_group = None
    with VGroup():
        box_in_group = ozdenui.LogView()
    assert "top" not in created(app, box_in_group)["props"]
    in_page = ozdenui.LogView()
    assert created(app, in_page)["props"]["top"] == 0  # the other components start at the corner
    bar.set_message("Saved", "success", 3000)
    assert commands(app, "call")[-1]["args"] == ["Saved", "success", 3000]
    assert bar.message == "Saved"


def test_set_theme_changes_the_package_in_place(app):
    objects = [ozdenui.LogView(), ozdenui.ImageView(), ozdenui.MenuBar(), ozdenui.StatusBar(), ozdenui.Splitter(), ozdenui.CodeEditor(theme="dark")]
    assert created(app, objects[5])["props"]["styleName"] == "dark"
    for obj in objects[:5]:
        obj.set_theme("dark")
    objects[0].theme = "light"
    objects[1].style_name = "light"
    calls = [c for c in commands(app, "call") if c["method"] == "setTheme"]
    assert [c["args"] for c in calls] == [["dark"]] * 5 + [["light"]] * 2
    assert objects[0].theme == "light" and objects[1].style_name == "light"


def test_the_areas_of_a_splitter_hold_objects(app):
    split = ozdenui.Splitter(first_size=240)
    with split.first as area:
        label = Label(text="Inside")
    assert split.first is area  # one proxy for each area
    assert created(app, label)["parent"] == area._id and "left" not in created(app, label)["props"]
    parts = commands(app, "part")
    assert [p["path"] for p in parts] == [["first"]] and parts[0]["of"] == split._id
    assert created(app, split)["state"] == {"firstSizeNow": "getFirstSize()"}
    split.set_first_size("40%")
    assert commands(app, "call")[-1]["args"] == ["40%", 1]


def test_a_code_editor_asks_for_its_text(app):
    seen = []
    editor = ozdenui.CodeEditor(value="x = 1", language="python", on_cursor_change=lambda e: seen.append(e.cursor_line))
    props = created(app, editor)["props"]
    assert props["value"] == "x = 1" and props["language"] == "python"
    assert "value" not in created(app, editor)["state"]  # WHY: a big text does not go to Python at every key
    app._dispatch(props["onCursorChange"]["__bpCallback"], "callback", {"args": [{"__bpObject": editor._id}], "state": {"cursorLine": 7, "cursorColumn": 2}})
    assert seen == [7] and editor.cursor_column == 2
    editor.value = "y = 2"
    editor.language = "json"
    editor.read_only = True
    calls = [(c["method"], c["args"]) for c in commands(app, "call")]
    assert calls == [("setValue", ["y = 2", 1]), ("setLanguage", ["json"]), ("setReadOnly", [1])]
    _ = editor.value
    assert app._window.scripts[-1].startswith("__bp.ask(") and "getValue" in app._window.scripts[-1]


def test_6_a_function_set_as_a_value_listens_and_replaces_the_one_before(app):
    calls = []
    button = Button(text="Go")
    button.on("click", lambda: calls.append("on"))
    button.on_click = lambda: calls.append("first")
    button.on_click = lambda: calls.append("second")
    app._dispatch(button._id, "click", {})
    assert calls == ["on", "second"]
    assert all("onClick" not in c["props"] for c in commands(app, "set"))


def test_7_the_size_of_the_page_is_always_current(app):
    assert any(c["id"] == "page" and c["event"] == "resize" for c in commands(app, "listen"))
    app._dispatch("page", "resize", {"state": {"width": 1024, "height": 700}})
    assert (app.page.width, app.page.height) == (1024, 700)


def test_8_true_and_false_go_as_one_and_zero_in_set_too(app):
    slider = ozdenui.SliderField()
    slider.set(editable=False)  # a param with no method of the kit: a value of the page
    assert commands(app, "set")[-1]["props"]["editable"] == 0
    slider.set(show_ticks=False)  # one with a method (setShowTicks): the method gets it
    assert calls(app, slider, "setShowTicks")[-1]["args"] == [0]
    select = ozdenui.SelectBox(options=[True, False], value=True)
    assert created(app, select)["props"]["options"] == [True, False]  # data stays as it is
    assert created(app, select)["props"]["value"] is True


def test_9_the_callbacks_of_removed_objects_are_forgotten(app):
    box = CheckBox(on_change=lambda checkbox: None)
    first_id = created(app, box)["props"]["onChange"]["__bpCallback"]
    box.set(on_change=lambda checkbox: None)
    assert first_id not in app._callbacks
    assert any(owner == box._id for _, _, owner in app._callbacks.values())
    app._after_apply({"errors": [], "removed": [box._id]})
    assert box._id not in app._objects  # its DOM events are not handled any more
    run_queued_tasks(app)  # WHY: forgotten after the events the page sent before (see the test of a Dialog below)
    assert not any(owner == box._id for _, _, owner in app._callbacks.values())
    assert box._id not in app._leaving


def test_a_function_given_as_none_is_the_default_of_the_component(app):
    # WHY: None went to the page as null and the component called it: an error of the page at every click, and
    #      box.checked never changed in Python
    box = CheckBox(text="Remember me", on_change=None)
    app._dispatch(callback_of(app, box, "onChange"), "callback", {"args": [], "state": {"checked": 1}})
    assert box.checked is True
    button = SmartButton(text="Save", on_click=None)
    assert created(app, button)["props"]["onClick"] == {"__bpNoop": 1}
    view = ozdenui.MarkdownView(text="[a](https://example.com)", on_link_click=None)
    assert created(app, view)["props"]["onLinkClick"] is None  # the null of the kit: the browser opens the link
    switch = Toggle(on_mark=None)
    assert created(app, switch)["props"]["onMark"] is None  # WHY: not a function: on_mark is a text ("check", "ON")
    field = ozdenui.TextField(on_change=lambda f: None)
    first_id = callback_of(app, field, "onChange")
    field.on_change = None
    assert first_id not in app._callbacks
    assert commands(app, "set")[-1]["props"]["onChange"]["__bpCallback"] in app._callbacks  # its text still comes


def test_a_handler_set_to_none_is_taken_away(app):
    seen = []
    label = Label(text="Go", on_click=lambda: seen.append("click"))
    label.on_click = None
    app._dispatch(label._id, "click", {})
    assert seen == []
    other = Label(text="Stay", on_click=None)
    assert "onClick" not in created(app, other)["props"]


def test_new_items_forget_the_functions_of_the_old_ones(app):
    def parts(text):
        return [{"key": "rows", "text": text, "on_click": lambda: None}]

    bar = ozdenui.StatusBar(items=parts("0 rows"))
    menus = ozdenui.MenuBar(menus=[{"text": "File", "items": [{"text": "Save", "on_click": lambda: None}]}])
    kept = len(app._callbacks)
    for count in range(50):  # WHY: a status bar given its parts every second kept every on_click for ever
        bar.set_items(parts(f"{count} rows"))
        menus.set_menus([{"text": "File", "items": [{"text": "Save", "on_click": lambda: None}]}])
    assert len(app._callbacks) == kept
    assert calls(app, bar, "setItems")[-1]["args"][0][0]["onClick"]["__bpCallback"] in app._callbacks


def test_an_item_selected_again_is_kept_once(app):
    fruits = ozdenui.ItemList(items=["Apple", "Pear"], selection="multiple")
    fruits.select("0")
    fruits.select("0")
    assert fruits.selected_keys == ["0"]


def test_on_enter_given_later_runs_on_enter(app):
    # WHY: as a value of the page it listened to an "enter" event, which the page does not have
    seen = []
    name = ozdenui.Input(placeholder="Name")
    name.on_enter = lambda: seen.append("input")
    field = ozdenui.TextField(title_text="Name", on_enter=lambda: seen.append("the first one"))
    field.on_enter = lambda changed: seen.append(changed.text)
    enter = {"key": "Enter", "state": {"text": "Ada"}}
    app._dispatch(name._id, "keydown", enter)
    app._dispatch(field._id, "keydown", enter)
    name.on_enter = None
    app._dispatch(name._id, "keydown", enter)
    assert seen == ["input", "Ada"]
    assert not any(c["event"] == "enter" for c in commands(app, "listen"))
    assert not any("onEnter" in c["props"] for c in commands(app, "set"))


def test_print_comes_back_when_the_window_closes_or_the_page_is_loaded_again(app):
    # WHY: after run() every print was a command for nobody; after a reload, an error of the page
    streams = (sys.stdout, sys.stderr)
    log = ozdenui.LogView()
    log.capture_print()
    app._start_again()
    assert (sys.stdout, sys.stderr) == streams
    stop = log.capture_print(errors=False)
    assert sys.stdout is not streams[0]
    app._on_window_closed()
    assert (sys.stdout, sys.stderr) == streams
    stop()  # stopped already: the streams are not changed again
    assert (sys.stdout, sys.stderr) == streams


def test_a_component_that_leaves_the_page_after_its_event_still_gets_it_handled(app):
    """A Dialog calls onClose and then removes itself; a flush of a busy timer reported it removed before the onClose of
    the queue ran: Dialog.ask() waited for ever (seen in a real window)."""
    seen = []
    loading = ozdenui.LoadingScreen(remove_on_close=True, on_close=lambda screen: seen.append(screen))
    on_close = callback_of(app, loading, "onClose")
    event = (on_close, "callback", {"args": [{"__bpObject": loading._id}]})
    app._event_order.add(1, event)  # the event is in the queue
    app._after_apply({"errors": [], "removed": [loading._id], "lastEvent": 1})  # a flush: the page removed it
    run_queued_tasks(app)
    assert seen == [loading]  # its function ran, with its object
    assert on_close not in app._callbacks and loading._id not in app._leaving  # then they were forgotten


def test_an_event_still_on_its_way_is_waited_for(app):
    seen = []
    loading = ozdenui.LoadingScreen(remove_on_close=True, on_close=lambda: seen.append("closed"))
    on_close = callback_of(app, loading, "onClose")
    app._after_apply({"errors": [], "removed": [loading._id], "lastEvent": 1})  # the answer came before the event
    run_queued_tasks(app)
    assert on_close in app._callbacks  # WHY: event 1 is not here yet
    app._event_order.add(1, (on_close, "callback", {"args": []}))
    run_queued_tasks(app)
    assert seen == ["closed"] and on_close not in app._callbacks


def test_what_waits_for_an_event_that_never_comes_goes_on(app, monkeypatch):
    monkeypatch.setattr(app_module, "_GAP_SECONDS", 0.05)
    app._event_order = app_module._EventOrder(app._queue_event)
    box = CheckBox(on_change=lambda checkbox: None)
    app._after_apply({"errors": [], "removed": [box._id], "lastEvent": 3})  # events 1 - 3 never come
    time.sleep(0.2)
    run_queued_tasks(app)
    assert not any(owner == box._id for _, _, owner in app._callbacks.values())
    app._event_order.add(2, ("late", "callback", {"args": []}))  # late is better than lost
    assert not app._tasks.empty()


def test_10_a_missing_event_is_skipped_and_a_new_page_starts_again(app, monkeypatch):
    monkeypatch.setattr(app_module, "_GAP_SECONDS", 0.05)
    delivered = []
    order = app_module._EventOrder(delivered.append)
    order.add(2, "after the hole")
    time.sleep(0.15)
    assert delivered == ["after the hole"]
    order.add(1, "late")
    assert delivered == ["after the hole", "late"]
    starts = []
    app._start = lambda page: starts.append(page)
    old_order = app._event_order
    app._ready.set()
    app._on_page_ready("26.11.01", 800, 600)
    assert app._event_order is not old_order
    run_queued_tasks(app)
    assert len(starts) == 1 and starts[0] is app.page


def test_another_thread_sends_its_commands_through_the_app_thread(app):
    label = Label(text="0")
    app._commands.clear()
    worker = threading.Thread(target=lambda: label.set(text="1"))
    worker.start()
    worker.join()
    assert app._commands == []
    run_queued_tasks(app)
    assert app._window.applied_commands()[-1]["props"] == {"plainText": "1"}


def test_measure_from_another_thread_is_refused(app):
    label = Label(text="0")
    problems = []

    def read():
        try:
            label.measure("width")
        except RuntimeError as error:
            problems.append(str(error))

    worker = threading.Thread(target=read)
    worker.start()
    worker.join()
    assert problems and "another thread" in problems[0]


def answer_when_sent(app, value):
    """Waits until the static call is sent to the page, then answers it as the page would."""
    for _ in range(200):
        for command in app._window.applied_commands():
            if command["op"] == "static" and command.get("answer"):
                app._on_page_event(1, command["answer"], "callback", {"args": [value]})
                return
        time.sleep(0.01)


def test_confirm_waits_for_its_answer(app):
    helper = threading.Thread(target=answer_when_sent, args=(app, True))
    helper.start()
    assert Dialog.confirm("Delete it?") is True
    helper.join()
    static = [c for c in app._window.applied_commands() if c["op"] == "static"][0]
    assert static["target"] == "Dialog" and static["method"] == "confirm"
    assert static["args"][0]["messageText"] == "Delete it?"


def test_a_closed_window_ends_the_waiting(app):
    app._tasks.put(None)
    with pytest.raises(WindowClosed):
        Dialog.confirm("Delete it?")


def test_a_timer_runs_on_the_app_thread_and_stops(app):
    ticks = []
    stop = app.every(10, lambda: ticks.append(threading.get_ident()))
    time.sleep(0.08)
    run_queued_tasks(app)
    assert len(ticks) == 1  # WHY one: a tick waits in the queue until it runs, it is not queued again
    assert set(ticks) == {threading.get_ident()}
    stop()
    time.sleep(0.05)
    run_queued_tasks(app)
    assert len(ticks) == 1


def test_the_functions_of_ozdenui_reach_the_app_of_the_window(app, monkeypatch):
    done = []
    stop = ozdenui.every(10, lambda: done.append("every"))
    ozdenui.after(10, lambda: done.append("after"))
    ozdenui.call_soon(lambda: done.append("soon"))
    time.sleep(0.08)
    run_queued_tasks(app)
    stop()
    assert sorted(set(done)) == ["after", "every", "soon"]

    asked = []

    def fake_dialog(kind, directory, multiple, file_name, file_types):
        asked.append((kind, directory, multiple, file_name, tuple(file_types)))
        return ["/notes/a.txt"]

    monkeypatch.setattr(app, "_file_dialog", fake_dialog)
    assert ozdenui.open_file(file_types=("Text (*.txt)",)) == "/notes/a.txt"
    assert ozdenui.save_file("b.txt") == "/notes/a.txt"
    assert ozdenui.choose_folder("/notes") == "/notes/a.txt"
    assert asked == [("open", "", False, "", ("Text (*.txt)",)), ("save", "", False, "b.txt", ()), ("folder", "/notes", False, "", ())]

    finished = threading.Event()
    ozdenui.run_in_background(finished.set).join(1)
    assert finished.is_set()


# *** THE CLASSES OF THE FIRST RELEASE (2026-11-06)

def callback_of(app, obj, name):
    return created(app, obj)["props"][name]["__bpCallback"]


def calls(app, obj, method=None):
    return [c for c in commands(app, "call") if c["id"] == obj._id and method in (None, c["method"])]


def test_a_text_field_keeps_its_text_and_gives_itself_to_on_change(app):
    seen = []
    field = ozdenui.TextField(title_text="Name", text="Ada", on_change=lambda f: seen.append(f.text))
    props = created(app, field)["props"]
    assert props["styleName"] == "light" and props["value"] == "Ada" and props["required"] == 0
    assert created(app, field)["state"] == {"text": "getValue()"}
    assert field.text == "Ada" and field.value == "Ada"
    me = {"__bpObject": field._id}  # WHY: the kit gives the field to onChange, onFocus and onBlur
    app._dispatch(callback_of(app, field, "onChange"), "callback", {"args": [me], "state": {"text": "Can"}})
    assert seen == ["Can"] and field.text == "Can"
    field.text = "New"
    assert field.text == "New" and calls(app, field, "setValue")[-1]["args"] == ["New"]
    field.value = "Newer"
    assert field.text == "Newer" and calls(app, field, "setValue")[-1]["args"] == ["Newer"]


def test_a_handler_of_a_field_takes_what_it_needs(app):
    seen = []
    field = ozdenui.TextField(on_change=lambda: seen.append("no values"), on_focus=lambda f: seen.append(f))
    me = {"__bpObject": field._id}
    app._dispatch(callback_of(app, field, "onChange"), "callback", {"args": [me], "state": {"text": ""}})
    app._dispatch(callback_of(app, field, "onFocus"), "callback", {"args": [me]})
    assert seen == ["no values", field]


def test_the_defaults_of_a_web_form_do_not_limit_a_program(app):
    for kind in (ozdenui.TextField, ozdenui.PasswordField):
        assert created(app, kind())["props"]["maxLength"] == 1000
    assert created(app, ozdenui.EmailField())["props"]["required"] == 0
    assert created(app, ozdenui.PasswordField())["props"]["required"] == 0
    assert created(app, ozdenui.PasswordField(required=True))["props"]["required"] == 1
    assert created(app, ozdenui.TextAreaField())["props"]["maxLength"] == 100000


def test_on_enter_of_a_field_runs_only_for_enter(app):
    seen = []
    field = ozdenui.TextField(on_enter=lambda f: seen.append(f))
    assert "onEnter" not in created(app, field)["props"]
    field._receive("keydown", {"key": "a"})
    assert seen == []
    field._receive("keydown", {"key": "Enter", "state": {"text": "Ada"}})
    assert seen == [field] and field.text == "Ada"


def test_check_shows_the_warnings_and_reads_the_status(app, monkeypatch):
    field = ozdenui.TextField(required=True)
    answers = {"status": 1}
    monkeypatch.setattr(app, "_read", lambda object_id, key: answers[key])
    assert field.check() is False
    assert calls(app, field, "checkInputValue")
    answers["status"] = 0
    assert field.check() is True


def test_a_field_is_focused_through_its_input(app):
    field = ozdenui.TextField()
    field.focus()
    field.select_text()
    parts = [c for c in commands(app, "part") if c["of"] == field._id]
    assert len(parts) == 1 and parts[0]["path"] == ["input"]
    assert [c["method"] for c in commands(app, "call") if c["id"] == parts[0]["id"]] == ["focus", "select"]


def test_a_number_field_reads_a_number(app):
    field = ozdenui.NumberField(value=3)
    assert created(app, field)["props"]["value"] == "3" and field.value == 3 and field.text == "3"
    for text, number in (("12.5", 12.5), ("125", 125), ("", None), ("-", None)):
        field._values["text"] = text
        assert field.value == number
    comma = ozdenui.NumberField(value=2.5, decimal_separator=",")
    assert created(app, comma)["props"]["value"] == "2,5" and comma.value == 2.5
    comma.value = 7.25
    assert comma.text == "7,25" and calls(app, comma, "setValue")[-1]["args"] == ["7,25"]
    comma.value = None
    assert comma.text == "" and comma.value is None


def test_a_url_field_gives_the_whole_address(app):
    field = ozdenui.UrlField(text="github.com")
    props = created(app, field)["props"]
    assert props["tinySelectParams"] == {"selectedIndex": 1} and props["required"] == 0 and props["maxLength"] == 2048
    assert field.text == "https://github.com" and field.value == "https://github.com"
    assert ozdenui.UrlField(text="http://example.com/a").text == "http://example.com/a" and ozdenui.UrlField().text == ""
    field._values["text"] = "http://www.example.com"  # the user chose http://www.
    field.text = "python.org"
    last = calls(app, field, "setValue")[-1]
    assert field.text == "http://www.python.org" and last["args"] == ["python.org"] and last["refresh"] == 1
    ftp = [{"value": "1", "label": "ftp://"}]
    mine = ozdenui.UrlField(tiny_select_params={"list": ftp, "selected_index": 0}, text="files.example.com")
    assert created(app, mine)["props"]["tinySelectParams"] == {"list": ftp, "selectedIndex": 0} and mine.text == "ftp://files.example.com"


def test_a_phone_field_keeps_the_number_in_its_mask(app):
    field = ozdenui.PhoneField(text="0555 123 45 67")
    assert created(app, field)["props"]["value"] == "0555 123 45 67" and field.text == "+90 (555) 123-4567"
    field.text = "5559876543"
    assert field.text == "+90 (555) 987-6543" and calls(app, field, "setValue")[-1]["refresh"] == 1
    field.set_country_code("+1")
    assert field.text == "+1 (555) 987-6543" and calls(app, field, "setCountryCode")[-1]["args"] == ["+1"]
    field.phone_mask = " ___ ___ __ __"
    assert field.text == "+1 555 987 65 43" and calls(app, field, "setPhoneMask")[-1]["refresh"] == 1
    field.text = "+1 555 12"
    assert field.text == "+1 555 12_ __ __"
    field.text = ""
    assert field.text == ""
    us = ozdenui.PhoneField(country_code="+1", text="+1 (212) 555-0100", unit_text="US")
    assert us.text == "+1 (212) 555-0100" and ozdenui.PhoneField().text == ""


def test_a_currency_field_writes_a_number_in_groups(app):
    field = ozdenui.CurrencyField(value=1234567.5)
    assert created(app, field)["props"]["value"] == "1,234,567.5" and field.value == 1234567.5 and field.text == "1,234,567.5"
    field.value = 1e20  # WHY a test: its text is "1e+20", and the page would keep only its digits
    assert field.text == "100,000,000,000,000,000,000" and field.value == 10 ** 20
    field.value = 12.345
    assert field.text == "12.34"  # cut as the page cuts a digit that is typed
    comma = ozdenui.CurrencyField(value=-9876543.21, decimal_separator=",", group_separator=".", unit_text="€")
    assert comma.text == "-9.876.543,21" and comma.value == -9876543.21
    whole = ozdenui.CurrencyField(value=-12.5, allow_negative=False, allow_decimal=False)
    assert whole.text == "12" and whole.value == 12
    field.value = "1000"  # a text: the page writes it in groups, and its text comes back
    assert calls(app, field, "setValue")[-1]["args"] == ["1000"] and calls(app, field, "setValue")[-1]["refresh"] == 1
    field._values["text"] = ""
    assert field.value is None
    with pytest.raises(ValueError, match="is not an amount"):
        field.value = float("nan")


def test_a_slider_gives_itself_to_its_handlers(app):
    seen = []
    slider = ozdenui.Slider(value=5, min_value=0, max_value=10, step=2, on_change=lambda s: seen.append((s, s.value)),
                            on_change_end=lambda s: seen.append(s.value))
    props = created(app, slider)["props"]
    assert props["styleName"] == "round" and props["value"] == 5 and props["minValue"] == 0 and props["maxValue"] == 10
    assert slider.value == 5
    me = {"__bpObject": slider._id}  # WHY: the kit gives the slider to onChangeStart, onChange and onChangeEnd
    app._dispatch(callback_of(app, slider, "onChange"), "callback", {"args": [me], "state": {"value": 8}})
    app._dispatch(callback_of(app, slider, "onChangeEnd"), "callback", {"args": [me], "state": {"value": 8}})
    assert seen == [(slider, 8), 8]
    slider.value = 50
    assert slider.value == 10
    last = calls(app, slider, "setValue")[-1]
    assert last["args"] == [50] and last["refresh"] == 1


def test_a_slider_keeps_its_value_without_a_handler(app):
    slider = ozdenui.Slider(value=5, max_value=10)
    assert "onChange" not in created(app, slider)["props"]
    app._dispatch(callback_of(app, slider, "onChangeEnd"), "callback", {"args": [{"__bpObject": slider._id}], "state": {"value": 9}})
    assert slider.value == 9


def test_a_search_input_gives_itself_to_its_handlers(app):
    seen = []
    box = ozdenui.SearchInput(placeholder="Find", text="sea", on_change=lambda b: seen.append((b.text, b)),
                              on_enter=lambda b: seen.append(("Enter", b.text)))
    props = created(app, box)["props"]
    assert props["placeholder"] == "Find" and props["styleName"] == "ozden"
    assert calls(app, box, "setValue")[-1]["args"] == ["sea", 1] and box.text == "sea"  # 1: silent
    me = {"__bpObject": box._id}
    app._dispatch(callback_of(app, box, "onChange"), "callback", {"args": [me], "state": {"text": "hill"}})
    app._dispatch(callback_of(app, box, "onEnter"), "callback", {"args": [me], "state": {"text": "hill"}})
    assert seen == [("hill", box), ("Enter", "hill")] and box.text == "hill"
    box.placeholder = "Search"
    assert calls(app, box, "setPlaceholder")[-1]["args"] == ["Search"]
    box.clear()
    assert box.text == "" and calls(app, box, "setValue")[-1]["args"] == ["", 1]


def test_a_number_format_goes_as_a_text_of_the_page(app):
    graph = ozdenui.GraphBox(type="bar", labels=["A"], values=[1], format_value="{:,.1f} TL")
    assert created(app, graph)["props"]["formatValue"] == {"__bpFormat": {"prefix": "", "suffix": " TL", "thousands": 1, "decimals": 1, "percent": 0}}
    graph.format_value = "{:.0%}"
    assert calls(app, graph, "setFormatValue")[-1]["args"][0]["__bpFormat"]["percent"] == 1
    graph.format_value = None
    assert calls(app, graph, "setFormatValue")[-1]["args"] == [None]
    with pytest.raises(TypeError, match="can not answer the page at once"):
        graph.set_format_x(lambda value: "x")
    with pytest.raises(TypeError, match="can not answer the page at once"):
        ozdenui.GraphBox(format_value=lambda value: str(value))
    with pytest.raises(ValueError, match="not known"):
        ozdenui.GraphBox(format_value="{:x}")
    with pytest.raises(ValueError, match="one {}"):
        ozdenui.GraphBox(format_x="no number")
    stepper = ozdenui.Stepper(value_format="{:.1f} kg")
    assert created(app, stepper)["props"]["valueFormat"]["__bpFormat"]["decimals"] == 1


def test_a_graph_box_takes_what_python_has(app):
    class Series:
        """As a numpy array and a pandas Series: tolist()."""

        def tolist(self):
            return [1, 2]

    graph = ozdenui.GraphBox(labels=Series(), datasets=[{"label": "A", "data": Series(), "show_points": 1}])
    props = created(app, graph)["props"]
    assert props["labels"] == [1, 2]
    assert props["datasets"] == [{"label": "A", "data": [1, 2], "showPoints": 1}]
    graph.set_values(Series())
    graph.add_value("Apr", 15)
    graph.type = "line"
    assert calls(app, graph, "setValues")[-1]["args"] == [[1, 2], 0]
    graph.values = [3, 4]
    assert graph.values == [3, 4] and calls(app, graph, "setValues")[-1]["args"] == [[3, 4], 0]
    assert calls(app, graph, "addValue")[-1]["args"] == ["Apr", 15]
    assert calls(app, graph, "setType")[-1]["args"] == ["line"] and graph.type == "line"


def test_a_graph_box_saves_a_picture(app, tmp_path, monkeypatch):
    graph = ozdenui.GraphBox()
    png = b"\x89PNG some bytes"
    address = "data:image/png;base64," + base64.b64encode(png).decode("ascii")
    asked = []
    monkeypatch.setattr(app, "_ask", lambda object_id, method, args: asked.append((method, args)) or address)
    graph.save_image(tmp_path / "chart.png")
    assert (tmp_path / "chart.png").read_bytes() == png and asked == [("getImage", ["image/png", 2])]
    graph.save_image(str(tmp_path / "chart.jpg"))
    assert asked[-1] == ("getImage", ["image/jpeg", 2])


def test_a_tree_names_its_nodes_as_the_page_does(app):
    seen = []
    tree = ozdenui.TreeView(items=[{"key": "a", "text": "A", "has_children": True, "icon_file": "x.png", "data": {"my_key": 1},
                                    "children": [{"key": "b", "text": "B", "tag_color": "red"}, "c"]}],
                            on_select=lambda t, node: seen.append((t, node["key"])))
    item = created(app, tree)["props"]["items"][0]
    assert item["hasChildren"] is True and item["iconFile"] == "x.png" and item["data"] == {"my_key": 1}
    assert item["children"][0]["tagColor"] == "red" and item["children"][1] == "c"
    app._dispatch(callback_of(app, tree, "onSelect"), "callback",
                  {"args": [{"__bpObject": tree._id}, {"key": "b"}], "state": {"value": "b", "previousValue": None}})
    assert seen == [(tree, "b")] and tree.value == "b"
    tree.value = "a"
    assert tree.value == "a" and tree.previous_value == "b"
    last = calls(app, tree, "setValue")[-1]
    assert last["args"] == ["a", 1] and last["refresh"] == 1
    tree.items = ["x"]
    assert tree.items == ["x"] and calls(app, tree, "setItems")[-1]["args"] == [["x"]]
    tree.set_children("a", [{"key": "d", "has_children": 1}])
    assert calls(app, tree, "setChildren")[-1]["args"] == ["a", [{"key": "d", "hasChildren": 1}]]


def test_the_items_of_a_context_menu_take_python_names_and_functions(app):
    seen = []
    button = Button()
    menu = ozdenui.ContextMenu(target=button, items=["Open", "-", {"text": "Sub", "items": [{"text": "A", "on_click": lambda: seen.append("a")}]}],
                               on_click=lambda m, item, index: seen.append((m, index)))
    props = created(app, menu)["props"]
    assert props["target"] == {"__bpObject": button._id} and "left" not in props
    inner = props["items"][2]["items"][0]["onClick"]["__bpCallback"]
    app._dispatch(inner, "callback", {"args": [{"__bpObject": menu._id}, {"key": "a"}, 0]})
    app._dispatch(props["onClick"]["__bpCallback"], "callback", {"args": [{"__bpObject": menu._id}, {"key": "a"}, 0]})
    assert seen == ["a", (menu, 0)]
    menu.open_at(10, 20)
    menu.set_item_enabled("a", False)
    assert calls(app, menu, "openAt")[-1]["args"] == [10, 20]
    assert calls(app, menu, "setItemEnabled")[-1]["args"] == ["a", 0]


def test_a_tooltip_needs_its_object(app):
    with pytest.raises(TypeError, match="needs its object"):
        ozdenui.Tooltip(text="Hi")
    button = Button()
    tip = ozdenui.Tooltip(target=button, text="Hi", position="left", look={"text_color": "white"})
    props = created(app, tip)["props"]
    assert props["hintText"] == "Hi" and props["hintPosition"] == "left" and props["look"] == {"textColor": "white"}
    tip.text = "Hello"
    assert calls(app, tip, "setHintText")[-1]["args"] == ["Hello"] and tip.text == "Hello"


def test_a_bubble_is_an_object_of_python(app):
    button = Button()
    bubble = ozdenui.Tooltip.show(button, "Saved.", side="bottom")
    command = commands(app, "static")[-1]
    assert command["method"] == "show" and command["keep"] == bubble._id
    assert command["args"][:2] == [{"__bpObject": button._id}, "Saved."] and command["args"][3] == "bottom"
    bubble.remove()
    assert commands(app, "remove")[-1]["id"] == bubble._id


def test_a_bubble_has_a_frame_so_it_is_seen_on_a_white_card(app):
    button = Button()
    ozdenui.Tooltip.show(button, "Saved.")
    look = commands(app, "static")[-1]["args"][2]
    assert look["border"] == 1 and look["shadow"] and look["color"] == "#FFFFFF"
    ozdenui.Tooltip.show(button, "Saved.", look={"color": "#222", "text_color": "white", "shadow": ""})
    look = commands(app, "static")[-1]["args"][2]
    assert look["color"] == "#222" and look["textColor"] == "white" and look["shadow"] == "" and look["border"] == 1


def test_a_bubble_is_dark_in_a_dark_window(dark_app):
    ozdenui.Tooltip.show(Button(), "Saved.")
    look = commands(dark_app, "static")[-1]["args"][2]
    assert look["color"] == "#2A2A29" and look["textColor"] == "rgba(255, 255, 255, 0.86)"


def test_a_popover_opens_with_a_click_and_makes_its_objects_inside(app):
    button = Button()
    closed = []
    labels = []
    popover = ozdenui.Tooltip.popover(button, lambda: labels.append(Label(text="Hi")), on_close=lambda: closed.append(1))
    assert "click" in button._handlers and popover.is_open is False
    button._receive("click", {})
    assert popover.is_open is True
    opened = commands(app, "static")[-1]
    assert opened["method"] == "openPopover" and opened["args"][1] == {"__bpNoop": 1}
    assert created(app, labels[0])["parent"] == opened["keep"]
    assert "left" not in created(app, labels[0])["props"]
    place = commands(app, "placeBubble")[-1]
    assert place["id"] == opened["keep"] and place["target"] == button._id
    button._receive("click", {})
    assert commands(app, "static")[-1]["method"] == "closePopover"
    app._dispatch(opened["args"][5]["onClose"]["__bpCallback"], "callback", {"args": []})
    assert popover.is_open is False and closed == [1]


def test_a_date_is_a_text_or_a_date(app):
    seen = []
    select = ozdenui.DatePicker(value=datetime.date(2026, 11, 20), min_date="2026-01-01", on_change=lambda s: seen.append(s.date))
    props = created(app, select)["props"]
    assert props["date"] == "2026-11-20" and props["minDate"] == "2026-01-01"
    assert select.value == "2026-11-20" and select.date == datetime.date(2026, 11, 20)
    app._dispatch(callback_of(app, select, "onChange"), "callback", {"args": [{"__bpObject": select._id}], "state": {"value": "2026-12-01"}})
    assert seen == [datetime.date(2026, 12, 1)]
    select.value = datetime.datetime(2027, 1, 2, 10, 0)
    last = calls(app, select, "setDate")[-1]
    assert select.value == "2027-01-02" and last["args"] == ["2027-01-02", 1] and last["refresh"] == 1
    select.value = ""
    assert select.date is None
    assert ozdenui.DatePicker().value == "" and ozdenui.DatePicker().date is None


def test_a_time_and_a_color(app):
    select = ozdenui.TimePicker(value=datetime.time(19, 30), max_time="22:00")
    props = created(app, select)["props"]
    assert props["time"] == "19:30" and props["maxTime"] == "22:00" and select.time == datetime.time(19, 30)
    select.value = "08:15"
    assert select.value == "08:15" and calls(app, select, "setTime")[-1]["args"] == ["08:15", 1]
    color = ozdenui.ColorPicker(value="#3871E0", colors=["#000000"])
    props = created(app, color)["props"]
    assert props["selectedColor"] == "#3871E0" and color.value == "#3871E0"
    color.value = "#FF0000"
    assert color.value == "#FF0000" and calls(app, color, "setColor")[-1]["args"] == ["#FF0000", 1]


def test_a_stepper_keeps_its_value_inside_its_range(app):
    assert ozdenui.Stepper().value == 1  # as the page: value 1, 0 - 10
    plain = ozdenui.Stepper()
    plain.value = 50
    assert plain.value == 10
    stepper = ozdenui.Stepper(value=5, min_value=0, max_value=10, on_change=lambda s: None)
    assert stepper.value == 5
    stepper.value = 50
    assert stepper.value == 10 and calls(app, stepper, "setValue")[-1]["args"] == [50, 1]
    stepper.set_range(0, 4)
    assert stepper.value == 4
    app._dispatch(callback_of(app, stepper, "onChange"), "callback", {"args": [{"__bpObject": stepper._id}], "state": {"value": 2}})
    assert stepper.value == 2


def test_the_methods_with_the_new_names_of_the_kit_reach_the_page(app, tmp_path):
    bar = ozdenui.ProgressBar(value=80)
    bar.max_value = 50
    assert bar.value == 50 and calls(app, bar, "setMaxValue")[-1]["args"] == [50]
    field = ozdenui.SliderField(value=8, min_value=0, max_value=10)
    field.set_range(2, 6)
    assert (field.min_value, field.max_value) == (2, 6) and calls(app, field, "setRange")[-1]["args"] == [2, 6]
    field.max_value = 4
    assert calls(app, field, "setRange")[-1]["args"] == [2, 4]
    stepper = ozdenui.Stepper(value=5)
    stepper.min_value = 3
    stepper.max_value = 8
    assert calls(app, stepper, "setRange")[-1]["args"] == [3, 8] and (stepper.min_value, stepper.max_value) == (3, 8)
    picture = tmp_path / "upload.png"
    picture.write_bytes(b"\x89PNG small")
    picker = ozdenui.FilePicker(description_text="or click", icon_file=picture)
    props = created(app, picker)["props"]
    assert props["descriptionText"] == "or click" and props["iconFile"].startswith("data:image/png;base64,")
    picker.description_text = "Drop it here"
    picker.icon_file = None
    assert calls(app, picker, "setDescriptionText")[-1]["args"] == ["Drop it here"] and calls(app, picker, "setIcon")[-1]["args"] == [""]
    acc = ozdenui.Accordion(sections=[{"key": "a", "text": "A", "description": "2 files", "enabled": False}])
    acc.set_section_text("a", "Alpha")
    acc.set_section_description("a", "3 files")
    assert [(c["method"], c["args"]) for c in calls(app, acc)][-2:] == [("setSectionText", ["a", "Alpha"]), ("setSectionDescription", ["a", "3 files"])]
    tree = ozdenui.TreeView(items=[{"key": "a", "text": "a.py", "description_color": "gray", "enabled": False}])
    assert created(app, tree)["props"]["items"] == [{"key": "a", "text": "a.py", "descriptionColor": "gray", "enabled": False}]
    tree.update_node("a", description="4 KB")
    assert calls(app, tree, "updateNode")[-1]["args"] == ["a", {"description": "4 KB"}]
    ozdenui.Toast.error("Could not save", title="Error")
    toast = commands(app, "static")[-1]["args"][0]
    assert (toast["messageText"], toast["titleText"]) == ("Could not save", "Error") and "message" not in toast


def page_file(name="a.txt", size=5, path=None):
    return {"name": name, "displayName": name, "path": path or name, "size": size, "sizeText": f"{size} B", "type": "text/plain",
            "extension": "txt", "lastModified": 1}


def test_the_file_types_of_the_dialog_come_from_accept():
    types_of = ozdenui.components._file_types_of
    assert types_of("") == () and types_of(None) == ()
    assert types_of(".csv, .TXT") == ("Files (*.csv;*.txt)",)
    assert "*.png" in types_of("image/*")[0] and "*.csv" not in types_of("image/*")[0]
    assert "*.png" in types_of("image/png")[0]
    assert types_of(".tar.gz") == ("Files (*.tar.gz)",)
    assert types_of(".c++") == ()
    from webview.util import parse_file_type
    for accept in (".csv,.txt", "image/*"):
        assert parse_file_type(types_of(accept)[0])  # WHY: pywebview refuses a type it can not read


def test_a_file_picker_listens_for_drops_once(app):
    ozdenui.FilePicker()
    ozdenui.FilePicker()
    assert [event for event, _handler in app._window.drop_handlers] == ["drop"]


def test_a_dropped_file_gets_its_path_from_pywebview_in_any_order(app):
    seen = []
    select = ozdenui.FilePicker(on_change=lambda s: seen.append(s.paths))
    callback = callback_of(app, select, "onChange")
    # The page tells first: the handler waits for the path.
    app._dispatch(callback, "callback", {"args": [{"__bpObject": select._id}], "state": {"files": [page_file()]}})
    assert seen == []
    _event, on_drop = app._window.drop_handlers[0]
    on_drop({"dataTransfer": {"files": [{"name": "a.txt", "size": 5, "pywebviewFullPath": "/Users/ada/a.txt"}]}})
    deadline = time.time() + 2
    while not seen and time.time() < deadline:
        run_queued_tasks(app)
        time.sleep(0.01)
    assert seen == [["/Users/ada/a.txt"]]
    assert select.files[0]["path"] == "/Users/ada/a.txt" and select.files[0]["size_text"] == "5 B"
    assert "file" not in select.files[0]


def test_a_file_nobody_knows_has_no_path_and_the_handler_still_runs(app, monkeypatch):
    monkeypatch.setattr(ozdenui.components, "_DROP_WAIT_STEPS", 1)
    seen = []
    select = ozdenui.FilePicker(on_change=lambda s: seen.append(s.files))
    app._dispatch(callback_of(app, select, "onChange"), "callback", {"args": [], "state": {"files": [page_file()]}})
    deadline = time.time() + 2
    while not seen and time.time() < deadline:
        run_queued_tasks(app)
        time.sleep(0.01)
    assert seen[0][0]["path"] is None and select.paths == []


def test_a_file_of_python_needs_no_waiting(app, tmp_path):
    file = tmp_path / "a.txt"
    file.write_text("hello")
    seen = []
    select = ozdenui.FilePicker(on_change=lambda s: seen.append(s.paths))
    select.add_paths(file)
    sent = calls(app, select, "addFiles")[-1]["args"][0][0]
    assert sent["path"] == str(file) and sent["size"] == 5 and sent["name"] == "a.txt" and sent["type"] == "text/plain"
    app._dispatch(callback_of(app, select, "onChange"), "callback", {"args": [], "state": {"files": [page_file(path=str(file))]}})
    assert seen == [[str(file)]]


def test_a_small_picture_of_the_dialog_gets_a_preview_and_a_big_one_does_not(app, tmp_path, monkeypatch):
    picture = tmp_path / "a.png"
    picture.write_bytes(b"\x89PNG small")
    select = ozdenui.FilePicker()
    select.add_paths([picture])
    assert calls(app, select, "addFiles")[-1]["args"][0][0]["previewAddress"].startswith("data:image/png;base64,")
    monkeypatch.setattr(ozdenui.components, "_MAX_PREVIEW_BYTES", 1)
    select.add_paths([picture])
    assert "previewAddress" not in calls(app, select, "addFiles")[-1]["args"][0][0]


def test_a_click_opens_the_dialog_of_the_system(app, monkeypatch, tmp_path):
    file = tmp_path / "a.csv"
    file.write_text("x")
    asked = []

    def fake_dialog(file_types=(), directory="", multiple=False):
        asked.append((file_types, multiple))
        return [str(file)] if multiple else str(file)

    monkeypatch.setattr(app, "open_file", fake_dialog)
    one = ozdenui.FilePicker(accept=".csv")
    app._dispatch(callback_of(app, one, "onOpenDialog"), "callback", {"args": [{"__bpObject": one._id}]})
    assert asked[-1] == (("Files (*.csv)",), False)
    assert calls(app, one, "addFiles")[-1]["args"][0][0]["path"] == str(file)
    many = ozdenui.FilePicker(multiple=True)
    many.open()
    assert asked[-1] == ((), True)
    assert calls(app, many, "addFiles")[-1]["args"][0][0]["path"] == str(file)


def test_a_folder_gives_its_files_with_their_place(app, monkeypatch, tmp_path):
    folder = tmp_path / "photos"
    (folder / "2026").mkdir(parents=True)
    (folder / "2026" / "sea.txt").write_text("x")
    monkeypatch.setattr(app, "choose_folder", lambda: str(folder))
    select = ozdenui.FilePicker(directory=True)
    select.open()
    sent = calls(app, select, "addFiles")[-1]["args"][0][0]
    assert sent["webkitRelativePath"] == "photos/2026/sea.txt" and sent["path"] == os.path.join(str(folder), "2026", "sea.txt")


def test_removing_a_file_in_code_does_not_call_the_handler(app):
    seen = []
    select = ozdenui.FilePicker(on_change=lambda s: seen.append(1))
    select._values["files"] = [page_file("a.txt"), page_file("b.txt")]
    select.remove_file(0)
    assert [file["name"] for file in select.files] == ["b.txt"] and calls(app, select, "removeFile")[-1]["args"] == [0, 1]
    select.clear()
    assert select.files == [] and calls(app, select, "clear")[-1]["args"] == [1] and seen == []


def test_a_tool_bar_names_its_items_as_the_page_does(app):
    clicks = []
    bar = ozdenui.ToolBar(items=[
        {"key": "save", "icon": "save", "hint": "Save", "on_click": lambda: clicks.append("save")},
        "-",
        " ",
        {"key": "left", "icon": "align_left", "icon_file": "x.png", "group": "align", "checked": True},
        {"key": "menu", "text": "Menu", "items": [{"key": "in", "icon": "align_right", "on_click": lambda b, item: clicks.append((b, item["key"]))}]},
        "Plain",
    ], on_click=lambda b, item: clicks.append(item["key"]))
    made = created(app, bar)
    items = made["props"]["items"]
    assert items[1] == "-" and items[2] == " " and items[5] == "Plain"
    assert "on_click" not in items[0] and "__bpCallback" in items[0]["onClick"]
    assert items[3]["icon"] == "alignLeft" and items[3]["iconFile"] == "x.png" and items[4]["items"][0]["icon"] == "alignRight"
    assert made["state"] == {"checkedKeys": "getCheckedKeys()"}
    press = {"args": [{"__bpObject": bar._id}, {"key": "in"}], "state": {"checkedKeys": ["left"]}}
    app._dispatch(items[0]["onClick"]["__bpCallback"], "callback", press)
    app._dispatch(items[4]["items"][0]["onClick"]["__bpCallback"], "callback", press)
    app._dispatch(callback_of(app, bar, "onClick"), "callback", press)
    assert clicks == ["save", (bar, "in"), "in"]


def test_a_wrong_name_of_an_icon_of_a_tool_bar_stops_at_its_line(app):
    with pytest.raises(ValueError, match='no icon named "savee"'):
        ozdenui.ToolBar(items=[{"icon": "savee"}])
    bar = ozdenui.ToolBar(items=[{"icon": "<svg></svg>"}, {"icon": "alignLeft"}])
    with pytest.raises(ValueError, match="align_left"):
        bar.set_items([{"icon": "left"}])
    assert [item["icon"] for item in created(app, bar)["props"]["items"]] == ["<svg></svg>", "alignLeft"]


def test_the_icons_of_a_tool_bar_are_the_ones_of_the_page():
    source = (Path(ozdenui.__file__).parent / "web" / "comp" / "tool-bar.js").read_text(encoding="utf-8")
    block = source[source.index("ToolBar.ICONS = {"):source.index("// An icon as an SVG text")]
    on_page = re.findall(r"^    (\w+): ", block, re.MULTILINE)
    assert on_page == [camel_case(name) for name in ozdenui.ToolBar.ICONS]


def test_a_tool_bar_keeps_its_pressed_buttons(app):
    bar = ozdenui.ToolBar(items=[
        {"key": "bold", "toggle": 1},
        {"key": "left", "group": "align", "checked": 1},
        {"key": "right", "group": "align"},
        {"key": "menu", "items": [{"key": "a", "group": "view", "checked": 1}, {"key": "b", "group": "view"}]},
    ])
    assert bar.checked_keys == ["left", "a"] and bar.is_checked("left") and not bar.is_checked("bold")
    bar.set_item_checked("right", True)
    last = calls(app, bar, "setItemChecked")[-1]
    assert bar.checked_keys == ["right", "a"] and last["args"] == ["right", 1] and last["refresh"] == 1
    bar.set_item_checked("bold", True)
    assert bar.checked_keys == ["bold", "right", "a"]
    bar.set_item_checked("bold", False)
    bar.set_item_checked("b", True)
    assert bar.checked_keys == ["right", "b"]
    app._dispatch(callback_of(app, bar, "onClick"), "callback",
                  {"args": [{"__bpObject": bar._id}, {"key": "bold", "checked": 1}], "state": {"checkedKeys": ["bold", "right", "b"]}})
    assert bar.checked_keys == ["bold", "right", "b"]


def test_the_methods_of_a_tool_bar_reach_the_page(app):
    bar = ozdenui.ToolBar()
    assert bar.checked_keys == []
    bar.set_items([{"key": "x", "icon": "save", "checked": 1}])
    assert calls(app, bar, "setItems")[-1]["args"] == [[{"key": "x", "icon": "save", "checked": 1}]] and bar.checked_keys == ["x"]
    bar.items = [{"key": "y", "on_click": print}, "-"]
    sent = calls(app, bar, "setItems")[-1]["args"][0]
    assert "__bpCallback" in sent[0]["onClick"] and sent[1] == "-" and bar.checked_keys == []
    bar.set_item_enabled("y", False)
    bar.set_item_text("y", "A text")
    bar.set_item_hint("y", "A hint")
    bar.click_item("y")
    bar.set_enabled(False)
    bar.close_menu()
    bar.set_theme("dark")
    seen = [(c["method"], c["args"]) for c in calls(app, bar)][-7:]
    assert seen == [("setItemEnabled", ["y", 0]), ("setItemText", ["y", "A text"]), ("setItemHint", ["y", "A hint"]), ("clickItem", ["y"]),
                    ("setEnabled", [0]), ("closeMenu", []), ("setTheme", ["dark"])]
    assert bar.enabled == 0


def test_a_markdown_view_sends_its_text_and_keeps_it(app):
    seen = []
    view = ozdenui.MarkdownView(text="# Hi", empty_text="Nothing", remote_pictures=True, on_link_click=lambda v, address: seen.append((v, address)))
    props = created(app, view)["props"]
    assert props["markdownText"] == "# Hi" and props["emptyText"] == "Nothing" and props["remotePictures"] == 1 and "text" not in props
    assert view.text == "# Hi"
    app._dispatch(callback_of(app, view, "onLinkClick"), "callback", {"args": [{"__bpObject": view._id}, "https://a.com"], "state": None})
    assert seen == [(view, "https://a.com")]
    assert ozdenui.MarkdownView(markdown_text="b").text == "b" and ozdenui.MarkdownView(text=None).text == "" and ozdenui.MarkdownView(text=12).text == "12"


def test_the_text_of_a_markdown_view_changes_and_grows(app):
    view = ozdenui.MarkdownView()
    assert view.text == ""
    view.set_text("a")
    view.append_text(" b")
    view.append_text(None)
    view.append_text(3)
    assert view.text == "a b3"
    assert [c["args"] for c in calls(app, view, "setMarkdownText")] == [["a"]]
    assert [c["args"] for c in calls(app, view, "appendText")] == [[" b"], [""], ["3"]]
    view.text = "new"
    view.markdown_text = "newer"
    assert view.text == "newer" and calls(app, view, "setMarkdownText")[-1]["args"] == ["newer"]
    view.clear()
    assert view.text == "" and calls(app, view, "setMarkdownText")[-1]["args"] == [""]


def test_the_methods_of_a_markdown_view_reach_the_page(app):
    view = ozdenui.MarkdownView()
    view.scroll_to_heading("a-title")
    view.scroll_to_top()
    view.scroll_to_end()
    view.empty_text = "Nothing"
    view.auto_scroll = False
    view.set_theme("dark")
    seen = [(c["method"], c["args"]) for c in calls(app, view)][-6:]
    assert seen == [("scrollToHeading", ["a-title"]), ("scrollToTop", []), ("scrollToEnd", []), ("setEmptyText", ["Nothing"]),
                    ("setAutoScroll", [0]), ("setTheme", ["dark"])]
    assert view.empty_text == "Nothing" and view.auto_scroll == 0


def test_a_picture_of_this_computer_goes_to_a_markdown_view_as_an_address(app, tmp_path, monkeypatch):
    (tmp_path / "plot.png").write_bytes(b"not a real picture")
    text = "![A plot](plot.png) ![Far](https://a.com/p.png) ![Near](//a.com/q.png) ![Gone](none.png) ![Data](data:image/png;base64,AA) [a link](plot.png)"
    view = ozdenui.MarkdownView(text=text, picture_folder=tmp_path)
    sent = created(app, view)["props"]["markdownText"]
    assert sent.startswith("![A plot](data:image/png;base64,") and "[a link](plot.png)" in sent
    assert "![Far](https://a.com/p.png) ![Near](//a.com/q.png) ![Gone](none.png) ![Data](data:image/png;base64,AA)" in sent
    assert view.text == text
    view.append_text("\n\n![Two](plot.png)")
    assert "![Two](data:image/png;base64," in calls(app, view, "appendText")[-1]["args"][0] and view.text.endswith("![Two](plot.png)")
    view.set_text("![Three](plot.png)")
    assert calls(app, view, "setMarkdownText")[-1]["args"][0].startswith("![Three](data:image/png;base64,") and view.text == "![Three](plot.png)"
    monkeypatch.chdir(tmp_path)
    in_folder_of_program = ozdenui.MarkdownView(text="![A plot](plot.png)")
    assert created(app, in_folder_of_program)["props"]["markdownText"].startswith("![A plot](data:image/png;base64,")


def test_a_markdown_view_loads_a_file_with_the_pictures_next_to_it(app, tmp_path):
    (tmp_path / "plot.png").write_bytes(b"not a real picture")
    report = tmp_path / "report.md"
    report.write_text("# Türkçe\n\n![A plot](plot.png)", encoding="utf-8")
    view = ozdenui.MarkdownView()
    view.load_file(report)
    assert view.text == "# Türkçe\n\n![A plot](plot.png)"
    assert "![A plot](data:image/png;base64," in calls(app, view, "setMarkdownText")[-1]["args"][0]
    assert calls(app, view)[-1]["method"] == "scrollToTop"
    view.append_text("![Two](plot.png)")
    assert "data:image/png" in calls(app, view, "appendText")[-1]["args"][0]
    with pytest.raises(FileNotFoundError):
        view.load_file(tmp_path / "none.md")


def test_a_step_bar_keeps_its_step(app):
    seen = []
    bar = ozdenui.StepBar(steps=["Cart", {"text": "Pay", "description": "Card"}, "Done"], step=1, can_go_back=False, on_step_click=lambda b, index: seen.append((b, index)))
    props = created(app, bar)["props"]
    assert props["steps"] == ["Cart", {"text": "Pay", "description": "Card"}, "Done"] and props["currentStep"] == 1 and props["canGoBack"] == 0
    assert bar.step == 1
    bar.next()
    bar.next()
    bar.next()
    assert bar.step == 3 and calls(app, bar, "setStep")[-1]["args"] == [4]
    bar.previous()
    bar.step = -5
    assert bar.step == 0
    bar.set_steps(["A"])
    assert bar.step == 0 and calls(app, bar, "setSteps")[-1]["args"] == [["A"]]
    bar.set_step(1)
    assert bar.step == 1
    app._dispatch(callback_of(app, bar, "onStepClick"), "callback", {"args": [{"__bpObject": bar._id}, 0], "state": {"step": 1}})
    assert seen == [(bar, 0)]


def test_a_range_slider_sends_its_params_and_keeps_its_values(app):
    seen = []
    slider = ozdenui.RangeSlider(low=200, high=800, min_value=0, max_value=1000, step=50, min_gap=100, value_format="{:,.0f} TL", on_change_end=lambda s: seen.append(s.values))
    made = created(app, slider)
    props = made["props"]
    assert props["lowValue"] == 200 and props["highValue"] == 800 and props["minValue"] == 0 and props["maxValue"] == 1000 and props["minGap"] == 100
    assert "__bpFormat" in props["formatValue"] and made["state"] == {"low": "lowValue", "high": "highValue"}
    assert slider.low == 200 and slider.high == 800 and slider.values == (200, 800) and slider.min_value == 0 and slider.max_value == 1000
    app._dispatch(callback_of(app, slider, "onChangeEnd"), "callback", {"args": [{"__bpObject": slider._id}], "state": {"low": 250, "high": 800}})
    assert seen == [(250, 800)] and slider.low == 250
    with pytest.raises(TypeError, match="format"):
        ozdenui.RangeSlider(value_format=lambda value: str(value))


def test_a_range_slider_starts_at_its_ends(app):
    assert ozdenui.RangeSlider().values == (0, 100)
    assert ozdenui.RangeSlider(min_value=10, max_value=20).values == (10, 20)
    assert ozdenui.RangeSlider(low=15, max_value=20).values == (15, 20)
    assert "lowValue" not in created(app, ozdenui.RangeSlider())["props"]


def test_the_methods_of_a_range_slider_reach_the_page(app):
    slider = ozdenui.RangeSlider(low=20, high=80)
    slider.set_values(90, 10)
    last = calls(app, slider, "setValues")[-1]
    assert slider.values == (10, 90) and last["args"] == [90, 10] and last["refresh"] == 1
    slider.set_values(-5, 500)
    assert slider.values == (0, 100)
    slider.low = 30
    assert slider.values == (30, 100) and calls(app, slider, "setValues")[-1]["args"] == [30, 100]
    slider.high = 60
    assert slider.values == (30, 60)
    slider.min_value = 10
    slider.max_value = 90
    slider.step = 5
    slider.min_gap = 10
    slider.enabled = False
    slider.theme = "roundDark"
    seen = [(c["method"], c["args"]) for c in calls(app, slider)][-6:]
    assert seen == [("setMinValue", [10]), ("setMaxValue", [90]), ("setStep", [5]), ("setMinGap", [10]), ("setEnabled", [0]), ("setTheme", ["roundDark"])]
    assert slider.min_value == 10 and slider.max_value == 90 and slider.enabled == 0


def test_the_page_is_read_from_the_disk_not_from_a_server():
    source = (Path(ozdenui.__file__).parent / "app.py").read_text(encoding="utf-8")
    assert "url=_page_address()" in source and "url=_INDEX_FILE" not in source
    assert app_module._page_address().startswith("file:///") and app_module._page_address().endswith("/index.html")


def test_a_page_that_comes_late_still_starts_the_program(monkeypatch, capsys):
    monkeypatch.setattr(app_module, "_READY_TIMEOUT_SECONDS", 0.05)
    started = threading.Event()
    late_app = App(lambda page: started.set())
    late_app._window = FakeWindow()
    loaded = []
    late_app._window.load_url = loaded.append
    shown = []
    monkeypatch.setattr(late_app, "_show_window", lambda: shown.append(1))
    monkeypatch.setattr(late_app, "_make_page", lambda: None)
    monkeypatch.setattr(late_app, "_load_components", lambda: None)
    thread = threading.Thread(target=late_app._run_app_thread, daemon=True)
    thread.start()
    time.sleep(0.2)
    assert not started.is_set() and shown, "the window is shown while the page is late"
    assert loaded == [app_module._page_address()], "the page is loaded once more"
    assert "not ready yet" in capsys.readouterr().err
    late_app._on_page_ready("v1", 100, 100)
    assert started.wait(2), "the program starts when the page comes"
    late_app._tasks.put(None)
    thread.join(2)


def test_the_page_keeps_its_focus_when_the_window_is_shown_on_windows(app, monkeypatch):
    """WHY: on Windows the shown window gave its focus to the first object of the page: its ring, and Enter pressed it."""
    app._ready.set()
    monkeypatch.setattr(app_module.sys, "platform", "win32")
    app._show_window()
    assert app._window.scripts == ["__bp.keepFocusWhenShown()"] and app._window.shown == 1
    app._show_window()
    assert len(app._window.scripts) == 1 and app._window.shown == 1, "once"


def test_the_focus_is_left_alone_on_other_systems_and_on_a_late_page(app, monkeypatch):
    monkeypatch.setattr(app_module.sys, "platform", "darwin")
    app._ready.set()
    app._show_window()
    assert app._window.scripts == [] and app._window.shown == 1
    late_app = App(lambda page: None)
    late_app._window = FakeWindow()
    monkeypatch.setattr(app_module.sys, "platform", "win32")
    late_app._show_window()
    assert late_app._window.scripts == [] and late_app._window.shown == 1, "a page that is not ready is not asked"


def test_a_json_view_sends_any_value_as_the_page_can_show_it(app):
    class Thing:
        def __str__(self):
            return "a thing"

    @dataclasses.dataclass
    class Point:
        x: int = 1

    class Table:
        def to_dict(self):
            return {"row": {"column": 1}}

    class Numbers:
        def tolist(self):
            return [1, 2]

    value = {"a": 1, 2: "a number key", "when": datetime.date(2026, 11, 7), "moment": datetime.datetime(2026, 11, 7, 9, 30), "set": {2, 1}, "tuple": (1, 2),
             "big": 2 ** 60, "edge": 2 ** 53, "thing": Thing(), "none": None, "ok": True, "ratio": 0.5, "bytes": b"ab", "point": Point(), "table": Table(), "numbers": Numbers()}
    view = ozdenui.JsonView(value=value)
    assert created(app, view)["props"]["value"] == {
        "a": 1, "2": "a number key", "when": "2026-11-07", "moment": "2026-11-07T09:30:00", "set": [1, 2], "tuple": [1, 2],
        "big": str(2 ** 60), "edge": 2 ** 53, "thing": "a thing", "none": None, "ok": True, "ratio": 0.5, "bytes": "b'ab'", "point": {"x": 1},
        "table": {"row": {"column": 1}}, "numbers": [1, 2]}
    assert view.value is value
    assert "value" not in created(app, ozdenui.JsonView())["props"] and ozdenui.JsonView().value is None
    assert created(app, ozdenui.JsonView(value=False))["props"]["value"] is False


def test_a_value_that_holds_itself_does_not_stop_a_json_view(app):
    loop = {"a": 1}
    loop["self"] = loop
    same = [1]
    view = ozdenui.JsonView(value={"loop": loop, "first": same, "second": same})
    sent = created(app, view)["props"]["value"]
    assert sent["loop"] == {"a": 1, "self": "<the same object again>"} and sent["first"] == [1] and sent["second"] == [1]


def test_a_json_view_keeps_the_selected_row(app):
    seen = []
    view = ozdenui.JsonView(value={"users": [{"name": "Ada", "when": datetime.date(2026, 11, 7)}]}, on_select=lambda v, entry: seen.append((v, entry["pathText"])))
    assert created(app, view)["state"] == {"selectedPath": "getSelectedPath()", "selectedPathText": "getSelectedPathText()"}
    assert view.selected_path is None and view.selected_path_text == "" and view.selected_value is None
    state = {"selectedPath": ["users", 0, "when"], "selectedPathText": "users[0].when"}
    app._dispatch(callback_of(app, view, "onSelect"), "callback", {"args": [{"__bpObject": view._id}, {"pathText": "users[0].when"}], "state": state})
    assert seen == [(view, "users[0].when")]
    assert view.selected_path == ["users", 0, "when"] and view.selected_path_text == "users[0].when" and view.selected_value == "2026-11-07"
    view.set_value({"other": 1})
    assert view.selected_path is None and view.selected_path_text == "" and view.selected_value is None and view.value == {"other": 1}


def test_the_methods_of_a_json_view_reach_the_page(app):
    view = ozdenui.JsonView()
    view.value = {"when": datetime.date(2026, 11, 7)}
    assert calls(app, view, "setValue")[-1]["args"] == [{"when": "2026-11-07"}]
    assert view.set_json_text('{"a": %d}' % 2 ** 60) is True
    assert calls(app, view, "setValue")[-1]["args"] == [{"a": str(2 ** 60)}] and view.value == {"a": 2 ** 60}
    assert view.set_json_text("{ not json") is False
    assert calls(app, view, "setJsonText")[-1]["args"] == ["{ not json"] and view.value is None
    view.select_path(("a", 0))
    last = calls(app, view, "selectPath")[-1]
    assert last["args"] == [["a", 0]] and last["refresh"] == 1
    view.expand_all()
    view.collapse_all()
    view.set_theme("dark")
    assert [c["method"] for c in calls(app, view)][-3:] == ["expandAll", "collapseAll", "setTheme"]


DEEP_VALUE = [{"a": {"b": {"c": {"d": {"e": {"f": 1}}}}}}]  # WHY: deeper than the bridge sends the values of an event


def test_a_json_editor_sends_its_params_as_the_page_names_them(app):
    seen = []
    editor = ozdenui.JsonEditor(value=({"name": "Apple", "tags": ("red",)},), title_text="Products", show_hint=False,
                                columns=[{"key": "unit", "options": ["kg", "box"]}], texts={"add_row": "Satır", "search": "Ara"},
                                on_change=lambda e, value: seen.append((e, value)))
    props = created(app, editor)["props"]
    assert props["value"] == [{"name": "Apple", "tags": ["red"]}]
    assert props["titleText"] == "Products" and props["showHint"] == 0 and props["columns"] == [{"key": "unit", "options": ["kg", "box"]}]
    assert props["texts"] == {"addRow": "Satır", "search": "Ara"}  # the keys of the kit are camelCase
    assert props["onChange"]["wholeArgs"] == [1]  # the value comes whole, as a JSON text
    app._dispatch(callback_of(app, editor, "onChange"), "callback",
                  {"args": [{"__bpObject": editor._id}, {"__bpJson": json.dumps(DEEP_VALUE)}], "state": None})
    assert seen == [(editor, DEEP_VALUE)]
    editor.set(on_change=lambda e, value: None)
    assert commands(app, "set")[-1]["props"]["onChange"]["wholeArgs"] == [1]
    assert "wholeArgs" not in created(app, CheckBox(on_change=lambda box: None))["props"]["onChange"]


def test_a_json_editor_takes_json_data_only(app):
    with pytest.raises(TypeError, match="a date is not JSON"):
        ozdenui.JsonEditor(value=[{"when": datetime.date(2026, 11, 9)}])  # WHY: it would come back as a text
    with pytest.raises(TypeError, match="a list or a dict is needed"):
        ozdenui.JsonEditor(value=3)
    with pytest.raises(ValueError, match="not JSON"):
        ozdenui.JsonEditor(value="{ not json")
    loop = []
    loop.append(loop)
    with pytest.raises(ValueError, match="holds itself"):
        ozdenui.JsonEditor(value=loop)
    big = ozdenui.JsonEditor(value='{"id": %d, "ok": true}' % 2 ** 60)  # its JSON text is read in Python
    assert created(app, big)["props"]["value"] == {"id": str(2 ** 60), "ok": True}  # the page would round it
    assert created(app, ozdenui.JsonEditor(value={1: [1.5, None, False]}))["props"]["value"] == {"1": [1.5, None, False]}
    assert "value" not in created(app, ozdenui.JsonEditor())["props"]  # the empty list of the page


def test_a_json_editor_refuses_the_functions_the_page_calls_itself(app):
    for name in ("color_of", "options_of", "on_pick_color", "on_pick_picture", "onPickColor"):
        with pytest.raises(TypeError, match="can not be a Python function"):
            ozdenui.JsonEditor(**{name: lambda *values: None})
    with pytest.raises(TypeError, match='"options": '):
        ozdenui.JsonEditor(options_of=lambda key: None)  # the message gives the way that works
    editor = ozdenui.JsonEditor()
    with pytest.raises(TypeError, match="answers later"):
        editor.set(color_of=lambda value: value)
    assert created(app, ozdenui.JsonEditor(on_pick_color=None))["props"]["onPickColor"] is None


def test_the_methods_of_a_json_editor_reach_the_page(app):
    editor = ozdenui.JsonEditor(title_text="Products", note_text="A row is a product")
    editor.value = [{"a": (1, 2)}]
    assert calls(app, editor, "setValue")[-1]["args"] == [[{"a": [1, 2]}]]
    assert editor.set_json_text('[{"id": %d}]' % 2 ** 60) is True
    assert calls(app, editor, "setValue")[-1]["args"] == [[{"id": str(2 ** 60)}]]
    assert editor.set_json_text("{ not json") is False and editor.set_json_text("3") is False
    assert [c["args"] for c in calls(app, editor, "setJsonText")] == [["{ not json"], ["3"]]  # the page shows the error
    editor.title_text = "Fruit"
    assert calls(app, editor, "setTitleText")[-1]["args"] == ["Fruit"] and editor.title_text == "Fruit"
    editor.note_text = "A row is a fruit"
    assert calls(app, editor, "setTitleText")[-1]["args"] == ["Fruit", "A row is a fruit"] and editor.note_text == "A row is a fruit"
    editor.undo()
    editor.redo()
    editor.focus()
    assert [c["method"] for c in calls(app, editor)][-3:] == ["undo", "redo", "focus"]


def test_a_json_editor_asks_the_page_for_its_value(app):
    editor = ozdenui.JsonEditor()
    answers = {"getJsonText": json.dumps(DEEP_VALUE, indent=2), "getView": "json", "setView": False, "hasChanges": 1}
    asked = []
    page = app._window.evaluate_js

    def evaluate_js(script, callback=None):
        question = re.match(r'__bp\.ask\("\w+", "(\w+)", (.*)\)$', script)
        if question:
            asked.append((question.group(1), json.loads(question.group(2))))
            return answers[question.group(1)]
        if script.startswith("__bp.read("):
            return "A row has no name."
        return page(script, callback)

    app._window.evaluate_js = evaluate_js
    assert editor.value == DEEP_VALUE and editor.get_json_text() == answers["getJsonText"]
    assert editor.view == "json" and editor.set_view("table") is False and editor.has_changes() is True
    assert ("setView", ["table"]) in asked
    assert editor.error_text == "A row has no name."
    answers["getJsonText"] = ""  # the table can not make a value now
    assert editor.value is None and editor.get_json_text() == ""


def test_json_editor_open_makes_a_window_whose_answers_come_to_python(app, capsys):
    applied, closed, changed = [], [], []
    window = ozdenui.JsonEditor.open(title_text="Settings", value={"a": {"b": 1}}, show_hint=False, on_apply=applied.append,
                                     on_close=lambda: closed.append(1), on_change=lambda e, value: changed.append((e, value)))
    opened = commands(app, "static")[-1]
    params = opened["args"][0]
    assert (opened["target"], opened["method"], opened["keep"]) == ("JsonEditor", "open", window._id)
    assert params["value"] == {"a": {"b": 1}} and params["titleText"] == "Settings" and params["showHint"] == 0
    assert params["onApply"]["wholeArgs"] == [0] and params["onChange"]["wholeArgs"] == [1] and "wholeArgs" not in params["onClose"]
    assert "onCancel" not in params  # not given: the page has its own
    editor = window.editor
    part = [c for c in commands(app, "part") if c["id"] == editor._id][-1]
    assert part["of"] == window._id and part["path"] == ["editor"]
    assert isinstance(editor, ozdenui.JsonEditor) and editor.title_text == "Settings" and window.is_open
    whole = {"__bpJson": json.dumps(DEEP_VALUE)}
    app._dispatch(params["onChange"]["__bpCallback"], "callback", {"args": [{"__bpObject": editor._id}, whole], "state": None})
    app._dispatch(params["onClose"]["__bpCallback"], "callback", {"args": [], "state": None})
    app._dispatch(params["onApply"]["__bpCallback"], "callback", {"args": [whole], "state": None})
    assert changed == [(editor, DEEP_VALUE)] and closed == [1] and applied == [DEEP_VALUE] and not window.is_open
    window.close()  # it is closed: nothing goes to the page
    assert not calls(app, window, "close")
    other = ozdenui.JsonEditor.open(value=[1], titel_text="A")
    assert 'did you mean "title_text"' in capsys.readouterr().err
    other.close()
    assert calls(app, other, "close") and not other.is_open
    with pytest.raises(TypeError, match="can not be a Python function"):
        ozdenui.JsonEditor.open(value=[], on_pick_picture=lambda editor, cell: None)


def test_the_window_of_a_json_editor_takes_the_look_of_the_window(dark_app):
    ozdenui.JsonEditor.open(value=[])
    assert commands(dark_app, "static")[-1]["args"][0]["styleName"] == "dark"
    ozdenui.JsonEditor.open(value=[], style_name="light")  # the code chose
    assert commands(dark_app, "static")[-1]["args"][0]["styleName"] == "light"


def sortable_event(app, lst, name, page_key, order, *values):
    """An event of a SortableList as the page sends it: its own copy of the item and its order (the keys Python gave)."""
    args = [{"__bpObject": lst._id}, {"key": page_key, "text": "x"}, *values]
    app._dispatch(callback_of(app, lst, name), "callback", {"args": args, "state": {"order": order}})


def test_a_sortable_list_gives_every_item_a_key_of_python(app):
    stock = {"key": "st", "text": "Stock", "description": "Pieces", "locked": True, "id": 7}
    lst = ozdenui.SortableList(items=["Sales", stock, "Sales"], texts={"move_up": "Up"})
    command = created(app, lst)
    assert command["props"]["items"] == [{"key": "i0", "text": "Sales"},
                                         {"key": "i1", "text": "Stock", "description": "Pieces", "locked": 1},
                                         {"key": "i2", "text": "Sales"}]
    assert command["state"] == {"order": "getKeys()"} and command["props"]["texts"] == {"moveUp": "Up"}
    assert sorted(name for name in command["props"] if name.startswith("on")) == ["onChange", "onRemove"]
    assert lst.items == ["Sales", stock, "Sales"] and lst.items[1] is stock  # your own items, in the order on the page
    assert lst.keys == ["Sales", "st", "Sales"] and lst.index_of("st") == 1 and lst.index_of("none") == -1


def test_a_move_in_a_sortable_list_reaches_python_with_your_item(app):
    seen = []
    pear = {"key": "p", "text": "Pear"}
    lst = ozdenui.SortableList(items=["Apple", pear, "Plum"], on_change=lambda l, item, a, b: seen.append((l, item, a, b)))
    sortable_event(app, lst, "onChange", "i1", ["i1", "i0", "i2"], 1, 0)
    assert seen == [(lst, pear, 1, 0)] and lst.items == [pear, "Apple", "Plum"] and lst.keys == ["p", "Apple", "Plum"]


def test_an_item_removed_from_a_sortable_list_leaves_python(app):
    seen = []
    lst = ozdenui.SortableList(items=["A", "B", "C"], removable=True, on_remove=lambda l, item, index: seen.append((item, index)))
    sortable_event(app, lst, "onRemove", "i1", ["i0", "i2"], 1)
    assert seen == [("B", 1)] and lst.items == ["A", "C"] and "i1" not in lst._item_of_key


def test_the_other_events_of_a_sortable_list_are_sent_when_they_are_given(app):
    seen = []
    lst = ozdenui.SortableList(items=["A", "B"], on_item_click=lambda l, item, index: seen.append(("click", item, index)))
    assert "onDragEnd" not in created(app, lst)["props"]
    sortable_event(app, lst, "onItemClick", "i1", ["i0", "i1"], 1)
    lst.on_drag_end = lambda _lst, item, index: seen.append(("end", item, index))
    drag_end = commands(app, "set")[-1]
    assert list(drag_end["props"]) == ["onDragEnd"]
    app._dispatch(drag_end["props"]["onDragEnd"]["__bpCallback"], "callback",
                  {"args": [{"__bpObject": lst._id}, {"key": "i0"}, 1], "state": {"order": ["i1", "i0"]}})
    lst.on_item_click = lambda: seen.append("new click")  # it is kept in Python: the page calls Python already
    assert commands(app, "set")[-1] is drag_end
    sortable_event(app, lst, "onItemClick", "i1", ["i1", "i0"], 0)
    assert seen == [("click", "B", 1), ("end", "A", 1), "new click"]


def test_a_change_of_a_sortable_list_in_code_is_kept_and_silent(app):
    seen = []
    lst = ozdenui.SortableList(items=["A", {"text": "Fixed", "locked": 1}, "C"], on_change=lambda: seen.append("change"))
    assert lst.move_item(0, 9) is True and lst.items == [{"text": "Fixed", "locked": 1}, "C", "A"]
    assert calls(app, lst, "moveItem")[-1]["args"] == [0, 2, 1] and calls(app, lst, "moveItem")[-1]["refresh"] == 1
    assert lst.move_item(0, 1) is False and lst.move_item(1, 1) is False and lst.move_item(5, 0) is False  # locked, same, none
    lst.add_item("New", 0)
    assert lst.items[0] == "New" and calls(app, lst, "addItem")[-1]["args"] == [{"key": "i3", "text": "New"}, 0]
    assert lst.remove_item(1) == {"text": "Fixed", "locked": 1} and lst.remove_item(9) is None
    assert calls(app, lst, "removeItem")[-1]["args"] == [1, 1] and lst.items == ["New", "C", "A"]
    lst.items = ["X", "Y"]
    assert lst.items == ["X", "Y"] and calls(app, lst, "setItems")[-1]["args"] == [[{"key": "i4", "text": "X"}, {"key": "i5", "text": "Y"}]]
    assert seen == []


def test_the_order_a_sortable_list_sends_after_the_last_call_is_the_truth(app):
    lst = ozdenui.SortableList(items=["A", "B"])
    lst.set_items(["C"])
    lst.add_item("D")
    lst._receive("__state", {"state": {"order": ["i2"]}})  # the answer of set_items: one more is waited for
    assert set(lst._item_of_key) == {"i0", "i1", "i2", "i3"} and lst.items == ["C"]
    lst._receive("__state", {"state": {"order": ["i0", "i1"]}})  # WHY possible: the page skips a change while a row is dragged
    assert lst.items == ["A", "B"] and set(lst._item_of_key) == {"i0", "i1"}


def test_a_sortable_list_refuses_a_python_function_for_its_rows(app):
    with pytest.raises(TypeError, match="create_item_view=.*can not be a Python function"):
        ozdenui.SortableList(items=["A"], create_item_view=lambda item, index, lst: None)


def test_a_sortable_list_takes_the_look_of_the_window(dark_app):
    assert created(dark_app, ozdenui.SortableList())["props"]["styleName"] == "dark"
    assert created(dark_app, ozdenui.SortableList(style_name="modern"))["props"]["styleName"] == "modern"


def test_a_web_view_shows_an_address_or_the_text_of_a_file(app, tmp_path):
    page = tmp_path / "report.html"
    page.write_text("<h1>Report</h1>", encoding="utf-8")
    view = ozdenui.WebView(url="https://example.com", height=300)
    assert created(app, view)["props"]["url"] == "https://example.com"
    local = created(app, ozdenui.WebView(url=str(page)))["props"]  # WHY its text: the web view opens no file outside its folder
    assert "url" not in local and local["htmlText"] == "<h1>Report</h1>"
    assert created(app, ozdenui.WebView(url=page.as_uri()))["props"]["htmlText"] == "<h1>Report</h1>"
    chart = created(app, ozdenui.WebView(html="<b>chart</b>"))["props"]
    assert chart["htmlText"] == "<b>chart</b>" and "html" not in chart  # WHY: html sets the inside of the box in basic.js
    view.load(page)
    assert calls(app, view, "loadHtml")[-1]["args"] == ["<h1>Report</h1>"] and view.html_text == "<h1>Report</h1>" and view.url == ""
    view.url = "https://python.org"
    assert calls(app, view, "load")[-1]["args"] == ["https://python.org"] and view.html_text == ""
    view.html = "<p>new</p>"
    view.post_message({"theme": "dark"})
    view.clear()
    assert calls(app, view, "loadHtml")[-1]["args"] == ["<p>new</p>"] and calls(app, view, "load")[-1]["args"] == [""]
    assert calls(app, view, "postMessage")[-1]["args"] == [{"theme": "dark"}, "*"]


def test_a_message_of_the_page_in_a_web_view_reaches_python(app):
    seen = []
    view = ozdenui.WebView(html="<script>parent.postMessage({ok: 1}, '*')</script>", on_message=lambda v, data: seen.append((v, data)))
    app._dispatch(callback_of(app, view, "onMessage"), "callback", {"args": [{"__bpObject": view._id}, {"ok": 1}, None]})
    assert seen == [(view, {"ok": 1})]


def test_a_chat_view_keeps_the_conversation_in_python(app):
    seen = []
    chat = ozdenui.ChatView(messages=[{"role": "user", "text": "Hi"}, "Hello! **How** can I help?"], empty_text="Ask something",
                            on_send=lambda c, text: seen.append((c, text)))
    command = created(app, chat)
    assert command["props"]["messages"] == [{"key": "p1", "role": "user", "text": "Hi"},
                                            {"key": "p2", "role": "assistant", "text": "Hello! **How** can I help?"}]
    assert command["state"] == {"busy": "busy"} and "onSend" in command["props"] and "onStop" in command["props"]
    me = {"__bpObject": chat._id}
    app._dispatch(callback_of(app, chat, "onSend"), "callback", {"args": [me, "Plan my week", "m1"], "state": {"busy": 0}})
    assert seen == [(chat, "Plan my week")] and chat.messages[-1] == {"key": "m1", "role": "user", "text": "Plan my week"}
    key = chat.add_message(role="assistant")
    chat.busy = True
    chat.append_text(key, "**Mon")
    chat.append_text(key, "day**")
    assert key == "p3" and chat.message_text(key) == "**Monday**" and chat.busy == 1
    assert calls(app, chat, "addMessage")[-1]["args"] == [{"key": "p3", "role": "assistant", "text": ""}]
    assert [c["args"] for c in calls(app, chat, "appendText")] == [["p3", "**Mon"], ["p3", "day**"]]
    app._dispatch(callback_of(app, chat, "onStop"), "callback", {"args": [me], "state": {"busy": 0}})
    assert chat.busy == 0  # WHY: Stop changes it on the page


def test_the_changes_of_a_chat_view_in_code(app):
    chat = ozdenui.ChatView()
    first = chat.add_message("A note", role="system")
    chat.add_message({"role": "user", "text": "Hi", "key": "mine"})
    chat.set_message_text(first, "Today")
    chat.remove_message("mine")
    assert chat.messages == [{"key": "p1", "role": "system", "text": "Today"}]
    chat.set_messages(["One", {"role": "user", "text": "Two"}])
    assert [m["text"] for m in chat.messages] == ["One", "Two"] and calls(app, chat, "setMessages")[-1]["args"][0][1]["key"] == "p3"
    chat.clear()
    chat.set_input_text("Draft")
    chat.empty_text = "Ask"
    assert chat.messages == [] and chat.empty_text == "Ask"
    assert [c["method"] for c in calls(app, chat)][-3:] == ["clear", "setInputText", "setEmptyText"]
    with pytest.raises(ValueError, match="the role of a message"):
        chat.add_message("x", role="bot")


def test_a_chat_view_takes_the_look_of_the_window(dark_app):
    assert created(dark_app, ozdenui.ChatView())["props"]["styleName"] == "dark"


def test_an_accordion_names_its_sections_as_the_page_does(app):
    seen = []
    acc = ozdenui.Accordion(sections=["One", {"key": "two", "text": "Two", "icon_file": "x.png", "opened": True}],
                            on_toggle=lambda a, section: seen.append((a, section["key"])))
    props = created(app, acc)["props"]
    assert props["sections"] == ["One", {"key": "two", "text": "Two", "iconFile": "x.png", "opened": True}]
    assert created(app, acc)["state"] == {"openKeys": "getOpenKeys()"}
    assert acc.open_keys == ["two"] and acc.is_open("two") and not acc.is_open("One")
    app._dispatch(callback_of(app, acc, "onToggle"), "callback",
                  {"args": [{"__bpObject": acc._id}, {"key": "One", "opened": 1}], "state": {"openKeys": ["One", "two"]}})
    assert seen == [(acc, "One")] and acc.open_keys == ["One", "two"]


def test_only_the_first_open_section_stays_without_multiple(app):
    acc = ozdenui.Accordion(multiple=False, sections=[{"key": "a", "opened": 1}, {"key": "b", "opened": 1}])
    assert acc.open_keys == ["a"]
    acc.open("b")
    last = calls(app, acc, "open")[-1]
    assert acc.open_keys == ["b"] and last["args"] == ["b", 1] and last["refresh"] == 1


def test_opening_and_closing_in_code_is_silent_and_kept(app):
    acc = ozdenui.Accordion(sections=["a", "b"])
    acc.open("a")
    acc.open("a")
    acc.open("b")
    assert acc.open_keys == ["a", "b"]
    acc.toggle("a")
    assert acc.open_keys == ["b"] and calls(app, acc, "close")[-1]["args"] == ["a", 1]
    acc.close_all()
    assert acc.open_keys == [] and calls(app, acc, "closeAll")[-1]["args"] == [1]


def test_the_section_of_an_accordion_holds_objects_and_is_made_once(app):
    acc = ozdenui.Accordion(sections=["a"])
    with acc.section("a"):
        label = Label(text="Hi")
    assert acc.section("a") is acc.section("a")
    parts = [c for c in commands(app, "part") if c["of"] == acc._id]
    assert len(parts) == 1 and parts[0]["path"] == [{"call": "getContent", "args": ["a"]}]
    assert created(app, label)["parent"] == parts[0]["id"] and "left" not in created(app, label)["props"]
    acc.remove_section("a")
    assert calls(app, acc, "removeSection")[-1]["args"] == ["a"]
    with acc.section("a"):
        pass
    assert len([c for c in commands(app, "part") if c["of"] == acc._id]) == 2


def test_a_grid_group_is_a_group_with_columns(app):
    with ozdenui.GridGroup(columns=[120, "1fr"], gap=[8, 4], align="left center") as grid:
        label = Label(text="Hi")
    command = created(app, grid)
    assert command["type"] == "GridGroup" and command["props"]["columns"] == [120, "1fr"] and command["props"]["gap"] == [8, 4]
    assert command["args"] == [] and command["props"]["left"] == 0 and command["props"]["align"] == "left center"
    assert created(app, label)["parent"] == grid._id and "left" not in created(app, label)["props"]  # it holds its objects as a group


def test_a_grid_group_takes_its_place_as_params(app):
    grid = ozdenui.GridGroup(10, 20, 300, 200, columns=3)
    props = created(app, grid)["props"]
    assert created(app, grid)["args"] == []
    assert (props["left"], props["top"], props["width"], props["height"], props["columns"]) == (10, 20, 300, 200, 3)


def test_a_grid_group_changes_through_its_methods(app):
    grid = ozdenui.GridGroup(columns=2)
    grid.columns = 4
    grid.set(rows=2, gap=8, align="center", color="red")
    assert grid.columns == 4 and grid.rows == 2 and grid.color == "red"
    methods = {c["method"]: c["args"] for c in calls(app, grid)}
    assert methods == {"setColumns": [4], "setRows": [2], "setGap": [8], "setAlign": ["center"]}
    assert commands(app, "set")[-1]["props"] == {"color": "red"}


def test_place_gives_an_object_a_cell_of_its_own(app):
    with ozdenui.GridGroup(columns=3) as grid:
        label = Label(text="Hi")
        assert grid.place(label, column_span=2) is label
        grid.place(label, column=1, row=0, row_span=2, align="right")
    first, second = calls(app, grid, "place")
    assert first["args"] == [{"__bpObject": label._id}, {"columnSpan": 2}]
    assert second["args"] == [{"__bpObject": label._id}, {"column": 1, "row": 0, "rowSpan": 2, "align": "right"}]


def test_a_value_with_tolist_goes_to_the_page_as_a_list(app):
    class Number:
        def tolist(self):
            return 5

    label = Label(padding=[Number(), 2])
    assert created(app, label)["props"]["padding"] == [5, 2]


def test_the_package_exports(app):
    assert re.match(r"\d+\.\d+\.\d+", ozdenui.__version__)
    for name in ozdenui.__all__:
        assert hasattr(ozdenui, name), name


# *** THE OPEN PROBLEMS AFTER THE SECOND REVIEW (2026-11-03)

def stop_waiting_after(app, seconds):
    """WHY: a test of waiting must fail, not hang: the window closes after a while (WindowClosed)."""
    watchdog = threading.Timer(seconds, lambda: app._tasks.put(None))
    watchdog.daemon = True
    watchdog.start()
    return watchdog


def test_ask_gives_none_when_its_dialog_can_not_be_made(app):
    app._window.failing_types = {"Dialog"}
    watchdog = stop_waiting_after(app, 3)
    assert Dialog.ask("Save the changes?", buttons=["Save", "Cancel"]) is None
    watchdog.cancel()


def test_ask_from_a_background_job_gives_none_when_its_dialog_can_not_be_made(app):
    app._window.failing_types = {"Dialog"}
    answers = []
    job = threading.Thread(target=lambda: answers.append(Dialog.ask("Save?")))
    job.start()
    for _ in range(300):  # the app thread: runs the tasks the job sends
        run_queued_tasks(app)
        if not job.is_alive():
            break
        time.sleep(0.01)
    job.join(1)
    assert answers == [None]


def test_a_page_loaded_again_answers_the_dialog_that_waits(app):
    starts = []
    app._start = lambda page: starts.append(page)
    app._ready.set()

    def load_the_page_again():
        for _ in range(200):
            if any(c["op"] == "static" for c in app._window.applied_commands()):
                app._on_page_ready("26.11.01", 800, 600)
                return
            time.sleep(0.01)

    helper = threading.Thread(target=load_the_page_again)
    helper.start()
    watchdog = stop_waiting_after(app, 3)
    assert Dialog.prompt("A name:") is None
    watchdog.cancel()
    helper.join()
    assert len(starts) == 1  # start() ran again


def test_every_new_hole_in_front_gets_its_own_time(monkeypatch):
    monkeypatch.setattr(app_module, "_GAP_SECONDS", 0.2)
    delivered = []
    order = app_module._EventOrder(delivered.append)
    order.add(2, 2)
    order.add(5, 5)  # two holes: 1 and 3-4
    time.sleep(0.15)
    order.add(1, 1)  # the first hole is filled: the hole in front is 3 now, with its own 0.2 s
    assert delivered == [1, 2]
    time.sleep(0.1)  # 0.25 s after the first hole: its old timer would have skipped the new hole here
    assert delivered == [1, 2]
    time.sleep(0.25)
    assert delivered == [1, 2, 5]


def test_a_canvas_keeps_its_shapes_in_python(app):
    canvas = ozdenui.Canvas(width=300, height=200, shapes=[{"type": "rect", "x": 0, "y": 0, "width": 10, "height": 10, "line_width": 2}])
    props = created(app, canvas)["props"]
    assert props["shapes"] == [{"type": "rect", "x": 0, "y": 0, "width": 10, "height": 10, "lineWidth": 2, "key": "p1"}]
    line = canvas.line(0, 0, 50, 50, color="tomato", line_width=4, dash=[6, 4])
    sun = canvas.circle(100, 50, 20, fill="orange", draggable=True, key="sun")
    picture = canvas.image(0, 0, 20, 20, b"<svg xmlns='http://www.w3.org/2000/svg'/>")
    assert (line, sun, picture) == ("p2", "sun", "p3")
    sent = calls(app, canvas, "addShape")
    assert sent[0]["args"][0] == {"type": "line", "x1": 0, "y1": 0, "x2": 50, "y2": 50, "color": "tomato", "lineWidth": 4, "dash": [6, 4], "key": "p2"}
    assert sent[2]["args"][0]["imageFile"].startswith("data:image/svg+xml")
    with pytest.raises(ValueError, match="already"):
        canvas.circle(0, 0, 5, key="sun")
    with pytest.raises(ValueError, match="type"):
        canvas.add_shape({"x": 1})
    canvas.move_shape(line, 5, 10)
    canvas.update_shape("sun", radius=30, line_width=1)
    assert canvas.shape(line)["x2"] == 55 and canvas.shape("sun")["radius"] == 30
    assert calls(app, canvas, "updateShape")[-1]["args"] == ["sun", {"radius": 30, "lineWidth": 1}]
    canvas.bring_to_front("p1")
    assert [shape["key"] for shape in canvas.shapes] == ["p2", "sun", "p3", "p1"]
    copy = canvas.shape("sun")
    copy["radius"] = 999
    assert canvas.shape("sun")["radius"] == 30  # a copy goes out
    canvas.remove_shape("p3")
    with pytest.raises(KeyError):
        canvas.remove_shape("p3")
    canvas.clear()
    assert canvas.shapes == [] and calls(app, canvas, "setShapes")[-1]["args"] == [[]]


def test_a_canvas_hears_the_page(app):
    seen = []
    canvas = ozdenui.Canvas(drawing=True, on_draw_end=lambda c, shape: seen.append(("draw", shape["line_width"])),
                            on_shape_move=lambda c, shape: seen.append(("move", shape["x"])),
                            on_click=lambda c, x, y, shape: seen.append(("click", x, y, shape and shape["key"])))
    canvas.circle(10, 10, 5, key="ball", draggable=True)
    me = {"__bpObject": canvas._id}
    app._dispatch(callback_of(app, canvas, "onDrawEnd"), "callback", {"args": [me, {"key": "s1", "type": "polyline", "points": [[1, 2], [3, 4]], "lineWidth": 3}]})
    app._dispatch(callback_of(app, canvas, "onShapeMove"), "callback", {"args": [me, {"key": "ball", "type": "circle", "x": 40, "y": 10, "radius": 5}]})
    app._dispatch(callback_of(app, canvas, "onClick"), "callback", {"args": [me, 7, 8, {"key": "ball", "type": "circle", "x": 40, "y": 10}]})
    app._dispatch(callback_of(app, canvas, "onClick"), "callback", {"args": [me, 1, 2, None]})
    assert seen == [("draw", 3), ("move", 40), ("click", 7, 8, "ball"), ("click", 1, 2, None)]
    assert canvas.shape("s1")["points"] == [[1, 2], [3, 4]] and canvas.shape("ball")["x"] == 40
    assert canvas.line(0, 0, 1, 1) == "p1"  # a key of Python is never one of the page ("s1")
    canvas.drawing = False
    assert calls(app, canvas, "setDrawing")[-1]["args"] == [0]
    quiet = ozdenui.Canvas()  # WHY: with no callback of the code, the page still tells Python its new lines
    assert "onDrawEnd" in created(app, quiet)["props"] and "onClick" not in created(app, quiet)["props"]


def test_side_panel_and_loading_screen_need_no_javascript_names(app):
    with VGroup():
        panel = ozdenui.SidePanel(title_text="Filters")
        loading = ozdenui.LoadingScreen(title_text="My App", message="Reading")
    assert created(app, loading)["parent"] == "page"  # it covers the window, also when it is made in a group
    assert created(app, loading)["props"]["messageText"] == "Reading"
    with panel.body:
        box = CheckBox(text="New ones")
    body = commands(app, "part")[-1]
    assert body["of"] == panel._id and body["path"] == [{"call": "getBody"}]
    assert created(app, box)["parent"] == body["id"]
    panel.open()
    assert panel.is_open and commands(app, "call")[-1]["method"] == "open"
    # The page closes it by itself (its cover, Escape): on_close brings the state.
    callback_id = created(app, panel)["props"]["onClose"]["__bpCallback"]
    app._dispatch(callback_id, "callback", {"args": [{"__bpObject": panel._id}], "state": {"isOpened": 0}})
    assert panel.is_open is False
    loading.set_progress(0.4)
    loading.close()
    assert [c["method"] for c in commands(app, "call")[-2:]] == ["setProgress", "close"]


def test_tag_input_keeps_its_tags_and_data_table_gives_the_row(app):
    seen = []
    tags = ozdenui.TagInput(tags=["audio"], on_change=lambda field: seen.append(field.tags))
    assert tags.tags == ["audio"]
    callback_id = created(app, tags)["props"]["onChange"]["__bpCallback"]
    app._dispatch(callback_id, "callback", {"args": [{"__bpObject": tags._id}], "state": {"tags": ["audio", "guide"]}})
    assert seen == [["audio", "guide"]] and tags.tags == ["audio", "guide"]
    tags.tags = ["x"]
    assert commands(app, "call")[-1]["method"] == "setTags" and commands(app, "call")[-1]["args"] == [["x"], 1]  # silent
    assert tags.tags == ["x"]

    rows = []
    table = ozdenui.DataTable(columns=[{"key": "name", "title": "Name"}], rows=[{"id": 1, "name": "Ada"}],
                              on_select=lambda t, row: rows.append(row))
    callback_id = created(app, table)["props"]["onSelect"]["__bpCallback"]
    page_row = {"__bpObject": None, "id": 1, "data": {"id": 1, "name": "Ada"}}
    app._dispatch(callback_id, "callback", {"args": [{"__bpObject": table._id}, page_row],
                                            "state": {"selectedRow": {"id": 1, "name": "Ada"}}})
    assert rows == [{"id": 1, "name": "Ada"}]  # the row as it was given, not the row object of the page
    assert table.selected_row == {"id": 1, "name": "Ada"}


def test_fill_takes_the_room_left_and_scroll_area_scrolls_it(app):
    with VGroup():
        column_part = ozdenui.Box(fill=True)
        with ozdenui.ScrollArea(gap=8, padding=16) as area:
            in_the_area = Label(text="A row")
        with HGroup():
            row_part = ozdenui.Box(fill=True)
    whole = ozdenui.ScrollArea()
    with area:
        added_later = Label(text="One more")
    column = created(app, column_part)["props"]
    assert (column["width"], column["height"], column["grow"]) == ("100%", "auto", 1)
    assert column["css"] == {"flexBasis": "0", "minHeight": "0"} and "fill" not in column
    row = created(app, row_part)["props"]
    assert (row["width"], row["height"], row["css"]) == ("auto", "100%", {"flexBasis": "0", "minWidth": "0"})
    # WHY nothing of a place: the ScrollArea of the kit takes the room left in a group, and fills the page
    made = created(app, area)
    assert made["type"] == "ScrollArea" and (made["props"]["gap"], made["props"]["padding"]) == (8, 16)
    assert "grow" not in made["props"] and "left" not in made["props"]
    assert (created(app, whole)["props"]["left"], created(app, whole)["props"]["top"]) == (0, 0)
    # the objects of its "with" block go into its content, one under the other
    content = next(c for c in commands(app, "part") if c["of"] == area._id)
    assert content["path"] == ["content"]
    assert created(app, in_the_area)["parent"] == created(app, added_later)["parent"] == content["id"]
    assert "left" not in created(app, in_the_area)["props"]  # WHY: the content is a group: it places them


def test_the_usual_window_keeps_the_tones(app):
    assert created(app, SmartButton(text="Send", tone="cyan"))["props"]["tone"] == "cyan"
    assert created(app, SmartButton(text="Delete", tone="orange"))["props"]["tone"] == "orange"


def test_the_keys_of_a_style_may_be_written_in_snake_case(app):
    toggle = Toggle(value=True, button_style={"selected_color": "#2A78D6"}, background_style={"selected_border_color": "#2A78D6"})
    props = created(app, toggle)["props"]
    assert props["buttonStyle"] == {"selectedColor": "#2A78D6"}
    assert props["backgroundStyle"] == {"selectedBorderColor": "#2A78D6"}
    box = CheckBox(text="A", style={"checked_mark": {"border_color": "red"}, "scroll_bar": {"bar_color": "#999"}})
    style = created(app, box)["props"]["style"]
    assert style == {"checkedMark": {"borderColor": "red"}, "scrollBar": {"bar_color": "#999"}}  # the kit's bar_ keys stay
    table = ozdenui.SmartTable(columns=[{"key": "first_name", "title": "Name"}], rows=[{"first_name": "Ada"}])
    assert created(app, table)["props"]["itemDataList"] == [{"first_name": "Ada"}]  # data keeps its keys
    toggle.button_style = {"selected_color": "green"}
    assert commands(app, "set")[-1]["props"]["buttonStyle"] == {"selectedColor": "green"}


def test_a_param_with_a_default_keeps_its_value(app, capsys):
    picked = []
    buttons = [Button(text=str(number), on_click=lambda number=number: picked.append(number)) for number in range(3)]
    app._dispatch(buttons[1]._id, "click", {"x": 1})
    app._dispatch(buttons[2]._id, "click", {"x": 1})
    smart = SmartButton(text="Go", on_click=lambda name="Ada": picked.append(name))
    app._dispatch(callback_of(app, smart, "onClick"), "callback", {"args": [{"__bpObject": smart._id}]})
    assert picked == [1, 2, "Ada"]
    assert "ozdenui" not in capsys.readouterr().err


def test_the_values_of_an_event_go_to_the_params_without_a_default(app):
    import functools

    picked = []

    def pick(number, button):
        picked.append((number, button))

    def on_click(button, event=None):
        picked.append(event)

    def every_value(*values):
        picked.append(len(values))

    first = Button(text="1", on_click=functools.partial(pick, 1))
    second = Button(text="2", on_click=lambda: picked.append(2))
    third = Button(text="3", on_click=lambda button, event: picked.append(event))
    fourth = Button(text="4", on_click=on_click)
    fifth = Button(text="5", on_click=every_value)
    sixth = Button(text="6", on_click=lambda button, event, more: picked.append(more))
    for button in (first, second, third, fourth, fifth, sixth):
        app._dispatch(button._id, "click", {"x": 1})
    assert picked == [(1, first), 2, {"x": 1}, None, 2, None]  # a value the event does not send is None


# *** AN ITEM OF A LIST WITH NO TEXT

def told_about_items(capsys):
    """The warnings about items, with "here" in place of the line of this file, and the lines."""
    told = [text for text in capsys.readouterr().err.splitlines() if 'has no "text"' in text]
    places = [int(re.search(r"test_ozdenui\.py:(\d+):", text).group(1)) for text in told]
    return [re.sub(r"test_ozdenui\.py:\d+", "here", text) for text in told], places


def test_an_item_with_no_text_and_a_key_of_its_own_is_told_once_at_its_line(app, capsys, monkeypatch):
    monkeypatch.setattr(ozdenui.components, "_warned_items", set())  # WHY: told once per line, also in another test
    fruits = ozdenui.ItemList(items=[{"key": "p", "title": "Pear"}, {"key": "q", "title": "Quince"}])
    for name in ("Apple", "Banana"):
        fruits.add_item({"title": name})
    texts, places = told_about_items(capsys)
    assert texts == [
        'ozdenui: here: ItemList: an item has no "text"; "title" is not a key of its items (key, text, description, icon_file, '
        'search_text, enabled, type)'] * 2
    assert places[0] < places[1]  # the line of ItemList(...), then the line of add_item(): each once
    assert fruits.items[0] == {"key": "p", "title": "Pear"}  # the item goes as it was given: only the terminal tells it


def test_an_item_with_a_text_or_with_only_keys_of_the_kit_is_not_told(app, capsys, monkeypatch):
    monkeypatch.setattr(ozdenui.components, "_warned_items", set())
    ozdenui.ItemList(items=["Apple", {"key": "p", "text": "Pear", "price": 3}, {"key": "sea", "icon_file": "data:image/png;base64,AA=="}])
    ozdenui.ToolBar(items=[{"key": "save", "icon": "save", "hint": "Save"}, "-", " "])
    ozdenui.StatusBar(items=[{"key": "busy", "icon": "<svg></svg>", "aria_label": "Busy"}])
    ozdenui.TreeView(items=[{"key": "a", "text": "a", "children": [{"key": "b", "text": "b", "size": 4}, "c"]}])
    assert 'has no "text"' not in capsys.readouterr().err


def test_every_list_tells_about_its_items_and_the_items_in_them(app, capsys, monkeypatch):
    monkeypatch.setattr(ozdenui.components, "_warned_items", set())
    tree = ozdenui.TreeView(items=[{"key": "src", "text": "src", "children": [{"key": "a", "note": "4 KB"}]}])
    tree.add_node("src", {"key": "b", "label": "b.py"})
    ozdenui.StepBar(steps=[{"title": "Pay"}])
    sections = ozdenui.Accordion(sections=["One"])
    sections.add_section({"key": "more", "title": "More"})
    Tabs(tabs=[{"key": "a", "label": "A"}])
    ozdenui.StatusBar(items=[{"key": "count", "value": "3 files"}])
    ozdenui.ToolBar(items=[{"key": "file", "text": "File", "items": [{"key": "open", "title": "Open"}]}])
    texts, _places = told_about_items(capsys)
    assert [text.split(": ")[2] for text in texts] == ["TreeView", "TreeView", "StepBar", "Accordion", "Tabs", "StatusBar", "ToolBar"]
    assert texts[0] == ('ozdenui: here: TreeView: an item has no "text"; "note" is not a key of its items (key, text, icon_file, tag, '
                        'tag_color, description, description_color, text_color, children, expanded, has_children, enabled, data)')
    assert '"label" is not a key' in texts[1] and '"value" is not a key' in texts[5]


def test_a_tab_names_its_keys_and_its_pictures_as_the_page_does(app, tmp_path):
    icon = tmp_path / "home.png"
    icon.write_bytes(b"\x89PNG\r\n\x1a\n")
    tabs = Tabs(tabs=["Plain", {"key": "home", "text": "Home", "icon_file": icon, "selected_icon_file": "https://example.com/home.svg",
                                "aria_label": "Home"}])
    plain, home = created(app, tabs)["props"]["tabs"]
    assert plain == "Plain" and tabs.value == "Plain"
    assert home["iconFile"].startswith("data:image/png;base64,") and home["selectedIconFile"] == "https://example.com/home.svg"
    assert home["ariaLabel"] == "Home" and "icon_file" not in home  # WHY: icon_file went as it was written: no icon


# *** A REVIEW OF THE PACKAGE: a file dropped again, the first selection of a list, a radio, the search of a table

def test_a_second_drop_of_a_file_like_the_first_gets_its_own_path(app):
    """The same name and size from another folder: when the page told first, the path of the first drop was given."""
    seen = []
    picker = ozdenui.FilePicker(on_change=lambda p: seen.append(p.paths))
    callback = callback_of(app, picker, "onChange")
    me = {"__bpObject": picker._id}
    app._keep_dropped_files([{"name": "a.txt", "size": 5, "lastModified": 1, "pywebviewFullPath": "/Users/ada/A/a.txt"}],
                            received=time.monotonic() - 10)  # the first drop, a while ago
    app._dispatch(callback, "callback", {"args": [me], "state": {"files": [page_file()]}})
    assert seen == [["/Users/ada/A/a.txt"]]
    picker.clear()
    seen.clear()
    # The second drop: bridge.js tells of it, then the FilePicker; the path of pywebview comes last
    app._on_page_event(1, "page", "__drop", {"files": [{"name": "a.txt", "size": 5, "lastModified": 1}]})
    app._on_page_event(2, callback, "callback", {"args": [me], "state": {"files": [page_file()]}})
    run_queued_tasks(app)
    assert seen == []  # it waits: the path Python has belongs to the first drop
    _event, on_drop = app._window.drop_handlers[0]
    on_drop({"dataTransfer": {"files": [{"name": "a.txt", "size": 5, "lastModified": 1, "pywebviewFullPath": "/Users/ada/B/a.txt"}]}})
    deadline = time.time() + 2
    while not seen and time.time() < deadline:
        run_queued_tasks(app)
        time.sleep(0.01)
    assert seen == [["/Users/ada/B/a.txt"]] and picker.paths == ["/Users/ada/B/a.txt"]


def test_a_path_that_came_just_before_the_drop_belongs_to_it(app):
    picker = ozdenui.FilePicker()
    _event, on_drop = app._window.drop_handlers[0]
    on_drop({"dataTransfer": {"files": [{"name": "a.txt", "size": 5, "lastModified": 1, "pywebviewFullPath": "/Users/ada/B/a.txt"}]}})
    app._on_page_event(1, "page", "__drop", {"files": [{"name": "a.txt", "size": 5, "lastModified": 1}]})  # pywebview first
    run_queued_tasks(app)
    picker._values["files"] = [page_file()]
    assert picker.paths == ["/Users/ada/B/a.txt"]


def test_two_dropped_files_of_the_same_name_and_size_keep_their_own_paths(app):
    picker = ozdenui.FilePicker(multiple=True)
    app._keep_dropped_files([{"name": "a.txt", "size": 5, "lastModified": 1, "pywebviewFullPath": "/Users/ada/A/a.txt"},
                             {"name": "a.txt", "size": 5, "lastModified": 2, "pywebviewFullPath": "/Users/ada/B/a.txt"}])
    picker._values["files"] = [page_file(), dict(page_file(), lastModified=2)]
    assert picker.paths == ["/Users/ada/A/a.txt", "/Users/ada/B/a.txt"]  # (both were B)


def test_a_list_keeps_its_first_selection_as_the_page_does(app):
    items = [{"key": "p", "text": "Projects"}, {"type": "section", "key": "s", "text": "MORE"}, {"key": "d", "text": "Designs"}]
    single = ozdenui.ItemList(items=items, selected_keys=["p", "d", "zz"])
    assert single.selected_keys == ["d"] and single.selected == [items[2]]  # WHY: it was [] until the first event
    multiple = ozdenui.ItemList(items=items, selection="multiple", selected_keys=["d", "s", "p", "d"])
    assert multiple.selected_keys == ["d", "p"] and [item["key"] for item in multiple.selected] == ["d", "p"]
    assert ozdenui.ItemList(items=items, selection="none", selected_keys=["p"]).selected_keys == []
    numbers = ozdenui.ItemList(items=["A", "B"], selected_keys=[1])
    assert numbers.selected_keys == ["1"] and numbers.selected == [{"key": "1", "text": "B"}]


def test_a_radio_is_read_while_a_background_job_makes_objects(app):
    for size in "SML":
        RadioButton(group="size", value=size, text=size, checked=(size == "M"))
    for number in range(500):
        Label(text=str(number))
    stop = threading.Event()

    def background_job():
        while not stop.is_set():
            Label(text="row")

    threading.Thread(target=background_job, daemon=True).start()
    try:
        deadline = time.time() + 0.5
        while time.time() < deadline:
            assert RadioButton.value_of("size") == "M"  # WHY: "dictionary changed size during iteration" before
    finally:
        stop.set()


def test_the_search_of_a_table_uses_one_box(app):
    table = ozdenui.SmartTable(columns=[{"key": "a"}])
    before = len(app._objects)
    for text in ("a", "ab", "abc"):
        table.search(text)
    assert len(app._objects) == before + 1  # WHY: a new part at every search stayed on both sides
    parts = [c for c in commands(app, "part") if c["of"] == table._id]
    assert len(parts) == 1 and [c["args"] for c in calls(app, SimpleNamespace(_id=parts[0]["id"]), "setValue")] == [["a", 1], ["ab", 1], ["abc", 1]]


# *** THE TEXT OF A LABEL AND OF A BUTTON IS PLAIN; html= IS HTML

def test_the_text_of_a_label_is_shown_as_it_is_written(app):
    label = Label(text="<b>Ada</b>")
    button = Button(text="1 < 2")
    assert created(app, label)["props"] == {"left": 0, "top": 0, "plainText": "<b>Ada</b>"}
    assert created(app, button)["props"]["plainText"] == "1 < 2"
    assert label.text == "<b>Ada</b>"

    # WHY text on the page: a Label and a Button of basic.js have no html (only a Box has one): their text is the HTML.
    #     Sent as html it showed nothing (seen in a real window).
    label.html = "<b>Bold</b>"
    assert commands(app, "set")[-1]["props"] == {"text": "<b>Bold</b>"}
    assert label.html == "<b>Bold</b>"
    assert created(app, Label(html="<b>3</b> new"))["props"] == {"left": 0, "top": 0, "text": "<b>3</b> new"}
    assert created(app, Button(html="<i>Go</i>"))["props"]["text"] == "<i>Go</i>"
    assert created(app, Box(0, 0, 10, 10, html="<u>box</u>"))["props"]["html"] == "<u>box</u>"  # a Box has html
    with pytest.raises(AttributeError, match="measure"):
        label.text  # WHY: the text it shows now came with the HTML: Python does not know it

    label.plain_text = "Typed"  # the name of basic.js works too
    assert commands(app, "set")[-1]["props"] == {"plainText": "Typed"}
    assert label.text == "Typed" and label.plain_text == "Typed"
    with pytest.raises(AttributeError):
        label.html

    label.measure("text")
    assert app._window.scripts[-1].count("plainText") == 1


def test_a_component_takes_allow_html_for_its_texts(app, capsys, monkeypatch):
    monkeypatch.setattr(ozdenui.objects, "_warned_names", set())
    plain = SmartButton(text="<b>Save</b>")
    html = SmartButton(text="<b>Save</b>", allow_html=True)
    assert "allowHtml" not in created(app, plain)["props"]  # WHY: the kit shows the text as it is written by itself
    assert created(app, html)["props"]["allowHtml"] == 1 and created(app, html)["props"]["labelText"] == "<b>Save</b>"
    assert "is not a param" not in capsys.readouterr().err


# *** A NAME AN OBJECT DOES NOT HAVE

def told_about_names(capsys):
    told = [text for text in capsys.readouterr().err.splitlines() if "is not a param" in text]
    return [re.sub(r"test_ozdenui\.py:\d+", "here", text) for text in told]


def test_a_misspelled_name_is_told_once_at_its_line(app, capsys, monkeypatch):
    monkeypatch.setattr(ozdenui.objects, "_warned_names", set())  # WHY: told once per line, also in another test
    for word in ("Hi", "Hello"):
        label = Label(txet=word, font_size=20)
    label.set(font_sise=22)
    SmartButton(lable_text="Save")
    CheckBox(text="Remember me", chekced=True)
    ozdenui.Tooltip(target=label, hint_text="Hi", lbl_arrow=10)  # WHY: it goes as lblArrow: not a guess
    assert told_about_names(capsys) == [
        'ozdenui: here: Label: "txet" is not a param of Label (did you mean "text"?)',
        'ozdenui: here: Label: "font_sise" is not a param of Label (did you mean "font_size"?)',
        'ozdenui: here: SmartButton: "lable_text" is not a param of SmartButton (did you mean "label_text"?)',
        'ozdenui: here: CheckBox: "chekced" is not a param of CheckBox (did you mean "checked"?)',
        'ozdenui: here: Tooltip: "lbl_arrow" is not a param of Tooltip',
    ]
    assert created(app, label)["props"]["txet"] == "Hello"  # it still goes to the page: only the terminal tells it


def test_the_names_of_the_kit_and_of_python_are_not_told(app, capsys, monkeypatch):
    monkeypatch.setattr(ozdenui.objects, "_warned_names", set())
    with VGroup(hug=True, gap=4, wrap=True, align="left top", justify="space-between", padding=[8, 4], clip_content=False):
        Label(text="A", font_size=13, text_color="red", plain_text="B", html="<b>C</b>", fill=True, on_click=lambda: None)
        Box(0, 0, 10, 10, color="red", round=4, scroll_y=True, css={"cursor": "pointer"}, on_mouse_enter=lambda: None)
    SmartButton(text="Save", icon_file="", tone="cyan", style_name="ozden", key="save", width=64)
    ozdenui.TextField(title_text="Name", text="Ada", on_enter=lambda: None, required=True)
    Component("Gauge", value=72, sub_text="Disk", framed=False)
    ozdenui.Input(20, 150, 200, 40, placeholder="A name", on_enter=lambda: None)
    Component("SomethingOfMine", whatever=1)  # its params are not known: nothing is told
    app.page.color = "#F4F5F7"
    assert told_about_names(capsys) == []


def test_the_text_of_a_box_is_not_a_name_of_a_component(app, capsys, monkeypatch):
    # WHY: given to a Slider, the html of its box went in as HTML, with no word (a Slider has no text)
    monkeypatch.setattr(ozdenui.objects, "_warned_names", set())
    ozdenui.Slider(value=3, html="<b>3</b>")
    Box(0, 0, 10, 10, html="<b>a Box has it</b>")
    assert told_about_names(capsys) == ['ozdenui: here: Slider: "html" is not a param of Slider']


def test_a_camel_case_name_given_to_a_class_is_told_with_its_python_name(app, capsys, monkeypatch):
    # WHY: a class reads its params and gives its defaults by their Python names, so a camelCase name went under them
    #      without a word: TextField(titleText="Name") had no title, CheckBox(onChange=fn) never called fn
    monkeypatch.setattr(ozdenui.objects, "_warned_names", set())
    for _ in range(2):
        field = ozdenui.TextField(titleText="Name")  # told once at its line
    CheckBox(text="Remember me", onChange=lambda box: None)
    field.titleText = "Surname"
    ozdenui.TextField(title_text="Name", titelText="x")  # not a name of the kit: only the warning of unknown names
    Component("Gauge", subText="Disk")  # a component with no class takes both ways
    told = [re.sub(r"test_ozdenui\.py:\d+", "here", line) for line in capsys.readouterr().err.splitlines()]
    reason = "(a class reads its params by their Python names)"
    assert told == [
        f'ozdenui: here: TextField: "titleText" is written "title_text" in Python {reason}',
        f'ozdenui: here: CheckBox: "onChange" is written "on_change" in Python {reason}',
        f'ozdenui: here: TextField: "titleText" is written "title_text" in Python {reason}',
        'ozdenui: here: TextField: "titelText" is not a param of TextField (did you mean "title_text"?)',
    ]


# *** A PARAM CHANGED AFTER THE START: THE METHOD OF THE KIT FOR IT

def test_a_param_with_a_method_of_the_kit_is_changed_with_it(app):
    # WHY: sent as a value, it changed nothing on the page, without a word (seen in a real window)
    field = ozdenui.TextField(title_text="Weight", unit_text="kg")
    field.unit_text = "lb"
    field.set(description_text="In pounds", focus_line_color="red")
    assert [(c["method"], c["args"]) for c in calls(app, field)] == [
        ("setUnitText", ["lb"]), ("setDescriptionText", ["In pounds"]), ("setFocusLineColor", ["red"])]
    assert (field.unit_text, field.description_text) == ("lb", "In pounds")
    assert commands(app, "set") == []

    table = ozdenui.DataTable(columns=[{"key": "name"}], rows=[{"id": 1, "name": "Ada"}])
    table.rows = [{"id": 2, "name": "Bob"}]
    command = calls(app, table, "setRows")[-1]
    assert command["args"] == [[{"id": 2, "name": "Bob"}]] and command["refresh"] == 1  # the selection comes back with it

    split = ozdenui.Splitter(first_size=100)
    split.first_size = 200
    assert calls(app, split, "setFirstSize")[-1]["args"] == [200, 1]  # WHY 1: silent, a change of the code calls no callback

    button = SmartButton(text="Save")
    button.style = {"box": {"border_color": "red"}}
    assert calls(app, button, "setStyle")[-1]["args"] == [{"box": {"borderColor": "red"}}]

    gauge = Component("Gauge", value=10)  # a component with no class of its own
    gauge.value = 80
    gauge.set(sub_text="Disk", whatever=1)
    assert [(c["method"], c["args"]) for c in calls(app, gauge)] == [("setValue", [80, 1]), ("setSubText", ["Disk"])]
    assert commands(app, "set")[-1]["props"] == {"whatever": 1}  # no method for it: a value of the page, as before


def test_a_short_name_set_later_is_read_back(app):
    loading = ozdenui.LoadingScreen(title="My App", message="Reading")
    loading.message = "Step 2"
    assert calls(app, loading, "setMessageText")[-1]["args"] == ["Step 2"]
    assert (loading.message, loading.message_text, loading.title) == ("Step 2", "Step 2", "My App")


def test_new_tabs_go_as_the_page_names_them_and_their_pages_are_made_again(app):
    tabs = Tabs(tabs=["Orders", "Customers"])
    old_page = tabs.panel("Orders")
    tabs.tabs = ["Orders", {"key": "stock", "text": "Stock", "selected_color": "red"}]
    command = calls(app, tabs, "setTabs")[-1]
    assert command["args"] == [["Orders", {"key": "stock", "text": "Stock", "selectedColor": "red"}], 1]
    assert command["refresh"] == 1  # the open tab as the page keeps it
    assert tabs.panel("Orders") is not old_page  # WHY: the page removed the old one with the old tabs


def test_a_toggle_set_in_code_is_silent(app):
    """WHY: the Toggle of the kit calls onChange from setValue() unless it is told to be silent; the other components
    are silent when the code sets their value, and so is the Python Toggle."""
    seen = []
    toggle = Toggle(value=False, on_change=lambda t: seen.append(t.value))
    toggle.value = True
    assert [c["args"] for c in calls(app, toggle, "setValue")] == [[1, 1]]
    assert toggle.value is True and seen == []


def test_on_enter_of_an_input_runs_only_for_enter(app):
    seen = []
    field = ozdenui.Input(20, 150, 200, 40, placeholder="Write a text", on_enter=lambda: seen.append("enter"))
    assert "onEnter" not in created(app, field)["props"]
    assert any(c["event"] == "keydown" for c in commands(app, "listen") if c["id"] == field._id)
    field._receive("keydown", {"key": "a", "text": "A"})
    assert seen == []
    field._receive("keydown", {"key": "Enter", "text": "Ada"})
    assert seen == ["enter"] and field.text == "Ada"


def test_framed_false_takes_the_frame_of_a_component(app):
    plain = ozdenui.LogView(height=200, framed=False)
    assert created(app, plain)["props"]["style"] == {"box": {"border": 0, "round": 0}}
    assert "framed" not in created(app, plain)["props"]
    own = ozdenui.LogView(height=200, framed=False, style={"box": {"round": 8, "color": "white"}, "line": {"font_size": 12}})
    assert created(app, own)["props"]["style"] == {"box": {"round": 8, "color": "white", "border": 0}, "line": {"fontSize": 12}}
    assert created(app, Component("Gauge", framed=False))["props"]["style"] == {"box": {"border": 0, "round": 0}}
    assert "style" not in created(app, ozdenui.LogView(height=200))["props"]  # framed=True, the default, adds nothing
