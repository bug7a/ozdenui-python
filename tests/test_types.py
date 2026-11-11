# Bismillah
"""test_types.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
mypy reads the examples and the whole programs of the two handbooks with the stubs of the package (ozdenui/__init__.pyi)
and finds no mistake about the package in them: a name a class or a function does not take, or a value of a wrong kind
for a function (every("soon", tick)). That is what an editor would mark. A small program with three such mistakes
proves that mypy reads the stubs. (The params of a class take any kind: make_stubs.py says why.)
WHY only the errors about the package: the programs keep their objects in a dict (view = {}), and mypy wants one kind
for the values of a dict; that is not a mistake of a program.
Skipped without mypy: .venv/bin/python -m pip install mypy

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import re
import tempfile
from pathlib import Path

import pytest

import ozdenui
from test_handbook import whole_programs

mypy_api = pytest.importorskip("mypy.api")

SOURCE_FOLDER = Path(__file__).resolve().parent.parent
CACHE_FOLDER = Path(tempfile.gettempdir()) / "ozdenui-mypy-cache"  # WHY kept: the next run takes seconds, not a minute
PACKAGE_ERROR_CODES = ("call-arg", "arg-type", "call-overload")
BAD_PROGRAM_NAME = "a_program_with_three_mistakes.py"
BAD_PROGRAM = '''from ozdenui import Label, SmartButton, every


def start(page):
    Label(txet="Hi")
    SmartButton(lable_text="Go")
    every("soon", start)
'''


def errors_about_the_package(files, monkeypatch):
    """The errors of mypy about the package: a name or a value given to a class or a function of ozdenui, and any
    error in the stubs themselves."""
    monkeypatch.setenv("MYPYPATH", str(SOURCE_FOLDER))  # WHY: the package of this folder, not an installed copy
    report, problems, _ = mypy_api.run([
        *files,
        "--check-untyped-defs",  # WHY: the code of start() has no annotations; without it mypy does not read it
        "--allow-untyped-globals",
        "--ignore-missing-imports",
        "--no-error-summary",
        "--cache-dir", str(CACHE_FOLDER),
    ])
    assert not problems, problems  # mypy itself could not run (a broken stub, a wrong option)
    names = set(ozdenui.__all__)
    found = []
    for line in report.splitlines():
        if ": error:" not in line:
            continue
        codes = re.findall(r"\[([a-z-]+)\]\s*$", line)
        is_in_the_stubs = "__init__.pyi" in line
        is_about_the_package = bool(codes) and codes[0] in PACKAGE_ERROR_CODES and bool(set(re.findall(r'"(\w+)"', line)) & names)
        if is_in_the_stubs or is_about_the_package:
            found.append(line)
    return found


def test_the_programs_make_no_mistake_about_the_package(tmp_path, monkeypatch):
    files = sorted(str(path) for path in (SOURCE_FOLDER / "examples").glob("*.py"))
    for program in whole_programs():
        path = tmp_path / ("handbook_" + re.sub(r"\W", "_", program.id) + ".py")
        path.write_text(program.values[0], encoding="utf-8")
        files.append(str(path))
    bad_program = tmp_path / BAD_PROGRAM_NAME
    bad_program.write_text(BAD_PROGRAM, encoding="utf-8")

    errors = errors_about_the_package(files + [str(bad_program)], monkeypatch)
    in_the_bad_program = [line for line in errors if BAD_PROGRAM_NAME in line]
    in_the_programs = [line for line in errors if BAD_PROGRAM_NAME not in line]
    assert len(files) > 50  # WHY: the programs were found (a wrong folder would pass with none)
    assert len(in_the_bad_program) == 3, in_the_bad_program  # txet, lable_text, every("soon")
    assert in_the_programs == []
