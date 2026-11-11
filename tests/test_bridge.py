# Bismillah
"""test_bridge.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
bridge.js, the page side of ozdenui, in Node (tests/bridge_harness.js: a small fake of basic.js and of pywebview): the
values from Python (a number format, a callback, an empty function), the values that go to Python and the answer of
__bp.apply() (its errors, the removed objects, the number of the last event). Skipped on a computer without node.
WHY: the functions of the page had no test; a format of Python written wrong on the page ({:.1%} without its %) was
found only in a real window.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from ozdenui.values import number_format

TESTS_FOLDER = Path(__file__).resolve().parent
BRIDGE_FILE = TESTS_FOLDER.parent / "ozdenui" / "web" / "bridge.js"
HARNESS_FILE = TESTS_FOLDER / "bridge_harness.js"
NODE = shutil.which("node")
PAGE_SECONDS = 30
# Python's own text of each (no tie of rounding: Python and the page round a tie in their own ways)
FORMATS = [("{:.1%}", 0.123), ("{:%}", 0.5), ("{:,.0f} TL", 1234567.89), ("{:.2f}", 3.14159), ("{}", 2.5),
           ("{:,}", 1234567), ("{:d}", 42), ("{:,.1f} kg", -1234.56), ("Total: {:,}", 98765)]

pytestmark = pytest.mark.skipif(NODE is None, reason="node is not on this computer")


def run_page(code):
    """What code (the body of a JavaScript function) returns on a page with bridge.js, as JSON."""
    finished = subprocess.run([NODE, str(HARNESS_FILE), str(BRIDGE_FILE)], input=code, capture_output=True, text=True,
                              encoding="utf-8", timeout=PAGE_SECONDS)
    assert finished.returncode == 0, finished.stderr
    return json.loads(finished.stdout)


def create(object_id, props, kind="Box", state=None):
    """A create command of Python, as a JavaScript value."""
    return json.dumps({"op": "create", "id": object_id, "type": kind, "args": [], "props": props, "parent": "page",
                       "state": state, "src": "test.py:1"})


def test_a_page_loaded_again_for_another_theme_has_its_ground_at_once():
    # WHY: the page loaded again by app.set_theme("dark") was light for a moment before Python drew it dark
    from ozdenui import app as app_module

    assert app_module._EARLY_PAGE_COLOR_PREFIX in BRIDGE_FILE.read_text(encoding="utf-8")
    colors = run_page("""
        window.start();
        const first = page.color === undefined ? null : page.color;
        window.name = "ozdenui-page-color:#1C1C1B";
        window.start();
        const dark = page.color;
        page.color = undefined;
        window.name = "ozdenui-page-color:";
        window.start();
        return [first, dark, page.color === undefined ? null : page.color];
    """)
    assert colors == [None, "#1C1C1B", None]


def test_a_number_format_writes_the_text_of_python():
    props = {f"format{place}": number_format(template, "test") for place, (template, _value) in enumerate(FORMATS)}
    texts = run_page(f"""
        __bp.apply([{create("o1", props)}]);
        const given = __bp.objectOf("o1").given;
        return {json.dumps([value for _template, value in FORMATS])}.map(function (value, place) {{
            return given["format" + place](value);
        }});
    """)
    assert texts == [template.format(value) for template, value in FORMATS]


def test_a_callback_sends_its_values_to_python():
    emitted = run_page(f"""
        __bp.apply([{create("o1", {"onChange": {"__bpCallback": "c1", "wholeArgs": [1]}, "onPick": {"__bpCallback": "c2"}})}]);
        const box = __bp.objectOf("o1");
        const deep = {{ a: {{ b: {{ c: {{ d: {{ e: 1 }} }} }} }} }};
        const looped = {{ name: "loop", list: [] }};
        looped.self = looped;
        looped.list.push(looped);
        const chain = {{}};
        let link = chain;
        for (let count = 0; count < 100; count++) {{
            link.next = {{}};
            link = link.next;
        }}
        box.given.onChange(box, deep);
        box.given.onPick(box, deep, looped, chain, new Date(Date.UTC(2026, 10, 10)));
        return emitted;
    """)
    (number, target, event, data), (next_number, next_target, _event, next_data) = emitted
    assert (number, target, event, next_number, next_target) == (1, "c1", "callback", 2, "c2")
    assert data["args"][0] == {"__bpObject": "o1"}  # an object of Python goes as its id
    assert json.loads(data["args"][1]["__bpJson"]) == {"a": {"b": {"c": {"d": {"e": 1}}}}}  # wholeArgs: a JSON text
    deep, looped, chain, date = next_data["args"][1:]
    assert deep == {"a": {"b": {"c": {"d": {"e": 1}}}}}  # WHY whole: data.owner.address of an item came as None
    assert looped == {"name": "loop", "list": [None], "self": None}  # a value that holds itself: None where it comes again
    levels = 0
    while chain is not None:
        chain, levels = chain["next"], levels + 1
    assert 20 < levels < 100  # MAX_VALUE_DEPTH: a guard against what is not data
    assert date == "2026-11-10T00:00:00.000Z"


def test_an_empty_function_does_nothing_and_a_callback_sends_the_state():
    seen = run_page(f"""
        __bp.apply([{create("o1", {"onClick": {"__bpNoop": 1}, "onChange": {"__bpCallback": "c1"}}, "Thing",
                            {"checked": "checked"})}]);
        const thing = __bp.objectOf("o1");
        const noop = thing.given.onClick(thing);
        thing.checked = 1;
        thing.given.onChange(thing);
        return {{ noop: (noop === undefined), emitted: emitted }};
    """)
    assert seen["noop"] is True
    assert seen["emitted"] == [[1, "c1", "callback", {"args": [{"__bpObject": "o1"}], "state": {"checked": 1}}]]


def test_the_answer_of_apply_tells_the_errors_the_removed_objects_and_the_last_event():
    answer = run_page(f"""
        __bp.apply([{create("o1", {})}, {create("o2", {})}]);
        return __bp.apply([
            {create("o3", {}, "NoSuchThing")},
            {{ op: "remove", id: "o1" }},
            {{ op: "set", id: "o9", props: {{}}, src: "test.py:8" }},
            {{ op: "static", target: "NoSuchThing", method: "show", args: [], answer: "c5", src: "test.py:9" }},
        ]);
    """)
    errors = [(error["op"], error["id"], error["src"], error["message"]) for error in answer["errors"]]
    assert errors == [
        ("create", "o3", "test.py:1", 'NoSuchThing is not loaded (App(components=["NoSuchThing"]) loads it)'),
        ("set", "o9", "test.py:8", "There is no object o9 (removed?)"),
        ("static", "NoSuchThing", "test.py:9", "NoSuchThing.show is not loaded"),
    ]
    assert answer["removed"] == ["o1"]  # and Python forgets its functions
    assert answer["lastEvent"] == 1  # WHY 1: the answer of the failed static (None), so Python does not wait for ever
