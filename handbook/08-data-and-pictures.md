# 8. Data and pictures

The components of this chapter show what a Python program usually has: numbers, rows, plots, logs, texts and code.
None of them needs another library on the page.

## Charts: GraphBox

```python
GraphBox(type="bar", labels=["Jan", "Feb", "Mar"], values=[1200, 1900, 700], format_value="{:,.0f} TL")
```

- `type`: `"line"`, `"area"`, `"bar"`, `"pie"`, `"doughnut"`, `"radar"`, `"scatter"`, `"bubble"`.
- More lines or bars: `datasets=[{"label": "2025", "data": [8, 11, 9]}, {"label": "2026", "data": [10, 14, 12]}]`.
- The values may be lists, numpy arrays or a pandas Series.
- `format_value` is a format text, not a function, because the page needs the text of a number while it draws:
  `"{}"`, `"{:.2f}"`, `"{:,}"`, `"{:,.0f} TL"`, `"{:.1%}"`.
- Later: `graph.set_values([...])`, `graph.set_type("line")`, `graph.add_value("Apr", 15)`,
  `graph.save_image("chart.png")`. `on_click(graph, item)`: `item["label"]`, `item["value"]`.

### A live chart and a log

```python
import random
import time
from ozdenui import App, GraphBox, LogView, VGroup, every

POINTS = 30
view = {}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=12, padding=20):
        view["chart"] = GraphBox(type="area", title_text="Temperature", labels=[], values=[], curve="smooth",
                                 show_points=False, max_count=POINTS, format_value="{:.1f}°", height=240)
        view["log"] = LogView(fill=True)
    every(1000, measure)

def measure():
    value = round(20 + random.uniform(-3, 3), 1)
    view["chart"].add_value(time.strftime("%H:%M:%S"), value)   # the oldest goes after POINTS values
    if value > 22:
        view["log"].warn(f"Warm: {value}°")
    else:
        view["log"].info(f"{value}°")

App(start, title="A sensor", size=(560, 520)).run()
```

`examples/charts.py` has a live chart, bars you can click, a doughnut and a chart saved as a picture.

## Tables

```python
people = [{"name": "Ada", "city": "London", "orders": 12}, {"name": "Alan", "city": "Manchester", "orders": 7}]
table = SmartTable(columns=[{"key": "name", "title": "Name", "width": 200}, {"key": "city", "title": "City"},
                            {"key": "orders", "title": "Orders", "type": "integer"}],
                   rows=people, height=300, on_select=lambda table, row: print(row["name"]))
```

- **`SmartTable`** makes only the rows that are seen: 100000 rows reach it in about 2 s on a Mac, and then it stays
  fast. It has a filter box and sorting on its titles. A row is a dict by the keys of the columns, or a list in their
  order. The values are shown as text: format them in Python (`f"{price:,.2f}"`).
- **`DataTable`** is for up to a few hundred rows; its columns fit their texts, `show_search=True` adds a search box,
  and `table.selected_row` is the row as you gave it.
- `examples/csv_viewer.py` opens a CSV file in a SmartTable.

## Pictures

A picture may be a file path, bytes, a Pillow image, a matplotlib figure or an address:

```python
Icon(width=48, height=48, picture="logo.png")
view = ImageView(height=400, image="photo.jpg")    # zoom with the wheel or two fingers, drag to move
view.set_image(figure)                             # a matplotlib figure
```

- A new picture of the same size keeps the zoom and does not blink, so a program can draw its plot again and again
  (`examples/image_viewer.py`).
- A picture goes to the page in the call: 8 MB take about 150 ms on a Mac. `picture_address(picture)` gives its address
  once, for a picture you show many times.
- `ItemList(layout="grid", style_name="gallery")` shows many pictures as tiles (`examples/photos.py`).

## Logs: LogView

```python
log = LogView(height=300)
log.info("Reading the file")
log.success("Done")
log.error("The file is not there")
log.capture_print()                                     # print() goes into it (and the errors, as errors)
logging.getLogger().addHandler(log.logging_handler())   # and the logging module
```

The view follows the last line until the reader scrolls up. A text is never read as HTML. `examples/job_log.py`.

## Texts, JSON and code

| | |
|---|---|
| `MarkdownView(text="# A report\n\nSome **bold** words")` | `view.append_text(piece)` adds to the end: the answer of an AI as it comes; `view.load_file("notes.md")` |
| `JsonView(value=data, height=400, on_select=fn)` | any value, a million items too; a click tells the path: `view.selected_path_text` (`users[0].name`), `view.selected_value` |
| `JsonEditor(value=rows, height=360, on_change=fn)` | a list or a dict of JSON written in a table; `on_change(editor, value)` gets the whole value, `editor.value` asks for it; `JsonEditor.open(value=settings, on_apply=fn)`: in a window with Cancel and Apply |
| `CodeEditor(value="x = 1", language="python", height=300, on_change=fn)` | `editor.value`; Python, JavaScript, JSON, HTML, CSS, SQL, Bash |
| `ChatView(empty_text="Ask something", on_send=answer)` | a conversation with an AI: `on_send(chat, text)`; an answer is Markdown: `key = chat.add_message(role="assistant")`, then `chat.append_text(key, piece)`; `chat.busy = True` shows the dots and Stop (`on_stop`) |
| `WebView(html=figure.to_html(), height=400)` | a web page or an HTML text with its scripts: a plotly chart, a folium map, a pandas table (`df.to_html()`); `view.load("https://...")`, `on_message(view, data)` |

- A Markdown text is never read as HTML and no script of it runs. `![A plot](plot.png)` reads a file of this computer;
  a picture with an `http` address stays a link (`remote_pictures=True` for a text you trust).
- A `JsonEditor` takes JSON data only (texts, numbers, True / False, None, lists and dicts): a date is refused, as the
  `json` module does, because it would come back as a text.
- The pieces of an answer of a `ChatView` may come from a background job (`run_in_background`): the window keeps working,
  and the view follows the end until the reader scrolls up (`examples/chat.py`).
- A `WebView` needs a connection for what its page takes from the internet (a script, a map tile, a picture). A file of
  this computer (`view.load_file("report.html")`) is shown by its text: a picture or a style next to it is not loaded.
- `examples/markdown_editor.py`, `examples/json_viewer.py`, `examples/json_editor.py` and `examples/editor.py` (a small
  editor that runs its Python) show them.

## Drawing: Canvas

```python
canvas = Canvas(height=400)
canvas.circle(100, 80, 30, fill="orange", draggable=True)
canvas.line(20, 20, 200, 120, color="tomato", line_width=4)
canvas.text(20, 180, "Drag the circle", font_size=16)
```

- Shapes: `line`, `rect`, `circle`, `ellipse`, `polyline`, `polygon`, `text`, `image`. Each returns its key:
  `canvas.update_shape(key, fill="red")`, `canvas.move_shape(key, 10, 0)`, `canvas.remove_shape(key)`.
- The page moves a `draggable=True` shape by itself; `on_shape_move(canvas, shape)` tells Python where it stopped.
- `drawing=True` gives the mouse a pen; `canvas.save_image("drawing.png")` (`examples/paint.py`).

## Next

[Chapter 9: Your own component](09-your-own-component.md).
