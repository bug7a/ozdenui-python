# Bismillah
"""look.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Opens an example (or a program file), waits, takes a picture of the window and closes it. The messages of the page
(errors, warnings) are printed by ozdenui.

Usage: .venv/bin/python checks/look.py gallery picture.png [seconds] [width height] [theme] [options]
       .venv/bin/python checks/look.py my_program.py picture.png ...   a program with start(page) and its
                    App(...).run() under if __name__ == "__main__" (a part of a window, a fix, without an example)
    --package dir   ozdenui from dir/ozdenui: a copy made before a change, for the picture of "before" (the package is
                    outside git, so its old version can not be read): cp -R ozdenui <dir>/ before the change
    --run "code"    Python code on the app thread after the wait, before the picture (more than one: one after the
                    other, --step-wait seconds between them). It has app, page, example, every name of ozdenui and:
                    first(kind, **values): the first object of a kind (first(ChatView), first(Label, text="Hi"))
                    scroll_to(obj, space=40): every box that scrolls around it brings it near its top
                    click(text): a click on the element that shows this text, as a person does
                    js(script): the value of a JavaScript expression of the page
    --clip "expr"   only the part of the picture with this object (a Python expression: first(ChatView)); more than
                    one --clip: the part that holds them all; --margin px around it (12). A part out of the window
                    (lower in a box that scrolls) is scrolled into it; a part taller than the window is an error
    --step-wait s   after every --run (0.6)
    --arg word      a word after the name of the program, as on its command line (more than one: in order); the
                    example reads it from sys.argv (Ex: files.py some/folder: --arg some/folder)
    --whole         the whole page: the box that scrolls most goes from its top to its end, a picture at every step;
                    the long page is cut in --columns (3) side by side, at the size of the window (no --clip)
    --compare-with before.png   where the picture differs from before.png, a picture of look.py of the same kind (two
                    --whole pictures of a page, or two windows): "differences" in the page (--whole) or in the window,
                    each one marked in <picture>-diff.png. before.png comes from a copy of the old file (my_program.py)
                    or from --package
    --moving-clock  the clock of the page goes on (a page that waits for the time to pass). Without it the clock stands
                    still at 6 Nov 2026 12:00 and a timer of the page of 2 s or more never comes; Math.random gives the
                    same numbers in every run (as compare-pages.js of the repository), so two pictures of a page that
                    did not change are the same. The page does not take the real mouse (no light under it)
Ex: look.py gallery chat.png 1.5 1000 860 --run "scroll_to(first(ChatView))" --run "first(ChatView).set_input_text('Hi')"
    --clip "first(ChatView)"
Ex: look.py old/gallery.py before.png 1.5 1000 820 dark --whole, then look.py gallery after.png 1.5 1000 820 dark --whole
    --compare-with before.png
WHY options and not a new script: every picture of a part of a window (a card lower in the gallery, a dialog open)
was a script of its own; this is the one tool for them. The whole page was scrolled and joined by hand each time.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import argparse
import json
import math
import os
import sys
import tempfile
import threading
import time

# WHY before the import of ozdenui: --package takes the package from another folder
if "--package" in sys.argv[:-1]:
    sys.path.insert(0, sys.argv[sys.argv.index("--package") + 1])

import ozdenui  # noqa: E402
from ozdenui import App  # noqa: E402
from window_check import load_example, snapshot_window  # noqa: E402

TIMEOUT_SECONDS = 20
EXTRA_SECONDS_PER_STEP = 2  # WHY: the timeout grows with the steps of --run, so a long play is not cut
SCROLL_JS = """(function (elem, space) {
    for (let box = elem.parentElement; box; box = box.parentElement) {
        const overflow = getComputedStyle(box).overflowY;
        if ((overflow === "auto" || overflow === "scroll") && box.scrollHeight > box.clientHeight) {
            box.scrollTop += elem.getBoundingClientRect().top - box.getBoundingClientRect().top - space;
        }
    }
    return "ok";
})(%s.elem, %d)"""
CLICK_JS = """(function (text) {
    const found = Array.from(document.querySelectorAll("body *")).filter(function (el) {
        return el.children.length === 0 && el.textContent.trim() === text && el.getClientRects().length > 0;
    });
    if (!found.length) return "not found";
    found[found.length - 1].click();
    return "ok";
})(%s)"""
RECT_JS = "(function (r) { return [r.left, r.top, r.right, r.bottom]; })(%s.elem.getBoundingClientRect())"
# The top and the bottom of the part of the window where the object can be seen: the box that scrolls around it
SEEN_JS = """(function (elem) {
    for (let box = elem.parentElement; box; box = box.parentElement) {
        const overflow = getComputedStyle(box).overflowY;
        if (overflow === "auto" || overflow === "scroll") return [box.getBoundingClientRect().top, box.getBoundingClientRect().bottom];
    }
    return [0, window.innerHeight];
})(%s.elem)"""
ANSWER_SECONDS = 10  # a step of --whole: an answer of the page, a picture
WHOLE_EXTRA_SECONDS = 60  # WHY: --whole takes a picture at every step of a long page
WHOLE_GAP = 12  # px between the columns of --whole
WHOLE_GROUND = "#808080"
WHOLE_KEY = "look.py whole"  # the text of a --whole picture: the width of its page and of a column, for --compare-with
DIFF_CELL = 16  # px: --compare-with looks for the differences in squares of this size
DIFF_MARK_WIDTH = 3
# The box that scrolls most is marked for the steps: [left, top, width, height] of its inside, and its whole height
WHOLE_JS = """(function () {
    let best = null;
    let hidden = 0;
    document.querySelectorAll("*").forEach(function (elem) {
        const overflow = getComputedStyle(elem).overflowY;
        if ((overflow === "auto" || overflow === "scroll") && elem.scrollHeight - elem.clientHeight > hidden) {
            best = elem;
            hidden = elem.scrollHeight - elem.clientHeight;
        }
    });
    if (!best) return null;
    best.setAttribute("data-look-whole", "1");
    const rect = best.getBoundingClientRect();
    return [rect.left + best.clientLeft, rect.top + best.clientTop, best.clientWidth, best.clientHeight, best.scrollHeight];
})()"""
# A timer of the page this long or longer never comes while the clock stands still. WHY 2 s (3 s in compare-pages.js):
# the scroll bar of a list hides 2 s after it was shown, just when --whole takes its first step: seen in one run, not in
# the other. A picture taken later than 2 s that waits for such a timer: --moving-clock.
LONG_TIMER_MS = 2000
# WHY: the real mouse over the window lit what was under it (a row of a tree, the scroll bar of a list) in one run and not
#     in the other, more so while --whole scrolls the page under it. A click of --run (click()) is a click of the script:
#     it still works.
NO_MOUSE_JS = """(function () {
    const style = document.createElement("style");
    style.textContent = "* { pointer-events: none !important; }";
    document.head.appendChild(style);
    return "ok";
})()"""
# WHY, as compare-pages.js of the repository: the time a page shows (a LogView) and a random value (the sample number of
#     a PhoneField) were different in every run, so two pictures of the same page were never the same; a thing that goes
#     away by itself (a toast) went away at another step in every run. The real id of a timer stays, for clearTimeout.
STILL_JS = """function (isClockStopped, longTimer) {
    let seed = 12345;
    Math.random = function () {
        seed = (seed * 16807) % 2147483647;
        return (seed - 1) / 2147483646;
    };
    const RealDate = Date;
    const fixedStart = new RealDate(2026, 10, 6, 12, 0, 0).getTime();
    const realStart = RealDate.now();
    const readNow = function () {
        return isClockStopped ? fixedStart : fixedStart + (RealDate.now() - realStart);
    };
    window.Date = class extends RealDate {
        constructor(...args) {
            if (args.length === 0) super(readNow());
            else super(...args);
        }
        static now() {
            return readNow();
        }
    };
    if (isClockStopped) {
        const realSetTimeout = window.setTimeout;
        const realSetInterval = window.setInterval;
        const doNothing = function () {};
        window.setTimeout = function (fn, ms, ...args) {
            return realSetTimeout.call(window, Number(ms) >= longTimer ? doNothing : fn, ms, ...args);
        };
        window.setInterval = function (fn, ms, ...args) {
            return realSetInterval.call(window, Number(ms) >= longTimer ? doNothing : fn, ms, ...args);
        };
    }
    return "ok";
}"""
SCROLL_WHOLE_JS = """(function (top) {
    const box = document.querySelector("[data-look-whole]");
    box.scrollTop = top;
    return box.scrollTop;
})(%d)"""


def read_arguments():
    parser = argparse.ArgumentParser(description="A picture of an example (or of a program file) in its window.")
    parser.add_argument("name", help="an example (gallery) or a program file (my_program.py)")
    parser.add_argument("picture_file")
    parser.add_argument("seconds", nargs="?", type=float, default=1.5)
    parser.add_argument("width", nargs="?", type=int, default=1000)
    parser.add_argument("height", nargs="?", type=int, default=820)
    parser.add_argument("theme", nargs="?", default="light")
    parser.add_argument("--run", action="append", default=[], help="Python code before the picture")
    parser.add_argument("--clip", action="append", default=[], help="a Python expression of an object: only its part")
    parser.add_argument("--margin", type=int, default=12)
    parser.add_argument("--step-wait", type=float, default=0.6)
    parser.add_argument("--package", default="", help="the folder of another copy of ozdenui/ (read before the import)")
    parser.add_argument("--whole", action="store_true", help="the whole page, step by step, in columns")
    parser.add_argument("--columns", type=int, default=3, help="--whole: the columns of the picture")
    parser.add_argument("--compare-with", default="", help="a picture of look.py: where this one differs from it")
    parser.add_argument("--moving-clock", action="store_true", help="the clock of the page goes on")
    parser.add_argument("--arg", action="append", default=[], help="a word of the command line of the example")
    found = parser.parse_args()
    if found.whole and found.clip:
        parser.error("--whole is the whole page: no --clip")
    return found


arguments = read_arguments()
outcome = {}
if arguments.package:
    outcome["package"] = ozdenui.__file__  # WHY: a folder without ozdenui/ took the package of this folder, with no word


# *** THE NAMES OF --run AND --clip

def first(kind, **values):
    for obj in list(app._objects.values()):
        if isinstance(obj, kind) and all(obj._values.get(key) == value for key, value in values.items()):
            return obj
    raise LookupError(f"no {kind.__name__} with {values}")


def scroll_to(obj, space=40):
    return app.evaluate(SCROLL_JS % (obj.js, space))


def click(text):
    result = app.evaluate(CLICK_JS % json.dumps(text))
    if result != "ok":
        raise LookupError(f"click({text!r}): {result}")
    return result


def js(script):
    return app.evaluate(script)


def names():
    found = {name: getattr(ozdenui, name) for name in ozdenui.__all__}
    found.update(app=app, page=app.page, example=example, first=first, scroll_to=scroll_to, click=click, js=js)
    return found


# *** THE PICTURE

def clip_rects(objects):
    return [app.evaluate(RECT_JS % obj.js) for obj in objects]


def clip_rect():
    """The part of the window that holds the objects of --clip, with the margin: (left, top, right, bottom) in px.
    WHY the scroll: a part lower in a box that scrolls was cut at the edge of the window, with no word (the picture
    had the bottom of the window); the highest object is brought to the top of the window first. Out is also under a bar
    of the window (a StatusBar under the box that scrolls)."""
    objects = [eval(expression, names()) for expression in arguments.clip]
    rects = clip_rects(objects)
    margin = arguments.margin
    seen = [app.evaluate(SEEN_JS % obj.js) for obj in objects]
    is_out = any(rect[1] < top or rect[3] > bottom for rect, (top, bottom) in zip(rects, seen))
    if is_out:
        highest = min(range(len(objects)), key=lambda index: rects[index][1])
        scroll_to(objects[highest], margin)
        rects = clip_rects(objects)
    if max(rect[3] for rect in rects) - min(rect[1] for rect in rects) + 2 * margin > arguments.height:
        outcome.setdefault("errors", []).append("--clip: the part is taller than the window, its bottom is cut: give a larger height")
    left = max(0, min(rect[0] for rect in rects) - margin)
    top = max(0, min(rect[1] for rect in rects) - margin)
    right = min(arguments.width, max(rect[2] for rect in rects) + margin)
    bottom = min(arguments.height, max(rect[3] for rect in rects) + margin)
    return left, top, right, bottom


def crop_picture(rect):
    # WHY here: Pillow is needed only to cut a part (the package itself does not need it)
    from PIL import Image

    with Image.open(arguments.picture_file) as image:
        scale = image.width / arguments.width
        part = image.crop(tuple(round(value * scale) for value in rect))
        part.load()
    part.save(arguments.picture_file)


def take_picture():
    rect = clip_rect() if arguments.clip else None

    def after_picture(error):
        if not error and rect:
            crop_picture(rect)
        if not error and arguments.compare_with:
            compare_pictures()
        outcome["picture"] = error or arguments.picture_file
        app.close()

    snapshot_window(app, arguments.picture_file, after_picture)


# *** THE WHOLE PAGE (--whole)

def on_app(func):
    """func() on the app thread (the page is asked there); its value here."""
    done = threading.Event()
    result = {}

    def run():
        try:
            result["value"] = func()
        except Exception as error:
            result["error"] = error
        finally:
            done.set()

    app.call_soon(run)
    if not done.wait(ANSWER_SECONDS):
        raise TimeoutError("the app thread did not answer")
    if "error" in result:
        raise result["error"]
    return result.get("value")


def snapshot_and_wait(path):
    """A picture of the window in path; its error, or None."""
    done = threading.Event()
    result = {}

    def after(error):
        result["error"] = error
        done.set()

    app.call_soon(lambda: snapshot_window(app, path, after))
    if not done.wait(ANSWER_SECONDS):
        return "no picture in time"
    return result["error"]


def whole_steps(height, whole_height):
    """The scrollTop of every picture: a window lower each time, the last one at the end."""
    last = max(0, whole_height - height)
    return list(range(0, last, height)) + [last]


def take_whole():
    """The box that scrolls most from its top to its end, as one long page (a window that does not scroll: the window).
    Returns the long page and the number of its pictures."""
    from PIL import Image

    box = on_app(lambda: app.evaluate(WHOLE_JS))
    scrolls = bool(box)
    window = (0, 0, arguments.width, arguments.height, arguments.height)
    left, top, width, height, whole_height = (round(value) for value in box) if scrolls else window
    page_picture = Image.new("RGB", (width, whole_height), "white")
    folder = tempfile.mkdtemp(prefix="look-whole-")
    steps = whole_steps(height, whole_height)
    for index, wanted in enumerate(steps):
        scrolled = on_app(lambda wanted=wanted: app.evaluate(SCROLL_WHOLE_JS % wanted)) if scrolls else 0
        time.sleep(arguments.step_wait)
        path = os.path.join(folder, f"step-{index}.png")
        error = snapshot_and_wait(path)
        if error:
            raise RuntimeError(error)
        with Image.open(path) as shot:
            scale = shot.width / arguments.width
            part = shot.convert("RGB").crop(tuple(round(value * scale) for value in (left, top, left + width, top + height)))
        page_picture.paste(part.resize((width, height)), (0, round(scrolled)))
    outcome["whole"] = {"steps": len(steps), "page": [width, whole_height]}
    return page_picture, len(steps)


def save_columns(page_picture, columns):
    """The long page cut in columns side by side; the width of the page and of a column go into the picture (its text)."""
    from PIL import Image
    from PIL.PngImagePlugin import PngInfo

    column_height = math.ceil(page_picture.height / columns)
    picture = Image.new("RGB", (columns * page_picture.width + (columns - 1) * WHOLE_GAP, column_height), WHOLE_GROUND)
    for column in range(columns):
        part = page_picture.crop((0, column * column_height, page_picture.width, min(page_picture.height, (column + 1) * column_height)))
        picture.paste(part, (column * (page_picture.width + WHOLE_GAP), 0))
    info = PngInfo()
    info.add_text(WHOLE_KEY, json.dumps({"width": page_picture.width, "column_height": column_height}))
    picture.save(arguments.picture_file, pnginfo=info)


def take_whole_then_close():
    # WHY finally: a step that fails must not keep the window open
    try:
        page_picture, steps = take_whole()
        save_columns(page_picture, max(1, min(arguments.columns, steps)))
        outcome["picture"] = arguments.picture_file
        if arguments.compare_with:
            compare_pictures()
    except Exception as error:
        outcome.setdefault("errors", []).append(f"--whole: {error!r}")
    finally:
        app.close()


# *** THE DIFFERENCES (--compare-with)

def join_cells(cells):
    """The squares that touch (at a corner too) as one part: (left, top, right, bottom) in squares."""
    parts = []
    left_over = set(cells)
    while left_over:
        found = [left_over.pop()]
        stack = list(found)
        while stack:
            x, y = stack.pop()
            for near in ((x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                if near in left_over:
                    left_over.remove(near)
                    found.append(near)
                    stack.append(near)
        parts.append((min(x for x, _ in found), min(y for _, y in found), max(x for x, _ in found), max(y for _, y in found)))
    return parts


def part_place(rect, layout, scale):
    """Where a part is, in the long page (a --whole picture) or in the window: (top, left, its text)."""
    left, top, right, bottom = rect
    if not layout:
        return top, left, f"window x {round(left / scale)}-{round(right / scale)}, y {round(top / scale)}-{round(bottom / scale)}"
    step = layout["width"] + WHOLE_GAP
    column = left // step
    page_top = column * layout["column_height"]
    return top + page_top, left, f"page y {top + page_top}-{bottom + page_top}, x {left - column * step}-{right - column * step}"


def compare_pictures():
    """Where the picture differs from the one of --compare-with: the squares of DIFF_CELL px that differ, joined into
    parts; each part in "differences" and marked in red in <picture>-diff.png."""
    from PIL import Image, ImageChops, ImageDraw

    with Image.open(arguments.compare_with) as before, Image.open(arguments.picture_file) as after:
        if before.size != after.size:
            outcome["differences"] = f"another size: {before.size} and {after.size} (another page height, window or --clip)"
            return
        layout = json.loads(after.text.get(WHOLE_KEY, "null"))
        marked = after.convert("RGB")
        diff = ImageChops.difference(before.convert("RGB"), marked)
    if not diff.getbbox():
        outcome["differences"] = "the same"
        return
    cells = {(x // DIFF_CELL, y // DIFF_CELL) for y in range(0, diff.height, DIFF_CELL) for x in range(0, diff.width, DIFF_CELL)
             if diff.crop((x, y, x + DIFF_CELL, y + DIFF_CELL)).getbbox()}
    scale = 1 if layout else marked.width / arguments.width
    draw = ImageDraw.Draw(marked)
    places = []
    for left, top, right, bottom in join_cells(cells):
        rect = (left * DIFF_CELL, top * DIFF_CELL, min(marked.width, (right + 1) * DIFF_CELL), min(marked.height, (bottom + 1) * DIFF_CELL))
        draw.rectangle(rect, outline="red", width=DIFF_MARK_WIDTH)
        places.append(part_place(rect, layout, scale))
    marked_file = os.path.splitext(arguments.picture_file)[0] + "-diff.png"
    marked.save(marked_file)
    outcome["differences"] = [text for _, _, text in sorted(places)]
    outcome["marked"] = marked_file


def run_step(code):
    try:
        exec(code, names())
    except Exception as error:
        outcome.setdefault("errors", []).append(f"--run {code!r}: {error!r}")


def wait_then_take():
    time.sleep(arguments.seconds)
    for code in arguments.run:
        app.call_soon(lambda code=code: run_step(code))
        time.sleep(arguments.step_wait)
    if arguments.whole:
        take_whole_then_close()
        return
    app.call_soon(take_picture)


def still_page():
    """The clock of the page stands still (--moving-clock: it goes on), Math.random gives the same numbers in every run and
    the real mouse does not touch the page.
    WHY before the example: its objects read the clock and Math.random when they are made.
    WHY its own try: a failure here kept the example from starting, and two empty pages were "the same"."""
    try:
        app.evaluate(f"({STILL_JS})({json.dumps(not arguments.moving_clock)}, {LONG_TIMER_MS})")
        app.evaluate(NO_MOUSE_JS)
    except Exception as error:
        outcome.setdefault("errors", []).append(f"the still clock: {error!r}")


def start(page):
    # WHY finally: an example that fails must still be pictured and closed (the window stayed open)
    try:
        still_page()
        example.start(page)
    finally:
        # WHY once: a page made again (app.set_theme(), a --run that presses its button) runs start() again
        if not outcome.get("started"):
            outcome["started"] = True
            threading.Thread(target=wait_then_take, daemon=True).start()


# WHY: an example reads its own words from sys.argv (python files.py some/folder), not the ones of look.py
sys.argv = [arguments.name] + arguments.arg
example = load_example(arguments.name)
# WHY STYLE, ACCENT and COMPONENTS of the example: its own window is not opened, so this one takes its look
app = App(start, title=arguments.name, size=(arguments.width, arguments.height), theme=arguments.theme,
          style=getattr(example, "STYLE", ""), accent=getattr(example, "ACCENT", ""), components=getattr(example, "COMPONENTS", ()))

if __name__ == "__main__":
    # WHY here and not in start(): a page that does not get ready never calls start(), and the window stayed for hours.
    extra_seconds = EXTRA_SECONDS_PER_STEP * len(arguments.run) + (WHOLE_EXTRA_SECONDS if arguments.whole else 0)
    closer = threading.Timer(TIMEOUT_SECONDS + extra_seconds, app.close)
    closer.daemon = True
    closer.start()
    app.run()
    print(outcome, "timings:", app.timings)
