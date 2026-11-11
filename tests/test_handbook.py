# Bismillah
"""test_handbook.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Every whole program of the handbook (handbook/*.md and handbook/turkce/*.md: a Python block that imports ozdenui and
ends with App(...).run()) makes its window without an error: its start() runs against the fake window of the tests. So
the handbook stays true when the package changes. checks/check_handbook.py opens the same programs in real windows.
Usage: .venv/bin/python -m pytest tests/test_handbook.py

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import re
import threading
from pathlib import Path

import pytest

from ozdenui import App
from ozdenui import app as app_module
from test_ozdenui import FakeWindow

HANDBOOK_FOLDER = Path(__file__).resolve().parent.parent / "handbook"
CODE_BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)


def chapters():
    """[(its name, its file)]: "03-layout", "turkce/03-layout"."""
    return [(chapter.relative_to(HANDBOOK_FOLDER).with_suffix("").as_posix(), chapter) for chapter in sorted(HANDBOOK_FOLDER.rglob("*.md"))]


def whole_programs():
    """(the name of the program, its code): the blocks that open a window."""
    programs = []
    for name, chapter in chapters():
        for number, code in enumerate(CODE_BLOCK.findall(chapter.read_text(encoding="utf-8")), start=1):
            if "from ozdenui import" in code and "App(" in code and ".run()" in code:
                programs.append(pytest.param(code, id=f"{name}-{number}"))
    return programs


def run_start_only(application):
    """App.run() of the tests: start() runs as in a window, nothing waits for a person."""
    application._window = FakeWindow()
    application._app_thread_id = threading.get_ident()
    app_module._current = application
    application._make_page()
    application._add_accent_packages()
    application._start(application.page)
    application.flush()


def test_the_handbook_has_programs_in_both_languages():
    names = [param.id for param in whole_programs()]
    assert len([name for name in names if not name.startswith("turkce/")]) >= 10
    assert len([name for name in names if name.startswith("turkce/")]) >= 10


def test_every_python_block_of_the_handbook_is_python():
    for name, chapter in chapters():
        for number, code in enumerate(CODE_BLOCK.findall(chapter.read_text(encoding="utf-8")), start=1):
            compile(code, f"{name}.md, block {number}", "exec")


@pytest.mark.parametrize("code", whole_programs())
def test_a_program_of_the_handbook_makes_its_window(code, monkeypatch):
    monkeypatch.setattr(App, "run", run_start_only)
    try:
        exec(compile(code, "handbook", "exec"), {"__name__": "__main__"})
    finally:
        app_module._current = None
