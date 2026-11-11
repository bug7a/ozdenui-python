# Bismillah
"""test_kit_names.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The names Python sends to the page are names of the kit copy in ozdenui/web: every param a class gives, every method it
calls, the state it reads, every param of the examples, the handbook and the README, and the keys of the items of their
lists (an item of an ItemList, a node of a TreeView, a step, a section, a tab, a part of a StatusBar, a tool).
WHY: the kit renames its params (Slider currentValue -> value, InputB -> TextField...). A name the page does not know
becomes a plain property of the box, with no word: the window opened, but the slider started at 0. After a new copy of
the kit (update-web.sh) this file names every place to change.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import ast
import inspect
import re
from pathlib import Path

import pytest

import ozdenui
from ozdenui import components, objects
from ozdenui._kit import (CONTENT_PROPS, PLAIN_PARAMS, component_files, component_params as params_of, component_setters,
                          item_keys as item_keys_of, object_props, source_of)
from ozdenui.values import camel_case, snake_case
from test_ozdenui import app, commands, created  # noqa: F401 (app is a fixture)

PACKAGE_FOLDER = Path(ozdenui.__file__).resolve().parent
SOURCE_FOLDER = PACKAGE_FOLDER.parent
CODE_BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)
# Python names that do not go to the page as they are (fill=True is a flex grow, framed=False a style of the box)
PYTHON_ONLY_PARAMS = {"fill", "framed"}
# Methods of every basic.js object (Basic_UIComponent), not of one component
OBJECT_METHODS = {"focus", "remove", "setMotion", "props"}
FILES = component_files()


def is_param(type_name, key):
    """A param of the component or a prop of basic.js; not the content of its box (text, html): a component fills it."""
    return key in params_of(type_name) or key in (object_props() - CONTENT_PROPS) or key in PLAIN_PARAMS


def has_method(type_name, name):
    """box.name = function, Comp.name = function or name: function. WHY not a plain name = function: a private helper
    of the component (const setText = function) is not a method of the page; it hid a call of a renamed one."""
    owner = r"\b(?:box|self|that|[A-Z]\w*)\.\s*" + re.escape(name) + r"\s*="
    in_an_object = r"\b" + re.escape(name) + r"\s*:"
    pattern = r"(?:" + owner + "|" + in_an_object + r")\s*(?:async\s+)?(?:function\b|\()"
    return name in OBJECT_METHODS or re.search(pattern, source_of(type_name)) is not None


def has_property(type_name, name):
    return is_param(type_name, name) or re.search(r"\bbox\." + re.escape(name) + r"\s*=", source_of(type_name)) is not None


def python_classes():
    """The component classes of Python: (the class, the name of its component)."""
    found = []
    for cls in vars(components).values():
        is_class = isinstance(cls, type) and issubclass(cls, objects.TypedComponent) and not cls.__name__.startswith("_")
        if is_class and cls.__module__ == components.__name__:
            found.append(cls)
    return sorted(found, key=lambda cls: cls.__name__)


def need_component(cls):
    if cls._type not in FILES:
        pytest.fail(f"{cls.__name__}: there is no {cls._type} in components.js (the kit renamed it?)")


def make(cls):
    """An object of the class with the values it must have."""
    needed = {"Tooltip": {"target": ozdenui.Box(0, 0, 10, 10)}, "SmartTable": {"columns": [{"key": "a"}]}}
    return cls(**needed.get(cls.__name__, {}))


def test_every_component_of_a_class_is_in_the_kit():
    missing = [cls.__name__ for cls in python_classes() if cls._type not in FILES]
    assert missing == [], f"no file in components.js for {missing}"


@pytest.mark.parametrize("cls", python_classes(), ids=lambda cls: cls.__name__)
def test_a_class_gives_only_params_of_the_kit(app, cls):
    need_component(cls)
    props = created(app, make(cls))["props"]
    unknown = sorted(key for key in props if not is_param(cls._type, key))
    unknown += sorted(f"{name} (an alias)" for name in cls._aliases.values() if not is_param(cls._type, camel_case(name)))
    unknown += sorted(f"{name} (a default)" for name in cls._defaults if not is_param(cls._type, camel_case(name)))
    assert unknown == [], f"{cls.__name__} gives params that {cls._type} does not have: {unknown}"


@pytest.mark.parametrize("cls", python_classes(), ids=lambda cls: cls.__name__)
def test_a_class_calls_only_methods_of_the_kit_and_reads_its_state(cls):
    need_component(cls)
    # WHY its bases too: a call of a shared base (the set_title of the fields) was not read, so a renamed method of
    #     the kit was not found
    own_classes = [klass for klass in cls.__mro__ if klass.__module__ == "ozdenui.components"]
    source = "\n".join(inspect.getsource(klass) for klass in own_classes)
    called = set(re.findall(r"\bself\.(?:call|_call_and_refresh|_change_and_refresh|ask)\(\s*\"(\w+)\"", source))
    called |= set(re.findall(r"\bself\._call_with_items\(\s*\"\w+\",\s*\"(\w+)\"", source))  # (slot, method, ...)
    missing = sorted(name for name in called if not has_method(cls._type, name))
    for accessor in cls._state.values():
        is_method = accessor.endswith("()")
        name = accessor[:-2] if is_method else accessor
        if not (has_method(cls._type, name) if is_method else has_property(cls._type, name)):
            missing.append(f"{accessor} (the state)")
    assert missing == [], f"{cls.__name__} uses what {cls._type} does not have: {missing}"


def python_names(cls):
    """The names a class takes besides the params of its component: its aliases, the named params of __init__."""
    names = set(cls._aliases) | PYTHON_ONLY_PARAMS
    for klass in cls.__mro__:
        if "__init__" in vars(klass):
            parameters = inspect.signature(vars(klass)["__init__"]).parameters.values()
            names |= {p.name for p in parameters if p.kind in (p.KEYWORD_ONLY, p.POSITIONAL_OR_KEYWORD)}
    return names


def calls_in(code, where):
    """[(where, the class or the component, its keyword names)] of the components made in a code."""
    classes = {cls.__name__: cls for cls in python_classes()}
    made = []
    for node in ast.walk(ast.parse(code)):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        keywords = [keyword.arg for keyword in node.keywords if keyword.arg]
        place = f"{where}:{node.lineno}"
        if node.func.id in classes:
            made.append((place, classes[node.func.id], keywords))
        elif node.func.id == "Component" and node.args and isinstance(node.args[0], ast.Constant):
            made.append((place, node.args[0].value, keywords))
    return made


def codes_of_the_package():
    """(where, code): every example, and every Python block of the handbook and of the README that is whole Python."""
    codes = [(f"examples/{path.name}", path.read_text(encoding="utf-8")) for path in sorted((SOURCE_FOLDER / "examples").glob("*.py"))]
    for chapter in [SOURCE_FOLDER / "README.md"] + sorted((SOURCE_FOLDER / "handbook").rglob("*.md")):
        for number, code in enumerate(CODE_BLOCK.findall(chapter.read_text(encoding="utf-8")), start=1):
            try:
                ast.parse(code)
            except SyntaxError:
                continue  # a piece of a program (the handbook checks it is Python where it is whole)
            codes.append((f"{chapter.relative_to(SOURCE_FOLDER).as_posix()} block {number}", code))
    return codes


def test_the_examples_and_the_handbook_give_only_names_of_the_kit():
    unknown = []
    for where, code in codes_of_the_package():
        for place, made, keywords in calls_in(code, where):
            type_name = made if isinstance(made, str) else made._type
            if type_name not in FILES:
                unknown.append(f"{place}: {type_name} is not a component of the kit")
                continue
            own = python_names(made) if not isinstance(made, str) else set()
            for keyword in keywords:
                if keyword not in own and not is_param(type_name, camel_case(keyword)):
                    unknown.append(f"{place}: {type_name}({keyword}=)")
    assert unknown == [], "names the kit does not have:\n" + "\n".join(unknown)


def test_the_check_finds_an_old_name():
    """WHY: a check that finds nothing must be able to find something."""
    assert not is_param("Slider", "currentValue") and is_param("Slider", "value")
    assert not is_param("SearchInput", "onSearch") and is_param("SearchInput", "onEnter")
    assert not has_method("SearchInput", "setPlaceholderText") and has_method("SearchInput", "setPlaceholder")
    assert is_param("EmailField", "maxLength")  # a param of TextField, the component it is made from
    assert calls_in("Slider(min=0, value=3)", "x") == [("x:1", ozdenui.Slider, ["min", "value"])]


# *** A PARAM CHANGED AFTER THE START GOES TO THE METHOD OF THE KIT FOR IT

def test_the_methods_that_change_a_param_are_read_from_the_kit():
    assert component_setters("TextField")["unitText"] == ("setUnitText", False)
    assert component_setters("EmailField")["unitText"] == ("setUnitText", False)  # of TextField, the one it is made from
    assert component_setters("Splitter")["firstSize"] == ("setFirstSize", True)  # (size, silent)
    assert "onChange" not in component_setters("TextField") and "width" not in component_setters("TextField")
    assert component_setters("NoSuchComponent") == {}


@pytest.mark.parametrize("cls", python_classes(), ids=lambda cls: cls.__name__)
def test_a_class_changes_a_param_with_its_own_method_or_the_one_of_the_kit(app, cls):
    """WHY: a setter of a class for a param the kit has a method for must call a method of the kit (not send a value)."""
    need_component(cls)
    obj = make(cls)
    plain = []
    for param, (method, _silent) in component_setters(cls._type).items():
        name = snake_case(param)
        if camel_case(name) != param or name in cls._setters:
            continue  # not reachable from Python, or the class has its own way
        before = len(commands(app, "set"))
        obj.set(**{name: None})
        if len(commands(app, "set")) != before or commands(app, "call")[-1]["method"] != method:
            plain.append(name)
    assert plain == [], f"{cls.__name__}: sent as a value, though {cls._type} has a method: {plain}"


# *** THE KEYS OF AN ITEM OF A LIST (an item of an ItemList, a node of a TreeView, a step, a section, a tab...)

# The params that take a list of items, and the keys of an item that hold more items of the same kind
ITEM_LISTS = {
    "ItemList": {"params": ("items",), "nested": ()},
    "TreeView": {"params": ("items",), "nested": ("children",)},
    "StepBar": {"params": ("steps",), "nested": ()},
    "Accordion": {"params": ("sections",), "nested": ()},
    "Tabs": {"params": ("tabs",), "nested": ()},
    "StatusBar": {"params": ("items",), "nested": ()},
    "ToolBar": {"params": ("items",), "nested": ("items",)},
    "SortableList": {"params": ("items",), "nested": ()},
}
# The methods that take items: the component (None: the one the object was made from) and the place of the argument
ITEM_METHODS = {
    "add_item": ("ItemList", 0), "set_items": (None, 0), "set_children": ("TreeView", 1), "add_node": ("TreeView", 1),
    "add_section": ("Accordion", 0), "set_sections": ("Accordion", 0), "set_steps": ("StepBar", 0),
}
# The keys an item takes as keywords: tree.update_node("a.py", description="4 KB")
KEYWORD_ITEM_METHODS = {"update_node": "TreeView"}
class _ItemFinder:
    """The keys of the items in a code: [(place, the component, the key)]. It follows what a program does most: a list
    in the call, a name of the module (FOLDERS = [...]), a function of the module that returns the items or appends them
    (nodes.append({...})), a list comprehension, the methods of a list (lst.add_item({...}))."""

    def __init__(self, code, where):
        self.tree = ast.parse(code)
        self.where = where
        self.constants = {}
        self.functions = {}
        for node in self.tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                self.constants[node.targets[0].id] = node.value
            elif isinstance(node, ast.FunctionDef):
                self.functions[node.name] = node
        self.receivers = self._made_objects()
        self.found = []

    def _made_objects(self):
        """The code of a target -> the class it was made from: view["list"] = ItemList(...) -> {'view["list"]': "ItemList"};
        also a second name of it: tree = TreeView(...), then view["tree"] = tree."""
        made = {}
        assignments = [node for node in ast.walk(self.tree) if isinstance(node, ast.Assign)]
        for node in assignments:
            is_making = isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)
            if is_making and node.value.func.id in ITEM_LISTS:
                made.update({ast.unparse(target): node.value.func.id for target in node.targets})
        for node in assignments:
            type_name = made.get(ast.unparse(node.value))
            if type_name:
                made.update({ast.unparse(target): type_name for target in node.targets})
        return made

    def dicts_in(self, node, depth=0):
        if node is None or depth > 6:
            return
        if isinstance(node, ast.Dict):
            yield node
        elif isinstance(node, (ast.List, ast.Tuple)):
            for element in node.elts:
                yield from self.dicts_in(element, depth + 1)
        elif isinstance(node, (ast.ListComp, ast.GeneratorExp)):
            yield from self.dicts_in(node.elt, depth + 1)
        elif isinstance(node, ast.BinOp):
            yield from self.dicts_in(node.left, depth + 1)
            yield from self.dicts_in(node.right, depth + 1)
        elif isinstance(node, ast.IfExp):
            yield from self.dicts_in(node.body, depth + 1)
            yield from self.dicts_in(node.orelse, depth + 1)
        elif isinstance(node, ast.Name) and node.id in self.constants:
            yield from self.dicts_in(self.constants[node.id], depth + 1)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in self.functions:
            yield from self.dicts_made_by(self.functions[node.func.id], depth + 1)

    def dicts_made_by(self, function, depth):
        """The dicts a function returns, or appends to a list (nodes.append({...}))."""
        for node in ast.walk(function):
            if isinstance(node, ast.Return):
                yield from self.dicts_in(node.value, depth)
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "append" and node.args:
                yield from self.dicts_in(node.args[0], depth)

    def add_items(self, type_name, node):
        for item in self.dicts_in(node):
            for key, value in zip(item.keys, item.values):
                if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
                    continue  # (a **dict: its keys are not seen here)
                self.found.append((f"{self.where}:{key.lineno}", type_name, key.value))
                if key.value in ITEM_LISTS[type_name]["nested"]:
                    self.add_items(type_name, value)

    def find(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                self._look_at_call(node)
        return self.found

    def _look_at_call(self, node):
        func = node.func
        if isinstance(func, ast.Name):
            type_name = func.id
            if func.id == "Component" and node.args and isinstance(node.args[0], ast.Constant):
                type_name = node.args[0].value
            for keyword in node.keywords:
                if type_name in ITEM_LISTS and keyword.arg in ITEM_LISTS[type_name]["params"]:
                    self.add_items(type_name, keyword.value)
        elif isinstance(func, ast.Attribute) and func.attr in ITEM_METHODS:
            type_name, place = ITEM_METHODS[func.attr]
            type_name = type_name or self.receivers.get(ast.unparse(func.value))
            if type_name and len(node.args) > place:
                self.add_items(type_name, node.args[place])
        elif isinstance(func, ast.Attribute) and func.attr in KEYWORD_ITEM_METHODS:
            type_name = KEYWORD_ITEM_METHODS[func.attr]
            self.found += [(f"{self.where}:{node.lineno}", type_name, keyword.arg) for keyword in node.keywords if keyword.arg]


def item_keys_in(code, where):
    return _ItemFinder(code, where).find()


@pytest.mark.parametrize("type_name", sorted(ITEM_LISTS))
def test_the_kit_writes_the_keys_of_its_items(type_name):
    """WHY: item_keys_of() reads the header of the component; a header written in another way would make every key wrong."""
    assert {"key", "text"} <= item_keys_of(type_name), sorted(item_keys_of(type_name))


def test_the_items_of_the_examples_and_the_handbook_have_keys_of_the_kit():
    found = [entry for where, code in codes_of_the_package() for entry in item_keys_in(code, where)]
    assert len(found) > 50, f"only {len(found)} keys of items were found: the finder lost them"
    unknown = sorted({f"{place}: {type_name} item {key!r}" for place, type_name, key in found
                      if camel_case(key) not in item_keys_of(type_name)})
    assert unknown == [], "keys of items the kit does not have:\n" + "\n".join(unknown)


def test_the_item_check_finds_an_old_key():
    """WHY: a check that finds nothing must be able to find something."""
    code = '''
FOLDERS = [{"key": "p", "title": "Projects"}]

def nodes_of(folder):
    nodes = []
    nodes.append({"key": folder, "text": folder, "note": "4 KB", "children": [{"key": "a", "disabled": True}]})
    return nodes

def start(page):
    view["list"] = ItemList(items=FOLDERS)
    tree = TreeView(items=nodes_of("src"))
    view["tree"] = tree
    view["list"].set_items([{"key": "b", "desc": "Green"}])
    view["tree"].set_items([{"key": "c", "title": "C"}] if page else [])
    Accordion(sections=[{"key": "s", "text": "S", "enabled": False}])
    tree.update_node("a", note="5 KB")
'''
    found = item_keys_in(code, "x")
    wrong = sorted((type_name, key) for _place, type_name, key in found if camel_case(key) not in item_keys_of(type_name))
    assert wrong == [("ItemList", "desc"), ("ItemList", "title"), ("TreeView", "disabled"), ("TreeView", "note"), ("TreeView", "note"),
                     ("TreeView", "title")]
    assert ("Accordion", "enabled") in [(type_name, key) for _place, type_name, key in found]


def item_classes():
    """The classes that name the keys of their items (_item_keys): the warning about an item with no text uses them."""
    return [cls for cls in python_classes() if "_item_keys" in vars(cls)]


def test_the_lists_of_this_check_are_the_lists_of_python():
    assert sorted(cls._type for cls in item_classes()) == sorted(ITEM_LISTS)


@pytest.mark.parametrize("cls", item_classes(), ids=lambda cls: cls.__name__)
def test_python_knows_the_keys_of_the_items_of_the_kit(cls):
    """WHY: components._check_items() tells about an item with no text from these keys; a key the kit renamed would make
    a right item wrong (or a wrong one right)."""
    assert set(cls._item_keys) == item_keys_of(cls._type), sorted(item_keys_of(cls._type))
    assert tuple(getattr(cls, "_nested_item_keys", ())) == ITEM_LISTS[cls._type]["nested"]
