# Bismillah
"""A small Markdown editor: write on the left, read on the right. Open a file with its pictures, save it, a dark theme. A
click on a link is told at the bottom, not opened."""

from ozdenui import App, CodeEditor, MarkdownView, Splitter, StatusBar, ToolBar, VGroup, open_file, save_file

THEME_COLORS = {"light": "#FFFFFF", "dark": "#1C1C1B"}
TYPING_REST_MS = 120  # the text is drawn again when the typing rests
FIRST_TEXT = """# A small report

The **sales** went up this month. Read the [notes](https://example.com/notes).

## The numbers

| Product | Count | Total |
|:---|:--:|---:|
| Olive oil | 120 | 7,200 TL |
| Honey | 45 | 3,150 TL |

## Next steps

- [x] Write the report
- [ ] Send it

> The numbers of the last week are not final.

```python
total = sum(row["total"] for row in rows)
print(f"Total: {total:,} TL")
```
"""

view = {"theme": "light", "path": None}


def start(page):
    page.color = THEME_COLORS["light"]
    view["page"] = page
    with VGroup(gap=0, align="left top"):
        view["tools"] = ToolBar(items=[
            {"key": "open", "icon": "open", "hint": "Open...", "shortcut": "Ctrl+O", "on_click": open_document},
            {"key": "save", "icon": "save", "hint": "Save", "shortcut": "Ctrl+S", "on_click": save_document},
            " ",
            {"key": "dark", "text": "Dark theme", "toggle": True, "on_click": toggle_theme},
        ])
        view["split"] = Splitter(fill=True, first_size="45%", min_first=160, min_second=160)
        with view["split"].first:
            view["editor"] = CodeEditor(height="100%", value=FIRST_TEXT, show_line_numbers=False, change_delay=TYPING_REST_MS,
                                        framed=False, on_change=show_text)
        with view["split"].second:
            view["text"] = MarkdownView(text=FIRST_TEXT, on_link_click=show_link)
        view["status"] = StatusBar(message="Ready", items=[{"key": "words", "text": words_of(FIRST_TEXT)}])


def words_of(text):
    return f"{len(text.split())} words"


def show_text(editor):
    text = editor.value
    view["text"].text = text
    view["status"].set_item_text("words", words_of(text))


def show_link(markdown_view, address):
    view["status"].set_message(f"Link: {address}", "info", 4000)


def toggle_theme(bar, item):
    view["theme"] = "dark" if item["checked"] else "light"
    view["page"].color = THEME_COLORS[view["theme"]]
    for name in ("tools", "split", "editor", "text", "status"):
        view[name].set_theme(view["theme"])


def open_document():
    path = open_file(file_types=("Markdown files (*.md)", "All files (*.*)"))
    if not path:
        return
    view["text"].load_file(path)
    view["editor"].value = view["text"].text
    view["path"] = path
    view["status"].set_message(path)
    view["status"].set_item_text("words", words_of(view["text"].text))


def save_document():
    path = view["path"] or save_file(file_name="report.md", file_types=("Markdown files (*.md)",))
    if not path:
        return
    with open(path, "w", encoding="utf-8") as file:
        file.write(view["editor"].value)
    view["path"] = path
    view["status"].set_message("Saved", "success", 3000)


if __name__ == "__main__":
    App(start, title="A small Markdown editor", size=(960, 640)).run()
