# Bismillah
"""check_handbook.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Opens every whole program of the handbook in its real window, one after the other. A whole program is a Python block of
handbook/*.md or handbook/turkce/*.md that imports ozdenui and ends with App(...).run() (the rule of tests/test_handbook.py,
which runs the same programs without a window). A program passes when its window opens and the terminal has no traceback
and no message of ozdenui. With a folder, it takes a picture of every window and puts them on one sheet (sheet.png), so a
change of the package or of a chapter is seen in one look.

Usage: .venv/bin/python checks/check_handbook.py [folder for the pictures] [--only text]
    --only turkce        only the programs whose name has this text (--only 03-layout: one chapter)
Exit code 0: every program passed. A mistake names its line in the chapter (03-layout.md:45).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HANDBOOK_FOLDER = Path(ROOT) / "handbook"
CODE_BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)
WAIT_SECONDS = 1.5  # after start(): the page draws, the first motions end
WINDOW_TIMEOUT_SECONDS = 30  # a window that does not get ready closes after it
CHECK_TIMEOUT_SECONDS = 90
SHEET_COLUMNS = 4
SHEET_CELL = (360, 260)  # px of a picture on the sheet
SHEET_GAP = 16
SHEET_LABEL_HEIGHT = 26
SHEET_COLORS = {"ground": "#E9EBEF", "text": "#1F2430", "failed": "#C0392B"}
SHEET_FONT_SIZE = 15


# *** THE PROGRAMS OF THE HANDBOOK:

def whole_programs(only=""):
    """[(name, chapter file, its first line, code)]: name is the chapter and the number of the block ("03-layout-2",
    "turkce/03-layout-2"); the code starts at that line of the chapter."""
    programs = []
    for chapter in sorted(HANDBOOK_FOLDER.rglob("*.md")):
        text = chapter.read_text(encoding="utf-8")
        chapter_name = chapter.relative_to(HANDBOOK_FOLDER).with_suffix("").as_posix()
        for number, block in enumerate(CODE_BLOCK.finditer(text), start=1):
            code = block.group(1)
            if not ("from ozdenui import" in code and "App(" in code and ".run()" in code):
                continue
            name = f"{chapter_name}-{number}"
            if only in name:
                first_line = text.count("\n", 0, block.start(1)) + 1
                programs.append((name, str(chapter), first_line, code))
    return programs


def file_name_of(name):
    return name.replace("/", "-")


# *** ONE PROGRAM, IN A PROCESS OF ITS OWN (WHY: one window loop in a process):

def open_one(program_file, chapter_file, picture_file):
    """Runs a program as its chapter has it, takes a picture of its window and closes it. Prints the result as JSON."""
    sys.path.insert(0, HERE)
    from ozdenui import App
    from window_check import TerminalProblems, snapshot_window

    terminal = TerminalProblems(sys.stderr)
    sys.stderr = terminal
    result = {"problems": [], "picture": None, "opened": False}
    run_of_the_package = App.run

    def take_picture(app):
        if not picture_file:
            app.close()
            return

        def after_picture(error):
            result["picture"] = error or picture_file
            app.close()

        snapshot_window(app, picture_file, after_picture)

    def wait_then_take(app):
        time.sleep(WAIT_SECONDS)
        app.call_soon(lambda: take_picture(app))

    def run_with_a_picture(app):
        start_of_the_program = app._start

        def start(page):
            # WHY finally: a program that fails must still be pictured and closed
            try:
                start_of_the_program(page)
            finally:
                threading.Thread(target=wait_then_take, args=(app,), daemon=True).start()

        app._start = start
        result["opened"] = True
        # WHY a timer: a page that does not get ready never calls start(), and its window stayed
        closer = threading.Timer(WINDOW_TIMEOUT_SECONDS, app.close)
        closer.daemon = True
        closer.start()
        run_of_the_package(app)

    App.run = run_with_a_picture
    code = Path(program_file).read_text(encoding="utf-8")
    try:
        # WHY the chapter as its file: a traceback and a message of ozdenui name the line of the chapter
        exec(compile(code, chapter_file, "exec"), {"__name__": "__main__", "__file__": chapter_file})
    except Exception:
        result["problems"].append(traceback.format_exc(limit=4))
    if not result["opened"]:
        result["problems"].append("it opened no window")
    if picture_file and result["opened"] and result["picture"] != picture_file:
        result["problems"].append(f"no picture: {result['picture']}")
    result["terminal_problems"] = terminal.lines
    result["passed"] = not result["problems"] and not terminal.lines
    sys.stderr = terminal.stream
    print(json.dumps(result))


def check_program(name, chapter_file, first_line, code, picture_folder):
    picture = os.path.join(picture_folder, file_name_of(name) + ".png") if picture_folder else ""
    with tempfile.TemporaryDirectory() as folder:
        program_file = os.path.join(folder, file_name_of(name) + ".py")
        # WHY the empty lines: the code stands at the line it has in its chapter
        Path(program_file).write_text("\n" * (first_line - 1) + code, encoding="utf-8")
        command = [sys.executable, os.path.abspath(__file__), "--one", program_file, chapter_file, picture]
        # WHY utf-8: the console of Windows has an old code page; the output is read as utf-8 below
        environment = dict(os.environ, PYTHONIOENCODING="utf-8")
        started = time.perf_counter()
        try:
            finished = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment,
                                      cwd=ROOT, timeout=CHECK_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            return {"name": name, "passed": False, "problems": [f"it did not end in {CHECK_TIMEOUT_SECONDS} s"], "seconds": CHECK_TIMEOUT_SECONDS}
    last_line = (finished.stdout.strip().splitlines() or ["{}"])[-1]
    try:
        result = json.loads(last_line)
    except json.JSONDecodeError:
        result = {"passed": False, "problems": [finished.stdout[-800:] + finished.stderr[-800:]]}
    result["name"] = name
    result["seconds"] = round(time.perf_counter() - started, 1)
    return result


# *** THE SHEET:

def make_sheet(results, picture_folder):
    """All the pictures on one image, each with its name (red: it failed). Returns its path or why there is none."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return "no sheet: it needs Pillow (pip install pillow)"
    pictured = [result for result in results if result.get("picture") and os.path.exists(str(result["picture"]))]
    if not pictured:
        return "no sheet: no picture"
    cell_width, cell_height = SHEET_CELL
    columns = min(SHEET_COLUMNS, len(pictured))
    rows = math.ceil(len(pictured) / columns)
    size = (SHEET_GAP + columns * (cell_width + SHEET_GAP), SHEET_GAP + rows * (cell_height + SHEET_LABEL_HEIGHT + SHEET_GAP))
    sheet = Image.new("RGB", size, SHEET_COLORS["ground"])
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=SHEET_FONT_SIZE)
    except TypeError:  # WHY: an old Pillow has one size of its own font
        font = ImageFont.load_default()
    for index, result in enumerate(pictured):
        picture = Image.open(result["picture"]).convert("RGB")
        picture.thumbnail(SHEET_CELL)
        left = SHEET_GAP + (index % columns) * (cell_width + SHEET_GAP)
        top = SHEET_GAP + (index // columns) * (cell_height + SHEET_LABEL_HEIGHT + SHEET_GAP)
        sheet.paste(picture, (left, top))
        color = SHEET_COLORS["text"] if result.get("passed") else SHEET_COLORS["failed"]
        draw.text((left, top + picture.height + 5), result["name"], fill=color, font=font)
    path = os.path.join(picture_folder, "sheet.png")
    sheet.save(path)
    return path


# *** RUN:

def main():
    parser = argparse.ArgumentParser(description="Opens every whole program of the handbook in its real window.")
    parser.add_argument("folder", nargs="?", default="", help="the pictures of the windows and sheet.png go here")
    parser.add_argument("--only", default="", help="only the programs whose name has this text (turkce, 03-layout)")
    arguments = parser.parse_args()
    if arguments.folder:
        os.makedirs(arguments.folder, exist_ok=True)
    programs = whole_programs(arguments.only)
    if not programs:
        print(f"no program of the handbook has {arguments.only!r} in its name")
        sys.exit(1)
    results = [check_program(name, chapter, line, code, os.path.abspath(arguments.folder) if arguments.folder else "")
               for name, chapter, line, code in programs]
    for result in results:
        mark = "PASS" if result.get("passed") else "FAIL"
        print(f"{mark}  {result['name']:<32} {result['seconds']:>5} s")
        for problem in result.get("problems", []) + result.get("terminal_problems", []):
            print("      -", ascii(problem.strip()))  # WHY ascii(): the console of Windows has an old code page
    if arguments.folder:
        print(make_sheet(results, arguments.folder))
    passed = sum(1 for result in results if result.get("passed"))
    print(f"{passed} / {len(results)} passed")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--one":
        open_one(*sys.argv[2:5])
    else:
        main()
