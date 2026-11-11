/* Bismillah */

/*

OzdenUI Website - Samples - v26.11 (2026-11-04)

The Python code of the page (shown, not run) and the pictures of the real windows.
NOTE: SAMPLES.counter is examples/counter.py (its picture is images/counter.png), SAMPLES.others is the code of
tools/shot_gauge.py (images/gauge.png) and SAMPLES.own the code of tools/shot_card.py and of the README (images/card.png):
change them together. The pictures are made by tools/make_images.py from the
real windows; it writes their sizes into js/image-sizes.js.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const SAMPLES = {};

SAMPLES.counter = [
    'from ozdenui import App, HGroup, Label, SmartButton, VGroup',
    '',
    '',
    'def start(page):',
    '    page.color = "#F4F5F7"',
    '    with VGroup(gap=16, padding=40):',
    '        Label(text="Counter", font_size=22, text_color="#5A6270")',
    '        count = Label(text="0", font_size=64, bold=True)',
    '        with HGroup(hug=True, gap=12):',
    '            SmartButton(text="−", width=64, height=44, on_click=lambda: change(count, -1))',
    '            SmartButton(text="+", width=64, height=44, tone="cyan", on_click=lambda: change(count, +1))',
    '',
    '',
    'def change(count, step):',
    '    count.text = str(int(count.text) + step)',
    '',
    '',
    'App(start, title="Counter", size=(400, 320)).run()',
].join("\n");

SAMPLES.dialogs = [
    'from ozdenui import Dialog, Toast',
    '',
    '',
    'def replace_file():',
    '    if Dialog.confirm("The old copy will be replaced.",',
    '                      title="Replace it?", confirm_text="Replace"):',
    '        write_the_new_copy()',
    '        Toast.success("Replaced.")',
    '',
    '',
    '# the text, or None when it is cancelled',
    'name = Dialog.prompt("A name for the folder:", value="Photos")',
    '',
    '# the text of the pressed button',
    'choice = Dialog.ask("Save the changes?",',
    '                    buttons=["Save", "Don\'t save", "Cancel"])',
].join("\n");

SAMPLES.others = [
    'from ozdenui import App, Component',
    '',
    '',
    'def start(page):',
    '    Component("Gauge", 20, 20, 180, 180,',
    '              value=72, sub_text="Disk")',
    '',
    '',
    'App(start, title="Disk", size=(220, 240),',
    '    components=["Gauge"]).run()',
].join("\n");

SAMPLES.own = [
    'from ozdenui import App, HGroup, Label, SmartButton, VGroup',
    '',
    'CARD_LOOK = dict(width=220, height="auto", align="left top",',
    '                 padding=16, gap=8, color="white", round=12)',
    '',
    '',
    'class Card:',
    '    """A card: a title, a text and a button."""',
    '',
    '    def __init__(self, title, text, on_open=None):',
    '        self.on_open = on_open',
    '        with VGroup(**CARD_LOOK) as self.box:',
    '            self.title = Label(text=title, font_size=18, bold=True)',
    '            Label(text=text, text_color="#5A6270")',
    '            SmartButton(text="Open", on_click=self.open)',
    '',
    '    def open(self):',
    '        if self.on_open:',
    '            self.on_open(self)',
    '',
    '    def set_title(self, title):',
    '        self.title.text = title',
    '',
    '',
    'def start(page):',
    '    page.color = "#F4F5F7"',
    '    with HGroup(gap=16, padding=24, wrap=True):',
    '        for name in ["Sales", "Stock", "Orders"]:',
    '            Card(name, "Updated today.",',
    '                 on_open=lambda card: card.set_title("Opened"))',
    '',
    '',
    'App(start, title="Cards", size=(760, 240)).run()',
].join("\n");

// One line for each component of the COMPONENTS section (the same order as the texts)
SAMPLES.componentLines = {
    SmartButton: 'SmartButton(text="Save", on_click=save)',
    TextField: 'TextField(title_text="Name", on_enter=fn)\nif email.check(): send()',
    TextAreaField: 'TextAreaField(title_text="Note")',
    "UrlField, PhoneField": 'UrlField(text="github.com")\nPhoneField(text=number)\nCurrencyField(value=1234.5)',
    SearchInput: 'SearchInput(on_change=find)',
    CheckBox: 'CheckBox(text="Remember me", checked=True)',
    Toggle: 'Toggle(value=True, on_change=fn)',
    RadioButton: 'RadioButton(group="size", value="M")',
    SelectBox: 'SelectBox(options=["Apple", "Pear"])',
    "Slider, RangeSlider": 'Slider(value=5, min_value=0, max_value=10)\nRangeSlider(low=2, high=8, max_value=10)\nSliderField(text="Size", value=5)',
    Stepper: 'Stepper(value=2, min_value=0, max_value=10)',
    DatePicker: 'DatePicker(on_change=fn)\nTimePicker(value="19:30")\nColorPicker(value="#3871E0")',
    FilePicker: 'FilePicker(multiple=True, on_change=fn)\npicker.paths',
    "ProgressBar, StepBar": 'bar.value = 40\nStepBar(steps=STEPS, step=1)',
    ItemList: 'ItemList(items=["Apple", "Pear"])\nItemList(items=PHOTOS, layout="grid", style_name="gallery")',
    SortableList: 'SortableList(items=["Sales", "Stock"], on_change=fn)\nlst.items',
    SmartTable: 'SmartTable(columns=COLUMNS, rows=ROWS)',
    TreeView: 'TreeView(items=NODES, on_select=fn)',
    Tabs: 'with tabs.panel("General"): ...',
    Accordion: 'with acc.section("More"): ...',
    GridGroup: 'with GridGroup(columns=3, gap=8): ...',
    GraphBox: 'GraphBox(type="bar", values=SALES,\n  format_value="{:,} TL")',
    LogView: 'log.capture_print()\nlog.error("It failed")',
    ImageView: 'view.set_image(figure)',
    Canvas: 'canvas.circle(100, 80, 30, fill="orange", draggable=True)',
    "MarkdownView, JsonView": 'view = MarkdownView(text="# A report")\nview.append_text("The next words")\nJsonView(value=answer)',
    JsonEditor: 'JsonEditor(value=rows, on_change=fn)\nJsonEditor.open(value=prefs, on_apply=fn)',
    ChatView: 'key = chat.add_message()\nchat.append_text(key, piece)',
    WebView: 'WebView(html=fig.to_html())\nWebView(url=address)',
    "MenuBar, ToolBar": 'MenuBar(menus=[{"text": "File", "items": ITEMS}])\nToolBar(items=[{"icon": "save", "on_click": save}])',
    "StatusBar, Splitter": 'bar.set_message("Saved", "success", 3000)\nwith split.first: ...',
    CodeEditor: 'CodeEditor(language="python", value=text)',
    "ContextMenu, Tooltip": 'ContextMenu(target=tree, items=ITEMS)\nTooltip(target=button, text="Saves it")',
    "Dialog, Toast": 'if Dialog.confirm("Delete it?"):\n    Toast.success("Deleted.")',
};

SAMPLES.dark = [
    'from ozdenui import App',
    '',
    '',
    'def start(page):',
    '    ...  # the same objects',
    '',
    '',
    'App(start, theme="dark").run()',
].join("\n");

SAMPLES.installPypi = 'pip install ozdenui';

SAMPLES.installSource = [
    'python3 -m venv .venv',
    'source .venv/bin/activate',
    'pip install --upgrade pip',
    'pip install path/to/ozdenui',
].join("\n");

SAMPLES.hello = [
    'from ozdenui import App, Label, VGroup',
    '',
    '',
    'def start(page):',
    '    with VGroup():',
    '        Label(text="Hello, window!", font_size=32)',
    '',
    '',
    'App(start, title="Hello").run()',
].join("\n");

SAMPLES.run = 'python app.py';
