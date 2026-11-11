# Bismillah
"""values.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Small helpers of the objects and the app: names, handlers, the values that may go to the page.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import base64
import inspect
import io
import itertools
import mimetypes
import os
import re
import string
import sys

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
ANY_COUNT = 99  # a handler with *args takes every value
_next_callback_number = itertools.count(1)
_PAGE_TYPES = (str, int, float, bool, type(None))
_NUMBER_SPEC = re.compile(r"(,?)(?:\.(\d+))?([fFd%]?)")
_DEFAULT_DECIMALS = 6


def camel_case(name):
    """font_size -> fontSize. A name in camelCase stays as it is."""
    first, *rest = name.split("_")
    return first + "".join(word[:1].upper() + word[1:] for word in rest)


def snake_case(name):
    """lineWidth -> line_width. A name in snake_case stays as it is."""
    return re.sub(r"(?<=[a-z0-9])([A-Z])", lambda match: "_" + match.group(1).lower(), name)


def event_name_of(prop_name):
    """on_click -> "click", on_mouse_enter -> "mouseenter" (the names of the DOM events)."""
    return prop_name[len("on_"):].replace("_", "")


def source_line():
    """file:line of the user code that made the call: the first frame outside this package."""
    frame = sys._getframe(1)
    while frame and os.path.dirname(os.path.abspath(frame.f_code.co_filename)) == PACKAGE_DIR:
        frame = frame.f_back
    if frame is None:
        return ""
    return f"{os.path.basename(frame.f_code.co_filename)}:{frame.f_lineno}"


def positional_count(handler):
    """How many values of its event a handler takes, in order: its parameters without a default (ANY_COUNT for *args).
    WHY not the ones with a default: they keep a value of their own, the way of other toolkits for the value of a loop
    (lambda key=key: press(key)); before, the event put its object into key."""
    try:
        params = inspect.signature(handler).parameters.values()
    except (TypeError, ValueError):
        return ANY_COUNT
    if any(p.kind == p.VAR_POSITIONAL for p in params):
        return ANY_COUNT
    return len([p for p in params if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD) and p.default is p.empty])


def call_with_count(handler, count, values):
    """handler(), handler(a), handler(a, b)...: as many values as it takes. A value the event does not send is None,
    as a missing argument is undefined in JavaScript."""
    given = list(values[:count])
    if count != ANY_COUNT:
        given += [None] * (count - len(given))
    return handler(*given)


def to_page(value, app, owner_id, where, callback_ids=None):
    """A Python value as it goes to the page (JSON): a function becomes a callback, an object its reference.
    callback_ids: a list that gets the id of every callback made here (its object forgets them when they are replaced).
    Raises TypeError at the line of the user for a value the page can not take."""
    if isinstance(value, _PAGE_TYPES):
        return value
    if callable(value) and not hasattr(value, "_id"):
        callback_id = "c" + str(next(_next_callback_number))
        app._register_callback(callback_id, value, owner_id)
        if callback_ids is not None:
            callback_ids.append(callback_id)
        return {"__bpCallback": callback_id}
    if hasattr(value, "_id") and hasattr(value, "_app"):
        return {"__bpObject": value._id}  # a ozdenui object (Ex: Tooltip(target=button))
    if isinstance(value, (list, tuple)):
        return [to_page(item, app, owner_id, where, callback_ids) for item in value]
    if isinstance(value, dict):
        return {str(key): to_page(item, app, owner_id, where, callback_ids) for key, item in value.items()}
    if hasattr(value, "tolist"):  # WHY: the values of a chart or a table often come from numpy or pandas
        return to_page(value.tolist(), app, owner_id, where, callback_ids)
    raise TypeError(
        f"{where}: a {type(value).__name__} can not go to the page "
        "(use text, numbers, True / False, None, lists, dicts or functions)"
    )


def number_format(template, where):
    """A text like "{:,.1f} TL" as the page takes it: the part of Python's format that shows a number ({}, {:.2f}, {:,},
    {:,.0f}, {:d}, {:.1%}). WHY not a function: the page needs the text of a number at once, while it draws, and the
    answer of a Python function comes later."""
    parts = list(string.Formatter().parse(template))
    fields = [part for part in parts if part[1] is not None]
    if len(fields) != 1 or fields[0][1] != "" or fields[0][3] is not None:
        raise ValueError(f'{where}: it needs one {{}} for the number, like "{{:,.1f}} TL": {template!r}')
    spec = _NUMBER_SPEC.fullmatch(fields[0][2])
    if spec is None:
        raise ValueError(f'{where}: this format is not known: {template!r}. It takes {{}}, {{:.2f}}, {{:,}}, {{:,.0f}}, {{:d}}, {{:.1%}}')
    has_comma, decimals, kind = spec.groups()
    field_place = parts.index(fields[0])
    prefix = "".join(part[0] for part in parts[:field_place + 1])
    suffix = "".join(part[0] for part in parts[field_place + 1:])
    return {"__bpFormat": {"prefix": prefix, "suffix": suffix, "thousands": int(bool(has_comma)),
                           "decimals": _decimals_of(decimals, kind), "percent": int(kind == "%")}}


def _decimals_of(decimals, kind):
    """As Python: {:d} has none, {:f} and {:%} have six when they do not say; {} and {:,} keep the digits of the number."""
    if decimals is not None:
        return int(decimals)
    if kind == "d":
        return 0
    return _DEFAULT_DECIMALS if kind else None


def _is_figure(picture):
    return hasattr(picture, "savefig")


def _is_pillow_image(picture):
    return hasattr(picture, "save") and hasattr(picture, "mode")


def _type_of_bytes(data):
    """The media type of a picture by its first bytes."""
    head = bytes(data[:32])
    if head.startswith(b"\xff\xd8"):
        return "image/jpeg"
    if head.startswith(b"GIF8"):
        return "image/gif"
    if head.startswith(b"RIFF") and head[8:12] == b"WEBP":
        return "image/webp"
    if head.lstrip().startswith((b"<svg", b"<?xml")):
        return "image/svg+xml"
    return "image/png"


def _data_address(data, media_type=None):
    encoded = base64.b64encode(bytes(data)).decode("ascii")
    return f"data:{media_type or _type_of_bytes(data)};base64,{encoded}"


def _png_of(save, **options):
    buffer = io.BytesIO()
    save(buffer, **options)
    return buffer.getvalue()


def picture_address(picture):
    """A picture as an address the page can show: a path (str or pathlib), bytes, a Pillow image, a matplotlib figure,
    or an address (http://, https://, data:). "" or None: no picture.

    WHY a data: address for what is on this computer: the web view refuses a file:// picture outside the folder of the
    page (WKWebView, measured 2026-11-05), and a data: address is fast enough: 8 MB in 150 ms, 32 MB in 0.7 s."""
    if picture is None or picture == "":
        return ""
    if _is_figure(picture):
        return _data_address(_png_of(picture.savefig, format="png", bbox_inches="tight"), "image/png")
    if _is_pillow_image(picture):
        return _data_address(_png_of(picture.save, format="PNG"), "image/png")
    if isinstance(picture, (bytes, bytearray, memoryview)):
        return _data_address(picture)
    path = os.fspath(picture)
    if path.startswith(("http://", "https://", "data:")):
        return path
    with open(path, "rb") as file:
        data = file.read()
    media_type, _encoding = mimetypes.guess_type(path)
    return _data_address(data, media_type if (media_type or "").startswith("image/") else None)
