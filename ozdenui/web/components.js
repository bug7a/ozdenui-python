/* Bismillah */

/*

components.js - ozdenui v0.1 (OzdenUI: basic.js for Python)
Every component of comp/ for the loader of bridge.js.

name: [file, [the components it needs, loaded before it]]. "needs" also has the optional ones that turn a feature
on (Ex: SearchInput for the filter of a SmartTable). index.html already loads the components of the Python
classes; App(components=["TreeView"]) loads the others with what they need.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

window.__bpComponents = (function () {

    const LIST = {
        ScrollBar: ["basic/scroll-bar.min.js", []],
        Accordion: ["comp/accordion.js", ["ScrollBar"]],
        ActionButton: ["comp/action-button.js", []],
        ActionTabBar: ["comp/action-tab-bar.js", []],
        AppBar: ["comp/app-bar.js", ["SmartButton"]],
        Badge: ["comp/badge.js", []],
        BottomBar: ["comp/bottom-bar.js", ["Badge"]],
        Breadcrumbs: ["comp/breadcrumbs.js", []],
        Canvas: ["comp/canvas.js", []],
        ChatView: ["comp/chat-view.js", ["MarkdownView", "ScrollArea", "CodeEditor", "ScrollBar"]],
        CheckBox: ["comp/check-box.js", []],
        CodeEditor: ["comp/code-editor.js", []],
        ColorPicker: ["comp/color-picker.js", []],
        ContextMenu: ["comp/context-menu.js", []],
        CurrencyField: ["comp/currency-field.js", ["TextField"]],
        DataTable: ["comp/data-table.js", ["SearchInput", "ScrollBar"]],
        DatePicker: ["comp/date-picker.js", []],
        Dialog: ["comp/dialog.js", ["SmartButton", "TextField"]],
        EmailField: ["comp/email-field.js", ["TextField"]],
        FilePicker: ["comp/file-picker.js", []],
        Filters: ["comp/filters.js", ["SearchInput", "CheckBox", "ScrollBar"]],
        Form: ["comp/form.js", ["Tooltip", "ScrollBar"]],
        FullScreenSelect: ["comp/full-screen-select.js", ["SearchInput", "ScrollBar"]],
        Gauge: ["comp/gauge.js", []],
        GraphBox: ["comp/graph-box.js", []],
        GridGroup: ["comp/grid-group.js", []],
        HoldToConfirmButton: ["comp/hold-to-confirm-button.js", []],
        ImageView: ["comp/image-view.js", []],
        ItemList: ["comp/item-list.js", ["SearchInput", "ScrollBar"]],
        JsonEditor: ["comp/json-editor.js", ["ContextMenu", "SearchInput"]],
        JsonView: ["comp/json-view.js", ["TreeView", "ContextMenu"]],
        LabelEditor: ["comp/label-editor.js", ["SidePanel", "Stepper", "ColorPicker", "Tabs", "CheckBox", "ScrollBar"]],
        LeftMenu: ["comp/left-menu.js", ["ScrollBar"]],
        LineProgressBar: ["comp/line-progress-bar.js", ["Tooltip"]],
        LoadingScreen: ["comp/loading-screen.js", ["SmartButton"]],
        LogView: ["comp/log-view.js", ["ScrollBar"]],
        LoginPage: ["comp/login-page.js", ["UIEffects", "Tooltip", "TextField", "EmailField", "PasswordField", "Tabs", "SmartButton", "LoadingScreen"]],
        MarkdownView: ["comp/markdown-view.js", ["CodeEditor", "ScrollBar"]],
        MenuBar: ["comp/menu-bar.js", ["ContextMenu"]],
        MiniGraphBox: ["comp/mini-graph-box.js", []],
        Notice: ["comp/notice.js", []],
        NumberField: ["comp/number-field.js", ["TextField"]],
        NumericKeyboard: ["comp/numeric-keyboard.js", []],
        PageControl: ["comp/page-control.js", []],
        PageHeader: ["comp/page-header.js", []],
        PasswordField: ["comp/password-field.js", ["TextField", "Tooltip"]],
        PeriodBar: ["comp/period-bar.js", []],
        PhoneField: ["comp/phone-field.js", ["TextField"]],
        ProgressBar: ["comp/progress-bar.js", []],
        PropertyPanel: ["comp/property-panel.js", ["ContextMenu", "ScrollBar"]],
        RadioButton: ["comp/radio-button.js", []],
        RangeSlider: ["comp/range-slider.js", []],
        RichTextEditor: ["comp/rich-text-editor.js", ["ScrollBar"]],
        ScrollArea: ["comp/scroll-area.js", ["ScrollBar"]],
        ScrollingText: ["comp/scrolling-text.js", []],
        SearchInput: ["comp/search-input.js", []],
        SearchResults: ["comp/search-results.js", ["ScrollBar"]],
        SelectBox: ["comp/select-box.js", ["SearchInput", "ItemList", "ScrollBar"]],
        SettingsRow: ["comp/settings-row.js", ["Toggle"]],
        SidePanel: ["comp/side-panel.js", []],
        Slider: ["comp/slider.js", []],
        SliderField: ["comp/slider-field.js", []],
        SmartButton: ["comp/smart-button.js", ["Tooltip"]],
        SmartTable: ["comp/smart-table.js", ["Tooltip", "SearchInput", "ScrollBar", "ContextMenu"]],
        SortableList: ["comp/sortable-list.js", ["ScrollBar"]],
        SparkLineBox: ["comp/spark-line-box.js", []],
        Splitter: ["comp/splitter.js", []],
        StatusBar: ["comp/status-bar.js", []],
        StepBar: ["comp/step-bar.js", []],
        Stepper: ["comp/stepper.js", []],
        Tabs: ["comp/tabs.js", []],
        TagInput: ["comp/tag-input.js", []],
        TapEffect: ["comp/tap-effect.js", []],
        TextAreaField: ["comp/text-area-field.js", ["TextField", "ScrollBar"]],
        TextField: ["comp/text-field.js", ["Tooltip"]],
        TimeLine: ["comp/time-line.js", []],
        TimePicker: ["comp/time-picker.js", ["ScrollBar"]],
        TinySelect: ["comp/tiny-select.js", []],
        TinyTable: ["comp/tiny-table.js", ["ScrollingText", "ScrollBar"]],
        Toast: ["comp/toast.js", []],
        Toggle: ["comp/toggle.js", []],
        ToolBar: ["comp/tool-bar.js", ["Tooltip", "ContextMenu", "MenuBar"]],
        Tooltip: ["comp/tooltip.js", []],
        TreeView: ["comp/tree-view.js", ["ScrollBar"]],
        UIEffects: ["comp/ui-effects.js", []],
        UI: ["comp/ui-standards.js", []],
        UrlField: ["comp/url-field.js", ["TextField", "TinySelect"]],
        WebView: ["comp/web-view.js", []],
    };

    const components = {};
    Object.keys(LIST).forEach(function (name) {
        components[name] = { file: LIST[name][0], needs: LIST[name][1] };
    });
    return components;

})();
