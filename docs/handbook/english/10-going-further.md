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

## Limits of v0.1

- A callback that must answer at once can not be a Python function, because the answer comes later: the
  `on_before_click` of a `SmartButton`, an `on_close` of `Tabs` that returns `False`, the `validate` of a `TagInput`,
  and the functions that build objects inside a component (`createItemView`, `createCellView`). Format the values
  of a table in Python; the numbers of a `GraphBox` or a `Stepper` take a format text.
- Fifteen components change their theme while they are on the page; the others take their look when they are made
  (chapter 7).
- It is made on macOS. The tests of the package run on Windows too (it needs the WebView2 runtime); Linux needs the GTK
  or Qt web view of pywebview.
- No browser or Jupyter mode yet.
- A program made into one file with PyInstaller needs the files of the package (`--collect-data ozdenui`); this has
  not been tried yet.

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
