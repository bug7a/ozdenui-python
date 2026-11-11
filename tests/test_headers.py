# Bismillah
"""test_headers.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Every code file of the package has the house header: Bismillah on its first line (after a #! line), its name and the
version, and the license block (Started Date, Webpage, the copyright line of LICENSE, the Apache lines). An example has
only Bismillah: the examples are written to be copied into the programs of other people.
WHY: a new file got its header only when somebody remembered it; Apache 2.0 4(c) wants the notice in every copy.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import os
import re
from pathlib import Path

import pytest

SOURCE_FOLDER = Path(__file__).resolve().parent.parent
CODE_SUFFIXES = (".py", ".pyi", ".js", ".css", ".html", ".htm", ".sh", ".bat")
# Not the files of the package: the copy of the kit (its files have their own headers, the kit checks them), the site
# that _make-repo.sh writes into docs/ from ../webpage-python, and what the tools make.
SKIPPED_PATHS = ("ozdenui/web/comp/", "ozdenui/web/basic/", "docs/")
SKIPPED_FOLDERS = ("dist", "build", "__pycache__")
COPYRIGHT = re.compile(r"Copyright (\d{4}(?:-\d{4})?) Bugra Ozden <bugra\.ozden@gmail\.com> \(https://bug7a\.github\.io/\)")
STARTED_DATE = re.compile(r"Started Date: (January|February|March|April|May|June|July|August|September|October|November"
                          r"|December) \d{4}")
WEBPAGE = re.compile(r"Webpage: https://\S+")
LICENSE_LINES = ("Licensed under the Apache License, Version 2.0", "SPDX-License-Identifier: Apache-2.0")


def is_skipped_folder(name):
    return name.startswith(".") or name in SKIPPED_FOLDERS or name.endswith(".egg-info")


def code_files():
    """The code files of the package, from its folder: "ozdenui/app.py", "update-web.sh"..."""
    found = []
    for folder, folders, files in os.walk(SOURCE_FOLDER):
        folders[:] = sorted(name for name in folders if not is_skipped_folder(name))
        for name in sorted(files):
            relative = (Path(folder) / name).relative_to(SOURCE_FOLDER).as_posix()
            if name.endswith(CODE_SUFFIXES) and not relative.startswith(SKIPPED_PATHS):
                found.append(relative)
    return found


def years_of_the_license():
    return COPYRIGHT.search((SOURCE_FOLDER / "LICENSE").read_text(encoding="utf-8")).group(1)


def has_bismillah_first(relative, text):
    """On the first line: # Bismillah (after a #! line), /* Bismillah */, @rem Bismillah; in a page before <html> (a page
    with no script of its own) or as the first line of its first script (as the pages of the kit)."""
    lines = text.splitlines()
    suffix = Path(relative).suffix
    if suffix in (".py", ".pyi", ".sh"):
        first = 1 if lines and lines[0].startswith("#!") else 0
        return len(lines) > first and lines[first] == "# Bismillah"
    if suffix in (".js", ".css"):
        return lines[:1] == ["/* Bismillah */"]
    if suffix == ".bat":
        return lines[:1] == ["@rem Bismillah"]
    head = text.split("<html", 1)[0]
    script = re.search(r"<script>\s*(?:\"use strict\";\s*)?(\S[^\n]*)", text)
    return "<!-- Bismillah -->" in head or (script is not None and script.group(1) == "/* Bismillah */")


def header_problems(relative, text, years):
    """What the header of a code file misses ([]: nothing)."""
    problems = []
    name = Path(relative).name
    if not has_bismillah_first(relative, text):
        problems.append("Bismillah is not on its first line")
    name_line = r"ozdenui v\d+\.\d+" if name == "__init__.py" else re.escape(name) + r" - ozdenui v\d+\.\d+"
    if not re.search(name_line, text):
        problems.append(f'no "{name} - ozdenui vX.Y" line')
    if not STARTED_DATE.search(text):
        problems.append('no "Started Date: Month YYYY"')
    if not WEBPAGE.search(text):
        problems.append('no "Webpage: https://..."')
    copyright_line = COPYRIGHT.search(text)
    if copyright_line is None:
        problems.append("no copyright line (the one of LICENSE)")
    elif copyright_line.group(1) != years:
        problems.append(f"the years {copyright_line.group(1)}, LICENSE: {years}")
    problems += [f'no "{line}"' for line in LICENSE_LINES if line not in text]
    return problems


def test_every_code_file_has_the_house_header():
    years = years_of_the_license()
    files = [relative for relative in code_files() if not relative.startswith("examples/")]
    assert len(files) > 10, files  # WHY: a walk that finds nothing passes every file
    problems = []
    for relative in files:
        found = header_problems(relative, (SOURCE_FOLDER / relative).read_text(encoding="utf-8"), years)
        problems += [f"{relative}: {problem}" for problem in found]
    assert problems == [], "\n".join(problems)


@pytest.mark.parametrize("relative", [relative for relative in code_files() if relative.startswith("examples/")])
def test_an_example_has_only_bismillah(relative):
    text = (SOURCE_FOLDER / relative).read_text(encoding="utf-8")
    assert text.splitlines()[:1] == ["# Bismillah"]
    assert not COPYRIGHT.search(text) and "SPDX-License-Identifier" not in text, "an example is copied into other programs"


def test_the_license_and_the_notice_go_with_the_package():
    years = years_of_the_license()
    notice = (SOURCE_FOLDER / "NOTICE").read_text(encoding="utf-8")
    assert COPYRIGHT.search(notice).group(1) == years
    assert '"NOTICE"' in (SOURCE_FOLDER / "pyproject.toml").read_text(encoding="utf-8")  # license-files: in the wheel
    assert "NOTICE" in (SOURCE_FOLDER / "MANIFEST.in").read_text(encoding="utf-8")  # in the source package


def test_the_check_finds_a_missing_header():
    """WHY: a check that finds nothing must be able to find something."""
    good = ("# Bismillah\n\"\"\"tool.py - ozdenui v0.1\nStarted Date: November 2026\nWebpage: https://bug7a.github.io/\n"
            "Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)\n"
            "Licensed under the Apache License, Version 2.0\nSPDX-License-Identifier: Apache-2.0\n\"\"\"\n")
    assert header_problems("checks/tool.py", good, "2020-2026") == []
    assert header_problems("checks/tool.py", "\"\"\"A tool.\"\"\"\n", "2020-2026") != []
    assert header_problems("checks/tool.py", good.replace("# Bismillah\n", "") + "# Bismillah\n", "2020-2026") == [
        "Bismillah is not on its first line"]
    assert header_problems("checks/tool.py", good, "2020-2027") == ["the years 2020-2026, LICENSE: 2020-2027"]
    assert has_bismillah_first("a.sh", "#!/bin/sh\n# Bismillah\n") and has_bismillah_first("a.bat", "@rem Bismillah\n")
    assert has_bismillah_first("a.html", "<!DOCTYPE html>\n<!-- Bismillah -->\n<html>")
    assert has_bismillah_first("a.htm", "<html><head><script>\n\n/* Bismillah */\n")
    assert not has_bismillah_first("a.js", "\"use strict\";\n/* Bismillah */\n")
