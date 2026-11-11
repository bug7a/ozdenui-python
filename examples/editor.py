# Bismillah
"""A small code editor: write Python, run it (F5) and read its output. A menu, a row of buttons, two areas with a line between them, the
line and the column of the cursor, a light and a dark theme, the keys Ctrl + S and F5 (Cmd on a Mac)."""

import subprocess
import sys

from ozdenui import App, CodeEditor, LogView, MenuBar, Splitter, StatusBar, ToolBar, VGroup, open_file, run_in_background, save_file

THEME_COLORS = {"light": "#FFFFFF", "dark": "#1C1C1B"}
OUTPUT_HEIGHT = 170
FIRST_TEXT = '''"""Press F5 to run this program."""

names = ["Ada", "Can", "Deniz"]

for number, name in enumerate(names, start=1):
    print(number, name)

print("Done")
'''

view = {"theme": "light", "path": None}


def start(page):
    page.color = THEME_COLORS["light"]
    view["page"] = page
    with VGroup(gap=0, align="left top"):
        view["menu"] = MenuBar(menus=[
            {"text": "File", "items": [
                {"text": "Open...", "key": "open", "shortcut": "Ctrl+O", "on_click": open_program},
                {"text": "Save", "key": "save", "shortcut": "Ctrl+S", "on_click": save_program},
            ]},
            {"text": "Run", "items": [
                {"text": "Run the program", "key": "run", "shortcut": "F5", "on_click": run_program},
                {"text": "Clear the output", "key": "clear", "on_click": lambda: view["log"].clear()},
            ]},
            {"text": "View", "items": [
                {"text": "Dark theme", "key": "dark", "checked": False, "on_click": toggle_theme},
                {"text": "Line numbers", "key": "numbers", "checked": True, "on_click": toggle_line_numbers},
            ]},
        ])
        # WHY the same shortcuts as the menu: the hint of a button tells them; a key that is in both bars runs once.
        view["tools"] = ToolBar(items=[
            {"key": "open", "icon": "open", "hint": "Open...", "shortcut": "Ctrl+O", "on_click": open_program},
            {"key": "save", "icon": "save", "hint": "Save", "shortcut": "Ctrl+S", "on_click": save_program},
            "-",
            {"key": "run", "icon": "play", "text": "Run", "shortcut": "F5", "on_click": run_program},
            {"key": "clear", "icon": "delete", "hint": "Clear the output", "on_click": lambda: view["log"].clear()},
        ])
        view["split"] = Splitter(fill=True,
                                 direction="vertical", second_size=OUTPUT_HEIGHT, min_first=80, min_second=60)
        with view["split"].first:
            view["editor"] = CodeEditor(height="100%", language="python", value=FIRST_TEXT, framed=False, on_cursor_change=show_cursor)
        with view["split"].second:
            view["log"] = LogView(height="100%", framed=False, empty_text="F5 runs the program.")
        view["status"] = StatusBar(message="Ready", items=[{"key": "place", "text": "Line 1, column 1"}, "Python"])


def themed_objects():
    return [view["menu"], view["tools"], view["split"], view["editor"], view["log"], view["status"]]


def toggle_theme(bar, item):
    view["theme"] = "light" if view["theme"] == "dark" else "dark"
    view["page"].color = THEME_COLORS[view["theme"]]
    for obj in themed_objects():
        obj.set_theme(view["theme"])
    bar.set_item_checked("dark", view["theme"] == "dark")


def toggle_line_numbers(bar, item):
    view["editor"].show_line_numbers = not item["checked"]
    bar.set_item_checked("numbers", not item["checked"])


def show_cursor(editor):
    view["status"].set_item_text("place", f"Line {editor.cursor_line}, column {editor.cursor_column}")


def open_program():
    path = open_file(file_types=("Python files (*.py)", "All files (*.*)"))
    if not path:
        return
    with open(path, encoding="utf-8") as file:
        view["editor"].value = file.read()
    view["path"] = path
    view["status"].set_message(path)


def save_program():
    path = view["path"] or save_file(file_name="program.py", file_types=("Python files (*.py)",))
    if not path:
        return
    with open(path, "w", encoding="utf-8") as file:
        file.write(view["editor"].value)
    view["path"] = path
    view["status"].set_message("Saved", "success", 3000)


def run_program():
    code = view["editor"].value  # WHY here: a question to the page works only on this thread, not in the job
    view["log"].clear()
    view["status"].set_busy(True)
    view["status"].set_message("Running...")
    run_in_background(run_in_python, code)


def run_in_python(code):
    process = subprocess.Popen([sys.executable, "-u", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, encoding="utf-8", errors="replace")
    for line in process.stdout:
        view["log"].add_line(line.rstrip("\n"))
    exit_code = process.wait()
    if exit_code == 0:
        view["log"].success("The program ended")
    else:
        view["log"].error(f"The program ended with the code {exit_code}")
    view["status"].set_busy(False)
    view["status"].set_message("Ready")


if __name__ == "__main__":
    App(start, title="A small code editor", size=(760, 600)).run()
