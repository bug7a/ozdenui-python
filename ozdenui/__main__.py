# Bismillah
"""__main__.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The command of the package: python -m ozdenui agents writes the rules of OzdenUI for an AI assistant (AGENTS.md of the
package) into the folder of a project, where the assistants read them by themselves.
Usage:
    python -m ozdenui agents              Writes them into AGENTS.md of this folder (most assistants read it).
    python -m ozdenui agents CLAUDE.md    Into another file (Claude Code reads CLAUDE.md).
    python -m ozdenui agents --print      Only prints them.
A file that is there keeps its own lines: the rules go between two marks at its end, and the next run changes only them.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

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
python -m ozdenui agents --print      Only prints them."""


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


def main(words):
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
