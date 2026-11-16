# Bismillah
"""test_agents.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The rules for an AI assistant (ozdenui/AGENTS.md) stay true, and python -m ozdenui agents writes them into a project
without touching the lines of the user: the program in the rules makes its window, every class of the package is named
in them, and the names they give in code marks are names of the package.
Usage: .venv/bin/python -m pytest tests/test_agents.py

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import inspect
import re

import ozdenui
from ozdenui import App
from ozdenui import __main__ as command
from ozdenui import app as app_module
from test_handbook import CODE_BLOCK, run_start_only

RULES = command.RULES_FILE.read_text(encoding="utf-8")
# Left out of the rules: the error of a closed window, and a helper of the pictures
NOT_NAMED = ("WindowClosed", "picture_address")
PYTHON_WORDS = ("None", "True", "False")


def test_the_program_of_the_rules_makes_its_window_and_adds_a_note(monkeypatch):
    programs = [code for code in CODE_BLOCK.findall(RULES) if "App(" in code and ".run()" in code]
    assert len(programs) == 1
    monkeypatch.setattr(App, "run", run_start_only)
    scope = {"__name__": "__main__"}
    try:
        exec(compile(programs[0], "AGENTS.md", "exec"), scope)
        scope["view"]["name"].text = "Milk"
        scope["add_note"]()
        assert scope["notes"] == ["Milk"]
        assert scope["view"]["count"].text == "Notes: 1"
        assert scope["view"]["name"].text == ""
    finally:
        app_module._current = None


def test_every_public_name_of_the_package_is_in_the_rules():
    missing = [name for name in ozdenui.__all__ if name not in NOT_NAMED and not re.search(rf"\b{name}\b", RULES)]
    assert missing == []


def test_a_class_named_in_the_rules_is_a_class_of_the_package():
    named = set(re.findall(r"`([A-Z][A-Za-z]+)(?:\(|`)", RULES))
    unknown = sorted(name for name in named if name not in PYTHON_WORDS and not hasattr(ozdenui, name))
    assert unknown == []


def test_the_params_of_the_app_in_the_rules_are_its_params():
    line = re.search(r"`App\(start, title=.*?\)`", RULES, re.DOTALL).group(0)
    known = inspect.signature(App.__init__).parameters
    assert [name for name in re.findall(r"(\w+)=", line) if name not in known] == []


def test_the_command_makes_the_file(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert command.main(["agents"]) == 0
    text = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert text.startswith(command.START_MARK) and text.endswith(command.END_MARK + "\n")
    assert "## Layout" in text
    assert "made" in capsys.readouterr().out


def test_the_command_keeps_the_lines_of_the_user_and_writes_the_rules_once(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "CLAUDE.md"
    target.write_text("# My project\n\nAnswer in Turkish.\n", encoding="utf-8")
    assert command.main(["agents", "CLAUDE.md"]) == 0
    first = target.read_text(encoding="utf-8")
    assert first.startswith("# My project\n\nAnswer in Turkish.\n\n" + command.START_MARK)
    assert "added" in capsys.readouterr().out
    command.main(["agents", "CLAUDE.md"])
    assert target.read_text(encoding="utf-8") == first
    assert "already" in capsys.readouterr().out


def test_the_command_changes_only_its_own_part(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "AGENTS.md"
    target.write_text(f"# Mine\n\n{command.START_MARK}\nold rules\n{command.END_MARK}\n\n## After\nMine too.\n", encoding="utf-8")
    command.main(["agents"])
    text = target.read_text(encoding="utf-8")
    assert "old rules" not in text and text.count(command.START_MARK) == 1
    assert text.startswith("# Mine\n\n") and text.endswith(command.END_MARK + "\n## After\nMine too.\n")
    assert "updated" in capsys.readouterr().out


def test_print_writes_no_file_and_a_wrong_word_shows_the_usage(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert command.main(["agents", "--print"]) == 0
    assert "## Layout" in capsys.readouterr().out
    assert command.main(["agent"]) == 2
    assert "python -m ozdenui agents" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_the_package_points_an_assistant_to_the_rules():
    # WHY: an assistant that was not given the rules opens the package to learn it; its first lines send it to them
    stubs = (command.RULES_FILE.parent / "__init__.pyi").read_text(encoding="utf-8")
    assert "read AGENTS.md next to this file" in ozdenui.__doc__
    assert "read AGENTS.md next to this file" in stubs[:800]


def test_look_asks_for_a_program_file_that_is_there(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert command.main(["look", "no_such.py"]) == 2
    assert "no such program file" in capsys.readouterr().out


def test_look_runs_the_program_in_the_asked_theme_and_tells_a_program_without_a_window(tmp_path, monkeypatch, capsys):
    from ozdenui import _look

    # A program with no window: look() says so, and the theme of the look reaches an App made meanwhile
    program = tmp_path / "plain.py"
    program.write_text("import sys\nfrom ozdenui import App\nsys.modules['__look_test__'] = App(lambda page: None)\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert command.main(["look", "plain.py", "--theme", "dark"]) == 1
    assert "opened no window" in capsys.readouterr().out
    import sys
    assert sys.modules.pop("__look_test__").theme == "dark"
    assert app_module._look is None
    assert _look.DEFAULT_WAIT_SECONDS > 0
    assert not (tmp_path / "plain.png").exists()


def test_the_window_tells_the_look_when_it_is_shown(monkeypatch):
    shown = []
    monkeypatch.setattr(app_module, "_look", {"theme": "", "on_shown": shown.append})
    monkeypatch.setattr(App, "run", run_start_only)
    application = App(lambda page: None)
    try:
        application.run()
        application._show_window()
        application._show_window()
        assert shown == [application]
    finally:
        app_module._current = None
