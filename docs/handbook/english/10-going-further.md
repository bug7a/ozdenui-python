# 10. Going further

## Finding a mistake

- **A mistake of Python** (a wrong name, a wrong type) stops at its line, as always: the traceback is in the terminal.
- **A mistake of the page** (a value the page could not use, a component that failed) is written to the terminal with
  the line of your code that sent it:

  ```
  ozdenui: settings.py:24: create o17: <what the page said>
  ```

- **A warning of a component** comes the same way: `ozdenui (page warn): SmartButton: tone not found: cyann`.
- **A name an object does not have** (a typo) is told once, at its line. The page would keep it without a word:

  ```
  ozdenui: form.py:12: Label: "txet" is not a param of Label (did you mean "text"?)
  ```

  A name of the kit written in camelCase to a class (`TextField(titleText=...)`) is told with its Python name
  (`title_text`): a class reads its params by their Python names.
  A value of your own on an object goes under a name that starts with `_`: `row._price = 12` stays in Python.
  An editor (VS Code, PyCharm) offers the params of every class and marks such a name before the program runs.
- `App(..., debug=True)` gives the window the developer tools of the web view: right click > Inspect.
- Reading a value that was never given raises an error that names `measure()` (chapter 2).

## basic.js from Python

Everything of basic.js is reachable, also what has no Python name yet:

```python
gauge.call("setValue", 80)                 # calls a method of the object on the page; does not wait
text = editor.ask("getSelectedText")       # calls a method and returns its result
width = page.app.evaluate(f"{label.js}.elem.offsetWidth")   # any JavaScript; label.js is the object
```

- `call()` goes with the other commands of the function; `ask()` and `evaluate()` wait for the page, so keep them out of
  loops.
- The methods and params of every component are in its source and in the [catalog](https://bug7a.github.io/js-components/).
  In Python a param is written in snake_case; a method keeps its name (`setValue`).

## Speed

Measured on a Mac:

| | |
|---|---|
| the window shows | about 0.5 s |
| 1000 objects made | about 50 ms |
| a click → your function → the screen | about 3 ms |
| 100000 rows into a `SmartTable` | about 2 s, then it stays fast |
| a picture of 8 MB | about 150 ms |

What makes a program slow is usually a loop that asks the page (`measure()`, `ask()`) or a slow job on the app thread.
All the commands of one function go together, so making 500 objects in a loop is one call, not 500.

A long task on the app thread can show its progress with `page.app.flush()`: the commands made until then go to the
page at once. A long job is better in `run_in_background()` (chapter 4).

## Threads, again

| | may change objects | may wait for a dialog | may ask the page (`measure()`, `ask()`) |
|---|---|---|---|
| `start()`, events, timers (the app thread) | yes | yes | yes |
| a job of `run_in_background()` | yes | yes | no |
| a thread of your own | through `call_soon(fn)` | | |

## Making an app

A program can go to people who have no Python: [PyInstaller](https://pyinstaller.org) makes it an app. The package
tells PyInstaller to take the page of the window (basic.js, the components, the fonts) into it, so no flag is needed
for it:

```
pip install pyinstaller
pyinstaller --onefile --windowed app.py    # Windows: dist/app.exe, no console next to the window
pyinstaller --windowed app.py              # macOS: dist/app.app
pyinstaller --onefile app.py               # Linux: dist/app
```

- Build it on the system it is for: a Windows app on Windows, a Mac app on a Mac. Tried with a small program: about
  14 MB on Windows, 17 MB on a Mac, 60 MB on Linux (GTK and WebKit go into it).
- The computer of the user still needs the web view of its system: WebView2 on Windows (most computers have it), the
  GTK web view on Linux (chapter 1). A Mac has its own.
- A new app from a maker the system does not know can get a warning the first time (SmartScreen on Windows, Gatekeeper
  on a Mac); signing the app removes it.
- Files of your own that the program reads (pictures, data) go in with `--add-data`: see the manual of PyInstaller.

## Limits of v0.1

- A callback that must answer at once can not be a Python function, because the answer comes later: the
  `on_before_click` of a `SmartButton`, an `on_close` of `Tabs` that returns `False`, the `validate` of a `TagInput`,
  and the functions that build objects inside a component (`createItemView`, `createCellView`). Format the values
  of a table in Python; the numbers of a `GraphBox` or a `Stepper` take a format text.
- Fifteen components change their theme while they are on the page; the others take their look when they are made
  (chapter 7).
- It is made on macOS. The tests of the package run on Windows and Linux too (Windows needs the WebView2 runtime,
  Linux the GTK web view of the system: chapter 1); the Qt web view on Linux has not been tried.
- No browser or Jupyter mode yet.

## With an AI assistant

OzdenUI is new, so an AI assistant (Claude Code, Codex, Cursor, Copilot...) does not know it yet and guesses from the
toolkits it knows. One command writes the rules of the package into the folder of your project, where the assistant
reads them by itself:

```
python -m ozdenui agents              # into AGENTS.md
python -m ozdenui agents CLAUDE.md    # into the file Claude Code reads
python -m ozdenui agents --print      # only prints them
```

- The rules are short: how a program is made, the layout, the events, the components, the mistakes to avoid, and where
  the params of every class are.
- A file that is there keeps your lines: the rules go to its end, between two marks. Run the command again after an
  upgrade of the package: only that part changes.

An assistant can not see the window it made. One more command takes a picture of it:

```
python -m ozdenui look app.py                              # runs app.py, saves app.png, closes the window
python -m ozdenui look app.py dark.png --theme dark --wait 3
```

- The program runs as it is; the picture is taken 1.5 s after its first drawing (`--wait`), then the window closes.
- `--theme dark` opens the window dark, whatever the program asks.
- On a Mac the picture comes from the window itself. On Windows it is that part of the screen: it needs Pillow
  (`pip install pillow`) and the window in front.

## Where to go next

- **The examples** of the package source, from the smallest: `basics`, `counter`, `greeting`, `calculator`, `todo`,
  `settings`, `dialogs`, `clock`, `game`, `file_tool`, `csv_viewer`, `charts`, `files`, `photos`, `paint`, `editor`,
  `markdown_editor`, `json_viewer`, `json_editor`, `chat`, `image_viewer`, `job_log`, `form`, `gallery` (every component),
  `minimal_theme`, `minimal_accent`.
- **The README** of the package: every component in one table.
- **`help(ClassName)`** in Python: the params, the callbacks and the methods of a component.
- **[basic.js](https://bug7a.github.io/basic.js/)** and **[the components](https://bug7a.github.io/js-components/)**:
  the library under it, with a live example of every component.

[Back to the start](README.md)
