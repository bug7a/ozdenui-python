# Bismillah
"""A to-do list: add a task (Enter or the button), tick the done ones, delete them (with a question).
The program is a class: the objects it changes later are its attributes (self.tasks), the events are its methods."""

import itertools

from ozdenui import App, Dialog, HGroup, ItemList, Label, SmartButton, TextField, VGroup

PAGE_COLOR = "#F4F5F7"
TEXT_SOFT = "#5A6270"
LIST_WIDTH = 440
FIRST_TASKS = ["Buy bread", "Call the bank", "Water the plants"]


class TodoApp:

    def __init__(self):
        self.next_number = itertools.count(1)

    def start(self, page):
        page.color = PAGE_COLOR
        with VGroup(gap=14, padding=36, align="left top"):
            Label(text="To do", font_size=24, bold=True)
            with HGroup(hug=True, gap=8, align="left bottom"):
                self.field = TextField(title_text="A new task", placeholder="Buy milk", width=LIST_WIDTH - 108, on_enter=self.add_task)
                SmartButton(text="Add", width=100, tone="cyan", on_click=self.add_task)
            self.tasks = ItemList(items=[self.new_item(title) for title in FIRST_TASKS], selection="multiple",
                                  width=LIST_WIDTH, height=300, empty_text="Nothing to do.", on_change=self.show_count)
            with HGroup(hug=True, gap=14, align="left center"):
                SmartButton(text="Delete the done ones", tone="orange", on_click=self.delete_done)
                self.count = Label(text="", font_size=14, text_color=TEXT_SOFT)
        self.show_count()

    def new_item(self, title):
        return {"key": f"t{next(self.next_number)}", "text": title}

    def add_task(self):
        title = self.field.text.strip()
        if not title:
            return
        self.tasks.add_item(self.new_item(title))
        self.field.text = ""
        self.show_count()

    def delete_done(self):
        done = list(self.tasks.selected_keys)
        if not done:
            Dialog.alert("Tick the done tasks first.", title="Nothing to delete")
            return
        if not Dialog.confirm(f"{len(done)} done task(s) will be deleted.", title="Delete them?", confirm_text="Delete",
                              danger=True):
            return
        for key in done:
            self.tasks.remove_item(key)
        self.show_count()

    def show_count(self):
        total = len(self.tasks.items)
        done = len(self.tasks.selected_keys)
        self.count.text = f"{total} tasks, {done} done"


if __name__ == "__main__":
    App(TodoApp().start, title="To do", size=(540, 560)).run()
