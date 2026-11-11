# Bismillah
"""test_stubs.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The stubs of the package (ozdenui/__init__.pyi) are current, compile, name everything the package gives, and take every
name the examples, the handbook and the README give an object.
WHY: an editor reads only the stubs; a name missing there is marked in a right program.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import ast
import re
import sys
from pathlib import Path

import ozdenui

SOURCE_FOLDER = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOURCE_FOLDER))
import make_stubs  # noqa: E402  (WHY here: it is a tool of the source folder, not of the package)

STUB_TEXT = make_stubs.STUB_FILE.read_text(encoding="utf-8")


def test_the_stubs_are_current():
    assert STUB_TEXT == make_stubs.stub_text(), "the stubs are old: .venv/bin/python make_stubs.py"


def test_the_stubs_compile():
    compile(STUB_TEXT, "__init__.pyi", "exec")  # WHY compile and not only parse: it finds a name given twice in a def


def test_every_name_of_the_package_is_in_the_stubs():
    tree = ast.parse(STUB_TEXT)
    defined = {node.name for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef))}
    assert sorted(set(ozdenui.__all__) - defined) == []


def test_a_class_of_the_package_takes_only_its_names():
    params = init_params_of_the_stubs()
    takes_any = sorted(name for name, (_, any_name) in params.items() if any_name)
    assert takes_any == ["Component"]  # WHY: Component("AnyName") is the one whose params are not known
    names, _ = params["Label"]
    assert {"text", "html", "plain_text", "font_size", "fill", "on_click"} <= names and "txet" not in names
    assert {"label_text", "text", "tone", "on_click", "style_name", "width"} <= params["SmartButton"][0]


def init_params_of_the_stubs():
    """{class: (its keyword names, takes any name)} of the __init__ of the stubs."""
    found = {}
    for node in ast.parse(STUB_TEXT).body:
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                names = {arg.arg for arg in item.args.args + item.args.kwonlyargs}
                found[node.name] = (names, item.args.kwarg is not None)
    return found


def code_of_the_programs():
    """(where, the code) of every example and every Python block of the handbook and the README."""
    for path in sorted((SOURCE_FOLDER / "examples").glob("*.py")):
        yield path.name, path.read_text(encoding="utf-8")
    pages = sorted((SOURCE_FOLDER / "handbook").rglob("*.md")) + [SOURCE_FOLDER / "README.md"]
    for page in pages:
        blocks = re.findall(r"```python\n(.*?)```", page.read_text(encoding="utf-8"), re.S)
        for number, block in enumerate(blocks, 1):
            yield f"{page.relative_to(SOURCE_FOLDER)} (block {number})", block


def called_class(node):
    """The name of the class a call makes: Label(...) or ozdenui.Label(...)."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "ozdenui":
        return node.func.attr
    return None


def test_every_name_the_programs_give_an_object_is_in_the_stubs():
    params = init_params_of_the_stubs()
    missing = []
    read = 0
    for where, code in code_of_the_programs():
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue  # a part of a program
        read += 1
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or called_class(node) not in params:
                continue
            names, takes_any = params[called_class(node)]
            for given in node.keywords:
                if given.arg and not takes_any and given.arg not in names:
                    missing.append(f"{where}:{node.lineno}: {called_class(node)}({given.arg}=...)")
    assert read > 60  # WHY: the programs were read (a wrong folder would pass with none)
    assert missing == []
