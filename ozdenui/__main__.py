# Bismillah
"""__main__.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The commands of the package. python -m ozdenui agents writes the rules of OzdenUI for an AI assistant (AGENTS.md of
the package) into the folder of a project, where the assistants read them by themselves. python -m ozdenui look takes
a picture of the window of a program (_look.py).
Usage:
    python -m ozdenui agents              Writes them into AGENTS.md of this folder (most assistants read it).
    python -m ozdenui agents CLAUDE.md    Into another file (Claude Code reads CLAUDE.md).
    python -m ozdenui agents --print      Only prints them.
    python -m ozdenui look app.py         Runs app.py, saves its window as app.png and closes it.
    python -m ozdenui look app.py dark.png --theme dark --wait 3
A file that is there keeps its own lines: the rules go between two marks at its end, and the next run changes only them.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import argparse
import sys
from pathlib import Path

from . import __version__

RULES_FILE = Path(__file__).resolve().parent / "AGENTS.md"
DEFAULT_TARGET = "AGENTS.md"
START_MARK = "<!-- ozdenui: start (written by python -m ozdenui agents; the next run writes this part again) -->"
END_MARK = "<!-- ozdenui: end -->"
USAGE = f"""ozdenui {__version__}

python -m ozdenui agents              The rules of OzdenUI for an AI assistant, into AGENTS.md of this folder.
python -m ozdenui agents CLAUDE.md    Into another file.
python -m ozdenui agents --print      Only prints them.

python -m ozdenui look app.py         Runs app.py, saves a picture of its window as app.png and closes it.
python -m ozdenui look app.py dark.png --theme dark --wait 3
                                      The picture file, the theme of the window, the seconds before the picture (1.5)."""


def rules_text():
    return RULES_FILE.read_text(encoding="utf-8").strip()


def with_rules(old_text, rules):
    """The text of the file with the rules between the marks: in the place of the old ones, or at its end."""
    block = f"{START_MARK}\n{rules}\n{END_MARK}\n"
    start = old_text.find(START_MARK)
    end = old_text.find(END_MARK)
    if start != -1 and end > start:
        return old_text[:start] + block + old_text[end + len(END_MARK):].lstrip("\n")
    if not old_text.strip():
        return block
    return old_text.rstrip("\n") + "\n\n" + block


def write_rules(target):
    """Writes the rules into the file; returns what it did: "made", "added", "updated" or "the same"."""
    old_text = target.read_text(encoding="utf-8") if target.exists() else ""
    new_text = with_rules(old_text, rules_text())
    if new_text == old_text:
        return "the same"
    target.write_text(new_text, encoding="utf-8")
    if not old_text.strip():
        return "made"
    return "updated" if START_MARK in old_text else "added"


def look_command(words):
    parser = argparse.ArgumentParser(prog="python -m ozdenui look", description="A picture of the window of a program.")
    parser.add_argument("program", help="the program file (Ex: app.py)")
    parser.add_argument("picture", nargs="?", help="the picture file, a PNG (default: the name of the program, .png)")
    parser.add_argument("--wait", type=float, default=None, help="seconds between the first drawing and the picture (1.5)")
    parser.add_argument("--theme", choices=("light", "dark"), default="", help="the theme of the window, whatever the program asks")
    arguments = parser.parse_args(words)
    if not Path(arguments.program).is_file():
        print(f"{arguments.program}: no such program file.")
        return 2
    from . import _look  # WHY here: agents must work without a window system

    picture = arguments.picture or str(Path(arguments.program).with_suffix(".png"))
    wait = _look.DEFAULT_WAIT_SECONDS if arguments.wait is None else arguments.wait
    error = _look.look(arguments.program, picture, wait, arguments.theme)
    if error:
        print(f"ozdenui look: {error}")
        return 1
    print(f"{picture}: the picture of the window of {arguments.program}.")
    return 0


def main(words):
    if words[:1] == ["look"]:
        return look_command(words[1:])
    if words[:1] != ["agents"] or len(words) > 2:
        print(USAGE)
        return 0 if not words else 2
    if words[1:] == ["--print"]:
        print(rules_text())
        return 0
    target = Path(words[1] if len(words) == 2 else DEFAULT_TARGET)
    done = write_rules(target)
    messages = {
        "made": f"{target}: made, with the rules of OzdenUI {__version__}.",
        "added": f"{target}: the rules of OzdenUI {__version__} are added at its end; your lines are as they were.",
        "updated": f"{target}: the rules of OzdenUI are updated to {__version__}; your lines are as they were.",
        "the same": f"{target}: already has the rules of OzdenUI {__version__}.",
    }
    print(messages[done])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
