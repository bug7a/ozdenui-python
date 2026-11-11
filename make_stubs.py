# Bismillah
"""make_stubs.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Writes ozdenui/__init__.pyi, the stubs of the package: every class with the names it takes, so an editor (VS Code,
PyCharm) offers them and marks a name an object does not have. The names are the ones the warning of objects.py knows:
the params of a component (the keys of its Defaults in the kit copy, web/), the props of basic.js, the names of Python.
Usage: .venv/bin/python make_stubs.py (update-web.sh runs it after a new copy of the kit). tests/test_stubs.py fails
while the file is not current.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import inspect
import keyword
from pathlib import Path

import ozdenui
from ozdenui import _kit
from ozdenui.objects import BasicObject, Component, Page
from ozdenui.values import camel_case, snake_case

STUB_FILE = Path(__file__).resolve().parent / "ozdenui" / "__init__.pyi"
HEADER = '''# Bismillah
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
'''
INDENT = "    "
# WHY not *position: a prop of basic.js is named position (the CSS one), and a name can not be there twice
PLACE = "*left_top_width_height: float | str"
LENGTH = "float | str"
FUNCTION = "Callable[..., Any]"
NOT_FOR_PYTHON = ("containerBox", "mainBox", "parentBox", "inputElement")  # the boxes and elements of basic.js itself
# The events of the page an object of basic.js takes as on_x=fn (any other works too: Python reads on_ as an event)
DOM_EVENTS = ("on_click", "on_dblclick", "on_mouse_enter", "on_mouse_leave", "on_mouse_down", "on_mouse_up", "on_mouse_move",
              "on_key_down", "on_key_up", "on_input", "on_change", "on_focus", "on_blur", "on_wheel", "on_context_menu")
ALLOWED_DUNDERS = ("__enter__", "__exit__", "__getattr__", "__setattr__")
# The kinds of the functions of the package: {name: ({param: its kind}, the kind it returns)}
FUNCTION_TYPES = {
    "every": ({"milliseconds": "float", "task": FUNCTION}, "Callable[[], None]"),
    "after": ({"milliseconds": "float", "task": FUNCTION}, "Callable[[], None]"),
    "call_soon": ({"task": FUNCTION}, "None"),
    "run_in_background": ({"job": FUNCTION, "args": "Any"}, "Any"),
    "open_file": ({}, "Any"),  # WHY Any: a path, a list of paths (multiple=True) or None
    "save_file": ({}, "str | None"),
    "choose_folder": ({}, "str | None"),
    "picture_address": ({"picture": "Any"}, "str"),
}
EXPORTED = set(ozdenui.__all__)


def stub_name(cls):
    """The name of a class in the stubs: a class the package does not give is private there (_TypedComponent)."""
    if cls.__name__ in EXPORTED or cls.__module__ == "builtins":
        return cls.__name__
    return "_" + cls.__name__.lstrip("_")


def docstring_lines(doc, indent):
    """The own docstring of a class or a function (not one of its base), for the hover of an editor."""
    if not doc or '"""' in doc:
        return []
    doc = inspect.cleandoc(doc)
    prefix = "r" if "\\" in doc else ""
    lines = doc.splitlines()
    if len(lines) == 1:
        return [f'{indent}{prefix}"""{lines[0]}"""']
    return [f'{indent}{prefix}"""{lines[0]}'] + [(indent + line if line else "") for line in lines[1:]] + [f'{indent}"""']


def signature_text(function, annotations=None):
    """The params of a function for the stubs: every default is ..."""
    annotations = annotations or {}
    parts = []
    has_star = False
    params = list(inspect.signature(function).parameters.values())
    for index, param in enumerate(params):
        text = param.name
        if param.kind == param.VAR_POSITIONAL:
            text, has_star = "*" + param.name, True
        elif param.kind == param.VAR_KEYWORD:
            text = "**" + param.name
        elif param.kind == param.KEYWORD_ONLY and not has_star:
            parts.append("*")
            has_star = True
        if param.name in annotations:
            text += ": " + annotations[param.name]
        if param.default is not param.empty:
            text += " = ..." if param.name in annotations else "=..."
        parts.append(text)
        is_last_positional_only = (param.kind == param.POSITIONAL_ONLY and
                                   (index + 1 == len(params) or params[index + 1].kind != param.POSITIONAL_ONLY))
        if is_last_positional_only:
            parts.append("/")
    return ", ".join(parts)


# *** THE NAMES AN OBJECT TAKES

def page_names(cls):
    """The names the page knows for this class, camelCase, in the order of the stubs (the own ones of a component first,
    in the order of the kit). None: not known (Component("AnyName")). The same list as the warning of objects.py."""
    known = _kit.known_names(cls._type)
    if known is None:
        return None
    if cls._type in _kit.component_files():
        own = list(_kit.component_defaults(cls._type))
    else:
        own = ["left", "top", "width", "height"] + (list(_kit.GROUP_PARAMS) if cls._type in _kit.GROUP_TYPES else [])
    rest = sorted(known - set(own))
    return [name for name in own + rest if name not in NOT_FOR_PYTHON]


def python_params(cls):
    """The params the Python classes name themselves (SearchInput(text=""), Icon(picture=...)), from the class up."""
    found = {}
    for klass in cls.__mro__:
        if klass is BasicObject:
            break
        if "__init__" not in klass.__dict__:
            continue
        for param in inspect.signature(klass.__init__).parameters.values():
            is_keyword = param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
            if is_keyword and param.name not in ("self", "type_name"):
                found.setdefault(param.name, None)
    for name in getattr(cls, "_aliases", {}):
        found.setdefault(name, None)
    return list(found)


def type_of(page_name, cls):
    """WHY Any: a look kept in a dict and given with ** (CARD_LOOK = dict(width=220, align="left top")) holds values of
    more than one kind, and a type checker marked that right program (also a callback given as None). The names are
    the point: a name a class does not take is still marked."""
    return "Any"


def init_params(cls):
    """[(the Python name, its type)] of the __init__ of a class; None: it takes any name (**params)."""
    names = page_names(cls)
    if names is None:
        return None
    params = {}
    for name in python_params(cls):
        params[name] = type_of(camel_case(name), cls)
    for page_name in names:
        name = snake_case(page_name)
        # WHY the way back: Python sends camel_case(name); a name that does not come back to the same one is not reachable
        if keyword.iskeyword(name) or not name.isidentifier() or camel_case(name) != page_name:
            continue
        params.setdefault(name, type_of(page_name, cls))
    if not issubclass(cls, Component):
        for name in DOM_EVENTS:
            params.setdefault(name, type_of(name, cls))
    params.setdefault("fill", "Any")  # WHY: Python's own, every object takes it (the room a group leaves)
    if issubclass(cls, Component):
        params.setdefault("framed", "Any")  # WHY: Python's own too: framed=False takes the frame of a component
    return list(params.items())


# *** THE CLASSES

def init_lines(cls):
    if cls is Component:
        return [f"{INDENT}def __init__(self, type_name: str, {PLACE}, **params: Any) -> None: ..."]
    params = init_params(cls)
    if params is None:
        return [f"{INDENT}def __init__(self, {PLACE}, **params: Any) -> None: ..."]
    lines = [f"{INDENT}def __init__(", f"{INDENT * 2}self,", f"{INDENT * 2}{PLACE},"]
    lines += [f"{INDENT * 2}{name}: {annotation} = ...," for name, annotation in params]
    lines.append(f"{INDENT}) -> None: ...")
    return lines


def member_lines(cls):
    """The public methods, properties and values the class itself defines (its bases have theirs)."""
    lines = []
    for name, member in cls.__dict__.items():
        if name == "__init__" or (name.startswith("_") and name not in ALLOWED_DUNDERS):
            continue
        if isinstance(member, staticmethod):
            lines += [f"{INDENT}@staticmethod", f"{INDENT}def {name}({signature_text(member.__func__)}) -> Any: ..."]
        elif isinstance(member, classmethod):
            lines += [f"{INDENT}@classmethod", f"{INDENT}def {name}({signature_text(member.__func__)}) -> Any: ..."]
        elif isinstance(member, property):
            returned = "App" if (cls is Page and name == "app") else "Any"
            lines += [f"{INDENT}@property", f"{INDENT}def {name}(self) -> {returned}: ..."]
            if member.fset:
                lines += [f"{INDENT}@{name}.setter", f"{INDENT}def {name}(self, value: Any) -> None: ..."]
        elif inspect.isfunction(member):
            lines += special_method_lines(name) or [f"{INDENT}def {name}({signature_text(member)}) -> Any: ..."]
        elif not callable(member):
            lines.append(f"{INDENT}{name}: Any")
    return lines


def special_method_lines(name):
    """WHY: "with VGroup() as group:" gives the group its class; any value is read and set (label.text)."""
    return {
        "__enter__": [f"{INDENT}def __enter__(self: _T) -> _T: ..."],
        "__exit__": [f"{INDENT}def __exit__(self, *error: Any) -> bool: ..."],
        "__getattr__": [f"{INDENT}def __getattr__(self, name: str) -> Any: ..."],
        "__setattr__": [f"{INDENT}def __setattr__(self, name: str, value: Any) -> None: ..."],
    }.get(name)


def value_lines(cls):
    """The values Python keeps and the page sends back (checkbox.checked), and the params the component changes with a
    method of its own when they are set (field.unit_text = "kg"): offered after a dot."""
    names = list(getattr(cls, "_setters", {})) + [snake_case(name) for name in getattr(cls, "_state", {})]
    if issubclass(cls, Component):
        # WHY the way back: Python sends camel_case(name); a name that does not come back to the same one is not reachable
        names += [snake_case(param) for param in _kit.component_setters(cls._type) if camel_case(snake_case(param)) == param]
    defined = set(cls.__dict__)
    lines = []
    for name in dict.fromkeys(names):
        if name.isidentifier() and not keyword.iskeyword(name) and name not in defined:
            lines.append(f"{INDENT}{name}: Any")
    return lines


def app_lines():
    """App: its values are made in __init__, so they are read from an App that is not run."""
    app = ozdenui.App(lambda page: None)
    values = [name for name in vars(app) if not name.startswith("_")]
    lines = [f"{INDENT}{name}: Any" for name in values]
    annotations = {"start": f"Callable[[{stub_name(Page)}], Any]"}
    lines.append(f"{INDENT}def __init__({signature_text(ozdenui.App.__init__, annotations)}) -> None: ...")
    return lines


def class_lines(cls):
    bases = [stub_name(base) for base in cls.__bases__ if base is not object]
    head = f"class {stub_name(cls)}({', '.join(bases)}):" if bases else f"class {stub_name(cls)}:"
    body = docstring_lines(cls.__dict__.get("__doc__"), INDENT)
    if cls is ozdenui.App:
        body += app_lines()
    elif issubclass(cls, BasicObject) and cls.__name__ in EXPORTED:
        body += init_lines(cls)  # WHY only the classes of the package: each one takes names of its own
    body += value_lines(cls) if issubclass(cls, BasicObject) else []
    body += member_lines(cls)
    if not body:
        body = [f"{INDENT}..."]
    return [head] + body


def classes_in_order():
    """Every class the stubs need, a base before its classes: the exported ones and their bases (and the Page)."""
    ordered = []

    def add(cls):
        if cls in ordered or cls is object or cls.__module__ == "builtins":
            return
        for base in cls.__bases__:
            add(base)
        ordered.append(cls)

    add(Page)
    for name in ozdenui.__all__:
        value = getattr(ozdenui, name)
        if inspect.isclass(value):
            add(value)
    return ordered


def function_lines(name):
    function = getattr(ozdenui, name)
    annotations, returned = FUNCTION_TYPES.get(name, ({}, "Any"))
    lines = [f"def {name}({signature_text(function, annotations)}) -> {returned}:"]
    doc = docstring_lines(function.__doc__, INDENT)
    return lines + (doc + [f"{INDENT}..."] if doc else [f"{INDENT}..."])


def stub_text():
    parts = [HEADER, "__version__: str", "__all__ = [" + ", ".join(f'"{name}"' for name in ozdenui.__all__) + "]", ""]
    for cls in classes_in_order():
        parts += ["", *class_lines(cls), ""]
    for name in ozdenui.__all__:
        if inspect.isfunction(getattr(ozdenui, name)):
            parts += ["", *function_lines(name), ""]
    text = "\n".join(parts)
    while "\n\n\n\n" in text:
        text = text.replace("\n\n\n\n", "\n\n\n")
    return text.rstrip("\n") + "\n"


def main():
    text = stub_text()
    STUB_FILE.write_text(text, encoding="utf-8")
    print(f"{STUB_FILE.relative_to(STUB_FILE.parent.parent)}: {text.count(chr(10))} lines")


if __name__ == "__main__":
    main()
