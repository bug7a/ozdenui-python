# Bismillah
"""ozdenui v0.1 (OzdenUI: basic.js for Python): a window whose objects are basic.js objects and components, written in
Python.

    from ozdenui import App, VGroup, Label, SmartButton

    def start(page):
        with VGroup(gap=16):
            count = Label(text="0", font_size=48)
            SmartButton(text="+1", on_click=lambda: count.set(text=str(int(count.text) + 1)))

    App(start, title="Counter", size=(400, 300)).run()

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

from .app import App, WindowClosed, after, call_soon, choose_folder, every, open_file, run_in_background, save_file
from .components import (Accordion, Canvas, ChatView, CheckBox, CodeEditor, ColorPicker, ContextMenu, CurrencyField, DataTable, DatePicker, Dialog, EmailField, FilePicker,
                         GraphBox, ImageView, ItemList, JsonEditor, JsonView, LoadingScreen, LogView, MarkdownView, MenuBar, NumberField, PasswordField, PhoneField,
                         ProgressBar, RadioButton, RangeSlider, ScrollArea, SearchInput, SelectBox, SidePanel, Slider, SliderField, SmartButton, SmartTable, SortableList,
                         Splitter, StatusBar, StepBar, Stepper, Tabs, TagInput, TextAreaField, TextField, TimePicker, Toast, Toggle, ToolBar,
                         Tooltip, TreeView, UrlField, WebView, picture_address)
from .objects import Box, Button, Component, GridGroup, HGroup, Icon, Input, Label, VGroup

__version__ = "0.1.0"
__all__ = [
    "App", "WindowClosed", "every", "after", "call_soon", "run_in_background", "open_file", "save_file", "choose_folder",
    "Box", "VGroup", "HGroup", "GridGroup", "ScrollArea", "Label", "Button", "Input", "Icon", "Component",
    "SmartButton", "CheckBox", "Toggle", "RadioButton", "SelectBox", "TextAreaField", "SliderField", "ProgressBar",
    "ItemList", "SmartTable", "Tabs", "Dialog", "Toast",
    "LogView", "ImageView", "MenuBar", "ToolBar", "StatusBar", "Splitter", "CodeEditor", "picture_address",
    "TextField", "EmailField", "PasswordField", "NumberField", "UrlField", "PhoneField", "CurrencyField", "Slider", "SearchInput", "GraphBox", "TreeView", "ContextMenu",
    "Tooltip", "DatePicker", "TimePicker", "ColorPicker", "Stepper", "FilePicker", "Accordion", "MarkdownView", "JsonView",
    "RangeSlider", "StepBar", "Canvas", "SidePanel", "LoadingScreen", "TagInput", "DataTable", "JsonEditor", "SortableList", "WebView", "ChatView",
]
