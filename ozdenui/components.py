# Bismillah
"""components.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The components of basic.js (comp/) with a Python class: the first ones a small app needs.

Every param of a component works by its name in snake_case (label_text, style_name...). A callback param takes a
Python function, called with the values the component gives (on_change=lambda box: print(box.checked)).
The state of a component (checked, value, the selection...) is kept in Python: reading it needs no question.
Changing it in code (box.checked = True) does not call on_change, except where it is written.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import base64
import datetime
import io
import logging
import mimetypes
import dataclasses
import decimal
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter

from . import app as _app
from .objects import (_POSITION_NAMES, ACCENT_STYLE_NAME, DARK_STYLE_NAMES, BasicObject, Component, Part, TypedComponent, _listen_for_enter, _new_id,
                      _takes_minimal_look, _warn_about_unknown_names, minimal_style_name)
from .values import call_with_count, camel_case, picture_address, positional_count, snake_case as _snake_case, source_line, to_page

# WHY mostly no package here: a new page of the kit takes the default of each component (CLAUDE.md of the repository).
_OZDEN = "ozden"  # the search box
_FIELD_LOOK = "light"  # the fields of text: the look of the kit for a new page ("dark" in a dark window)
_FIELD_IS_RIGHT = 0  # the status of a TextField with no warning (1: empty but required, 2: not valid)
_LONG_FIELD_CHARS = 1000  # WHY: the defaults of the page (25, 30 letters) are for a form of a web site: a path, an API key does not fit
_LONGEST_EMAIL = 254
_CHILD_LISTS = ("items", "children")
_FILE_TYPE = re.compile(r"(\.\w+)+")
_DROP_WAIT_STEP_MS = 30
_DROP_WAIT_STEPS = 33  # WHY: the page and pywebview tell about a drop separately, in any order; about 1 s on a busy computer
_MAX_PREVIEW_BYTES = 1000000  # a picture chosen in the dialog goes to the page as a whole: only a small one gets a preview
_MAX_PREVIEWS = 20
_POPOVER_LOOK = {"color": "#FFFFFF", "textColor": "rgba(0, 0, 0, 0.85)", "border": 1, "borderColor": "rgba(0, 0, 0, 0.12)", "round": 10,
                 "padding": [16, 14], "contentGap": 10, "shadow": "0 10px 30px rgba(0, 0, 0, 0.12)"}
_POPOVER_DARK_LOOK = dict(_POPOVER_LOOK, color="#2A2A29", textColor="rgba(255, 255, 255, 0.86)",
                          borderColor="rgba(255, 255, 255, 0.14)", shadow="0 10px 30px rgba(0, 0, 0, 0.4)")
# WHY: the bubble of the kit is white with no line and no shadow, so on a white card only its text was seen
_BUBBLE_FRAME_KEYS = ("color", "textColor", "border", "borderColor", "shadow")


def _accent_tone(app):
    """The tone of tone="accent": the main action of the window."""
    if getattr(app, "accent", ""):
        return ACCENT_STYLE_NAME
    if getattr(app, "style", "") == "minimal":
        return "ink"
    return "cyan"


class SmartButton(TypedComponent):
    """A button: SmartButton(text="Save", tone="cyan", on_click=save). on_click(button).
    style_name: "ozden" (default), "ozden2", "ozden3", "ozden4", "pill", "outlined", "ozdenDark" ... "ozden4Dark"...
    tone: "cyan" (the main action), "orange" (a delete), "yellow", "green", "blue", "white", "ink" (the main action of
    App(style="minimal")); "cyanDark"... on a dark
    page; in a dark window (App(theme="dark")) tone="cyan" is already its dark tone.
    tone="accent": the main action of the window: the color of App(accent=...), "ink" in a minimal window without one,
    "cyan" in a usual window.
    icon: a data: address (picture_address() makes one from a file)."""

    _type = "SmartButton"
    _defaults = {"style_name": "ozden"}
    _aliases = {"text": "label_text", "icon": "icon_file"}
    _setters = {"text": "set_text", "label_text": "set_text", "icon": "set_icon", "icon_file": "set_icon",
                "enabled": "set_enabled", "waiting": "set_waiting", "tone": "set_tone"}
    _TONES_WITH_A_DARK_ONE = ("cyan", "orange", "yellow", "green", "blue", "ink", ACCENT_STYLE_NAME)

    def __init__(self, *position, **params):
        # WHY only without a look of its own: a page that names its template has chosen its colors too. "accent" is
        #      not a tone of the page: it always becomes one.
        has_own_look = "style_name" in params or "styleName" in params
        if "tone" in params and (not has_own_look or params["tone"] == "accent"):
            params["tone"] = self._tone_of_window(params["tone"])
        super().__init__(*position, **params)

    def _tone_of_window(self, tone):
        app = _app.current_app()
        if tone == "accent":
            tone = _accent_tone(app)
        is_dark = app.theme == "dark"
        return tone + "Dark" if is_dark and tone in self._TONES_WITH_A_DARK_ONE else tone

    def set_tone(self, tone):
        self._keep("tone", tone)
        return self.call("setTone", self._tone_of_window(tone))

    def set_text(self, text):
        self._keep("text", text)
        self._keep("labelText", text)
        return self.call("setLabelText", text)

    def set_icon(self, file):
        self._keep("icon", file)
        self._keep("iconFile", file)
        return self.call("setIcon", file)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def set_waiting(self, waiting):
        """A clock on the button (a job runs); it can not be clicked meanwhile."""
        self._keep("waiting", int(bool(waiting)))
        return self.call("setWaiting", int(bool(waiting)))

    def press(self):
        """Clicks the button from code (on_click runs)."""
        return self.call("press")


class CheckBox(TypedComponent):
    """CheckBox(text="Remember me", checked=True, on_change=fn). on_change(box): read box.checked.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern"."""

    _type = "CheckBox"
    _aliases = {"text": "label_text"}
    _state = {"checked": "checked"}
    _setters = {"checked": "set_checked", "text": "set_text", "label_text": "set_text", "enabled": "set_enabled"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"checked": 0, "enabled": 1}

    @property
    def checked(self):
        return bool(self._values.get("checked", 0))

    def set_checked(self, checked):
        self._keep("checked", int(bool(checked)))
        return self.call("setChecked", int(bool(checked)), 1)

    def set_text(self, text):
        self._keep("text", text)
        return self.call("setLabelText", text)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))


class Toggle(TypedComponent):
    """An on / off switch: Toggle(value=True, on_change=fn). on_change(toggle): read toggle.value.
    toggle.value = True in code does not call on_change, as in every component (the silent setValue(value, 1) of the kit).
    style_name: "modern" (default), "classic", "float", "round", "slim", "outline", "square", "tick", "badge", "label"."""

    _type = "Toggle"
    _data_params = ()  # WHY: its value is a switch: True goes as 1 (it compares value === 1)
    _state = {"value": "value"}
    _setters = {"value": "set_value"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"value": 0}

    @property
    def value(self):
        return bool(self._values.get("value", 0))

    def set_value(self, value):
        self._keep("value", int(bool(value)))
        return self.call("setValue", int(bool(value)), 1)


class RadioButton(TypedComponent):
    """One choice of a group: RadioButton(group="size", value="M", text="Medium", on_change=fn).
    on_change(radio) runs when it becomes checked. RadioButton.value_of("size") is the value of the checked one.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern". NOTE: the group names are shared by the whole page."""

    _type = "RadioButton"
    _aliases = {"text": "label_text"}
    _state = {"checked": "checked"}
    _setters = {"checked": "set_checked", "text": "set_text", "label_text": "set_text", "enabled": "set_enabled"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"checked": 0, "group": "default", "value": ""}

    def __init__(self, *position, **params):
        super().__init__(*position, **params)
        # WHY: two checked at the start: the page keeps the last one, Python kept both (value_of gave the first)
        self._state_changed()

    @property
    def checked(self):
        return bool(self._values.get("checked", 0))

    def set_checked(self, checked):
        self._keep("checked", int(bool(checked)))
        self._state_changed()
        return self.call("setChecked", int(bool(checked)), 1)

    def set_text(self, text):
        self._keep("text", text)
        return self.call("setLabelText", text)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def _group_members(self):
        group = self._values.get("group", "default")
        # WHY list(): a background job that made an object meanwhile stopped the loop ("dictionary changed size")
        return [obj for obj in list(self._app._objects.values())
                if isinstance(obj, RadioButton) and obj._values.get("group", "default") == group]

    def _state_changed(self):
        # WHY: the page unchecks the others of the group without telling: Python does the same
        if not self.checked:
            return
        for other in self._group_members():
            if other is not self:
                other._values["checked"] = 0

    @staticmethod
    def value_of(group):
        """The value of the checked radio of a group, or None."""
        for obj in list(_app.current_app()._objects.values()):
            is_member = isinstance(obj, RadioButton) and obj._values.get("group", "default") == group
            if is_member and obj.checked:
                return obj._values.get("value")
        return None


class SelectBox(TypedComponent):
    """A drop-down list: SelectBox(options=["Apple", "Pear"], value="Pear", on_change=fn).
    An option is a text or {"value", "label", "description", "icon_file"...}. on_change(box): read box.value
    (a list with multiple=True). style_name: "light" (default; its old name "classic"), "dark" (a dark page), "ozden", "ozdenDark"."""

    _type = "SelectBox"
    _state = {"value": "value"}
    _setters = {"value": "set_value", "options": "set_options", "enabled": "set_enabled", "placeholder": "set_placeholder"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"value": None, "options": []}

    # WHY refresh: the page keeps only a value that is in the options (else null), without a word
    def set_value(self, value):
        self._keep("value", value)
        return self._call_and_refresh("setValue", value, 1)

    def set_options(self, options):
        self._keep("options", options)
        return self._call_and_refresh("setOptions", options, 1)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def set_placeholder(self, text):
        self._keep("placeholder", text)
        return self.call("setPlaceholder", text)

    def open(self):
        return self.call("open")

    def close(self):
        return self.call("close")


class _Field(TypedComponent):
    """The common part of the fields with a title: field.text is the text on the page (field.value too, the name of the
    kit). on_change(field) runs at every change of the user, on_focus(field) and on_blur(field) when the cursor comes and
    goes."""

    _aliases = {"text": "value"}
    _state = {"text": "getValue()"}
    _setters = {"text": "set_text", "value": "set_text", "title_text": "set_title", "placeholder": "set_placeholder",
                "max_length": "set_max_length", "required": "set_required", "warning_text": "set_warning_text"}
    _sync_callbacks = ("on_change",)

    def __init__(self, *position, **params):
        super().__init__(*position, **params)
        self._values.setdefault("text", self._values.get("value", ""))

    @property
    def value(self):
        return self._values.get("text", "")

    def set_text(self, text):
        self._keep("text", text)
        return self.call("setValue", text)

    def set_title(self, text):
        self._keep("titleText", text)
        return self.call("setTitleText", text)

    def set_placeholder(self, text):
        self._keep("placeholder", text)
        return self.call("setPlaceholder", text)

    def set_max_length(self, count):
        """The most letters it takes."""
        self._keep("maxLength", count)
        return self.call("setMaxLength", count)

    def set_required(self, value):
        self._keep("required", int(bool(value)))
        return self.call("setRequired", int(bool(value)))

    def set_warning_text(self, text):
        self._keep("warningText", text)
        return self.call("setWarningText", text)

    def is_valid(self):
        """The value is right for this field (an e-mail, the rules of a password). A question to the page."""
        return bool(self.ask("isValid"))

    def check(self):
        """Shows the warning of an empty required field or a wrong value. True when there is none:
        if name.check() and email.check(): save(). A question to the page."""
        self.call("checkInputValue")
        return self.measure("status") == _FIELD_IS_RIGHT


class TextAreaField(_Field):
    """A text of more lines: TextAreaField(text="...", on_change=fn). area.text is the text on the page.
    on_change(area) runs at every change. title_text: a small title above it.
    style_name: as TextField."""

    _type = "TextAreaField"
    _defaults = {
        "style_name": _FIELD_LOOK,
        "title_text": "",
        "placeholder": "",
        "required": 0,
        "min_char_count": 0,
        "show_count": 0,
        "max_length": 100000,
        "warning_text": "",
    }


class TextField(_Field):
    """A text field with a title: TextField(title_text="Name", text="Ada", on_change=fn). field.text is the text on the
    page. on_change(field) runs at every change, on_enter(field) on Enter. required=True: field.check() shows the warning
    of an empty field and returns False (required_text: its text). max_length: the most letters. unit_text="kg": a unit
    at its end. description_text: a small text under it.
    style_name: "light" (default), "dark" (a dark page), "modern", "modernDark", "ozden", "ozdenDark"."""

    _type = "TextField"
    _defaults = {"style_name": _FIELD_LOOK, "title_text": "", "placeholder": "", "required": 0, "max_length": _LONG_FIELD_CHARS}
    _setters = dict(_Field._setters, on_enter="_set_on_enter")

    def __init__(self, *position, on_enter=None, **params):
        super().__init__(*position, **params)
        self._input = None
        if on_enter is not None:
            _listen_for_enter(self, on_enter)

    def _set_on_enter(self, handler):
        """field.on_enter = fn (None: no more). WHY: as a param of the page it was never called (the kit has none)."""
        _listen_for_enter(self, handler)
        return self

    def _input_part(self):
        if self._input is None:
            self._input = self.part("input")
        return self._input

    def focus(self):
        return self._input_part().call("focus")

    def select_text(self):
        return self._input_part().call("select")

    def set_description(self, text):
        self._keep("descriptionText", text)
        return self.call("setDescriptionText", text)

    def set_unit_text(self, text):
        self._keep("unitText", text)
        return self.call("setUnitText", text)


class EmailField(TextField):
    """A field for an e-mail address: EmailField(title_text="E-mail"). email.is_valid() and email.check() look at its form.
    style_name: as TextField."""

    _type = "EmailField"
    _defaults = {"style_name": _FIELD_LOOK, "title_text": "", "required": 0, "max_length": _LONGEST_EMAIL}


class PasswordField(TextField):
    """A password with a button that shows it: PasswordField(title_text="Password"). Its rules: min_length, must_use_number,
    must_use_letter, must_use_uppercase, must_use_lowercase, must_use_special_char; field.check() shows the one that is
    not kept (min_length_warning_text: its text). style_name: as TextField."""

    _type = "PasswordField"
    _defaults = {"style_name": _FIELD_LOOK, "title_text": "", "required": 0, "max_length": _LONG_FIELD_CHARS}

    def set_show_password(self, value):
        return self.call("setShowPassword", int(bool(value)))


class NumberField(TextField):
    """Only a number can be typed: NumberField(title_text="Count", value=3). field.value is a number, or None when the
    field is empty; field.text is what is written. allow_negative, allow_decimal (True by default), decimal_separator ("."
    or ","), max_decimal_digits (2). style_name: as TextField."""

    _type = "NumberField"
    _defaults = {"style_name": _FIELD_LOOK, "title_text": "", "placeholder": "", "required": 0}
    _setters = dict(TextField._setters, value="set_value")

    def __init__(self, *position, value=None, **params):
        if value is not None:
            params["text"] = self._text_of(value, params.get("decimal_separator", params.get("decimalSeparator", ".")))
        super().__init__(*position, **params)

    @staticmethod
    def _text_of(value, separator):
        return "" if value is None else str(value).replace(".", separator)

    @property
    def value(self):
        text = str(self._values.get("text", "")).replace(self._values.get("decimalSeparator", "."), ".")
        try:
            return int(text)
        except ValueError:
            pass
        try:
            return float(text)
        except ValueError:
            return None

    def set_value(self, value):
        return self.set_text(self._text_of(value, self._values.get("decimalSeparator", ".")))


# The protocols of a UrlField, as the kit lists them; Python chooses https:// (the kit: https://www.)
_URL_PROTOCOLS = ("http://", "https://", "http://www.", "https://www.")
_HTTPS = 1  # WHY: the address of a server or of an API has no "www." (api.example.com is not www.api.example.com)
_LONGEST_URL = 2048  # WHY: the default of the page (255) is for a form of a web site: an address with its query is longer


class UrlField(TextField):
    """A web address: UrlField(title_text="Site", text="https://github.com"). The protocol is chosen at its start
    (http://, https://, http://www., https://www.); field.text is the whole address with it ("" when nothing is written).
    A text without a protocol takes the chosen one (https:// by default). on_change(field) runs at every change, also of
    the protocol. field.is_valid() and field.check() look at its form (a name with a dot, a port, a path).
    style_name: as TextField."""

    _type = "UrlField"
    _defaults = {"style_name": _FIELD_LOOK, "title_text": "", "required": 0, "max_length": _LONGEST_URL}

    def __init__(self, *position, **params):
        select = {}
        for name in ("tiny_select_params", "tinySelectParams"):
            select.update({camel_case(str(key)): value for key, value in (params.pop(name, None) or {}).items()})
        if "list" not in select:
            select.setdefault("selectedIndex", _HTTPS)
        params["tiny_select_params"] = select
        object.__setattr__(self, "_protocols", [str(item.get("label", "")) for item in select.get("list", [])] or list(_URL_PROTOCOLS))
        object.__setattr__(self, "_first_protocol", select.get("selectedIndex", len(_URL_PROTOCOLS) - 1))
        super().__init__(*position, **params)
        self._values["text"] = self._with_protocol(str(self._values.get("text") or ""))

    def _protocol_of(self, text):
        """The protocol at the start of the text (the longest: "https://www." before "https://"), or None."""
        found = [protocol for protocol in self._protocols if protocol and text.startswith(protocol)]
        return max(found, key=len) if found else None

    def _with_protocol(self, text):
        """The address as the page gives it: a text without a protocol takes the one of the field now."""
        if not text or self._protocol_of(text):
            return text
        current = self._protocol_of(str(self._values.get("text") or ""))
        if current is None and 0 <= self._first_protocol < len(self._protocols):
            current = self._protocols[self._first_protocol]
        return (current or "") + text

    def set_text(self, text):
        text = "" if text is None else str(text)
        self._keep("text", self._with_protocol(text))
        return self._call_and_refresh("setValue", text)


_KIT_COUNTRY_CODE = "+90"
_KIT_PHONE_MASK = " (___) ___-____"


def _phone_digits(text, codes, mask):
    """The digits of a phone number for its mask, as the page takes a number given in code or pasted: the country code at
    its start goes; with too many digits, also "0090", the code without "+" and a leading 0."""
    starts = sorted((code for code in codes if code and text.startswith(code)), key=len, reverse=True)
    if starts:
        text = text[len(starts[0]):]
    digits = re.sub(r"[^0-9]", "", text)
    most = mask.count("_")
    code_digits = re.sub(r"[^0-9]", "", codes[-1] or "")
    if len(digits) > most and code_digits and digits.startswith("00" + code_digits):
        digits = digits[2 + len(code_digits):]
    if len(digits) > most and code_digits and digits.startswith(code_digits):
        digits = digits[len(code_digits):]
    if len(digits) > most and digits.startswith("0"):
        digits = digits[1:]
    return digits[:most]


def _phone_text(digits, code, mask):
    """The digits in the country code and the mask; "" with no digit (the page gives "" for the mask alone)."""
    if not digits:
        return ""
    rest = iter(digits)
    return "".join(next(rest, "_") if char == "_" else char for char in code + mask)


class PhoneField(TextField):
    """A phone number in its mask: PhoneField(title_text="Phone", country_code="+1", unit_text="US"). Only digits are
    typed: the country code and the marks of the mask (phone_mask=" (___) ___-____", a "_" for a digit) are written by
    the field, and a number given in code or pasted goes into it ("0555 123 45 67", "+90 555 123 45 67").
    field.text is the number in its mask ("" with no digit); field.is_valid(): every digit is written.
    set_country_code(code), set_phone_mask(mask) keep the digits. The kit's defaults: "+90", " (___) ___-____", "TR".
    style_name: as TextField."""

    _type = "PhoneField"
    _defaults = {"style_name": _FIELD_LOOK, "title_text": "", "required": 0}
    _setters = dict(TextField._setters, country_code="set_country_code", phone_mask="set_phone_mask")

    def __init__(self, *position, **params):
        super().__init__(*position, **params)
        self._values["text"] = self._masked(str(self._values.get("text") or ""), self._code())

    def _code(self):
        return str(self._values.get("countryCode", _KIT_COUNTRY_CODE))

    def _mask(self):
        return str(self._values.get("phoneMask", _KIT_PHONE_MASK))

    def _masked(self, text, *codes):
        return _phone_text(_phone_digits(text, list(codes) + [self._code()], self._mask()), self._code(), self._mask())

    def set_text(self, text):
        text = "" if text is None else str(text)
        self._keep("text", self._masked(text, self._code()))
        return self._call_and_refresh("setValue", text)

    def set_country_code(self, code):
        old_code = self._code()
        self._keep("countryCode", str(code))
        self._keep("text", self._masked(str(self._values.get("text") or ""), old_code))
        return self._call_and_refresh("setCountryCode", str(code))

    def set_phone_mask(self, mask):
        digits = _phone_digits(str(self._values.get("text") or ""), [self._code()], self._mask())
        self._keep("phoneMask", str(mask))
        self._keep("text", _phone_text(digits[:str(mask).count("_")], self._code(), str(mask)))
        return self._call_and_refresh("setPhoneMask", str(mask))


class CurrencyField(TextField):
    """An amount of money, written in groups of three: CurrencyField(title_text="Price", value=1234.5, unit_text="$")
    shows "1,234.5". field.value is a number (int or float; None when empty), field.text is what is written.
    allow_negative (True), allow_decimal (True), decimal_separator ("." or ","), group_separator (","),
    max_decimal_digits (2: more digits are cut, as the page does when they are typed). The kit's unit is "TL".
    style_name: as TextField."""

    _type = "CurrencyField"
    _defaults = {"style_name": _FIELD_LOOK, "title_text": "", "placeholder": "", "required": 0}
    _setters = dict(TextField._setters, value="set_value")

    def __init__(self, *position, value=None, **params):
        if value is not None:
            params["text"] = self._text_of(value, {camel_case(name): given for name, given in params.items()})
        super().__init__(*position, **params)

    @staticmethod
    def _text_of(value, values):
        """A number as the field writes it, in groups. A text goes as it is: the page writes it in groups.
        WHY Decimal: the text of a big float is "1e+20", and the page would keep only its digits."""
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        number = decimal.Decimal(str(value))
        if not number.is_finite():
            raise ValueError(f"CurrencyField: {value!r} is not an amount")
        text = format(number, "f")
        sign = "-" if text.startswith("-") and values.get("allowNegative", 1) else ""
        whole, _, fraction = text.lstrip("-").partition(".")
        digits = values.get("maxDecimalDigits", 2)
        if digits is not None and digits >= 0:
            fraction = fraction[:digits]
        group = str(values.get("groupSeparator", ","))
        text = sign + f"{int(whole):,}".replace(",", group)
        if fraction and values.get("allowDecimal", 1):
            text += str(values.get("decimalSeparator", ".")) + fraction
        return text

    @property
    def value(self):
        text = str(self._values.get("text", ""))
        group = str(self._values.get("groupSeparator", ","))
        if group:
            text = text.replace(group, "")
        text = text.replace(str(self._values.get("decimalSeparator", ".")), ".")
        try:
            return int(text)
        except ValueError:
            pass
        try:
            return float(text)
        except ValueError:
            return None

    def set_value(self, value):
        if isinstance(value, str):
            self._keep("text", value)
            return self._call_and_refresh("setValue", value)
        return self.set_text(self._text_of(value, self._values))


class SliderField(TypedComponent):
    """A number on a bar: SliderField(text="Size", value=3, min_value=0, max_value=10, step=1, on_change=fn).
    on_change(slider) runs while it is dragged, on_change_end(slider) when it is let go: read slider.value.
    set_range(min_value, max_value) changes both ends. style_name: "light" (default; its old name "classic"), "dark" (a
    dark page), "modern"."""

    _type = "SliderField"
    _aliases = {"text": "label_text"}
    _state = {"value": "value", "minValue": "minValue", "maxValue": "maxValue"}
    _setters = {"value": "set_value", "text": "set_text", "label_text": "set_text", "enabled": "set_enabled",
                "min_value": "set_min_value", "max_value": "set_max_value", "step": "set_step"}
    _sync_callbacks = ("on_change", "on_change_end")
    _state_defaults = {"value": 0, "minValue": 0, "maxValue": 10}

    def set_value(self, value):
        # WHY here too: the page keeps the value inside min_value..max_value (and on the step) without a word, so Python
        #     read 15 while the slider showed 10. The page sends its exact value back after the call.
        self._keep("value", _inside(value, self._values.get("minValue", 0), self._values.get("maxValue", 10)))
        return self._call_and_refresh("setValue", value, 1)

    def set_range(self, min_value, max_value):
        """The value stays inside the new ends (on_change is not called)."""
        self._keep("minValue", min_value)
        self._keep("maxValue", max(min_value, max_value))
        return self._call_and_refresh("setRange", min_value, max_value)

    def set_min_value(self, value):
        return self.set_range(value, max(value, self._values.get("maxValue", 10)))

    def set_max_value(self, value):
        return self.set_range(min(self._values.get("minValue", 0), value), value)

    def set_step(self, value):
        self._keep("step", value)
        return self._call_and_refresh("setStep", value)

    def set_text(self, text):
        self._keep("text", text)
        return self.call("setLabelText", text)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))


def _inside(value, low, high):
    return min(max(value, low), high)


class Slider(TypedComponent):
    """A number on a thin bar: Slider(value=30, min_value=0, max_value=100, step=1, width=280, on_change_end=fn).
    on_change(slider) runs while it is dragged, on_change_end(slider) when it is let go (a key and a click on the bar too),
    on_change_start(slider) when it is taken: read slider.value. Its title and its number are yours (SliderField has
    them inside). style_name: "round" (default), "roundDark" (a dark page), "split", "splitDark" (split on a dark page)."""

    _type = "Slider"
    _defaults = {"style_name": "round"}
    _state = {"value": "value"}
    _setters = {"value": "set_value", "min_value": "set_min_value", "max_value": "set_max_value", "step": "set_step"}
    # WHY only the end: a move of the mouse is a call to Python; a key and a click are short drags, so they end too.
    _sync_callbacks = ("on_change_end",)
    _state_defaults = {"value": 0, "minValue": 0, "maxValue": 100}

    def set_value(self, value):
        # WHY here too: the page keeps the value inside min_value..max_value and on the step, without a word.
        self._keep("value", _inside(value, self._values.get("minValue", 0), self._values.get("maxValue", 100)))
        return self._call_and_refresh("setValue", value)

    def set_min_value(self, value):
        self._keep("minValue", value)
        return self._call_and_refresh("setMinValue", value)

    def set_max_value(self, value):
        self._keep("maxValue", value)
        return self._call_and_refresh("setMaxValue", value)

    def set_step(self, value):
        self._keep("step", value)
        return self._call_and_refresh("setStep", value)


class SearchInput(TypedComponent):
    """A search box: SearchInput(placeholder="Search", on_change=fn). on_change(box) runs at every change (typed, pasted,
    cleared), on_enter(box) on Enter and after the clear icon: read box.text. show_clear_icon=False: no clear icon.
    style_name: "ozden" (default), "ozdenDark" (a dark page), "light", "original"."""

    _type = "SearchInput"
    _defaults = {"style_name": _OZDEN, "shrink": 0}  # WHY shrink: as in MenuBar
    _state = {"text": "getValue()"}
    _setters = {"text": "set_text", "placeholder": "set_placeholder"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"text": ""}

    def __init__(self, *position, text="", **params):
        super().__init__(*position, **params)
        if text:
            self.set_text(text)

    def set_text(self, text):
        """Fills the box (on_change is not called)."""
        self._keep("text", text)
        return self.call("setValue", text, 1)

    def clear(self):
        return self.set_text("")

    def set_placeholder(self, text):
        self._keep("placeholder", text)
        return self.call("setPlaceholder", text)

    def focus(self):
        return self.call("focus")


class ProgressBar(TypedComponent):
    """The progress of a job: bar = ProgressBar(title_text="Copying", max_value=100); bar.value = 40.
    It may be changed from a background job (run_in_background). status: "normal", "success", "error".
    on_complete(bar) runs once when the value reaches max_value. style_name: "light" (default), "dark" (a dark page),
    "ozden", "modern"; style={"bar": {"color": "..."}} changes the color of the bar."""

    _type = "ProgressBar"
    _state = {"value": "value"}
    _setters = {"value": "set_value", "title_text": "set_title", "status": "set_status",
                "indeterminate": "set_indeterminate", "max_value": "set_max_value"}
    _state_defaults = {"value": 0, "maxValue": 100}

    def set_value(self, value):
        # WHY here too: the bar keeps its value inside 0..max_value (a value of 150 read 150 in Python)
        self._keep("value", _inside(value, 0, self._values.get("maxValue", 100)))
        return self._call_and_refresh("setValue", value)

    def add_value(self, step=1):
        self._keep("value", _inside(self._values.get("value", 0) + step, 0, self._values.get("maxValue", 100)))
        return self._call_and_refresh("addValue", step)

    def set_title(self, text):
        self._keep("titleText", text)
        return self.call("setTitleText", text)

    def set_status(self, status):
        self._keep("status", status)
        return self.call("setStatus", status)

    def set_indeterminate(self, indeterminate):
        """A moving bar for a job whose length is not known."""
        self._keep("indeterminate", int(bool(indeterminate)))
        return self.call("setIndeterminate", int(bool(indeterminate)))

    def set_max_value(self, value):
        # WHY the value too: the page keeps its value inside 0..max_value (a value of 80 read 80 after set_max_value(50))
        self._keep("maxValue", value)
        self._keep("value", _inside(self._values.get("value", 0), 0, value))
        return self._call_and_refresh("setMaxValue", value)


# *** THE ITEMS OF A LIST: an item of an ItemList, a node of a TreeView, a step, a section, a tab, a part, a tool.
# A class of a list names the keys of its items as the kit does (_item_keys; tests/test_kit_names.py compares them with
# the files of the kit) and the keys that hold more items of the same kind (_nested_item_keys).
_warned_items = set()  # (the class, the line of the program, the keys) already told in the terminal


def _check_items(cls, items):
    """Tells once in the terminal, at the line of the program, about an item with no "text" that has keys its list does not
    know: ItemList(items=[{"key": "p", "title": "Pear"}]) was an empty row, with no word.
    WHY only with no text: a key of your own on an item with a text is yours to keep (lst.selected gives it back), and an
    item with only known keys and no text is on purpose (a picture on a tile, an icon on a tool)."""
    for item in items or ():
        if not isinstance(item, dict):
            continue
        if "text" not in item:
            unknown = tuple(sorted(str(key) for key in item if camel_case(str(key)) not in cls._item_keys))
            if unknown:
                _warn_about_item(cls, unknown)
        for name in getattr(cls, "_nested_item_keys", ()):
            if isinstance(item.get(name), (list, tuple)):
                _check_items(cls, item[name])


def _warn_about_item(cls, unknown):
    place = source_line()
    told = (cls.__name__, place, unknown)
    if told in _warned_items:
        return
    _warned_items.add(told)
    names = ", ".join(f'"{key}"' for key in unknown)
    verb = "is not a key" if len(unknown) == 1 else "are not keys"
    keys = ", ".join(_snake_case(key) for key in cls._item_keys)
    print(f'ozdenui: {place}: {cls.__name__}: an item has no "text"; {names} {verb} of its items ({keys})', file=sys.stderr)


def _list_for_page(cls, items):
    """The items of a list as the page names their keys (icon_file -> iconFile, also inside), after the check."""
    _check_items(cls, items)
    return [_item_for_page(item) for item in items]


class ItemList(TypedComponent):
    """A list to choose from: ItemList(items=["Apple", {"key": "p", "text": "Pear", "description": "Green"}], on_change=fn).
    An item: a text or {"key", "text", "description", "icon_file", "search_text", "enabled"}; enabled=False: it can not be
    chosen. Every item gets a key: a text "Apple" becomes {"key": "0", "text": "Apple"} (its index), as the page names it.
    selection: "single" (default), "multiple", "none". on_change(lst, selected_items);
    on_item_click(lst, item, index). lst.items, lst.selected_keys and lst.selected are kept in Python.
    style_name: "ozden" (default, a gray list), "ozdenDark" (a dark page), "light" (a white box, flat rows), "dark".
    Another ground: style={"box": {"color": "white"}}.
    Pictures: ItemList(layout="grid", style_name="gallery" (a dark window takes "galleryDark"), items=[{"text": "Sea",
    "icon_file": "sea.jpg"}]): a big photo on every tile. icon_file takes a path, bytes, a Pillow image or an address.
    An item with no text and a key the list does not know ("title") is told in the terminal."""

    _type = "ItemList"
    _state = {"selectedKeys": "getSelectedKeys()", "selected": "getSelected()"}
    _setters = {"items": "set_items", "selected_keys": "set_selected", "enabled": "set_enabled"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"selectedKeys": [], "selected": [], "items": []}
    _item_keys = ("key", "text", "description", "iconFile", "searchText", "enabled", "type")  # type: "section", a title row

    def __init__(self, *position, **params):
        if "items" in params:
            _check_items(type(self), params["items"])
            params["items"] = _items_with_keys(params["items"])
        super().__init__(*position, **params)
        # WHY: lst.selected was [] (and lst.selected_keys as given) until the first event, though the page showed them
        self._keep_selection(self._start_keys(self._values.get("selectedKeys", [])))

    def _start_keys(self, keys):
        """The keys selected at the start as the page keeps them: of an item (not of a title row), each once; "single":
        the last one, "none": none."""
        items = {item["key"]: item for item in self._values.get("items", [])}
        known = []
        for key in map(str, keys):
            if key in items and items[key].get("type") != "section" and key not in known:
                known.append(key)
        selection = self._values.get("selection", "single")
        if selection == "none":
            return []
        return known[-1:] if selection == "single" else known

    def set_items(self, items):
        _check_items(type(self), items)
        keyed = _items_with_keys(items)
        self._keep("items", keyed)
        keys = _keys_of(keyed)
        self._keep_selection([key for key in self._values.get("selectedKeys", []) if key in keys])
        return self._call_and_refresh("setItems", keyed)

    def add_item(self, item, index=-1):
        """Adds an item (at index; -1: at the end). A key that is in the list already is an error."""
        _check_items(type(self), [item])
        items = list(self._values.get("items", []))
        entry = _item_with_key(item, _free_key(items))
        if entry["key"] in _keys_of(items):
            raise ValueError(f"ItemList.add_item(): there is an item with the key {entry['key']!r} already")
        position = len(items) if index < 0 else min(index, len(items))
        items.insert(position, entry)
        self._keep("items", items)
        return self.call("addItem", entry, index)

    def remove_item(self, key):
        key = str(key)
        self._keep("items", [item for item in self._values.get("items", []) if item["key"] != key])
        self._keep_selection([selected for selected in self._values.get("selectedKeys", []) if selected != key])
        return self._call_and_refresh("removeItem", key, 1)

    def set_selected(self, keys):
        self._keep_selection([str(key) for key in keys])
        return self._call_and_refresh("setSelected", [str(key) for key in keys], 1)

    def select(self, key):
        keys = [str(key)] if self._values.get("selection", "single") == "single" else self.selected_keys + [str(key)]
        self._keep_selection(list(dict.fromkeys(keys)))  # WHY: a key selected again was kept twice (the page keeps it once)
        return self._call_and_refresh("select", str(key), 1)

    def clear_selection(self):
        self._keep_selection([])
        return self.call("clearSelection", 1)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def scroll_to_item(self, key):
        return self.call("scrollToItem", str(key))

    def _keep_selection(self, keys):
        items = {item["key"]: item for item in self._values.get("items", [])}
        self._keep("selectedKeys", [key for key in keys if key in items])
        self._keep("selected", [items[key] for key in keys if key in items])


# The Python names of the keys of an item, and their names on the page.
_ITEM_KEYS = {"icon_file": "iconFile", "search_text": "searchText"}


def _item_with_key(item, free_key):
    """An item of an ItemList with a key: {"key": "3", "text": "Apple"} for a text, its own key as a text.
    icon_file: a path, bytes, a Pillow image or an address (picture_address()); iconFile goes to the page as it is."""
    if not isinstance(item, dict):
        return {"key": free_key, "text": str(item)}
    entry = {_ITEM_KEYS.get(name, name): value for name, value in item.items()}
    if "icon_file" in item:
        entry["iconFile"] = picture_address(item["icon_file"])
    if entry.get("key") is None:
        entry["key"] = free_key
    entry["key"] = str(entry["key"])
    return entry


def _items_with_keys(items):
    """The items with a key each, the way the page names them (its index for one without a key).
    WHY in Python: the keys Python guessed after add_item and remove_item were not the ones of the page."""
    keyed = [_item_with_key(item, str(index)) for index, item in enumerate(items)]
    counts = Counter(item["key"] for item in keyed)
    doubles = sorted(key for key, count in counts.items() if count > 1)
    if doubles:
        raise ValueError(f"ItemList: two items have the same key: {', '.join(doubles)}")
    return keyed


def _keys_of(items):
    return {item["key"] for item in items}


def _free_key(items):
    """The first index (as a text) that no item has as its key."""
    keys = _keys_of(items)
    number = len(items)
    while str(number) in keys:
        number += 1
    return str(number)


# The events of a SortableList: the page gives its own copy of an item, Python gives yours.
_SORTABLE_EVENTS = ("on_change", "on_remove", "on_item_click", "on_drag_start", "on_drag_end")
_SORTABLE_PASSED_EVENTS = ("on_item_click", "on_drag_start", "on_drag_end")  # sent to the page only when given


def _sortable_text_of(item):
    """The text of an item as the page shows it: a dict's "text", else its "key"; any other item as it is written."""
    if not isinstance(item, dict):
        return str(item)
    for name in ("text", "key"):
        if item.get(name) is not None:
            return str(item[name])
    return ""


def _sortable_key_of(item):
    """The key of an item as the kit names it: a dict's "key", else its text (a text is its own key)."""
    if isinstance(item, dict) and item.get("key") is not None:
        return str(item["key"])
    return _sortable_text_of(item)


def _sortable_item_for_page(item, page_key):
    """An item as the page takes it, with the key Python gave it (yours stays in Python)."""
    page_item = {"key": page_key, "text": _sortable_text_of(item)}
    if isinstance(item, dict):
        if item.get("description") is not None:
            page_item["description"] = str(item["description"])
        if item.get("locked"):
            page_item["locked"] = 1
    return page_item


class SortableList(TypedComponent):
    """A list whose order the user changes: SortableList(items=["Sales", "Stock", {"key": "home", "text": "Home",
    "description": "The first page", "locked": True}], on_change=fn). The grip at the left drags a row (drag_by="row":
    the whole row); with the keys: the arrows move the focus, Space grabs and drops a row, Alt + an arrow moves it at once.
    lst.items: your items (the same texts and dicts) in the order on the page; lst.keys: their keys (a dict's "key", else
    its text). on_change(lst, item, from_index, to_index) after a move of the user. removable=True: an x button and the
    Delete key, on_remove(lst, item, index). on_item_click(lst, item, index), on_drag_start(lst, item, index),
    on_drag_end(lst, item, index). An item: a text or {"key", "text", "description", "locked"}; locked=True: it does not
    move, and the user can not move a row past it. show_buttons=True: up / down buttons; show_numbers=False: no numbers;
    height="auto": it grows with its rows. In code: move_item(from_index, to_index), add_item(item, index=-1),
    remove_item(index), set_items(items), index_of(key), focus_item(index), set_enabled(); they do not call on_change or
    on_remove. style_name: "light" (default), "dark" (a dark page), "modern".
    NOTE: create_item_view takes a function of the page, not a Python function: the page draws a row at once."""

    _type = "SortableList"
    _setters = {"items": "set_items", "enabled": "set_enabled"}
    _state = {"order": "getKeys()"}  # the keys Python gave, in the order on the page
    _item_keys = ("key", "text", "description", "locked")

    def __init__(self, *position, **params):
        view_maker = params.get("create_item_view", params.get("createItemView"))
        if callable(view_maker):
            raise TypeError("SortableList(create_item_view=...) can not be a Python function: the page draws a row at once, "
                            "and a Python function answers later. Give the items a text and a description")
        object.__setattr__(self, "_item_of_key", {})  # the key Python gave -> your item
        object.__setattr__(self, "_next_key_number", 0)
        object.__setattr__(self, "_handler_of", {})  # on_change... -> your function
        object.__setattr__(self, "_waited_states", 0)  # the calls whose state the page has not sent back yet
        for name in list(params):
            if _snake_case(name) in _SORTABLE_EVENTS:
                self._handler_of[_snake_case(name)] = params.pop(name)
        items = list(params.pop("items", []))
        _check_items(type(self), items)
        page_items = [self._keep_item(item) for item in items]
        params["items"] = page_items
        # WHY always: the page sends its order with them, and a removed item must leave Python too
        params["on_change"] = self._changed
        params["on_remove"] = self._removed
        for name in _SORTABLE_PASSED_EVENTS:
            if self._handler_of.get(name):
                params[name] = self._passer_of(name)
        super().__init__(*position, **params)
        self._keep("order", [page_item["key"] for page_item in page_items])

    def _prepare_params(self, params):
        if isinstance(params.get("texts"), dict):
            # WHY: the keys of the kit are camelCase (moveUp); in Python they are written as names are (move_up)
            params["texts"] = {camel_case(str(key)): text for key, text in params["texts"].items()}
        super()._prepare_params(params)

    # *** YOUR ITEMS:

    def _keep_item(self, item):
        """Your item kept in Python under a key of its own; the item as the page takes it.
        WHY a key of Python: two items may have the same text (or key), and Python must know which one moved."""
        page_key = f"i{self._next_key_number}"
        object.__setattr__(self, "_next_key_number", self._next_key_number + 1)
        self._item_of_key[page_key] = item
        return _sortable_item_for_page(item, page_key)

    def _order(self):
        """The keys of Python in the order on the page."""
        return [key for key in self._values.get("order", []) if key in self._item_of_key]

    @property
    def items(self):
        """Your items (the same texts and dicts) in the order on the page."""
        return [self._item_of_key[key] for key in self._order()]

    @property
    def keys(self):
        """The keys of the items in their order: a dict's "key", else its text."""
        return [_sortable_key_of(item) for item in self.items]

    def index_of(self, key):
        """The place of the item with this key (or text), or -1."""
        keys = self.keys
        return keys.index(str(key)) if str(key) in keys else -1

    # *** EVENTS:

    def set(self, **props):
        for name in list(props):
            if _snake_case(name) in _SORTABLE_EVENTS:
                self._set_handler(_snake_case(name), props.pop(name))
        return super().set(**props)

    def _set_handler(self, name, handler):
        """lst.on_item_click = fn: the function is kept in Python; the page is told only when it did not call Python."""
        had_one = self._handler_of.get(name)
        self._handler_of[name] = handler
        if name in _SORTABLE_PASSED_EVENTS and handler and not had_one:
            super().set(**{name: self._passer_of(name)})

    def _item_of_page(self, page_item):
        return self._item_of_key.get(page_item.get("key")) if isinstance(page_item, dict) else None

    def _tell(self, name, item, *values):
        handler = self._handler_of.get(name)
        if handler:
            call_with_count(handler, positional_count(handler), [self, item, *values])

    def _changed(self, _lst, page_item, from_index, to_index):
        self._tell("on_change", self._item_of_page(page_item), from_index, to_index)

    def _removed(self, _lst, page_item, index):
        key = page_item.get("key") if isinstance(page_item, dict) else None
        self._tell("on_remove", self._item_of_key.pop(key, None), index)

    def _passer_of(self, name):
        def pass_on(_lst, page_item, index):
            self._tell(name, self._item_of_page(page_item), index)

        return pass_on

    def _receive(self, event_name, data):
        super()._receive(event_name, data)
        if event_name != "__state":
            return
        object.__setattr__(self, "_waited_states", max(0, self._waited_states - 1))
        if self._waited_states:
            return
        # WHY here: the order the page sends after the last call of Python is the truth (the page skips a change while
        #     the user drags a row): the items that are not on the page any more are forgotten.
        shown = set(self._values.get("order", []))
        for key in [key for key in self._item_of_key if key not in shown]:
            del self._item_of_key[key]

    def _change_and_refresh(self, method, *args):
        object.__setattr__(self, "_waited_states", self._waited_states + 1)
        return self._call_and_refresh(method, *args)

    # *** CHANGES IN CODE (on_change and on_remove are not called):

    def set_items(self, items):
        items = list(items)
        _check_items(type(self), items)
        page_items = [self._keep_item(item) for item in items]
        self._keep("order", [page_item["key"] for page_item in page_items])
        return self._change_and_refresh("setItems", page_items)

    def move_item(self, from_index, to_index):
        """Moves the item at from_index to to_index (an index past the end: the last place). A locked item does not move.
        True when it moved."""
        order = self._order()
        if not 0 <= from_index < len(order):
            return False
        to_index = max(0, min(int(to_index), len(order) - 1))
        item = self._item_of_key[order[from_index]]
        if from_index == to_index or (isinstance(item, dict) and item.get("locked")):
            return False
        order.insert(to_index, order.pop(from_index))
        self._keep("order", order)
        self._change_and_refresh("moveItem", from_index, to_index, 1)
        return True

    def add_item(self, item, index=-1):
        """Adds an item at index (-1: at the end)."""
        _check_items(type(self), [item])
        page_item = self._keep_item(item)
        order = self._order()
        at = len(order) if index < 0 or index > len(order) else index
        order.insert(at, page_item["key"])
        self._keep("order", order)
        return self._change_and_refresh("addItem", page_item, at)

    def remove_item(self, index):
        """Removes the item at index; returns it (None: there is none)."""
        order = self._order()
        if not 0 <= index < len(order):
            return None
        item = self._item_of_key[order.pop(index)]
        self._keep("order", order)
        self._change_and_refresh("removeItem", index, 1)
        return item

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def focus_item(self, index=0):
        """The keyboard focus on a row."""
        return self.call("focusItem", index)


class SmartTable(TypedComponent):
    """A table for data of any size: only the rows that are seen are made, so very many rows stay fast. It has a filter
    box, sorting on its titles and the keys of a list (arrows, Page Up / Down, Home, End, Enter).

    SmartTable(columns=[{"key": "name", "title": "Name", "width": 200}], rows=[{"name": "Ada"}], height=300)
    A column: key, title (the key by default), width (px), type ("string", "integer", "boolean"), sortable (True).
    A row: a dict by the keys of the columns, or a list in the order of the columns. The values are shown as text:
    format them in Python. on_select(table, row): a click, or Enter on a row (row: the dict). table.rows is kept in
    Python; table.selected_row asks the page which row is selected now (the arrow keys move it without an event).
    height: a number or "100%": the rows fill it; none: as high as line_count rows. width: "100%" by default.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page), "green"."""

    _type = "SmartTable"
    _setters = {"rows": "set_rows", "item_data_list": "set_rows"}  # WHY the name of the kit too: table.rows stays right
    _state_defaults = {"rows": []}
    _DEFAULT_LINE_COUNT = 10

    def __init__(self, *position, columns=(), rows=(), on_select=None, line_count=_DEFAULT_LINE_COUNT, **params):
        params = dict(zip(_POSITION_NAMES, position), **params)
        # WHY in the style: the size of a SmartTable is read from its style, not from the box.
        style = dict(params.get("style") or {})
        style.setdefault("width", params.pop("width", "100%"))
        height = params.pop("height", None)
        style.setdefault("height", "auto" if height is None else height)
        params["style"] = style
        params["fit_line_count"] = params.get("fit_line_count", int(height is not None))
        params["item_line_count"] = line_count
        object.__setattr__(self, "_column_keys", [column["key"] for column in columns])
        params["title_data_list"] = [_title_of_column(column) for column in columns]
        table_rows = self._rows_as_dicts(rows)
        params["item_data_list"] = table_rows
        if on_select is not None:
            params["on_select"] = self._page_select_handler(on_select)
        super().__init__(**params)
        self._keep("rows", table_rows)

    def _page_select_handler(self, handler):
        """WHY: the page gives the table of the page and the row; the function gets this object and the row."""
        count = positional_count(handler)

        def on_page_select(_table, row):
            call_with_count(handler, count, [self, row])

        return on_page_select

    def _rows_as_dicts(self, rows):
        return [row if isinstance(row, dict) else dict(zip(self._column_keys, row)) for row in rows]

    @property
    def selected_row(self):
        return self.measure("selected_item_data")

    def set_rows(self, rows):
        table_rows = self._rows_as_dicts(rows)
        self._keep("rows", table_rows)
        return self.call("setItemDataList", table_rows)

    def add_row(self, row):
        """One more row. NOTE: all the rows go to the page again: a big table takes set_rows() for many rows."""
        return self.set_rows(list(self.rows) + [row])

    def remove_row(self, row):
        """Removes the first row with these values."""
        rows = list(self.rows)
        rows.remove(self._rows_as_dicts([row])[0])
        return self.set_rows(rows)

    def clear_rows(self):
        return self.set_rows([])

    def select_row(self, index):
        """Selects a row by its place in table.rows and shows it. WHY by its place: the page compares the objects."""
        return self._app.evaluate(f"{self.js}.selectItem({self.js}.itemDataList[{int(index)}])")

    def clear_selection(self):
        return self.call("clearSelection")

    def sort_by(self, key, direction="asc"):
        """direction: "asc" or "desc"."""
        self.set(sort_by_title_index=self._column_keys.index(key), sort_direction="A-Z" if direction == "asc" else "Z-A")
        self.call("filterAndSortData")
        return self.call("updateSortIcon")

    def search(self, text):
        """Fills the filter box."""
        self.set(search_keyword=text)
        if getattr(self, "_search_box", None) is None:
            object.__setattr__(self, "_search_box", self.part("searchInput"))
        self._search_box.call("setValue", text, 1)  # WHY silent: the table was filtered above
        return self.call("filterAndSortData")


def _title_of_column(column):
    """A column as SmartTable names it."""
    title = {"dataTitle": column["key"], "name": column.get("title", column["key"]), "dataType": column.get("type", "string")}
    if "width" in column:
        title["width"] = column["width"]
    title["sortable"] = int(bool(column.get("sortable", True)))
    return title


class Tabs(TypedComponent):
    """Pages in one window: tabs = Tabs(tabs=["Orders", "Customers"]); with tabs.panel("Orders"): Label(...)
    A tab is a text or {"key", "text", "icon_file", "count", "badge", "disabled"}. on_change(tabs): read
    tabs.value (the key of the open tab). panels=False makes only the bar. variant: "underline" or "pill".
    set_tabs([...]) (tabs.tabs = [...]): new tabs; their pages are made again. set_count(key, 3): the number of a tab.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern"."""

    _type = "Tabs"
    _defaults = {"width": "100%", "panels": 1}
    _state = {"value": "value", "previousValue": "previousValue"}
    _setters = {"value": "set_value", "tabs": "set_tabs"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"previousValue": None}
    _item_keys = ("key", "text", "iconFile", "count", "badge", "disabled", "closable", "selectedColor", "selectedTextColor",
                  "selectedIconFile", "ariaLabel")

    def __init__(self, *position, **params):
        if "tabs" in params:
            params["tabs"] = [_tab_for_page(tab) for tab in _list_for_page(type(self), params["tabs"])]
        super().__init__(*position, **params)
        object.__setattr__(self, "_panels", {})
        tabs = params.get("tabs", [])
        first = tabs[0] if tabs else None
        first_key = first.get("key", first.get("text")) if isinstance(first, dict) else first
        self._values.setdefault("value", params.get("value", first_key))

    def panel(self, key):
        """The page of a tab, to put objects into: with tabs.panel("Orders"): Label(...)"""
        if key not in self._panels:
            # WHY setPanelContent once: it makes the box of the content (panel.wrapper); a second call clears it
            self.call("setPanelContent", key, {"__bpNoop": 1})
            self._panels[key] = self.part({"call": "getPanel", "args": [key]}, "wrapper")
        return self._panels[key]

    def set_value(self, key):
        self._keep("previousValue", self._values.get("value"))
        self._keep("value", key)
        return self.call("setValue", key, 1)

    def set_tabs(self, tabs):
        """New tabs in the place of all of them: their pages go with the old tabs (tabs.panel(key) makes the new ones).
        The open tab stays open when it is still there; on_change is not called."""
        page_tabs = [_tab_for_page(tab) for tab in _list_for_page(type(self), tabs)]
        self._keep("tabs", page_tabs)
        self._panels.clear()  # WHY: the page removed them with the old tabs
        return self._call_and_refresh("setTabs", page_tabs, 1)

    def set_count(self, key, count):
        return self.call("setCount", key, count)


def _tab_for_page(tab):
    """A tab with its pictures as addresses: a path, bytes or a Pillow image, as in an ItemList."""
    if not isinstance(tab, dict):
        return tab
    pictures = {name: picture_address(tab[name]) for name in ("iconFile", "selectedIconFile") if tab.get(name)}
    return dict(tab, **pictures)


class _ThemedComponent(TypedComponent):
    """The components that change their look while they are on the page: comp.theme = "dark" or comp.set_theme("dark").
    What they show stays."""

    _aliases = {"theme": "style_name"}
    _setters = {"theme": "set_theme", "style_name": "set_theme"}

    def set_theme(self, name):
        """"light" or "dark" (or a package of the component)."""
        self._keep("theme", name)
        self._keep("styleName", name)
        return self.call("setTheme", name)


class _LogWriter(io.TextIOBase):
    """print() into a LogView: whole lines go to it, one line at a time. The terminal gets them too."""

    def __init__(self, log, level, terminal):
        super().__init__()
        self._log = log
        self._level = level
        self._terminal = terminal
        self._waiting = ""

    def writable(self):
        return True

    def write(self, text):
        if self._terminal is not None:
            self._terminal.write(text)
        self._waiting += text
        *lines, self._waiting = self._waiting.split("\n")
        for line in lines:
            self._log.add_line(line, self._level)
        return len(text)

    def flush(self):
        if self._terminal is not None:
            self._terminal.flush()


class _LogHandler(logging.Handler):
    """The logging module into a LogView."""

    def __init__(self, log, level):
        super().__init__(level)
        self._log = log

    def emit(self, record):
        try:
            self._log.add_line(self.format(record), _LOG_LEVELS.get(record.levelno, "info"))
        except Exception:
            self.handleError(record)


_LOG_LEVELS = {logging.DEBUG: "debug", logging.INFO: "info", logging.WARNING: "warn", logging.ERROR: "error", logging.CRITICAL: "error"}


class LogView(_ThemedComponent):
    """The output of a program: colored lines that follow the last line. log = LogView(height=300); log.info("Reading")
    add_line(text, level), info(), success(), warn(), error(), debug(), clear(). A scroll up stops the following; a small
    button goes back to the end. The texts are never HTML. lines=[...]: the first lines; max_lines=1000: the oldest go.
    capture_print() sends print() into it, logging_handler() the logging module. style_name / theme: "light", "dark"."""

    _type = "LogView"
    _setters = dict(_ThemedComponent._setters, auto_scroll="set_auto_scroll", show_time="set_show_time",
                    show_level="set_show_level", wrap_lines="set_wrap_lines", max_lines="set_max_lines")

    def add_line(self, text, level="info"):
        """level: "info", "success", "warn", "error", "debug". A text of many lines becomes many lines."""
        return self.call("addLine", str(text), level)

    def info(self, text):
        return self.add_line(text, "info")

    def success(self, text):
        return self.add_line(text, "success")

    def warn(self, text):
        return self.add_line(text, "warn")

    def error(self, text):
        return self.add_line(text, "error")

    def debug(self, text):
        return self.add_line(text, "debug")

    def clear(self):
        return self.call("clearLines")

    def get_text(self):
        """All the lines that are shown, as they look (a question to the page)."""
        return self.ask("getText")

    def scroll_to_end(self):
        return self.call("scrollToEnd")

    def set_levels(self, levels):
        """Shows only these levels: log.set_levels(["warn", "error"]). []: all of them."""
        return self.call("setLevels", list(levels))

    def set_auto_scroll(self, value):
        self._keep("autoScroll", int(bool(value)))
        return self.call("setAutoScroll", int(bool(value)))

    def set_show_time(self, value):
        self._keep("showTime", int(bool(value)))
        return self.call("setShowTime", int(bool(value)))

    def set_show_level(self, value):
        self._keep("showLevel", int(bool(value)))
        return self.call("setShowLevel", int(bool(value)))

    def set_wrap_lines(self, value):
        self._keep("wrapLines", int(bool(value)))
        return self.call("setWrapLines", int(bool(value)))

    def set_max_lines(self, count):
        self._keep("maxLines", count)
        return self.call("setMaxLines", count)

    def capture_print(self, errors=True, terminal=True):
        """print() writes into this view; with errors=True sys.stderr too (a level of "error"): the errors of the
        code are seen in the window. terminal=True: the terminal gets them too. Returns a function that stops it;
        print() comes back by itself when the window closes (or the page is loaded again)."""
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout = _LogWriter(self, "info", old_out if terminal else None)
        if errors:
            sys.stderr = _LogWriter(self, "error", old_err if terminal else None)
        end_tasks = self._app._page_end_tasks

        def stop_capture():
            if stop_capture not in end_tasks:
                return  # WHY: stopped already (by the code, or as the window closed): the streams are not ours now
            end_tasks.remove(stop_capture)
            sys.stdout, sys.stderr = old_out, old_err

        end_tasks.append(stop_capture)
        return stop_capture

    def logging_handler(self, level=logging.INFO):
        """A handler for the logging module: logging.getLogger().addHandler(log.logging_handler())"""
        return _LogHandler(self, level)


class ImageView(_ThemedComponent):
    """A place to look at a picture or a plot: the wheel and two fingers zoom, a drag moves it, a small toolbar.
    view = ImageView(height=400, image="photo.png"); view.set_image(figure)
    A picture: a path, bytes, a Pillow image, a matplotlib figure, or an address (see picture_address()). A new picture
    of the same size keeps the zoom and the place and does not blink: a program can keep drawing its plot.
    view.zoom_level, view.natural_width, view.natural_height are kept in Python. on_load(view), on_error(view),
    on_zoom_change(view). enlarge_to_fit=True: a small picture grows to the box. style_name / theme: "light", "dark"."""

    _type = "ImageView"
    _aliases = dict(_ThemedComponent._aliases, image="image_file", alt="alt_text")
    _setters = dict(_ThemedComponent._setters, image="set_image", image_file="set_image", show_toolbar="set_show_toolbar")
    _state = {"zoomLevel": "zoomLevel", "naturalWidth": "naturalWidth", "naturalHeight": "naturalHeight"}
    _sync_callbacks = ("on_zoom_change", "on_load")
    _state_defaults = {"zoomLevel": 1, "naturalWidth": 0, "naturalHeight": 0}

    def __init__(self, *position, **params):
        for name in ("image", "image_file"):
            if name in params:
                params[name] = picture_address(params[name])
        super().__init__(*position, **params)

    def set_image(self, picture, alt_text=None):
        address = picture_address(picture)
        if alt_text is None:
            return self.call("setImage", address)
        return self.call("setImage", address, alt_text)

    def clear_image(self):
        return self.call("clearImage")

    def zoom_in(self):
        return self._call_and_refresh("zoomIn")

    def zoom_out(self):
        return self._call_and_refresh("zoomOut")

    def zoom_to_fit(self):
        return self._call_and_refresh("zoomToFit")

    def zoom_to_actual_size(self):
        return self._call_and_refresh("zoomToActualSize")

    def set_zoom_level(self, zoom):
        """1 is 100%."""
        return self._call_and_refresh("setZoomLevel", zoom)

    def set_show_toolbar(self, value):
        self._keep("showToolbar", int(bool(value)))
        return self.call("setShowToolbar", int(bool(value)))


def _item_for_page(item):
    """A menu, an item of a menu, a part of a StatusBar or a node of a tree as the page names its keys: on_click ->
    onClick, has_children -> hasChildren, also inside."""
    if not isinstance(item, dict):
        return item
    page_item = {camel_case(key): value for key, value in item.items()}
    for name in _CHILD_LISTS:
        if isinstance(page_item.get(name), (list, tuple)):
            page_item[name] = [_item_for_page(child) for child in page_item[name]]
    return page_item


class MenuBar(_ThemedComponent):
    """The row of menus of a window, in the page (not the menu of the system):
    MenuBar(menus=[{"text": "File", "items": [{"text": "Save", "key": "save", "shortcut": "Ctrl+S", "on_click": save}, "-"]}])
    An item: text, key, shortcut, checked, enabled, items (a submenu), on_click: fn(bar, item, menu) (fn() too), or a
    text; "-" is a line. Ctrl is also Cmd on a Mac, and a shortcut runs its item. on_click=fn of the bar: every item.
    set_item_checked(key, True), set_item_enabled(key, False). style_name / theme: "light", "dark"."""

    _type = "MenuBar"
    _defaults = {"shrink": 0}  # WHY: as high as its content: a column with a part that fills made it lower
    _setters = dict(_ThemedComponent._setters, menus="set_menus", enabled="set_enabled")
    _data_params = TypedComponent._data_params + ("menus",)

    def __init__(self, *position, **params):
        if "menus" in params:
            params["menus"] = [_item_for_page(menu) for menu in params["menus"]]
        super().__init__(*position, **params)

    def set_menus(self, menus):
        page_menus = [_item_for_page(menu) for menu in menus]
        self._keep("menus", page_menus)
        return self._call_with_items("menus", "setMenus", page_menus)

    def set_item_checked(self, key, value):
        return self.call("setItemChecked", key, int(bool(value)))

    def set_item_enabled(self, key, value):
        return self.call("setItemEnabled", key, int(bool(value)))

    def set_enabled(self, value):
        self._keep("enabled", int(bool(value)))
        return self.call("setEnabled", int(bool(value)))

    def close_menu(self):
        return self.call("closeMenu")


def _all_items(items):
    """The items of a list and of the menus in them, in order."""
    for item in items:
        if isinstance(item, dict):
            yield item
            yield from _all_items(item.get("items") or [])


class ToolBar(_ThemedComponent):
    """The row of small buttons of a window, under its menus:
    ToolBar(items=[{"key": "save", "icon": "save", "hint": "Save", "shortcut": "Ctrl+S", "on_click": save}, "-",
                   {"key": "bold", "icon": "bold", "hint": "Bold", "toggle": True}, " ", {"key": "run", "text": "Run"}])
    An item: key, text, icon (a name of ToolBar.ICONS or an SVG text), icon_file, hint, shortcut, toggle=True (it stays
    pressed), group="align" (one of the group stays pressed), checked, enabled, items (it opens a menu, as in MenuBar),
    on_click: fn(bar, item) (fn() too), or a text. "-" is a line; " ": the next ones stand at the right end. What does not
    fit goes into a "..." menu. on_click=fn of the bar: every item. Ctrl is also Cmd on a Mac; a key that is also in a
    MenuBar runs once. bar.checked_keys, is_checked(key), set_item_checked(key, True), set_item_enabled(key, False),
    set_item_text(key, text), set_item_hint(key, text), click_item(key). style_name / theme: "light", "dark"."""

    _type = "ToolBar"
    _defaults = {"shrink": 0}  # WHY: as high as its content: a column with a part that fills made it lower
    _item_keys = ("key", "text", "icon", "iconFile", "hint", "shortcut", "toggle", "group", "checked", "enabled", "items", "data",
                  "onClick")
    _nested_item_keys = ("items",)
    _state = {"checkedKeys": "getCheckedKeys()"}
    _setters = dict(_ThemedComponent._setters, items="set_items", enabled="set_enabled")
    _sync_callbacks = ("on_click",)
    _state_defaults = {"checkedKeys": []}
    ICONS = ("new", "open", "save", "undo", "redo", "cut", "copy", "paste", "delete", "search", "refresh", "settings", "play", "stop",
             "plus", "minus", "bold", "italic", "underline", "align_left", "align_center", "align_right", "more", "arrow_down")

    def __init__(self, *position, **params):
        if "items" in params:
            params["items"] = self._items_for_page(params["items"])
        super().__init__(*position, **params)
        self._keep_checked_keys_of(params.get("items", []))

    def _items_for_page(self, items):
        page_items = _list_for_page(type(self), items)
        for item in _all_items(page_items):
            if "icon" in item:
                item["icon"] = self._icon_for_page(item["icon"])
        return page_items

    def _icon_for_page(self, icon):
        """align_left -> alignLeft, the name on the page. WHY the error: on the page a wrong name is only an empty button."""
        if str(icon).lstrip().startswith("<"):
            return icon
        if icon not in self.ICONS and icon not in [camel_case(name) for name in self.ICONS]:
            raise ValueError(f'ToolBar: there is no icon named "{icon}". The names: {", ".join(self.ICONS)}; or an SVG text')
        return camel_case(icon)

    def _keep_checked_keys_of(self, items):
        self._keep("checkedKeys", [item["key"] for item in _all_items(items) if item.get("checked") and "key" in item])

    @property
    def checked_keys(self):
        return list(self._values.get("checkedKeys", []))

    def is_checked(self, key):
        return key in self.checked_keys

    def set_items(self, items):
        page_items = self._items_for_page(items)
        self._keep("items", page_items)
        self._keep_checked_keys_of(page_items)
        return self._call_with_items("items", "setItems", page_items)

    def set_item_checked(self, key, value):
        """on_click is not called. In a group the others go off."""
        items = list(_all_items(self._values.get("items", [])))
        group = next((item.get("group") for item in items if item.get("key") == key), None)
        checked = set(self.checked_keys)
        if value and group:
            checked -= {item.get("key") for item in items if item.get("group") == group}
        if value:
            checked.add(key)
        else:
            checked.discard(key)
        self._keep("checkedKeys", [item["key"] for item in items if item.get("key") in checked])
        return self._call_and_refresh("setItemChecked", key, int(bool(value)))

    def set_item_enabled(self, key, value):
        return self.call("setItemEnabled", key, int(bool(value)))

    def set_item_text(self, key, text):
        return self.call("setItemText", key, text)

    def set_item_hint(self, key, text):
        return self.call("setItemHint", key, text)

    def click_item(self, key):
        """As a click on it (on_click runs). A button with a menu does nothing."""
        return self.call("clickItem", key)

    def set_enabled(self, value):
        self._keep("enabled", int(bool(value)))
        return self.call("setEnabled", int(bool(value)))

    def close_menu(self):
        return self.call("closeMenu")


class StatusBar(_ThemedComponent):
    """The thin bar at the bottom of a window: bar = StatusBar(message="Ready", items=["3 files", "UTF-8"])
    bar.set_message("Saved", "success", 3000): a tone ("success", "warn", "error", "info") and a time (ms), after which
    the lasting message comes back. bar.set_busy(True): a turning circle. A part: a text, or {"key", "text", "tone",
    "on_click": fn(bar, part)}. It stands at the bottom of a Box by itself; in a VGroup it takes its place."""

    _type = "StatusBar"
    _defaults = {"shrink": 0}  # WHY: as high as its content: a column with a part that fills made it lower
    _item_keys = ("key", "text", "icon", "tone", "ariaLabel", "onClick")
    _has_own_place = True  # WHY: a top of 0 would hold it at the top of a Box
    _aliases = dict(_ThemedComponent._aliases, message="message_text", tone="message_tone")
    _setters = dict(_ThemedComponent._setters, busy="set_busy", items="set_items", message="set_message",
                    message_text="set_message")

    def __init__(self, *position, **params):
        if "items" in params:
            params["items"] = _list_for_page(type(self), params["items"])
        super().__init__(*position, **params)

    def set_message(self, text, tone="", time=0):
        """time (ms): after it the bar goes back to its lasting message. 0: this one is the lasting message."""
        self._keep("messageText", text)
        self._keep("message", text)
        return self.call("setMessageText", text, tone, time)

    def set_busy(self, value):
        self._keep("busy", int(bool(value)))
        return self.call("setBusy", int(bool(value)))

    def set_items(self, items):
        return self._call_with_items("items", "setItems", _list_for_page(type(self), items))

    def set_item_text(self, key, text):
        return self.call("setItemText", key, str(text))

    def set_item_visible(self, key, value):
        return self.call("setItemVisible", key, int(bool(value)))


class ScrollArea(TypedComponent):
    """A box that scrolls what is in it (comp/scroll-area.js): with ScrollArea(gap=12, padding=20): Label(...)
    The objects of its "with" block go one under the other into its content (align, gap, padding, as in a VGroup) and
    scroll when they are taller than the area. As an object of the page it is the whole window; in a group it takes the
    room the other objects leave (a VGroup with a MenuBar over it and a StatusBar under it: the height between them). A
    size of its own wins (height=300). scroll_x=True: to the side too. color, border, round: its look. The scroll bar
    of the kit: style_name "light" (default), "dark", "minimal", "minimalDark".
    area.scroll_to_top(), scroll_to_end(), scroll_to_object(obj), area.scroll_top (a question to the page),
    set_scroll_top(px), on_scroll(area). Objects added later: with area: ... (they go under the others)."""

    _type = "ScrollArea"
    _is_container = True
    _setters = {"align": "set_align", "gap": "set_gap", "padding": "set_padding", "scroll_x": "set_scroll_x",
                "scroll_y": "set_scroll_y"}

    def __init__(self, *position, **params):
        super().__init__(*position, **params)
        object.__setattr__(self, "_content", self.part("content"))

    # WHY the content: the area is only its frame (the place and the look); its objects are in the VGroup that scrolls
    def __enter__(self):
        self._app._open_container(self._content._id)
        return self

    def __exit__(self, *error):
        self._app._close_container(self._content._id)
        return False

    def set_align(self, value):
        self._keep("align", value)
        return self.call("setAlign", value)

    def set_gap(self, value):
        self._keep("gap", value)
        return self.call("setGap", value)

    def set_padding(self, value):
        self._keep("padding", value)
        return self.call("setPadding", value)

    def set_scroll_x(self, value):
        self._keep("scrollX", int(bool(value)))
        return self.call("setScrollX", int(bool(value)))

    def set_scroll_y(self, value):
        self._keep("scrollY", int(bool(value)))
        return self.call("setScrollY", int(bool(value)))

    def scroll_to_top(self):
        return self.call("scrollToTop")

    def scroll_to_end(self):
        """The bottom of the content (an area that scrolls only to the side: its right end)."""
        return self.call("scrollToEnd")

    def scroll_to_object(self, obj):
        """An object of the area comes into view; the area moves as little as it can."""
        return self.call("scrollToObject", obj)

    @property
    def scroll_top(self):
        """How far it is scrolled, in px (a question to the page)."""
        return self.ask("getScrollTop")

    def set_scroll_top(self, value):
        return self.call("setScrollTop", value)


class Splitter(_ThemedComponent):
    """Two areas with a line between them: a drag of the line changes their sizes.
    split = Splitter(first_size=240); with split.first: ...; with split.second: ...
    direction: "horizontal" (side by side) or "vertical". first_size or second_size: px, or a part ("30%"): a part stays
    a part when the window changes, px stay px. min_first, min_second (px). on_change_end(split): read split.first_size_now.
    set_area_visible("first", False) hides an area. Objects go one under the other in an area, as in a VGroup."""

    _type = "Splitter"
    _state = {"firstSizeNow": "getFirstSize()"}
    _sync_callbacks = ("on_change_end",)
    _state_defaults = {"firstSizeNow": 0}

    def __init__(self, *position, **params):
        super().__init__(*position, **params)
        object.__setattr__(self, "_areas", {})

    def _area(self, name):
        if name not in self._areas:
            self._areas[name] = self.part(name)
        return self._areas[name]

    @property
    def first(self):
        return self._area("first")

    @property
    def second(self):
        return self._area("second")

    def set_first_size(self, size):
        """px, or a part of the box ("40%")."""
        return self._call_and_refresh("setFirstSize", size, 1)

    def set_area_visible(self, name, value):
        """name: "first" or "second"."""
        return self.call("setAreaVisible", name, int(bool(value)))


class CodeEditor(_ThemedComponent):
    """A text editor for code: line numbers and colors: CodeEditor(value="x = 1", language="python", height=300)
    language: "python", "javascript", "json", "html", "css", "sql", "bash", "text". Tab, Shift + Tab, Enter and Ctrl + /
    edit the lines; undo takes them back. A big text stays fast (only the lines that are seen are drawn).
    editor.value asks the page for the text. editor.cursor_line, editor.cursor_column are kept in Python.
    on_change(editor), on_cursor_change(editor). change_delay (ms): on_change waits for the typing to rest."""

    _type = "CodeEditor"
    _setters = dict(_ThemedComponent._setters, value="set_value", language="set_language", read_only="set_read_only",
                    show_line_numbers="set_show_line_numbers", tab_size="set_tab_size")
    _state = {"cursorLine": "cursorLine", "cursorColumn": "cursorColumn"}
    _sync_callbacks = ("on_cursor_change",)
    _state_defaults = {"cursorLine": 1, "cursorColumn": 1}

    @property
    def value(self):
        """The text now. WHY a question: a big text does not go to Python at every key."""
        return self.ask("getValue")

    def set_value(self, text):
        """A new text (on_change is not called). NOTE: the undo starts again."""
        return self.call("setValue", text, 1)

    def insert_text(self, text):
        """At the cursor, over the selected text. Undo takes it back."""
        return self.call("insertText", text)

    def get_selected_text(self):
        return self.ask("getSelectedText")

    def set_language(self, language):
        self._keep("language", language)
        return self.call("setLanguage", language)

    def set_read_only(self, value):
        self._keep("readOnly", int(bool(value)))
        return self.call("setReadOnly", int(bool(value)))

    def set_show_line_numbers(self, value):
        self._keep("showLineNumbers", int(bool(value)))
        return self.call("setShowLineNumbers", int(bool(value)))

    def set_tab_size(self, size):
        self._keep("tabSize", size)
        return self.call("setTabSize", size)

    def go_to_line(self, line):
        """Puts the cursor at the start of a line (from 1) and shows it."""
        return self.call("goToLine", line)

    def focus(self):
        return self.call("focusEditor")


class GraphBox(TypedComponent):
    """A chart, drawn by the page with no other library: GraphBox(type="bar", labels=["Jan", "Feb"], values=[12, 19]).
    type: "line", "area", "bar", "pie", "doughnut", "radar", "scatter", "bubble". More lines or bars: datasets=[{"label":
    "2026", "data": [12, 19]}, ...]; a dataset also takes color, fill, dashed, curve, show_points. The values may be numpy
    arrays or a pandas Series. Scatter: data=[{"x": 1, "y": 2}, ...].
    format_value="{:,.0f} TL": the numbers of the axis and the tooltip, a text and not a function (the page needs them at
    once); format_x for the x axis of a scatter. title_text, subtitle_text, legend ("auto", "top", "none"...), stacked,
    horizontal, show_values, curve ("linear", "smooth"), target_lines=[{"value": 90, "label": "Target"}], max_count (a live
    chart: the oldest value goes). on_click(graph, item): item has label, value, dataset_label...
    graph.save_image("chart.png") writes a picture of it. theme: "light", "dark", "auto"."""

    _type = "GraphBox"
    _format_params = ("formatValue", "formatX")
    _setters = {"labels": "set_labels", "values": "set_values", "datasets": "set_datasets", "type": "set_type", "title_text": "set_title",
                "subtitle_text": "set_subtitle", "theme": "set_theme", "legend": "set_legend", "show_values": "set_show_values",
                "table_view": "set_table_view", "stacked": "set_stacked", "horizontal": "set_horizontal", "curve": "set_curve",
                "target_lines": "set_target_lines", "format_value": "set_format_value", "format_x": "set_format_x",
                "center_text": "set_center_text"}

    def __init__(self, *position, **params):
        if "datasets" in params:
            params["datasets"] = self._datasets_for_page(params["datasets"])
        super().__init__(*position, **params)

    @staticmethod
    def _datasets_for_page(datasets):
        return [_item_for_page(dataset) for dataset in datasets]

    def set_labels(self, labels):
        self._keep("labels", labels)
        return self.call("setLabels", labels)

    def set_values(self, values, dataset_index=0):
        self._keep("values", values)
        return self.call("setValues", values, dataset_index)

    def set_datasets(self, datasets):
        self._keep("datasets", datasets)
        return self.call("setDatasets", self._datasets_for_page(datasets))

    def set_data(self, labels, datasets):
        """New labels and datasets together."""
        return self.call("setData", {"labels": labels, "datasets": self._datasets_for_page(datasets)})

    def add_value(self, label, values):
        """One more place: graph.add_value("Apr", 15), with more datasets a list: graph.add_value("Apr", [15, 20])."""
        return self.call("addValue", label, values)

    def add_point(self, point, dataset_index=0):
        """A scatter: graph.add_point({"x": 1, "y": 2})."""
        return self.call("addPoint", point, dataset_index)

    def add_dataset(self, dataset):
        return self.call("addDataset", _item_for_page(dataset))

    def remove_dataset(self, position):
        return self.call("removeDataset", position)

    def set_dataset_visible(self, position, value):
        return self.call("setDatasetVisible", position, int(bool(value)))

    def set_type(self, type_name):
        self._keep("type", type_name)
        return self.call("setType", type_name)

    def set_title(self, text):
        self._keep("titleText", text)
        return self.call("setTitleText", text)

    def set_subtitle(self, text):
        self._keep("subtitleText", text)
        return self.call("setSubtitleText", text)

    def set_center_text(self, text):
        self._keep("centerText", text)
        return self.call("setCenterText", text)

    def set_legend(self, legend):
        self._keep("legend", legend)
        return self.call("setLegend", legend)

    def set_show_values(self, value):
        return self.call("setShowValues", int(bool(value)))

    def set_table_view(self, value):
        """The same values as a table."""
        return self.call("setTableView", int(bool(value)))

    def set_stacked(self, value):
        return self.call("setStacked", int(bool(value)))

    def set_horizontal(self, value):
        return self.call("setHorizontal", int(bool(value)))

    def set_curve(self, curve):
        return self.call("setCurve", curve)

    def set_target_lines(self, lines):
        return self.call("setTargetLines", lines)

    def set_value_limits(self, minimum, maximum):
        return self.call("setValueLimits", minimum, maximum)

    def set_format_value(self, text):
        """None: the numbers as the chart writes them."""
        return self.call("setFormatValue", self._format_of("set_format_value", text))

    def set_format_x(self, text):
        return self.call("setFormatX", self._format_of("set_format_x", text))

    def set_theme(self, name):
        """"light", "dark" or "auto"."""
        self._keep("theme", name)
        return self.call("setTheme", name)

    def get_table_data(self):
        """The values as rows (a question to the page)."""
        return self.ask("getTableData")

    def save_image(self, path, scale=2):
        """Writes a picture of the chart into a file: .png or .jpg (a question to the page)."""
        is_jpeg = str(path).lower().endswith((".jpg", ".jpeg"))
        address = self.ask("getImage", "image/jpeg" if is_jpeg else "image/png", scale)
        with open(path, "wb") as file:
            file.write(base64.b64decode(address.split(",", 1)[1]))


class TreeView(TypedComponent):
    """A tree: TreeView(items=[{"key": "src", "text": "src", "children": ["a.py", "b.py"]}, "readme"], height=300, on_select=fn).
    A node: a text or {"key", "text", "children", "expanded", "has_children", "description", "description_color", "tag",
    "tag_color", "text_color", "icon_file", "enabled", "data"}; enabled=False: it can not be selected or opened.
    on_select(tree, node) runs for a click and the arrow keys: tree.value is the key of the selected node.
    on_activate(tree, node): a double click or Enter. on_toggle(tree, node): it opened or closed.
    A branch made when it opens: {"key": "photos", "text": "photos", "has_children": True}, then on_load_children(tree, node)
    gives its nodes: tree.set_children(node["key"], [...]). style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern"."""

    _type = "TreeView"
    _state = {"value": "value", "previousValue": "previousValue"}
    _setters = {"value": "set_value", "items": "set_items", "enabled": "set_enabled", "empty_text": "set_empty_text"}
    _sync_callbacks = ("on_select",)
    _state_defaults = {"value": None, "previousValue": None}
    _item_keys = ("key", "text", "iconFile", "tag", "tagColor", "description", "descriptionColor", "textColor", "children",
                  "expanded", "hasChildren", "enabled", "data")
    _nested_item_keys = ("children",)

    def __init__(self, *position, **params):
        if "items" in params:
            params["items"] = _list_for_page(type(self), params["items"])
        super().__init__(*position, **params)

    def set_items(self, items):
        self._keep("items", items)
        return self.call("setItems", _list_for_page(type(self), items))

    def set_value(self, key):
        """Selects a node (on_select is not called). None: nothing."""
        self._keep("previousValue", self._values.get("value"))
        self._keep("value", key)
        return self._call_and_refresh("setValue", key, 1)

    @property
    def selected_node(self):
        """The selected node, or None (a question to the page)."""
        return self.ask("getSelectedNode")

    def get_node(self, key):
        return self.ask("getNode", key)

    def get_path(self, key):
        """The keys from the first level down to this node (a question to the page)."""
        return [node["key"] for node in self.ask("getPath", key)]

    def set_children(self, key, children):
        """The nodes of a branch: on_load_children answers with this."""
        return self.call("setChildren", key, _list_for_page(type(self), children))

    def add_node(self, parent_key, node, position=-1):
        """parent_key None: on the first level."""
        return self.call("addNode", parent_key, _list_for_page(type(self), [node])[0], position)

    def remove_node(self, key):
        return self.call("removeNode", key)

    def update_node(self, key, **values):
        """tree.update_node("a.py", description="4 KB") paints one row."""
        return self.call("updateNode", key, _item_for_page(values))

    def expand(self, key):
        return self.call("expand", key)

    def collapse(self, key):
        return self.call("collapse", key)

    def toggle(self, key):
        return self.call("toggle", key)

    def expand_all(self):
        return self.call("expandAll")

    def collapse_all(self):
        return self.call("collapseAll")

    def reveal(self, key):
        """Opens its parents and scrolls to it."""
        return self.call("reveal", key)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def set_empty_text(self, text):
        self._keep("emptyText", text)
        return self.call("setEmptyText", text)

    def focus(self):
        return self.call("focus")


class ContextMenu(TypedComponent):
    """A menu that opens at the mouse: ContextMenu(target=table, items=["Open", "-", {"text": "Delete", "key": "delete",
    "on_click": fn}], on_click=fn). An item: a text or {"text", "key", "icon", "icon_file", "items" (a submenu), "shortcut",
    "checked", "enabled", "data", "on_click"}; "-" is a line. A right click on the target opens it; trigger="click": a click.
    fn(menu, item, index) (fn() too). on_click=fn of the menu: every item. menu.open_at(x, y), menu.open_below(obj), menu.close().
    style_name: "light" (default; its old name "classic"), "dark" (a dark page)."""

    _type = "ContextMenu"
    _has_own_place = True
    _setters = {"items": "set_items", "enabled": "set_enabled"}

    def __init__(self, *position, **params):
        if "items" in params:
            params["items"] = [_item_for_page(item) for item in params["items"]]
        super().__init__(*position, **params)

    def set_items(self, items):
        self._keep("items", items)
        return self._call_with_items("items", "setItems", [_item_for_page(item) for item in items])

    def attach_to(self, obj, trigger="contextmenu"):
        """One more object that opens it. trigger: "contextmenu" (a right click) or "click"."""
        return self.call("attachTo", obj, trigger)

    def detach(self, obj):
        return self.call("detach", obj)

    def open_at(self, x, y):
        return self.call("openAt", x, y)

    def open_below(self, obj):
        return self.call("openBelow", obj)

    def close(self):
        return self.call("close")

    def is_open(self):
        """A question to the page."""
        return bool(self.ask("isOpen"))

    def set_item_enabled(self, key, value):
        return self.call("setItemEnabled", key, int(bool(value)))

    def set_item_checked(self, key, value):
        return self.call("setItemChecked", key, int(bool(value)))

    def set_enabled(self, value):
        self._keep("enabled", int(bool(value)))
        return self.call("setEnabled", int(bool(value)))


class _Bubble(Part):
    """A bubble on the page, made by Tooltip.show() or a popover: bubble.remove() takes it away."""

    def __init__(self, app):
        self._init_proxy(app, _new_id(), {})
        app._register(self)


class _Popover:
    """A bubble that stays, with objects in it. A click on its target opens and closes it; the page closes it too (a click
    outside, Escape): its on_close runs. Made by Tooltip.popover()."""

    def __init__(self, target, content, side, look, on_close):
        self._app = _app.current_app()
        self._target = target
        self._content = content
        self._side = side
        self._look = look
        self._on_close = on_close
        self.is_open = False
        # WHY one callback for all its openings: a new one at every opening would be kept for ever.
        self._page_on_close = to_page(self._on_page_close, self._app, None, "Tooltip.popover()")
        target.on("click", self.toggle)

    def open(self):
        if self.is_open:
            return
        self.is_open = True
        bubble = _Bubble(self._app)
        look = _item_for_page(self._look) if self._look else (_POPOVER_DARK_LOOK if self._app.theme == "dark" else _POPOVER_LOOK)
        target = to_page(self._target, self._app, None, "Tooltip.popover()")
        args = [target, {"__bpNoop": 1}, look, self._side, "", {"onClose": self._page_on_close}]
        self._app._call_static("Tooltip", "openPopover", args, keep=bubble._id)
        with bubble:
            call_with_count(self._content, positional_count(self._content), [bubble])
        self._app._send({"op": "placeBubble", "id": bubble._id, "target": self._target._id, "side": self._side})

    def close(self):
        if self.is_open:
            self._app._call_static("Tooltip", "closePopover", [])

    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()

    def _on_page_close(self):
        self.is_open = False
        if self._on_close:
            self._on_close()


class Tooltip(TypedComponent):
    """A hint under the mouse: Tooltip(target=button, text="Save the file"). position: "top" (default), "bottom", "left",
    "right". look={"arrow": 10, "color": "#222", "text_color": "white"}: its look (shadow, padding, round, border, border_color...).
    Tooltip.show(button, "Saved.", time=2000): a bubble at the object, not under the mouse; bubble.remove() takes it away.
    Tooltip.popover(button, make_content): a click on the button opens a bubble that stays; make_content() makes its objects."""

    _type = "Tooltip"
    _has_own_place = True
    _aliases = {"text": "hint_text", "position": "hint_position"}
    _setters = {"text": "set_text", "hint_text": "set_text"}

    def __init__(self, *position, **params):
        if params.get("target") is None:
            raise TypeError('Tooltip() needs its object: Tooltip(target=button, text="Save the file")')
        if params.get("look"):
            params["look"] = _item_for_page(params["look"])
        super().__init__(*position, **params)

    def set_text(self, text):
        self._keep("text", text)
        return self.call("setHintText", text)

    @staticmethod
    def show(target, text, side="top", look=None, time=0):
        """A bubble at an object. side: "top", "bottom", "left", "right". time (ms): it goes by itself. Returns the bubble.
        look: its keys over the frame of a popover (its colors, its line and its shadow; dark in a dark window)."""
        app = _app.current_app()
        bubble = _Bubble(app)
        popover_look = _POPOVER_DARK_LOOK if app.theme == "dark" else _POPOVER_LOOK
        frame = {key: popover_look[key] for key in _BUBBLE_FRAME_KEYS}
        args = [to_page(target, app, None, "Tooltip.show()"), text, dict(frame, **_item_for_page(look or {})), side]
        app._call_static("Tooltip", "show", args, keep=bubble._id)
        if time:
            app.after(time, bubble.remove)
        return bubble

    @staticmethod
    def popover(target, content, side="bottom", look=None, on_close=None):
        """A click on the target opens and closes a bubble that stays. content() makes its objects, one under the other,
        each time it opens. A click outside and Escape close it too. Returns it: popover.open(), close(), is_open."""
        return _Popover(target, content, side, look, on_close)

    @staticmethod
    def close_popover():
        """Closes the popover that is open (a button in it)."""
        _app.current_app()._call_static("Tooltip", "closePopover", [])


class _Picker(TypedComponent):
    """The common part of a field that opens a panel (a date, a time, a color). inline=True: the panel stays in its place.
    on_change(picker) runs when it changes: read picker.value. "" is no value."""

    _state = {"value": "value"}
    _setters = {"value": "set_value", "enabled": "set_enabled"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"value": ""}

    def open(self):
        return self.call("open")

    def close(self):
        return self.call("close")

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))


def _date_text(value):
    return value.strftime("%Y-%m-%d") if isinstance(value, datetime.date) else value


class DatePicker(_Picker):
    """A date: a field that opens a calendar: DatePicker(value="2026-11-20", on_change=fn). inline=True: a calendar that stays.
    picker.value is a text ("2026-11-20", "": none), picker.date a datetime.date or None; a date may be given as either.
    min_date, max_date, format ("DD.MM.YYYY"), language ("en", "tr"), first_day_of_week (1: Monday).
    style_name: "light" (default; its old name "classic"), "dark" (a dark page)."""

    _type = "DatePicker"
    _setters = dict(_Picker._setters, date="set_value", min_date="set_min_date", max_date="set_max_date")

    def __init__(self, *position, value=None, **params):
        if value is not None:
            params["date"] = value
        for name in ("date", "min_date", "max_date"):
            if name in params:
                params[name] = _date_text(params[name])
        super().__init__(*position, **params)
        self._keep("value", params.get("date") or "")

    @property
    def date(self):
        text = self._values.get("value")
        return datetime.date.fromisoformat(text) if text else None

    def set_value(self, value):
        """A date out of min_date..max_date is not taken: the value stays."""
        self._keep("value", _date_text(value) or "")
        return self._call_and_refresh("setDate", _date_text(value), 1)

    def set_min_date(self, value):
        return self._call_and_refresh("setMinDate", _date_text(value))

    def set_max_date(self, value):
        return self._call_and_refresh("setMaxDate", _date_text(value))


def _time_text(value):
    return value.strftime("%H:%M") if isinstance(value, datetime.time) else value


class TimePicker(_Picker):
    """A time: a field that opens two columns: TimePicker(value="19:30", on_change=fn). inline=True: the columns stay.
    picker.value is a text ("19:30", "": none), picker.time a datetime.time or None; a time may be given as either.
    min_time, max_time, minute_step (5), language ("en", "tr"). style_name: "light" (default; its old name "classic"), "dark" (a dark page)."""

    _type = "TimePicker"
    _setters = dict(_Picker._setters, time="set_value", min_time="set_min_time", max_time="set_max_time", minute_step="set_minute_step")

    def __init__(self, *position, value=None, **params):
        if value is not None:
            params["time"] = value
        for name in ("time", "min_time", "max_time"):
            if name in params:
                params[name] = _time_text(params[name])
        super().__init__(*position, **params)
        self._keep("value", params.get("time") or "")

    @property
    def time(self):
        text = self._values.get("value")
        return datetime.time.fromisoformat(text) if text else None

    def set_value(self, value):
        """A time out of min_time..max_time is not taken: the value stays."""
        self._keep("value", _time_text(value) or "")
        return self._call_and_refresh("setTime", _time_text(value), 1)

    def set_min_time(self, value):
        return self._call_and_refresh("setMinTime", _time_text(value))

    def set_max_time(self, value):
        return self._call_and_refresh("setMaxTime", _time_text(value))

    def set_minute_step(self, step):
        return self._call_and_refresh("setMinuteStep", step)


class ColorPicker(_Picker):
    """A color: a field that opens a palette: ColorPicker(value="#3871E0", on_change=fn). inline=True: a palette that stays.
    picker.value is the color ("#3871E0", "": none). colors=[...]: your own palette, columns: how many in a row.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page)."""

    _type = "ColorPicker"
    _aliases = {"value": "selected_color"}
    _setters = dict(_Picker._setters, selected_color="set_value", colors="set_colors")

    def set_value(self, color):
        self._keep("value", color)
        return self._call_and_refresh("setColor", color, 1)

    def set_colors(self, colors):
        self._keep("colors", list(colors))
        return self.call("setColors", list(colors))


class Stepper(TypedComponent):
    """A number with - and + buttons: Stepper(value=2, min_value=0, max_value=10, step=1, on_change=fn). on_change(stepper):
    read stepper.value. A click on the number types it (editable=False: no); a button that is held keeps counting.
    precision: its decimals. unit_text=" kg". value_format="{:,.1f} kg": its text. wrap=True: after max_value comes
    min_value.
    layout: "horizontal" or "compact". style_name: "light" (default; its old name "classic"), "dark" (a dark page), "modern", "ozden",
    "ozdenDark" (ozden on a dark page)."""

    _type = "Stepper"
    _state = {"value": "value"}
    _setters = {"value": "set_value", "enabled": "set_enabled", "unit_text": "set_unit_text", "step": "set_step",
                "precision": "set_precision", "min_value": "set_min_value", "max_value": "set_max_value"}
    _sync_callbacks = ("on_change",)
    _state_defaults = {"value": 1, "minValue": 0, "maxValue": 10}
    _format_params = ("valueFormat",)

    def set_value(self, value):
        # WHY here too: the page keeps the value inside min_value..max_value, without a word.
        self._keep("value", _inside(value, self._values.get("minValue", 0), self._values.get("maxValue", 10)))
        return self._call_and_refresh("setValue", value, 1)

    def increase(self):
        """One step up (on_change runs)."""
        return self.call("increase")

    def decrease(self):
        """One step down (on_change runs)."""
        return self.call("decrease")

    def set_min_value(self, value):
        return self.set_range(value, self._values.get("maxValue", 10))

    def set_max_value(self, value):
        return self.set_range(self._values.get("minValue", 0), value)

    def set_range(self, min_value, max_value):
        # WHY max(): the page keeps max_value >= min_value
        self._keep("minValue", min_value)
        self._keep("maxValue", max(min_value, max_value))
        self._keep("value", _inside(self._values.get("value", 0), min_value, max(min_value, max_value)))
        return self._call_and_refresh("setRange", min_value, max_value)

    def set_step(self, step):
        self._keep("step", step)
        return self.call("setStep", step)

    def set_precision(self, digits):
        self._keep("precision", digits)
        return self._call_and_refresh("setPrecision", digits)

    def set_unit_text(self, text):
        self._keep("unitText", text)
        return self.call("setUnitText", text)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def focus(self):
        return self.call("focus")


def _file_types_of(accept):
    """accept of the page as the file types of the dialog of the system: ".csv,.txt" -> ("Files (*.csv;*.txt)",),
    "image/*" -> every extension of a picture. "": every file."""
    extensions = []
    for rule in (accept or "").split(","):
        rule = rule.strip().lower()
        if rule.startswith("."):
            extensions.append(rule)
        elif rule.endswith("/*"):
            prefix = rule[:-1]
            extensions.extend(sorted(ext for ext, kind in mimetypes.types_map.items() if kind.startswith(prefix)))
        elif rule:
            extensions.extend(sorted(mimetypes.guess_all_extensions(rule)))
    extensions = [extension for extension in extensions if _FILE_TYPE.fullmatch(extension)]  # WHY: pywebview refuses ".c++"
    if not extensions:
        return ()
    return ("Files (" + ";".join("*" + extension for extension in extensions) + ")",)


class FilePicker(TypedComponent):
    """A place for files: a file dropped on it, or chosen in the file dialog of the system after a click:
    FilePicker(accept=".csv,.txt", multiple=True, on_change=fn). on_change(picker) runs when the list changes.
    picker.files: [{"name", "path", "size", "size_text", "type", "extension", "last_modified"}]: "path" is the real path on
    this computer, so open(file["path"]) reads it. picker.paths: only the paths.
    accept: ".pdf,.txt", "image/*"; max_size (bytes), max_files: what does not pass goes to on_error(picker, errors).
    multiple=True adds to the list; without it a new file takes the place of the old one. directory=True: a click chooses a
    folder, and the list holds its files. picker.add_paths([...]), picker.remove_file(0), picker.clear(), picker.open().
    title_text, description_text: its texts. icon_file: a picture of yours in the place of its icon (a path, bytes, a
    Pillow image or an address; set_icon() changes it). NOTE: a folder dropped on it is not read.
    style_name: "light" (default; its old name "classic"), "dark" (a dark page)."""

    _type = "FilePicker"
    _defaults = {"shrink": 0}  # WHY: it is as high as its content: a full group cut its zone
    _state = {"files": "getFileDetails()"}
    _setters = {"enabled": "set_enabled", "title_text": "set_title_text", "description_text": "set_description_text",
                "icon_file": "set_icon", "on_change": "set_on_change"}
    _state_defaults = {"files": []}

    def __init__(self, *position, on_change=None, **params):
        self._on_change = on_change
        params["on_change"] = self._on_page_change
        params["on_open_dialog"] = self._open_dialog
        if params.get("icon_file"):
            params["icon_file"] = picture_address(params["icon_file"])
        super().__init__(*position, **params)
        self._app._listen_for_dropped_files()

    @property
    def files(self):
        return [self._file_for_python(file) for file in self._values.get("files", [])]

    @property
    def paths(self):
        return [file["path"] for file in self.files if file["path"]]

    def set_on_change(self, handler):
        self._on_change = handler
        return self

    def _real_path(self, file):
        """The path a dialog gave, or the one pywebview gave for a drop. None: nobody knows it (yet, or a file made by the
        page)."""
        path = file.get("path") or ""
        if os.path.isabs(path):
            return path
        return self._app._dropped_path(file.get("name"), file.get("size"), file.get("lastModified"))

    def _file_for_python(self, file):
        return {"name": file.get("name"), "path": self._real_path(file), "size": file.get("size"), "size_text": file.get("sizeText"),
                "type": file.get("type"), "extension": file.get("extension"), "last_modified": file.get("lastModified")}

    def _on_page_change(self):
        self._wait_for_paths(_DROP_WAIT_STEPS)

    def _wait_for_paths(self, steps_left):
        """WHY the wait: the page and pywebview tell about a drop separately, in any order. A task of the app thread, so the
        window keeps working."""
        is_path_missing = any(self._real_path(file) is None for file in self._values.get("files", []))
        if is_path_missing and steps_left > 0:
            self._app.after(_DROP_WAIT_STEP_MS, lambda: self._wait_for_paths(steps_left - 1))
            return
        if self._on_change:
            call_with_count(self._on_change, positional_count(self._on_change), [self])

    def _open_dialog(self):
        """WHY the dialog of the system: the dialog of the page gives no path."""
        if self._values.get("directory"):
            folder = self._app.choose_folder()
            if folder:
                self._add_folder(folder)
            return
        multiple = bool(self._values.get("multiple"))
        chosen = self._app.open_file(file_types=_file_types_of(self._values.get("accept")), multiple=multiple)
        if chosen:
            self.add_paths(chosen)

    def _add_folder(self, folder):
        files = []
        for root, _folders, names in os.walk(folder):
            for name in sorted(names):
                path = os.path.join(root, name)
                # WHY the folder's name too: a row says where the file is, as the dialog of the page does
                relative = os.path.relpath(path, os.path.dirname(folder))
                files.append(dict(self._file_for_page(path), webkitRelativePath=relative.replace(os.sep, "/")))
        self.call("addFiles", files)

    def _file_for_page(self, path, with_preview=False):
        path = os.path.abspath(os.fspath(path))
        info = os.stat(path)
        media_type = mimetypes.guess_type(path)[0] or ""
        file = {"name": os.path.basename(path), "path": path, "size": info.st_size, "type": media_type,
                "lastModified": int(info.st_mtime * 1000)}
        if with_preview and media_type.startswith("image/") and info.st_size <= _MAX_PREVIEW_BYTES:
            file["previewAddress"] = picture_address(path)
        return file

    def add_paths(self, paths):
        """Adds files of this computer to the list. accept, max_size and max_files look at them too. on_change runs."""
        paths = [paths] if isinstance(paths, (str, os.PathLike)) else list(paths)
        with_preview = len(paths) <= _MAX_PREVIEWS and self._values.get("showPreview", 1)
        return self.call("addFiles", [self._file_for_page(path, with_preview) for path in paths])

    def open(self):
        """The file dialog of the system."""
        return self._open_dialog()

    def remove_file(self, index):
        files = list(self._values.get("files", []))
        if 0 <= index < len(files):
            del files[index]
        self._keep("files", files)
        return self.call("removeFile", index, 1)

    def clear(self):
        self._keep("files", [])
        return self.call("clear", 1)

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def set_title_text(self, text):
        self._keep("titleText", text)
        return self.call("setTitleText", text)

    def set_description_text(self, text):
        self._keep("descriptionText", text)
        return self.call("setDescriptionText", text)

    def set_icon(self, picture):
        """A picture in the place of the icon, with its own colors. None or "": the icon of the look."""
        address = picture_address(picture) if picture else ""
        self._keep("iconFile", address)
        return self.call("setIcon", address)


class RangeSlider(_ThemedComponent):
    """A range of values on a thin bar, with two knobs: RangeSlider(low=200, high=800, min_value=0, max_value=1000, step=50,
    width=280, on_change_end=fn). on_change(slider) runs while it moves, on_change_end(slider) when it is let go (a key and a click on
    the bar too): read slider.low, slider.high, slider.values. min_gap: the smallest distance between them.
    value_format="{:,.0f} TL": the text of its bubble. set_values(low, high). style_name / theme: "round" (default), "roundDark" (a dark page)."""

    _type = "RangeSlider"
    _aliases = dict(_ThemedComponent._aliases, low="low_value", high="high_value", value_format="format_value")
    _state = {"low": "lowValue", "high": "highValue"}
    _setters = dict(_ThemedComponent._setters, low="set_low", low_value="set_low", high="set_high", high_value="set_high",
                    min_value="set_min_value", max_value="set_max_value", step="set_step", min_gap="set_min_gap",
                    enabled="set_enabled")
    # WHY only the end: a move of the mouse is a call to Python; a key and a click are short moves, so they end too.
    _sync_callbacks = ("on_change_end",)
    _state_defaults = {"minValue": 0, "maxValue": 100}
    _format_params = ("formatValue",)

    def __init__(self, *position, **params):
        super().__init__(*position, **params)
        self._values.setdefault("low", self._values["minValue"])
        self._values.setdefault("high", self._values["maxValue"])

    @property
    def values(self):
        """(low, high)"""
        return (self._values["low"], self._values["high"])

    def set_values(self, low=None, high=None):
        """on_change is not called. None: that knob stays."""
        new_low = self._values["low"] if low is None else low
        new_high = self._values["high"] if high is None else high
        # WHY here too: the page keeps them inside min_value..max_value, in order and on the step, without a word.
        lowest, highest = self._values["minValue"], self._values["maxValue"]
        self._keep("low", _inside(min(new_low, new_high), lowest, highest))
        self._keep("high", _inside(max(new_low, new_high), lowest, highest))
        return self._call_and_refresh("setValues", new_low, new_high)

    def set_low(self, value):
        return self.set_values(low=value)

    def set_high(self, value):
        return self.set_values(high=value)

    def set_min_value(self, value):
        self._keep("minValue", value)
        return self._call_and_refresh("setMinValue", value)

    def set_max_value(self, value):
        self._keep("maxValue", value)
        return self._call_and_refresh("setMaxValue", value)

    def set_step(self, value):
        self._keep("step", value)
        return self._call_and_refresh("setStep", value)

    def set_min_gap(self, value):
        self._keep("minGap", value)
        return self._call_and_refresh("setMinGap", value)

    def set_enabled(self, value):
        self._keep("enabled", int(bool(value)))
        return self.call("setEnabled", int(bool(value)))


class StepBar(_ThemedComponent):
    """The steps of a job in a row: StepBar(steps=["Cart", "Address", {"text": "Payment", "description": "Card or cash"}, "Done"],
    step=1). A step: a text or {"key", "text", "description"}.
    A step behind has a check mark; on_step_click(bar, index) runs for a click on it (the page goes there with set_step()).
    can_go_back=False: no step can be clicked. bar.step, set_step(index), next(), previous(), set_steps([...]).
    show_titles=False: only the circles. style_name / theme: "light", "dark"."""

    _type = "StepBar"
    _item_keys = ("key", "text", "description")
    _aliases = dict(_ThemedComponent._aliases, step="current_step")
    _state = {"step": "currentStep"}
    _setters = dict(_ThemedComponent._setters, step="set_step", current_step="set_step", steps="set_steps")
    _state_defaults = {"step": 0}

    def __init__(self, *position, **params):
        if "steps" in params:
            params["steps"] = _list_for_page(type(self), params["steps"])
        super().__init__(*position, **params)
        self._values.setdefault("steps", params.get("steps", []))

    def _in_range(self, index):
        return _inside(int(index), 0, len(self._values.get("steps", [])))

    def set_step(self, index):
        """on_step_click is not called. len(steps): every step is done."""
        self._keep("step", self._in_range(index))
        return self._call_and_refresh("setStep", index)

    def next(self):
        return self.set_step(self._values["step"] + 1)

    def previous(self):
        return self.set_step(self._values["step"] - 1)

    def set_steps(self, steps):
        page_steps = _list_for_page(type(self), steps)
        self._keep("steps", page_steps)
        self._keep("step", self._in_range(self._values["step"]))
        return self._call_and_refresh("setSteps", page_steps)


class Canvas(_ThemedComponent):
    """A place to draw on: canvas = Canvas(width=600, height=400); canvas.line(20, 20, 200, 120, color="tomato", line_width=4)
    Shapes: line(x1, y1, x2, y2), rect(x, y, width, height, round=), circle(x, y, radius), ellipse(x, y, radius_x, radius_y),
    polyline(points), polygon(points), text(x, y, text, font_size=, bold=, align=), image(x, y, width, height, picture).
    The look: color (the line), fill, line_width, dash=[6, 4], opacity, draggable=True. Each returns the key of the shape.
    update_shape(key, x=..., fill=...), move_shape(key, dx, dy), remove_shape(key), bring_to_front(key), clear().
    canvas.shapes (copies) and canvas.shape(key) are kept in Python. on_click(canvas, x, y, shape): shape is None on an
    empty place. drawing=True: the mouse draws free lines with the pen (set_pen(color, width)); on_draw_end(canvas, shape).
    A draggable shape is moved by the page: on_shape_move(canvas, shape) at the end (a move of the mouse is not sent).
    save_image("drawing.png"). style_name / theme: "light", "dark"."""

    _type = "Canvas"
    _setters = dict(_ThemedComponent._setters, drawing="set_drawing", shapes="set_shapes")

    def __init__(self, *position, **params):
        object.__setattr__(self, "_shape_of_key", {})
        object.__setattr__(self, "_next_key_number", 1)
        object.__setattr__(self, "_on_draw_end", params.pop("on_draw_end", None))
        object.__setattr__(self, "_on_shape_move", params.pop("on_shape_move", None))
        object.__setattr__(self, "_on_click", params.pop("on_click", None))
        shapes = [self._keep_shape(shape) for shape in params.pop("shapes", [])]
        params["shapes"] = [_shape_for_page(shape) for shape in shapes]
        params["on_draw_end"] = self._draw_ended
        params["on_shape_move"] = self._shape_moved
        if self._on_click:
            params["on_click"] = self._clicked
        super().__init__(*position, **params)

    # *** THE SHAPES IN PYTHON:

    def _free_key(self):
        # WHY "p": the page names its free lines "s1", "s2"...: a key of Python is never one of them.
        while f"p{self._next_key_number}" in self._shape_of_key:
            object.__setattr__(self, "_next_key_number", self._next_key_number + 1)
        return f"p{self._next_key_number}"

    def _keep_shape(self, shape):
        """A copy of a shape with its Python names and a key, kept in Python."""
        kept = {_snake_case(name): value for name, value in shape.items()}
        kept["key"] = self._free_key() if kept.get("key") is None else str(kept["key"])
        if kept["key"] in self._shape_of_key:
            raise ValueError(f"Canvas: there is a shape with the key {kept['key']!r} already")
        if "points" in kept:
            kept["points"] = [list(point) for point in kept["points"]]
        self._shape_of_key[kept["key"]] = kept
        return kept

    def _from_page(self, shape):
        return {_snake_case(name): value for name, value in shape.items()}

    def _draw_ended(self, canvas, shape):
        kept = self._from_page(shape)
        self._shape_of_key[kept["key"]] = kept
        if self._on_draw_end:
            call_with_count(self._on_draw_end, positional_count(self._on_draw_end), [self, dict(kept)])

    def _shape_moved(self, canvas, shape):
        kept = self._from_page(shape)
        if kept["key"] in self._shape_of_key:
            self._shape_of_key[kept["key"]].update(kept)
        if self._on_shape_move:
            call_with_count(self._on_shape_move, positional_count(self._on_shape_move), [self, dict(kept)])

    def _clicked(self, canvas, x, y, shape):
        found = self._from_page(shape) if shape else None
        call_with_count(self._on_click, positional_count(self._on_click), [self, x, y, found])

    @property
    def shapes(self):
        return [_copy_of_shape(shape) for shape in self._shape_of_key.values()]

    def shape(self, key):
        """A copy of one shape, or None."""
        shape = self._shape_of_key.get(str(key))
        return _copy_of_shape(shape) if shape else None

    # *** ADDING SHAPES:

    def add_shape(self, shape):
        """A shape as a dict: {"type": "rect", "x": 10, "y": 10, "width": 80, "height": 40, "fill": "gold"}. Returns its key."""
        if shape.get("type") not in _SHAPE_TYPES:
            raise ValueError(f"Canvas: a shape needs a type: {', '.join(_SHAPE_TYPES)}")
        kept = self._keep_shape(shape)
        self.call("addShape", _shape_for_page(kept))
        return kept["key"]

    def line(self, x1, y1, x2, y2, **look):
        return self.add_shape(dict(look, type="line", x1=x1, y1=y1, x2=x2, y2=y2))

    def rect(self, x, y, width, height, **look):
        return self.add_shape(dict(look, type="rect", x=x, y=y, width=width, height=height))

    def circle(self, x, y, radius, **look):
        return self.add_shape(dict(look, type="circle", x=x, y=y, radius=radius))

    def ellipse(self, x, y, radius_x, radius_y, **look):
        return self.add_shape(dict(look, type="ellipse", x=x, y=y, radius_x=radius_x, radius_y=radius_y))

    def polyline(self, points, **look):
        return self.add_shape(dict(look, type="polyline", points=points))

    def polygon(self, points, **look):
        return self.add_shape(dict(look, type="polygon", points=points))

    def text(self, x, y, text, **look):
        return self.add_shape(dict(look, type="text", x=x, y=y, text=str(text)))

    def image(self, x, y, width, height, picture, **look):
        """picture: a path, bytes, a Pillow image, a matplotlib figure or an address (picture_address())."""
        return self.add_shape(dict(look, type="image", x=x, y=y, width=width, height=height, image_file=picture))

    # *** CHANGING SHAPES:

    def _shape_or_error(self, key):
        shape = self._shape_of_key.get(str(key))
        if shape is None:
            raise KeyError(f"Canvas: no shape with the key {key!r}")
        return shape

    def update_shape(self, key, **changes):
        shape = self._shape_or_error(key)
        shape.update({_snake_case(name): value for name, value in changes.items()})
        return self.call("updateShape", shape["key"], _shape_for_page(changes))

    def move_shape(self, key, dx, dy):
        _move_shape_by(self._shape_or_error(key), dx, dy)
        return self.call("moveShape", str(key), dx, dy)

    def remove_shape(self, key):
        del self._shape_of_key[self._shape_or_error(key)["key"]]
        return self.call("removeShape", str(key))

    def bring_to_front(self, key):
        shape = self._shape_or_error(key)
        del self._shape_of_key[shape["key"]]
        self._shape_of_key[shape["key"]] = shape
        return self.call("bringToFront", shape["key"])

    def set_shapes(self, shapes):
        self._shape_of_key.clear()
        kept = [self._keep_shape(shape) for shape in shapes]
        return self.call("setShapes", [_shape_for_page(shape) for shape in kept])

    def clear(self):
        return self.set_shapes([])

    # *** THE PEN AND THE PICTURE:

    def set_drawing(self, is_on):
        self._keep("drawing", bool(is_on))
        return self.call("setDrawing", int(bool(is_on)))

    def set_pen(self, color=None, width=None):
        """The pen of the free lines; None keeps that one."""
        return self.call("setPen", color, width)

    def save_image(self, path):
        """Writes the drawing on its ground into a file: .png or .jpg (a question to the page)."""
        is_jpeg = str(path).lower().endswith((".jpg", ".jpeg"))
        address = self.ask("getImage", "image/jpeg" if is_jpeg else "image/png")
        if not address:
            raise ValueError("Canvas.save_image(): the page can not read a picture of another site in the drawing")
        with open(path, "wb") as file:
            file.write(base64.b64decode(address.split(",", 1)[1]))


_SHAPE_TYPES = ("line", "rect", "circle", "ellipse", "polyline", "polygon", "text", "image")


def _shape_for_page(shape):
    """A shape as the page names its keys (line_width -> lineWidth), its picture as an address."""
    page_shape = {camel_case(name): value for name, value in shape.items()}
    if "imageFile" in page_shape:
        page_shape["imageFile"] = picture_address(page_shape["imageFile"])
    if "points" in page_shape:
        page_shape["points"] = [list(point) for point in page_shape["points"]]
    return page_shape


def _copy_of_shape(shape):
    copy = dict(shape)
    if "points" in copy:
        copy["points"] = [list(point) for point in copy["points"]]
    return copy


def _move_shape_by(shape, dx, dy):
    """The same move as on the page: every type keeps its places in its own keys."""
    if shape["type"] == "line":
        for name, step in (("x1", dx), ("y1", dy), ("x2", dx), ("y2", dy)):
            shape[name] = shape[name] + step
    elif "points" in shape:
        shape["points"] = [[x + dx, y + dy] for x, y in shape["points"]]
    else:
        shape["x"] = shape["x"] + dx
        shape["y"] = shape["y"] + dy


_LARGEST_EXACT_NUMBER = 2 ** 53  # WHY: a bigger whole number changes on the page, and a number to look at must be right


def _json_for_page(value, parents=()):
    """A Python value as a JsonView shows it. WHY not an error as in to_page(): a value to look at must not stop the program:
    a date, a set or an object of yours is shown as its text."""
    if value is None or isinstance(value, (str, bool, float)):
        return value
    if isinstance(value, int):
        return value if abs(value) <= _LARGEST_EXACT_NUMBER else str(value)
    if id(value) in parents:
        return "<the same object again>"
    parents = parents + (id(value),)
    if isinstance(value, dict):
        return {str(key): _json_for_page(item, parents) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_for_page(item, parents) for item in value]
    if isinstance(value, (set, frozenset)):
        return [_json_for_page(item, parents) for item in sorted(value, key=str)]
    if hasattr(value, "to_dict"):  # pandas: the names of the rows stay
        return _json_for_page(value.to_dict(), parents)
    if hasattr(value, "tolist"):  # numpy
        return _json_for_page(value.tolist(), parents)
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return _json_for_page(dataclasses.asdict(value), parents)
    if isinstance(value, (datetime.date, datetime.time)):
        return value.isoformat()
    return str(value)


class JsonView(_ThemedComponent):
    """A value as a tree: the answer of a server, a dictionary of your program: JsonView(value={"name": "Ada", "tags": ["a"]}).
    Keys and values in colors. A branch is made when it opens and a long list comes in pages, so a list of a million items
    opens at once. A date, a set or an object of yours is shown as its text. expand_level: how many levels are open at the start.
    on_select(view, entry): a row was clicked: entry["pathText"] (users[0].name), entry["path"], entry["kind"], entry["value"]
    (None for a branch: a dict, a list, or a page of one longer than page_size, 100; the page does not send them).
    view.selected_value is the value of the selected row, a branch too (a page: the whole dict or list it is part of);
    view.selected_path, selected_path_text. select_path(["users", 0, "name"]) opens the rows down to it.
    Right click or Ctrl+C: its value or its path goes to the clipboard; on_copy(view, text). set_json_text(text): a text that
    is not JSON shows its error and returns False. expand_all(), collapse_all(). height: none: it fills its group; a number;
    "auto": it grows with its rows. style_name / theme: "light", "dark"."""

    _type = "JsonView"
    _state = {"selectedPath": "getSelectedPath()", "selectedPathText": "getSelectedPathText()"}
    _setters = dict(_ThemedComponent._setters, value="set_value")
    _sync_callbacks = ("on_select",)
    _state_defaults = {"selectedPath": None, "selectedPathText": ""}

    def __init__(self, *position, **params):
        value = params.pop("value", None)
        page_value = _json_for_page(value)
        if page_value is not None:
            params["value"] = page_value
        super().__init__(*position, **params)
        self._value = value
        self._page_value = page_value

    def _keep_value(self, value, page_value):
        self._value = value
        self._page_value = page_value
        self._keep("selectedPath", None)
        self._keep("selectedPathText", "")

    @property
    def value(self):
        """As it was given."""
        return self._value

    def set_value(self, value):
        page_value = _json_for_page(value)
        self._keep_value(value, page_value)
        return self.call("setValue", page_value)

    def set_json_text(self, text):
        """True: it is drawn. False: it is not JSON, and its error is on the view."""
        try:
            value = json.loads(text)
        except ValueError:
            self._keep_value(None, None)
            self.call("setJsonText", text)
            return False
        self.set_value(value)
        return True

    @property
    def selected_path(self):
        """["users", 0, "name"], or None: no row is selected."""
        return self._values.get("selectedPath")

    @property
    def selected_path_text(self):
        """users[0].name"""
        return self._values.get("selectedPathText", "")

    @property
    def selected_value(self):
        """The value of the selected row as it is shown (a date is its text), a branch too; a page of a long dict or list:
        all of it. None: no row is selected, or its value is None."""
        path = self.selected_path
        if path is None:
            return None
        value = self._page_value
        for part in path:
            value = value[part]
        return value

    def select_path(self, path):
        """on_select is not called."""
        return self._call_and_refresh("selectPath", list(path))

    def expand_all(self):
        """Up to 3000 rows and 20 levels."""
        return self.call("expandAll")

    def collapse_all(self):
        return self.call("collapseAll")


# The function params of a JsonEditor that can not be Python functions, and why
_EDITOR_PAGE_FUNCTIONS = {
    "colorOf": "the page asks it while it paints a swatch, and a Python function answers later",
    "optionsOf": "the page asks it while it opens a cell, and a Python function answers later. The choices of a value: "
                 'columns=[{"key": "size", "options": ["S", "M", "L"]}]',
    "onPickColor": "its cell is written with a function of the page (cell.setValue), which can not go to Python. Without it a "
                   "color cell opens the color picker of the web view",
    "onPickPicture": "its cell is written with a function of the page (cell.setValue), which can not go to Python. Without it "
                     "the address of a picture is written in its cell",
}
_EDITOR_WINDOW_CALLBACKS = ("onApply", "onCancel")  # given as they are; onClose keeps is_open first


def _json_for_editor(value, where, parents=()):
    """A Python value as a JsonEditor takes it: JSON data, as the json module writes it (a tuple is a list, a key a text).
    A whole number bigger than 2**53 goes as its text, as in a JsonView: the page would round it.
    WHY not a date as its text (a JsonView shows it so): an editor gives its value back, and the date would come back as
    a text without a word. The json module refuses it too."""
    if value is None or isinstance(value, (str, bool, float)):
        return value
    if isinstance(value, int):
        return value if abs(value) <= _LARGEST_EXACT_NUMBER else str(value)
    if id(value) in parents:
        raise ValueError(f"{where}: the value holds itself, and JSON can not")
    parents = parents + (id(value),)
    if isinstance(value, dict):
        return {str(key): _json_for_editor(item, where, parents) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_for_editor(item, where, parents) for item in value]
    if hasattr(value, "tolist"):  # numpy
        return _json_for_editor(value.tolist(), where, parents)
    raise TypeError(f"{where}: a {type(value).__name__} is not JSON: a JsonEditor takes texts, numbers, True / False, None, "
                    "lists and dicts")


def _value_for_editor(value, where):
    """The value of a JsonEditor: a list or a dict, or its JSON text (read here, so its fault is told at its line).
    WHY not as the page does (anything else is an empty list): the data of the program would be gone without a word."""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError as error:
            raise ValueError(f"{where}: the text is not JSON: {error}") from None
    page_value = _json_for_editor(value, where)
    if not isinstance(page_value, (list, dict)):
        raise TypeError(f"{where}: a list or a dict is needed (or its JSON text), not {page_value!r}")
    return page_value


def _editor_params(params, where):
    """The params of a JsonEditor (or of its window) that Python checks or changes before they go to the page."""
    for name, value in params.items():
        why = _EDITOR_PAGE_FUNCTIONS.get(camel_case(name))
        if why and callable(value):
            raise TypeError(f"{where}: {name}= can not be a Python function: {why}")
    if params.get("value") is not None:
        params["value"] = _value_for_editor(params["value"], f"{where}: value")
    if isinstance(params.get("texts"), dict):
        # WHY: the keys of the kit are camelCase (addRow); in Python they are written as names are (add_row)
        params["texts"] = {camel_case(str(key)): text for key, text in params["texts"].items()}


class JsonEditor(TypedComponent):
    """A list or a dict of JSON written in a table: the items of a menu, the products of a shop, the settings of a program:
    JsonEditor(value=[{"name": "Apple", "price": 1.2, "in_stock": True}], height=360, on_change=fn).
    + adds a row, a click on a cell writes in it, a title sorts, the dots of a row drag it. A dict is a table of names and
    values; a cell that holds a list or a dict opens as a table of its own. The kind of a column comes from its values and
    its name (a text, a number, on / off, a color, a picture); columns=[{"key": "unit", "options": ["kg", "piece"]}] gives the
    choices of a cell (a column: key, kind, options, note, columns). Rows pasted from a spreadsheet or as a JSON list, its own
    undo (Cmd/Ctrl+Z), a search, a JSON view (Table | JSON). texts={"add_row": "Satır"}: its own texts.
    value: a list or a dict, or its JSON text; JSON data only (a date is refused: it would come back as a text). A whole
    number bigger than 2**53 goes as its text. on_change(editor, value): a change in the table, with the whole value (not
    at create time, not with set_value()). editor.value asks the page: a cell being written is written first; None: the table
    can not make a value now (a name used twice), editor.error_text says why. set_value(), set_json_text(text) (False: not
    JSON, its error is on the editor), get_json_text(), editor.view = "json" ("table"), undo(), redo(), has_changes(),
    set_title_text(title_text, note_text), focus(). style_name: "light", "dark", "minimal", "minimalDark".
    JsonEditor.open(value=..., on_apply=fn): the editor in a window over the page, with Cancel and Apply.
    NOTE: color_of, options_of, on_pick_color and on_pick_picture take a function of the page, not a Python function."""

    _type = "JsonEditor"
    _setters = {"value": "set_value", "title_text": "set_title_text", "note_text": "_set_note_text", "view": "set_view"}
    _whole_args = {"onChange": (1,)}

    def _prepare_params(self, params):
        _editor_params(params, f"{type(self).__name__}()")
        super()._prepare_params(params)

    @property
    def value(self):
        """The list or the dict of the table now (a question to the page). A cell being written is written first, and the
        text of the JSON view goes into the table. None: the table can not make one now (error_text says why)."""
        text = self.ask("getJsonText")
        return json.loads(text) if text else None

    @property
    def error_text(self):
        """Why the table could not make a value ("": it could): a row of a dict with no name, a name used twice."""
        return self.measure("errorText") or ""

    def set_value(self, value):
        """A new list or dict (or its JSON text). Its undo starts again; on_change is not called."""
        return self.call("setValue", _value_for_editor(value, f"{type(self).__name__}.set_value()"))

    def set_json_text(self, text):
        """True: it is in the table. False: it is not JSON, or not a list or a dict: its error is on the editor."""
        try:
            data = json.loads(text)
        except ValueError:
            data = None
        if not isinstance(data, (list, dict)):
            self.call("setJsonText", text)
            return False
        self.set_value(data)
        return True

    def get_json_text(self):
        """The value as a JSON text of 2 spaces, as the page writes it. "": the table can not make a value now."""
        return self.ask("getJsonText") or ""

    @property
    def view(self):
        """"table" or "json" (a question to the page: its Table | JSON switch changes it too)."""
        return self.ask("getView")

    def set_view(self, view):
        """"table" or "json". False: the text of the JSON view is not right; it stays, and the bottom bar says why."""
        return bool(self.ask("setView", view))

    def undo(self):
        return self.call("undo")

    def redo(self):
        return self.call("redo")

    def has_changes(self):
        """True: something was changed since the value was given (also a text written in the JSON view)."""
        return bool(self.ask("hasChanges"))

    def set_title_text(self, title_text, note_text=None):
        """The name of the value at the start of the path, and the soft line under it (None: the note stays)."""
        self._keep("title_text", title_text)
        if note_text is None:
            return self.call("setTitleText", title_text)
        self._keep("note_text", note_text)
        return self.call("setTitleText", title_text, note_text)

    def _set_note_text(self, note_text):
        return self.set_title_text(self._values.get("titleText", ""), note_text)

    def focus(self):
        """The keys go to the table."""
        return self.call("focus")

    @staticmethod
    def open(**params):
        """The editor in a window over the page, with Cancel and Apply: JsonEditor.open(title_text="The menu", value=items,
        on_apply=save). Cmd/Ctrl+Enter applies; Esc and Cancel close it (when something was changed, at the second press).
        on_apply(value): Apply, when something was changed (the whole value). on_cancel(): Cancel. on_close(): the window
        closed (also after Apply and close()). The other params are the params of JsonEditor.
        Returns the window: window.editor is its JsonEditor, window.close() closes it, window.is_open."""
        return _JsonEditorWindow(params)

    @classmethod
    def _made_by_the_page(cls, window, values):
        """The JsonEditor of a window: the page made it (JsonEditor.open), so no create command goes; its methods work."""
        editor = cls.__new__(cls)
        app = window._app
        editor._init_proxy(app, _new_id(), {key: value for key, value in values.items() if not callable(value)})
        app._register(editor)
        app._send({"op": "part", "id": editor._id, "of": window._id, "path": ["editor"], "src": source_line()})
        return editor


class _JsonEditorWindow(BasicObject):
    """The window of JsonEditor.open() (the cover over the page, made by the page): window.editor, window.close(),
    window.is_open."""

    _type = "JsonEditor"
    _callback_params = True
    _whole_args = {"onChange": (1,), "onApply": (0,)}

    def __init__(self, params):
        app = _app.current_app()
        where = "JsonEditor.open()"
        self._init_proxy(app, _new_id(), {})
        app._register(self)
        self._is_open = True
        _editor_params(params, where)
        window_names = _EDITOR_WINDOW_CALLBACKS + ("onClose",)
        _warn_about_unknown_names(self._type, [name for name in params if camel_case(name) not in window_names])
        values = {camel_case(name): value for name, value in params.items()}
        self._on_close = values.pop("onClose", None)
        callbacks = {name: values.pop(name, None) for name in _EDITOR_WINDOW_CALLBACKS}
        callbacks = {name: handler for name, handler in callbacks.items() if handler is not None}
        Component._take_window_theme(self._type, values)
        values = {camel_case(name): value for name, value in values.items()}  # WHY again: the theme gives style_name
        for name, value in values.items():
            if isinstance(value, bool) and name not in TypedComponent._data_params:
                values[name] = int(value)  # WHY: as TypedComponent gives them (the page compares showHint == 1)
        page_values = self._page_values(dict(values, onClose=self._closed, **callbacks), where)
        app._call_static("JsonEditor", "open", [page_values], keep=self._id)
        self._editor = JsonEditor._made_by_the_page(self, values)

    @property
    def editor(self):
        """The JsonEditor of the window: editor.value, editor.undo()..."""
        return self._editor

    @property
    def is_open(self):
        return self._is_open

    def close(self):
        """Closes it without a question; on_close runs (on_apply and on_cancel do not)."""
        if not self._is_open:
            return
        self._is_open = False
        self.call("close")

    def remove(self):
        self.close()

    def _closed(self):
        self._is_open = False
        if self._on_close:
            call_with_count(self._on_close, positional_count(self._on_close), [])


_MARKDOWN_PICTURE =re.compile(r"!\[([^\]]*)\]\(\s*([^()\s]+)\s*\)")
_WEB_ADDRESS = re.compile(r"^(https?|data|about|blob):", re.IGNORECASE)  # the page opens it; anything else is a file


def _is_web_address(address):
    return isinstance(address, str) and bool(_WEB_ADDRESS.match(address))


def _html_of_file(path):
    """The text of an HTML file of this computer (a path, a Path or a file:// address).
    WHY its text and not its address: the web view opens no file outside the folder of the page of OzdenUI."""
    path = os.fspath(path)
    if path.startswith("file:"):
        path = urllib.request.url2pathname(urllib.parse.urlparse(path).path)
    with open(path, encoding="utf-8", errors="replace") as file:
        return file.read()


class WebView(TypedComponent):
    """A web page or an HTML text in a box: WebView(url="https://example.com", height=400), WebView(html=fig.to_html()).
    The HTML of other libraries runs in it with its scripts: a plotly chart (fig.to_html()), a folium map
    (m.get_root().render()), a pandas table (df.to_html()); a script or a picture from the internet needs a connection.
    url: a web address, or a path of this computer (its text is shown: a picture or a style next to the file is not
    loaded; give them as https:// or data: addresses). load(address), load_html(html), load_file(path), reload(), clear().
    on_load(view). on_error(view): a page that is not there. load_timeout=15 (seconds), on_timeout(view): a page that does
    not come. on_message(view, data): the page sends with window.parent.postMessage(data, "*"); post_message(data) sends
    to it. auto_height=True: the box grows with the page (an HTML text). scale=0.5: a smaller copy; interactive=False:
    the page can not be clicked, on_click(view) runs instead. toolbar=True: the address, reload and "open in the browser".
    A site may refuse to be shown in a frame (its own rule). It has one look, also in a dark window."""

    _type = "WebView"
    _aliases = {"html": "html_text"}
    _setters = {"url": "load", "html_text": "load_html", "html": "load_html", "scale": "set_scale",
                "interactive": "set_interactive", "auto_height": "set_auto_height"}

    def __init__(self, *position, **params):
        url = params.get("url")
        if url and not _is_web_address(url):
            params.pop("url")
            params["html_text"] = _html_of_file(url)
        super().__init__(*position, **params)

    def load(self, address):
        """A web address (https://...), or a path of this computer: its text is shown (load_file). "": nothing."""
        if address and not _is_web_address(address):
            return self.load_file(address)
        self._keep("url", address or "")
        self._keep("htmlText", "")
        return self.call("load", address or "")

    def load_html(self, html):
        """An HTML text as the page (with its scripts)."""
        self._keep("htmlText", html or "")
        self._keep("url", "")
        return self.call("loadHtml", html or "")

    def load_file(self, path):
        """An HTML file of this computer: its text is shown."""
        return self.load_html(_html_of_file(path))

    def reload(self):
        return self.call("reload")

    def clear(self):
        """Nothing is shown (its empty text)."""
        return self.load("")

    def post_message(self, data):
        """Sends data (JSON) to the page: window.addEventListener("message", (event) => event.data) in it."""
        return self.call("postMessage", data, "*")

    def set_scale(self, scale):
        self._keep("scale", scale)
        return self.call("setScale", scale)

    def set_interactive(self, interactive):
        self._keep("interactive", int(bool(interactive)))
        return self.call("setInteractive", int(bool(interactive)))

    def set_auto_height(self, auto_height):
        self._keep("autoHeight", int(bool(auto_height)))
        return self.call("setAutoHeight", int(bool(auto_height)))

    def show_error(self, text):
        """A message of yours over the page ("The report could not be made.")."""
        return self.call("showError", text)

    def hide_error(self):
        return self.call("hideError")


_ANY_ADDRESS = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.-]*:|//)")


def _markdown_for_page(text, folder):
    """![A plot](plot.png): a file of this computer goes to the page as a data: address. WHY: the web view refuses a
    file:// picture outside the folder of the page. The picture of a file that is not there stays as it is written."""

    def address_of(match):
        description, address = match.groups()
        if _ANY_ADDRESS.match(address):
            return match.group(0)
        path = os.path.join(folder or os.getcwd(), address)
        if not os.path.isfile(path):
            return match.group(0)
        return f"![{description}]({picture_address(path)})"

    return _MARKDOWN_PICTURE.sub(address_of, text)


class MarkdownView(_ThemedComponent):
    """A text written in Markdown, drawn on the page: a report, the answer of an AI:
    MarkdownView(text="# A title\n\nSome **bold** words"). Headings, lists, check marks, quotes, tables, links, pictures,
    code with colors and a button that copies it. A text is never read as HTML, and no script of it runs.
    view.text, set_text(text), clear(), load_file("report.md"). append_text(piece): a text that comes piece by piece, from
    a background job too: what is above stays, and the view follows the end until the reader scrolls up.
    A picture: ![A plot](plot.png), a file in picture_folder (default: the folder the program runs in) or next to the file
    of load_file(); a matplotlib figure: f"![A plot]({picture_address(figure)})". A picture with an http address stays a
    link, because its address can carry data and its server sees that the text was opened: a text you trust: remote_pictures=True.
    on_link_click(view, address): a link comes to you; without it the browser of the computer opens it. A link to
    "#a-heading" goes to that heading. view.headings, scroll_to_heading(id), scroll_to_top(), scroll_to_end().
    height: none: it fills its group; a number; "auto": it grows with its text. empty_text. style_name / theme: "light", "dark"."""

    _type = "MarkdownView"
    _setters = dict(_ThemedComponent._setters, text="set_text", markdown_text="set_text", empty_text="set_empty_text",
                    auto_scroll="set_auto_scroll")

    def __init__(self, *position, picture_folder=None, text=None, **params):
        # WHY a name of its own: text is the short name of markdown_text, not the text of the box of the view
        markdown_text = params.pop("markdown_text", "")
        text = markdown_text if text is None else text
        text = "" if text is None else str(text)
        params["markdown_text"] = _markdown_for_page(text, picture_folder)
        super().__init__(*position, **params)
        self._text = text
        self._picture_folder = picture_folder

    @property
    def text(self):
        """As it was written: the pictures of this computer with their file names."""
        return self._text

    def set_text(self, text):
        """The scroll stays where it is. A new document: scroll_to_top() after it."""
        self._text = "" if text is None else str(text)
        return self.call("setMarkdownText", _markdown_for_page(self._text, self._picture_folder))

    def append_text(self, piece):
        """The next piece of the text. WHY the piece is sent, not the whole text: a long answer comes in many pieces."""
        piece = "" if piece is None else str(piece)
        self._text += piece
        return self.call("appendText", _markdown_for_page(piece, self._picture_folder))

    def clear(self):
        return self.set_text("")

    def load_file(self, path):
        """A Markdown file (UTF-8), with the pictures next to it. The view goes to its top."""
        with open(path, encoding="utf-8") as file:
            text = file.read()
        self._picture_folder = os.path.dirname(os.path.abspath(path))
        self.set_text(text)
        return self.scroll_to_top()

    @property
    def headings(self):
        """[{"id", "level", "text"}]: for a list of the headings next to the text."""
        return self.ask("getHeadings")

    def scroll_to_heading(self, heading_id):
        return self.call("scrollToHeading", heading_id)

    def scroll_to_top(self):
        return self.call("scrollToTop")

    def scroll_to_end(self):
        """It goes to the end, and follows again."""
        return self.call("scrollToEnd")

    def set_empty_text(self, text):
        self._keep("emptyText", text)
        return self.call("setEmptyText", text)

    def set_auto_scroll(self, value):
        self._keep("autoScroll", int(bool(value)))
        return self.call("setAutoScroll", int(bool(value)))


_CHAT_ROLES = ("user", "assistant", "system")


class ChatView(_ThemedComponent):
    """A conversation with an AI: ChatView(height=500, empty_text="Ask something", on_send=answer). The messages of the
    user are bubbles on the right; an answer is Markdown (headings, lists, tables, code with a button that copies it).
    on_send(chat, text): the user sent a text (Enter; Shift+Enter makes a new line): its message is on the view already.
    Answer it piece by piece, from a background job too:

        def answer(chat, text):
            key = chat.add_message(role="assistant")
            chat.busy = True  # three dots until the first words, and Stop in the place of Send
            run_in_background(write_answer, chat, key, text)  # chat.append_text(key, piece)..., then chat.busy = False

    on_stop(chat): Stop was pressed (chat.busy is False already): stop your answer. A message: {"key", "role", "text"},
    role "user", "assistant" (default) or "system" (a soft line in the middle). chat.messages: copies, kept in Python.
    add_message(text="", role="assistant", key=None) returns its key; append_text(key, piece), set_message_text(key, text),
    message_text(key), remove_message(key), clear(), set_messages([...]). send() sends the text of the field,
    chat.input_text asks the page for it, set_input_text(), focus(). show_input=False: only the messages.
    A picture of an answer: as in a MarkdownView (picture_folder). style_name / theme: "light", "dark", "minimal",
    "minimalDark" (a minimal window takes them: small, made of lines)."""

    _type = "ChatView"
    _state = {"busy": "busy"}  # WHY: Stop changes it on the page
    _sync_callbacks = ("on_stop",)
    _setters = dict(_ThemedComponent._setters, busy="set_busy", messages="set_messages", empty_text="set_empty_text",
                    placeholder="set_placeholder", show_input="set_show_input", input_text="set_input_text")

    def __init__(self, *position, picture_folder=None, **params):
        object.__setattr__(self, "_messages", [])
        object.__setattr__(self, "_next_key_number", 1)
        object.__setattr__(self, "_picture_folder", picture_folder)
        object.__setattr__(self, "_on_send", params.pop("on_send", params.pop("onSend", None)))
        params["messages"] = [self._message_for_page(self._keep_message(message)) for message in params.pop("messages", [])]
        params["on_send"] = self._sent
        super().__init__(*position, **params)

    # *** THE MESSAGES IN PYTHON:

    def _free_key(self):
        """A key no message had: "p1", "p2"...
        WHY "p": the page names the messages the user sends "m1", "m2"...: a key of Python is never one of them.
        WHY never again after clear(): an answer still coming from a background job would write into a new message."""
        keys = {message["key"] for message in self._messages}
        while f"p{self._next_key_number}" in keys:
            object.__setattr__(self, "_next_key_number", self._next_key_number + 1)
        key = f"p{self._next_key_number}"
        object.__setattr__(self, "_next_key_number", self._next_key_number + 1)
        return key

    def _keep_message(self, message, role="assistant", key=None):
        """A message as Python keeps it: {"key", "role", "text"}. A text alone is an answer."""
        if isinstance(message, dict):
            text, role, key = message.get("text", ""), message.get("role", role), message.get("key", key)
        else:
            text = message
        if role not in _CHAT_ROLES:
            raise ValueError(f"ChatView: the role of a message is one of {', '.join(_CHAT_ROLES)}, not {role!r}")
        kept = {"key": self._free_key() if key is None else str(key), "role": role, "text": "" if text is None else str(text)}
        self._messages.append(kept)
        return kept

    def _message_for_page(self, message):
        if message["role"] != "assistant":
            return dict(message)
        return dict(message, text=_markdown_for_page(message["text"], self._picture_folder))

    def _find(self, key):
        key = str(key)
        return next((message for message in self._messages if message["key"] == key), None)

    @property
    def messages(self):
        """[{"key", "role", "text"}]: copies, in order."""
        return [dict(message) for message in self._messages]

    def message_text(self, key):
        message = self._find(key)
        return message["text"] if message else ""

    def _sent(self, _chat, text, key):
        self._messages.append({"key": str(key), "role": "user", "text": text})
        if self._on_send:
            call_with_count(self._on_send, positional_count(self._on_send), [self, text, str(key)])

    # *** CHANGES:

    def add_message(self, text="", role="assistant", key=None):
        """A message at the end; returns its key. add_message(role="assistant"): an answer that comes (append_text)."""
        kept = self._keep_message(text, role, key)
        self.call("addMessage", self._message_for_page(kept))
        return kept["key"]

    def append_text(self, key, piece):
        """The next piece of a message (an answer as it comes); from a background job too."""
        message = self._find(key)
        if message is None or piece is None:
            return self
        piece = str(piece)
        message["text"] += piece
        if message["role"] == "assistant":
            piece = _markdown_for_page(piece, self._picture_folder)
        return self.call("appendText", message["key"], piece)

    def set_message_text(self, key, text):
        message = self._find(key)
        if message is None:
            return self
        message["text"] = "" if text is None else str(text)
        return self.call("setMessageText", message["key"], self._message_for_page(message)["text"])

    def remove_message(self, key):
        message = self._find(key)
        if message is not None:
            self._messages.remove(message)
        return self.call("removeMessage", str(key))

    def clear(self):
        """Every message goes (the field keeps its text)."""
        self._messages.clear()
        return self.call("clear")

    def set_messages(self, messages):
        """Another conversation: its end is shown."""
        self._messages.clear()
        page_messages = [self._message_for_page(self._keep_message(message)) for message in messages]
        return self.call("setMessages", page_messages)

    def set_busy(self, value):
        """True: an answer is coming: three dots until its first words, and Stop in the place of Send."""
        self._keep("busy", int(bool(value)))
        return self.call("setBusy", int(bool(value)))

    def send(self):
        """Sends the text of the field, as the button does (on_send is called)."""
        return self.call("send")

    def stop(self):
        """As the Stop button: busy becomes False, then on_stop."""
        return self.call("stop")

    @property
    def input_text(self):
        """The text of the field now (a question to the page)."""
        return self.ask("getInputText")

    def set_input_text(self, text):
        return self.call("setInputText", "" if text is None else str(text))

    def focus(self):
        """The keys go to the field."""
        return self.call("focus")

    def set_placeholder(self, text):
        self._keep("placeholder", text)
        return self.call("setPlaceholder", text)

    def set_empty_text(self, text):
        self._keep("emptyText", text)
        return self.call("setEmptyText", text)

    def set_show_input(self, value):
        self._keep("showInput", int(bool(value)))
        return self.call("setShowInput", int(bool(value)))

    def scroll_to_end(self):
        """It goes to the end, and follows again."""
        return self.call("scrollToEnd")

    def scroll_to_top(self):
        return self.call("scrollToTop")


class Accordion(_ThemedComponent):
    """Sections that fold: acc = Accordion(sections=["General", {"key": "more", "text": "Advanced", "opened": True}]);
    with acc.section("General"): Label(...). Objects go one under the other, also while a section is closed.
    A section: a text (its key too) or {"key", "text", "description", "icon_file", "icon", "opened", "enabled", "data"};
    description: a soft text at the end of its row, enabled=False: it does not open or close.
    multiple=False: a section that opens closes the others. on_toggle(acc, section): read section["key"], section["opened"],
    or acc.open_keys. height: none: it grows with its sections; a number or "100%": they scroll inside it. animated=True: the
    arrow turns and the objects fade in. arrow_side: "right" or "left". style_name / theme: "light", "dark"."""

    _type = "Accordion"
    _item_keys = ("key", "text", "description", "iconFile", "icon", "opened", "enabled", "data")
    _state = {"openKeys": "getOpenKeys()"}
    _setters = dict(_ThemedComponent._setters, sections="set_sections", enabled="set_enabled", animated="set_animated")
    _sync_callbacks = ("on_toggle",)
    _state_defaults = {"openKeys": []}

    def __init__(self, *position, **params):
        sections = _list_for_page(type(self), params.get("sections", []))
        if "sections" in params:
            params["sections"] = sections
        super().__init__(*position, **params)
        self._contents = {}
        self._keep_open_keys(self._opened_at_start(sections))

    def _opened_at_start(self, sections):
        """As the page: with multiple=False only the first open section stays open."""
        keys = [section.get("key", section.get("text")) for section in sections if isinstance(section, dict) and section.get("opened")]
        return keys if self._values.get("multiple", 1) else keys[:1]

    def _keep_open_keys(self, keys):
        self._keep("openKeys", keys)

    @property
    def open_keys(self):
        return list(self._values.get("openKeys", []))

    def section(self, key):
        """The place of the objects of a section: with acc.section("General"): Label(...)"""
        if key not in self._contents:
            self._contents[key] = self.part({"call": "getContent", "args": [key]})
        return self._contents[key]

    def open(self, key):
        """on_toggle is not called. With multiple=False the others close."""
        keys = self.open_keys if self._values.get("multiple", 1) else []
        self._keep_open_keys(keys + [key] if key not in keys else keys)
        return self._call_and_refresh("open", key, 1)

    def close(self, key):
        self._keep_open_keys([other for other in self.open_keys if other != key])
        return self._call_and_refresh("close", key, 1)

    def toggle(self, key):
        return self.close(key) if self.is_open(key) else self.open(key)

    def is_open(self, key):
        return key in self.open_keys

    def open_all(self):
        """Only with multiple=True."""
        return self._call_and_refresh("openAll", 1)

    def close_all(self):
        self._keep_open_keys([])
        return self._call_and_refresh("closeAll", 1)

    def add_section(self, section):
        return self._call_and_refresh("addSection", _list_for_page(type(self), [section])[0])

    def remove_section(self, key):
        self._contents.pop(key, None)
        self._keep_open_keys([other for other in self.open_keys if other != key])
        return self.call("removeSection", key)

    def set_sections(self, sections):
        """New sections in the place of all of them (their objects go too)."""
        self._contents.clear()
        self._keep("sections", sections)
        return self._call_and_refresh("setSections", _list_for_page(type(self), sections))

    def set_section_text(self, key, text):
        return self.call("setSectionText", key, text)

    def set_section_description(self, key, text):
        return self.call("setSectionDescription", key, text)

    def set_section_enabled(self, key, value):
        return self.call("setSectionEnabled", key, int(bool(value)))

    def set_enabled(self, value):
        self._keep("enabled", int(bool(value)))
        return self.call("setEnabled", int(bool(value)))

    def set_animated(self, value):
        self._keep("animated", int(bool(value)))
        return self.call("setAnimated", int(bool(value)))

    def focus(self, key=None):
        return self.call("focus", key)


class SidePanel(TypedComponent):
    """A panel that slides in from a side of the window, over the page: panel = SidePanel(title_text="Filters");
    with panel.body: CheckBox(...); then panel.open() and panel.close(). side: "right" (default), "left", "top", "bottom";
    panel_size: px. It is made on the page, wherever the code makes it. A click on its cover or Escape closes it, so
    panel.is_open is kept in Python. on_open(panel), on_close(panel).
    style_name: "light" (default), "modern", "dark"."""

    _type = "SidePanel"
    _state = {"isOpened": "isOpened"}
    _setters = {"title_text": "set_title"}
    _sync_callbacks = ("on_open", "on_close")

    def __init__(self, *position, **params):
        super().__init__(*position, **params)
        object.__setattr__(self, "_body", None)
        self._keep("isOpened", int(bool(params.get("opened", 0))))

    @property
    def body(self):
        """The place of its objects, one under the other: with panel.body: Label(...)"""
        if self._body is None:
            object.__setattr__(self, "_body", self.part({"call": "getBody"}))
        return self._body

    @property
    def is_open(self):
        return bool(self._values.get("isOpened", 0))

    def open(self):
        """on_open runs when it has come in."""
        self._keep("isOpened", 1)
        return self.call("open")

    def close(self):
        self._keep("isOpened", 0)
        return self.call("close")

    def toggle(self):
        return self.close() if self.is_open else self.open()

    def set_title(self, text):
        self._keep("titleText", text)
        return self.call("setTitleText", text)


class LoadingScreen(TypedComponent):
    """A cover while the app gets ready: loading = LoadingScreen(title_text="My App", message_text="Reading the files...");
    later loading.close(): it fades out (after min_duration ms at least, so a fast job does not blink). It covers the
    window (cover=box: that box). loading.set_message(text), loading.set_progress(0.4) (a bar; -1 hides it),
    loading.open() shows it again. spinner_type: "clock" (default), "ring", "dots", "none". remove_on_close=True: it
    goes away for good. on_close(loading) after it has faded out. style_name: "light" (default), "dark", "ozden"."""

    _type = "LoadingScreen"
    _aliases = {"title": "title_text", "message": "message_text"}

    def __init__(self, *position, cover=None, **params):
        # WHY the page: made in a "with" block it was one more object of that group, not a cover of the window
        place = cover if cover is not None else _app.current_app().page
        with place:
            super().__init__(*position, **params)

    def open(self):
        return self.call("open")

    def close(self):
        return self.call("close")

    def set_title(self, text):
        self._keep("titleText", text)
        return self.call("setTitleText", text)

    def set_message(self, text):
        self._keep("messageText", text)
        return self.call("setMessageText", text)

    def set_progress(self, value):
        """0 - 1: a progress bar under the spinner; -1 hides it."""
        self._keep("progress", value)
        return self.call("setProgress", value)


class TagInput(TypedComponent):
    """Tags in a field: TagInput(tags=["audio"], suggestions=["audio", "fitness", "guide"], on_change=fn).
    on_change(field): read field.tags (a list of texts, kept in Python). Enter or a comma ends a tag, a pasted list is
    split. allow_custom=False: only the suggestions; max_tags; lowercase=True; placeholder. In code (not calling
    on_change): field.tags = [...], field.add_tag(tag), field.remove_tag(tag), field.clear().
    style_name: "light" (default), "modern", "dark"."""

    _type = "TagInput"
    _state = {"tags": "getTags()"}
    _setters = {"tags": "set_tags", "suggestions": "set_suggestions", "enabled": "set_enabled", "placeholder": "set_placeholder"}
    _sync_callbacks = ("on_change",)

    def __init__(self, *position, **params):
        super().__init__(*position, **params)
        self._keep("tags", list(params.get("tags", [])))

    @property
    def tags(self):
        return list(self._values.get("tags", []))

    def set_tags(self, tags):
        self._keep("tags", list(tags))
        return self._call_and_refresh("setTags", list(tags), 1)

    def add_tag(self, tag):
        return self._call_and_refresh("addTag", tag, 1)

    def remove_tag(self, tag):
        return self._call_and_refresh("removeTag", tag, 1)

    def clear(self):
        self._keep("tags", [])
        return self.call("clear", 1)

    def set_suggestions(self, suggestions):
        return self.call("setSuggestions", list(suggestions))

    def set_enabled(self, enabled):
        self._keep("enabled", int(bool(enabled)))
        return self.call("setEnabled", int(bool(enabled)))

    def set_placeholder(self, text):
        self._keep("placeholder", text)
        return self.call("setPlaceholder", text)


class DataTable(TypedComponent):
    """A table that fits its texts, for up to a few hundred rows: DataTable(columns=[{"key": "name", "title": "Name"}],
    rows=[...], on_select=fn). A row is a dict (by the keys of the columns, with an "id") or a list in their order (the
    id first). on_select(table, row): the row as it was given, or None; on_row_click(table, row): a click or Enter.
    table.selected_row is kept in Python. A column: key, title, width, align, type ("number"), sortable. show_search=True:
    a search box in its head; sort_key, sort_direction. Very many rows: SmartTable.
    style_name: "light" (default), "plain", "dark"."""

    _type = "DataTable"
    _state = {"selectedRow": "getSelectedData()"}
    _sync_callbacks = ("on_select",)

    def __init__(self, *position, on_select=None, on_row_click=None, **params):
        if on_select is not None:
            params["on_select"] = self._with_row_data(on_select)
        if on_row_click is not None:
            params["on_row_click"] = self._with_row_data(on_row_click)
        super().__init__(*position, **params)
        self._keep("selectedRow", None)

    def _with_row_data(self, handler):
        """WHY: the page gives its own row (its id, its data, its cells); Python gets the row as it gave it."""
        count = positional_count(handler)

        def on_page_row(table, row):
            data = row.get("data") if isinstance(row, dict) else None
            call_with_count(handler, count, [self, data])

        return on_page_row

    @property
    def selected_row(self):
        return self._values.get("selectedRow")

    def set_rows(self, rows):
        self._keep("selectedRow", None)
        return self.call("setRows", list(rows))

    def add_row(self, row):
        return self.call("addRow", row)

    def remove_row(self, row_id):
        return self._call_and_refresh("removeRow", row_id)

    def select(self, row_id):
        """on_select is not called."""
        return self._call_and_refresh("select", row_id, 1)

    def clear_selection(self):
        self._keep("selectedRow", None)
        return self.call("clearSelection", 1)

    def sort_by(self, key, direction="asc"):
        return self.call("sortBy", key, direction)


class Dialog:
    """The dialogs of comp/dialog.js. Each one waits for its answer and returns it; the window keeps working
    meanwhile (other events and timers run). They work from a background job too."""

    @staticmethod
    def alert(message, title="", button_text="OK"):
        _show_dialog("alert", {"titleText": title, "messageText": message, "buttonText": button_text})

    @staticmethod
    def confirm(message, title="Are you sure?", confirm_text="Confirm", cancel_text="Cancel", danger=False):
        """True when the confirm button is pressed."""
        params = {"titleText": title, "messageText": message, "confirmText": confirm_text,
                  "cancelText": cancel_text, "danger": int(bool(danger))}
        return bool(_show_dialog("confirm", params))

    @staticmethod
    def prompt(message="", title="", value="", placeholder="", field_text="", required=False,
               confirm_text="OK", cancel_text="Cancel"):
        """The text written, or None (cancelled)."""
        params = {"titleText": title, "messageText": message, "value": value, "placeholder": placeholder,
                  "fieldText": field_text, "required": int(bool(required)), "confirmText": confirm_text,
                  "cancelText": cancel_text}
        return _show_dialog("prompt", params)

    @staticmethod
    def ask(message, title="", buttons=("OK",)):
        """A dialog with your own buttons: the text of the pressed one, or None (Escape, a click outside).
        The first button is the main one: Dialog.ask("Save the changes?", buttons=["Save", "Don't save", "Cancel"])"""
        app = _app.current_app()
        answer = _app._Answer()

        def on_close(dialog, reason, button_key):
            answer.give(button_key if reason == "button" else None)

        button_list = [{"text": text, "key": text, "type": "primary" if index == 0 else "secondary"}
                       for index, text in enumerate(buttons)]
        dialog = Component("Dialog", title_text=title, message_text=message, buttons=button_list, on_close=on_close)
        # WHY by the id of the dialog: when the page can not make it, its answer is None (the code waited for ever)
        return app._wait_for_answer(dialog._id, answer)


def _show_dialog(method, params):
    app = _app.current_app()
    if _takes_minimal_look("Dialog"):
        params["styleName"] = minimal_style_name("Dialog", app.theme == "dark")
    elif app.theme == "dark":
        params["styleName"] = DARK_STYLE_NAMES["Dialog"]
    page_params = to_page(params, app, None, f"Dialog.{method}()")
    return app._call_static("Dialog", method, [page_params], wait_for_answer=True)


class Toast:
    """A short message in a corner: Toast.success("Saved"), Toast.error("Could not save", title="Error").
    type: "success", "error", "warning", "info". duration: milliseconds (0: it stays until closed).
    Its theme is the theme of the window (App(style="minimal"): "minimal" / "minimalDark"); Toast.THEME = "dark" chooses
    one for every toast."""

    THEME = None

    @staticmethod
    def _theme_of_window(app):
        if getattr(app, "style", "") == "minimal":
            return minimal_style_name("Toast", app.theme == "dark")
        return app.theme

    @staticmethod
    def show(message, type="info", title="", duration=None):
        app = _app.current_app()
        params = {"messageText": message, "type": type, "titleText": title, "theme": Toast.THEME or Toast._theme_of_window(app)}
        if duration is not None:
            params["duration"] = duration
        app._call_static("Toast", "show", [to_page(params, app, None, "Toast.show()")])

    @staticmethod
    def success(message, title="", duration=None):
        Toast.show(message, "success", title, duration)

    @staticmethod
    def error(message, title="", duration=None):
        Toast.show(message, "error", title, duration)

    @staticmethod
    def warning(message, title="", duration=None):
        Toast.show(message, "warning", title, duration)

    @staticmethod
    def info(message, title="", duration=None):
        Toast.show(message, "info", title, duration)


__all__ = [
    "SmartButton", "CheckBox", "Toggle", "RadioButton", "SelectBox", "TextAreaField", "SliderField", "ProgressBar",
    "ItemList", "SmartTable", "Tabs", "Dialog", "Toast",
    "LogView", "ImageView", "MenuBar", "StatusBar", "Splitter", "CodeEditor", "picture_address",
    "TextField", "EmailField", "PasswordField", "NumberField", "Slider", "SearchInput", "GraphBox", "TreeView", "ContextMenu",
    "Tooltip", "DatePicker", "TimePicker", "ColorPicker", "Stepper", "FilePicker", "Accordion", "Canvas",
    "SidePanel", "LoadingScreen", "TagInput", "DataTable", "JsonEditor",
]
