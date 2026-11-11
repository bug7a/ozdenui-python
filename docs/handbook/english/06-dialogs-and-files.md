# 6. Dialogs, messages and files

## Dialogs return their answer

A dialog in OzdenUI is a function call that returns the answer, as `input()` does:

```python
from ozdenui import Dialog

if Dialog.confirm("The file will be deleted.", title="Delete it?", confirm_text="Delete", danger=True):
    delete_the_file()

name = Dialog.prompt("A name for the folder:", value="Photos")    # the text, or None (cancelled)
choice = Dialog.ask("Save the changes?", buttons=["Save", "Don't save", "Cancel"])   # the text of the button, or None
Dialog.alert("The copy is done.", title="Done")
```

- **The window keeps working while your code waits**: other events and timers run, a clock keeps ticking. Only the
  function that asked waits for the answer.
- `danger=True` draws the confirm button as a delete. `Dialog.ask()` makes the first button the main one.
- Escape or a click outside is "no": `False` for `confirm()`, `None` for the others.
- A dialog works in `start()` too (the window is shown first), and in a job of `run_in_background()`.

## Short messages: Toast

```python
from ozdenui import Toast

Toast.success("Saved.")
Toast.error("Could not save the file.", title="Error")
Toast.warning("The disk is almost full.")
Toast.info("3 new messages", duration=0)      # ms; 0 stays until it is closed
```

A toast comes in a corner and goes by itself. It never waits: the code goes on at once.

## Bubbles: Tooltip

```python
Tooltip(target=save_button, text="Saves the file (Ctrl+S)")     # under the mouse
bubble = Tooltip.show(save_button, "Saved.", time=2000)          # at the button now, for 2 s
```

A popover is a bubble that stays and holds objects; your function makes them each time it opens:

```python
def make_filters():
    CheckBox(text="Only the new ones")
    CheckBox(text="With a picture")

filters = Tooltip.popover(filter_button, make_filters)   # a click on the button opens and closes it
filters.close()                                           # also: filters.open(), filters.is_open
```

## The file dialogs of the system

```python
from ozdenui import choose_folder, open_file, save_file

path = open_file(file_types=("Images (*.png;*.jpg)", "All files (*.*)"))  # a path, or None
paths = open_file(multiple=True)                                          # a list, or None
target = save_file(file_name="report.csv", file_types=("CSV (*.csv)",))   # where to save, or None
folder = choose_folder()                                                  # a folder, or None
```

They are the dialogs of the computer, so the paths are real: open them with `open()` or `pathlib`.

### A small editor

```python
from pathlib import Path
from ozdenui import App, Dialog, HGroup, SmartButton, TextAreaField, Toast, VGroup, open_file, save_file

FILE_TYPES = ("Text files (*.txt;*.md)", "All files (*.*)")
view = {"path": None}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=12, padding=20, align="left top"):
        with HGroup(hug=True, gap=8):
            SmartButton(text="Open", on_click=open_note)
            SmartButton(text="Save", tone="cyan", on_click=save_note)
            SmartButton(text="Clear", tone="orange", on_click=clear_note)
        view["note"] = TextAreaField(title_text="Note", width="100%", height=260)

def open_note():
    path = open_file(file_types=FILE_TYPES)
    if not path:
        return
    view["note"].text = Path(path).read_text(encoding="utf-8")
    view["path"] = path
    view["note"].title_text = Path(path).name

def save_note():
    path = view["path"] or save_file(file_name="note.txt", file_types=FILE_TYPES)
    if not path:
        return
    Path(path).write_text(view["note"].text, encoding="utf-8")
    view["path"] = path
    Toast.success("Saved.", title=Path(path).name)

def clear_note():
    if Dialog.confirm("The text in the window goes away.", title="Clear the note?", confirm_text="Clear", danger=True):
        view["note"].text = ""

App(start, title="Note", size=(560, 420)).run()
```

## Files dropped on the window: FilePicker

`FilePicker` is a place to drop files on, or to click for the file dialog. Every file reaches Python with its real path:

```python
def show_files(picker):
    for file in picker.files:
        print(file["name"], file["size_text"], file["path"])

FilePicker(accept=".csv,.txt", multiple=True, title_text="Drop files here", on_change=show_files)
```

- A file is a dict: `name`, `path`, `size`, `size_text`, `type`, `extension`, `last_modified`.
  `picker.paths` is only the paths.
- `accept=".pdf,.txt"` or `"image/*"`; `max_size` (bytes) and `max_files`: what does not pass goes to
  `on_error(picker, errors)`.
- `multiple=True` adds to the list; without it a new file takes the place of the old one. `directory=True` chooses a
  folder with a click. `picker.add_paths([...])` adds files from code, `picker.clear()` empties it.
- `title_text`, `description_text`: its texts; `icon_file`: a picture of yours in the place of its icon.
- A folder dropped on it is not read: choose a folder with `directory=True` or `choose_folder()`.

`examples/files.py` shows a tree of a folder, a menu on it and a place to drop files.

## Next

[Chapter 7: Looks](07-looks.md): dark windows, the minimal look and your colors.
