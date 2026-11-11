# Bismillah
"""run_all.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Runs every example in its real window with checks/check_example.py, one after the other, and prints a table.
Usage: .venv/bin/python checks/run_all.py [folder for the pictures]
Exit code 0: every example passed. On Windows: checks\\run_windows.bat does everything.
Another engine on a Mac (Chromium, as WebView2): PYWEBVIEW_GUI=qt python checks/run_all.py (it needs PyQt6, PyQt6-WebEngine,
qtpy; WHY: Windows can not be tested on a Mac, but the page runs in the same engine there).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLES = ["basics", "calculator", "counter", "greeting", "gallery", "file_tool", "csv_viewer", "todo", "settings", "dialogs", "clock", "game", "image_viewer", "job_log",
            "editor", "markdown_editor", "json_viewer", "json_editor", "photos", "paint", "form", "charts", "files", "minimal_theme", "minimal_accent", "chat",
            "gallery-styled"]
DARK_EXAMPLES = ["gallery", "json_editor", "minimal_theme", "minimal_accent", "chat", "gallery-styled"]
CHECK_TIMEOUT_SECONDS = 120


def run(name, theme, picture_folder):
    picture = os.path.join(picture_folder, f"{name}-{theme}.png") if picture_folder else ""
    command = [sys.executable, os.path.join(HERE, "check_example.py"), name, picture, theme]
    # WHY utf-8: the console of Windows has an old code page; the output of an example is read as utf-8 below.
    environment = dict(os.environ, PYTHONIOENCODING="utf-8")
    started = time.perf_counter()
    try:
        finished = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment, timeout=CHECK_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        # WHY: One window that does not close must not stop the others for hours.
        return {"passed": False, "problems": [f"it did not end in {CHECK_TIMEOUT_SECONDS} s"], "seconds": CHECK_TIMEOUT_SECONDS}
    seconds = time.perf_counter() - started
    last_line = (finished.stdout.strip().splitlines() or ["{}"])[-1]
    try:
        result = json.loads(last_line)
    except json.JSONDecodeError:
        result = {"passed": False, "problems": [finished.stdout[-800:] + finished.stderr[-800:]]}
    result["seconds"] = round(seconds, 1)
    return result


def main():
    picture_folder = sys.argv[1] if len(sys.argv) > 1 else ""
    if picture_folder:
        os.makedirs(picture_folder, exist_ok=True)
    results = [run(name, "light", picture_folder) for name in EXAMPLES]
    results += [run(name, "dark", picture_folder) for name in DARK_EXAMPLES]
    for result in results:
        mark = "PASS" if result.get("passed") else "FAIL"
        print(f"{mark}  {result.get('example', '?'):<11} {result['seconds']:>5} s")
        for problem in result.get("problems", []) + result.get("terminal_problems", []):
            print("      -", ascii(problem.strip()))  # WHY ascii(): the console of Windows has an old code page
    passed = sum(1 for result in results if result.get("passed"))
    print(f"{passed} / {len(results)} passed")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
