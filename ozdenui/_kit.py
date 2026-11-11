# Bismillah
"""_kit.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The names of the kit copy in web/, read from its files the first time they are needed: the components and their files
(components.js), the params of a component (the first keys of its Defaults) and its methods that change one (setTitleText),
the props of a basic.js object (the setters of basic.min.js), the default of a callback param and the keys of
an item of a list. The warning about a name an object does not have, a param changed after the start, a callback given
as None, make_stubs.py and tests/test_kit_names.py use them.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import re
from functools import lru_cache
from pathlib import Path

WEB_FOLDER = Path(__file__).resolve().parent / "web"
# The objects of basic.js itself (the makers of bridge.js), not components of comp/
BASIC_TYPES = ("Box", "Label", "Button", "Input", "Icon", "VGroup", "HGroup")
GROUP_TYPES = ("VGroup", "HGroup")
GROUP_PARAMS = ("flow", "align", "gap", "padding", "wrap", "justify", "hug", "fit")  # startFlexBox() of basic.js
PLAIN_PARAMS = ("styleName", "style", "key")  # every component takes them besides its own
EXTRA_ITEM_KEYS = {"ItemList": ("type",)}  # WHY: ItemList names a title row { type: "section", text }
# The props of a box that are not names of a component: the content of the box, which a component fills itself.
# WHY: Toggle(text="Dark <b>mode</b>") was not told (a Toggle has no text), and the text went into its box as HTML.
CONTENT_PROPS = frozenset(("text", "html"))
_DEFAULTS_BLOCK = re.compile(r"^( *)const \w*[Dd]efaults = \{[ \t]*\n(.*?)^\1\};", re.S | re.M)
_SET_METHOD = re.compile(r"\bbox\.(set[A-Z]\w*)\s*=\s*(?:async\s+)?function\s*\(([^)]*)\)")


@lru_cache(maxsize=None)
def component_files():
    """The name of a component -> its file, from the list of the loader (components.js)."""
    text = (WEB_FOLDER / "components.js").read_text(encoding="utf-8")
    return {name: WEB_FOLDER / file for name, file in re.findall(r'^\s+(\w+): \["([^"]+)"', text, re.M)}


@lru_cache(maxsize=None)
def object_props():
    """The props of every basic.js object: the setters of its classes (set left(...), set color(...)...)."""
    text = (WEB_FOLDER / "basic" / "basic.min.js").read_text(encoding="utf-8")
    return frozenset(re.findall(r"\bset (\w+)\(", text))


@lru_cache(maxsize=None)
def source_of(type_name):
    """The code of a component and of the component it is made from (startExtendedObject)."""
    text = component_files()[type_name].read_text(encoding="utf-8")
    parent = re.search(r"startExtendedObject\((\w+),", text)
    if parent and parent.group(1) in component_files() and parent.group(1) != type_name:
        text += source_of(parent.group(1))
    return text


@lru_cache(maxsize=None)
def component_defaults(type_name):
    """The params of a component and the text of their default values: {"labelText": '""', "onClick": "function..."}.
    WHY the indent: an older component keeps them in its function (Tooltip: const defaults = {...})."""
    defaults = {}
    for block in _DEFAULTS_BLOCK.finditer(source_of(type_name)):
        key_indent = block.group(1) + "    "
        for name, value in re.findall(r"^" + key_indent + r"([A-Za-z_$][\w$]*)\s*:\s*(.*)$", block.group(2), re.M):
            defaults.setdefault(name, value)
    return defaults


def no_function(type_name, key):
    """What a callback param takes when the program gives None (on_click=None): the default of the component. An empty
    function where the kit has a function (the component calls it); None where the kit has null (the component has its
    own way then: a MarkdownView opens a link in the browser) and for a param that is no function at all (on_mark of
    a Toggle is a text: a function there was shown as its mark)."""
    default = component_defaults(type_name).get(key, "") if type_name in component_files() else ""
    is_function = default.startswith("function") or "=>" in default.split("//")[0]
    return {"__bpNoop": 1} if is_function else None


@lru_cache(maxsize=None)
def component_params(type_name):
    """The params of a component (its own and its parent's)."""
    return frozenset(component_defaults(type_name))


@lru_cache(maxsize=None)
def component_setters(type_name):
    """The params of a component it has a method for, the way of the kit to change a param after the start:
    {"unitText": ("setUnitText", False)}. True: the method takes silent after the value (1: its callback is not
    called). {}: a type this file does not know."""
    if type_name not in component_files():
        return {}
    methods = {name: arguments for name, arguments in _SET_METHOD.findall(source_of(type_name))}
    setters = {}
    for param in component_defaults(type_name):
        method = "set" + param[:1].upper() + param[1:]
        if method in methods:
            second = [argument.split("=")[0].strip() for argument in methods[method].split(",")][1:2]
            setters[param] = (method, second == ["silent"])
    return setters


@lru_cache(maxsize=None)
def known_names(type_name):
    """Every name an object of this type takes, as the page names it (camelCase). None: a type this file does not know."""
    if type_name in component_files():
        return component_params(type_name) | (object_props() - CONTENT_PROPS) | frozenset(PLAIN_PARAMS)
    if type_name in GROUP_TYPES:
        return object_props() | frozenset(GROUP_PARAMS)
    if type_name in BASIC_TYPES:
        return object_props()
    return None


@lru_cache(maxsize=None)
def item_keys(type_name):
    """The keys of an item of a list as the kit writes them: the { key, ... } groups of its header and of its defaults
    (before the function of the component: a group in the function is a record of its own)."""
    text = component_files()[type_name].read_text(encoding="utf-8")
    function = re.search(r"^const " + type_name + r" = function", text, re.M)
    head = text[:function.start()] if function else text
    keys = set(EXTRA_ITEM_KEYS.get(type_name, ()))
    for group in re.findall(r"\{ ?(key, [A-Za-z, ]+)\}", head):
        keys |= {name.strip() for name in group.split(",") if name.strip()}
    return frozenset(keys)
