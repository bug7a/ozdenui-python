# Bismillah
"""app.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The window and the bridge to the page.

Threads:
- The main thread runs the window (pywebview needs it).
- The app thread runs the user code: start(page), every event handler, every timer and call_soon() task, one at a
  time. The user code never needs a lock.
- pywebview calls Python from the page on threads of its own: those calls only put a task in the queue.
- A background job (run_in_background) may change objects too: its commands go to the app thread, in order.

The commands of a task are sent to the page together, when the task ends (flush): one call to the page for a
whole start(), not one for each object.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import json
import os
import pathlib
import queue
import sys
import threading
import time
import traceback

import webview

from . import values as _values

_WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
_INDEX_FILE = os.path.join(_WEB_DIR, "index.html")
_READY_TIMEOUT_SECONDS = 15
_GAP_SECONDS = 1.0  # a missing event (a call of the page that failed) holds the ones after it at most this long
# A path of pywebview belongs to a drop the page told of when it came at most this long before it (the two come apart by
# a few ms); an older one is the path of an earlier drop of a file like it.
_SAME_DROP_SECONDS = 0.5
_MIN_REPEAT_SECONDS = 0.001  # WHY: every(0) waited 0 s, so its thread spun a whole CPU core
_FILE_DIALOGS = {"open": webview.FileDialog.OPEN, "save": webview.FileDialog.SAVE, "folder": webview.FileDialog.FOLDER}
_THEMES = ("light", "dark", "auto")
_STYLES = ("", "minimal")
_DARK_PAGE_COLOR = "#1C1C1B"
_EARLY_PAGE_COLOR_PREFIX = "ozdenui-page-color:"  # window.name of a page loaded again for another theme (bridge.js)
_WEBVIEW2_ADDRESS = "https://developer.microsoft.com/microsoft-edge/webview2/"
_current = None


def _check_accent(style, accent, accent_dark):
    for name, color in (("accent", accent), ("accent_dark", accent_dark)):
        if not isinstance(color, str):
            raise TypeError(f'App({name}={color!r}): a color as a text, Ex: "#2A78D6"')
    if accent_dark and not accent:
        raise ValueError("App(accent_dark=...): it goes with accent=...")
    if accent and style != "minimal":
        raise ValueError('App(accent=...): the color of the minimal look; give style="minimal" too')


def current_app():
    if _current is None:
        raise RuntimeError("ozdenui: create the objects in start(page): App(start).run()")
    return _current


# *** THE TIME AND THE FILES OF THE WINDOW, from any function: from ozdenui import every, open_file
# WHY functions: a button had to give its function page.app (on_click=lambda: save(page.app)) only to reach them.

def every(milliseconds, task):
    """Runs task() again and again (the loop() of basic.js). Returns a function that stops it."""
    return current_app().every(milliseconds, task)


def after(milliseconds, task):
    """Runs task() once, after a time. Returns a function that cancels it."""
    return current_app().after(milliseconds, task)


def call_soon(task):
    """Runs task() on the app thread, after the task that runs now. Any thread may call it."""
    current_app().call_soon(task)


def run_in_background(job, *args):
    """Runs job(*args) on a thread of its own, so the window does not wait for it (see App.run_in_background).
    Returns the thread."""
    return current_app().run_in_background(job, *args)


def open_file(file_types=(), directory="", multiple=False):
    """The path of the chosen file (a list with multiple=True), or None. file_types: ("Images (*.png;*.jpg)", ...)"""
    return current_app().open_file(file_types, directory, multiple)


def save_file(file_name="", file_types=(), directory=""):
    """The path to save to, or None."""
    return current_app().save_file(file_name, file_types, directory)


def choose_folder(directory=""):
    """The path of the chosen folder, or None."""
    return current_app().choose_folder(directory)


def _page_address():
    return pathlib.Path(_INDEX_FILE).as_uri()


def _ready_hint():
    """WHY: without the WebView2 runtime pywebview falls back to the Internet Explorer of Windows, which can not run
    basic.js: the window stays empty."""
    return f". Windows needs the WebView2 runtime: {_WEBVIEW2_ADDRESS}" if sys.platform == "win32" else ""


class WindowClosed(Exception):
    """The window was closed while the code waited for an answer (a dialog)."""


class _Answer:
    """An answer the code waits for (a dialog): from the page, or None when it can not come (the dialog could not
    be made, the page was loaded again). Only the first one counts."""

    def __init__(self):
        self.value = None
        self.is_given = threading.Event()

    def give(self, value):
        if self.is_given.is_set():
            return
        self.value = value
        self.is_given.set()


class _PageApi:
    """The functions the page calls (window.pywebview.api.*).

    WHY only methods and "_" names: pywebview gives every public attribute of this object to the page, and walks
    into the objects it holds.
    """

    def __init__(self, app):
        self._app = app

    def ready(self, basic_version, width=0, height=0, prefers_dark=False):
        self._app._on_page_ready(basic_version, width, height, prefers_dark)

    def emit(self, number, target_id, event_name, data):
        self._app._on_page_event(number, target_id, event_name, data)


class _EventOrder:
    """Puts the events of the page back in the order they happened (see send() in bridge.js) and gives each one to
    deliver(event). WHY the gap timer: a call of the page that failed left a hole in the numbers, and every event
    after it waited for ever; the hole is skipped after _GAP_SECONDS."""

    def __init__(self, deliver):
        self._deliver = deliver
        self._lock = threading.Lock()
        self._next_number = 1
        self._waiting = {}
        self._actions = []  # (number, action): what waits until every event up to number is delivered
        self._gap_timer = None

    def add(self, number, event):
        # WHY deliver in the lock: two threads of pywebview must not put their events in the queue in another order
        with self._lock:
            if number < self._next_number:
                self._deliver(event)  # WHY: it came after its hole was skipped; late is better than lost
                return
            self._waiting[number] = event
            self._deliver_in_order()

    def when_delivered(self, number, action):
        """Calls action() once every event up to this number is delivered (or skipped as a hole): what it puts in the
        queue comes after them."""
        with self._lock:
            if number < self._next_number:
                action()
                return
            self._actions.append((number, action))
            self._deliver_in_order()

    def _deliver_in_order(self):
        has_moved = False
        while self._next_number in self._waiting:
            self._deliver(self._waiting.pop(self._next_number))
            self._next_number += 1
            has_moved = True
        self._run_due_actions()
        is_waiting = bool(self._waiting or self._actions)
        # WHY again when it moved: the hole in front is a new one and gets its own _GAP_SECONDS. The timer of the
        #     old hole skipped the next one before its time (events out of order), also when events still waited.
        if self._gap_timer is not None and (has_moved or not is_waiting):
            self._gap_timer.cancel()
            self._gap_timer = None
        if is_waiting and self._gap_timer is None:
            timer = threading.Timer(_GAP_SECONDS, lambda: self._skip_gap(timer))
            timer.daemon = True
            self._gap_timer = timer
            timer.start()

    def _run_due_actions(self):
        due = [entry for entry in self._actions if entry[0] < self._next_number]
        if not due:
            return
        self._actions = [entry for entry in self._actions if entry[0] >= self._next_number]
        for _number, action in due:
            action()

    def _skip_gap(self, timer):
        with self._lock:
            if self._gap_timer is not timer:
                return  # WHY: cancelled while it waited for the lock
            self._gap_timer = None
            if self._waiting:
                self._next_number = min(self._waiting)
            elif self._actions:
                # an event that never came: what waits for it goes on
                self._next_number = min(number for number, _action in self._actions) + 1
            self._deliver_in_order()


class _Timer:
    """Runs a task on the app thread after a time, once or again and again. stop() ends it."""

    def __init__(self, app, milliseconds, task, repeat):
        self._app = app
        self._seconds = max(0, milliseconds) / 1000
        if repeat:
            self._seconds = max(self._seconds, _MIN_REPEAT_SECONDS)
        self._task = task
        self._repeat = repeat
        self._stopped = threading.Event()
        self._is_queued = False  # WHY: a slow task must not pile up ticks in the queue
        app._timers.add(self)
        threading.Thread(target=self._wait_and_queue, name="ozdenui-timer", daemon=True).start()

    def stop(self):
        self._stopped.set()
        self._app._timers.discard(self)

    def _wait_and_queue(self):
        while not self._stopped.wait(self._seconds):
            if not self._is_queued:
                self._is_queued = True
                self._app.call_soon(self._run)
            if not self._repeat:
                self._app._timers.discard(self)
                return

    def _run(self):
        self._is_queued = False
        if self._stopped.is_set():
            return
        self._task()


class App:
    """A window with a basic.js page. App(start, title="Counter", size=(400, 300)).run()
    theme: "light" (default), "dark" or "auto" (what the system asks). In a dark window every component takes its dark
    look unless it is given another one, and the plain objects and the page are dark too. app.theme: "light" or "dark".
    app.set_theme("dark") draws the window again in another theme: the page is made again and start() runs again.
    style: "" (default: the usual looks) or "minimal": small and made of lines (minimal / minimalDark, by the theme), for
    the components that have it; the others keep their usual look. app.style.
    accent: a color of the minimal look ("#2A78D6"): an on toggle, a checked box, the selected tab and the main button
    (SmartButton(tone="accent")) take it; the lines and the texts stay as they are. accent_dark: its color in a dark
    window ("": the same color made lighter until it reads on the dark ground). app.accent, app.accent_dark."""

    def __init__(self, start, title="basic.js", size=(800, 600), components=(), debug=False, theme="light", style="",
                 accent="", accent_dark=""):
        if theme not in _THEMES:
            raise ValueError(f'App(theme={theme!r}): it is "light", "dark" or "auto"')
        if style not in _STYLES:
            raise ValueError(f'App(style={style!r}): it is "" or "minimal"')
        _check_accent(style, accent, accent_dark)
        self.style = style
        self.accent = accent
        self.accent_dark = accent_dark
        self._wanted_theme = theme
        self.theme = "dark" if theme == "dark" else "light"  # "auto": the page tells it before start() runs
        self._start = start
        self._title = title
        self._size = size
        self._components = list(components)  # more components to load (Ex: ["TreeView"])
        self._debug = debug
        self._window = None
        self._tasks = queue.Queue()
        self._ready = threading.Event()
        self._event_order = _EventOrder(self._queue_event)
        self._timers = set()
        self._is_shown = False
        self._app_thread_id = None
        self._commands = []
        self._other_thread_commands = []
        self._other_thread_lock = threading.Lock()
        self._is_other_thread_flush_queued = False
        self._thread_state = threading.local()  # the open "with" blocks of each thread
        self._objects = {}  # id -> object, so an event finds its object
        self._leaving = {}  # id -> an object the page removed, until the events it sent before are handled
        self._callbacks = {}  # id -> (handler, positional count, owner id): Python functions given to the page
        self._pending_answers = {}  # a callback id or an object id -> the _Answer a code waits for
        self._failed_ids = set()  # the objects the page could not make (an answer that belongs to one gets None)
        self._is_listening_for_drops = False
        self._dropped_paths = {}  # (name, size) of a file dropped on the window -> {its lastModified: (its path, when it came)}
        self._drop_times = {}  # (name, size, lastModified) -> when the page told of its last drop
        self._page_end_tasks = []  # run when the objects of the page are gone (closed, loaded again): capture_print() ends
        self._is_closed = False
        self._prefers_dark = False  # what the system asked when the page was ready (set_theme("auto"))
        self._is_loading_for_theme = False  # set_theme() loads the page again: no command goes to it until it is ready
        self._page_size = (0, 0)
        self.page = None
        self.basic_version = ""
        self.timings = {}  # milliseconds from run(): "page_ready", "first_draw_sent", "shown"
        self.started_at = 0.0

    # *** RUN:

    def run(self):
        """Opens the window and returns when it is closed. Call it from the main thread."""
        global _current
        _current = self
        self.started_at = time.perf_counter()
        width, height = self._size
        # WHY hidden: the window is shown when the first drawing of start() is on the page (an empty window was
        #      seen for a while before).
        # WHY a file:// address: pywebview starts its server for a plain path, also with http_server=False. Its queue holds
        #      5 connections and the page asks for about 50 files: rarely a page needed 5 s, and rarely it never finished
        #      (seen once in about 50 opens on a busy Mac). The disk has no queue.
        self._window = webview.create_window(
            self._title, url=_page_address(), js_api=_PageApi(self), width=width, height=height, hidden=True
        )
        self._window.events.closed += self._on_window_closed
        webview.start(self._start_app_thread, http_server=False, debug=self._debug)

    def close(self):
        """Closes the window (from any thread)."""
        self._window.destroy()

    def set_title(self, title):
        self._title = title
        self._window.set_title(title)

    def set_theme(self, theme):
        """Draws the window again in another theme: "light", "dark" or "auto" (what the system asks). The page is made
        again and start() runs again, as when the window opened: its objects start again (a text typed in a field is
        gone), what the program keeps in its own variables stays. app.theme is the new one in that start(). Any thread
        may call it; the change comes after the task that runs now."""
        if theme not in _THEMES:
            raise ValueError(f'set_theme({theme!r}): it is "light", "dark" or "auto"')
        self.call_soon(lambda: self._change_theme(theme))

    def call_soon(self, task):
        """Runs task() on the app thread, after the task that runs now. Any thread may call it."""
        self._tasks.put(task)

    def every(self, milliseconds, task):
        """Runs task() again and again (the loop() of basic.js). Returns a function that stops it."""
        return _Timer(self, milliseconds, task, repeat=True).stop

    def after(self, milliseconds, task):
        """Runs task() once, after a time. Returns a function that cancels it."""
        return _Timer(self, milliseconds, task, repeat=False).stop

    def run_in_background(self, job, *args):
        """Runs job(*args) on a thread of its own, so the window does not wait for it. The job may change objects
        (a progress bar) and wait for a dialog (Dialog.confirm); it may not measure(), ask() or flush().
        Returns the thread."""

        def run_job():
            try:
                job(*args)
            except Exception:
                traceback.print_exc()

        thread = threading.Thread(target=run_job, name="ozdenui-job", daemon=True)
        thread.start()
        return thread

    def flush(self):
        """Sends the waiting commands to the page now (a long task can show its progress). Returns the answer."""
        self._check_app_thread("flush()")
        if not self._commands or self._is_closed or self._is_loading_for_theme:
            return None
        commands, self._commands = self._commands, []
        script = "__bp.apply(" + json.dumps(commands, ensure_ascii=False, separators=(",", ":")) + ")"
        answer = self._window.evaluate_js(script)
        self._after_apply(answer)
        return answer

    def evaluate(self, script):
        """Runs JavaScript on the page and returns its value (after the waiting commands)."""
        self.flush()
        return self._window.evaluate_js(script)

    # *** FILE DIALOGS of the system. file_types: ("Images (*.png;*.jpg)", "All files (*.*)")

    def open_file(self, file_types=(), directory="", multiple=False):
        """The path of the chosen file (a list with multiple=True), or None."""
        paths = self._file_dialog("open", directory, multiple, "", file_types)
        if not paths:
            return None
        return list(paths) if multiple else paths[0]

    def save_file(self, file_name="", file_types=(), directory=""):
        """The path to save to, or None."""
        paths = self._file_dialog("save", directory, False, file_name, file_types)
        if not paths:
            return None
        return paths if isinstance(paths, str) else paths[0]

    def choose_folder(self, directory=""):
        """The path of the chosen folder, or None."""
        paths = self._file_dialog("folder", directory, False, "", ())
        if not paths:
            return None
        return paths if isinstance(paths, str) else paths[0]

    def _file_dialog(self, kind, directory, multiple, file_name, file_types):
        if threading.get_ident() == self._app_thread_id:
            self.flush()
            self._show_window()  # WHY: a file dialog in start() opened over a hidden window
        return self._window.create_file_dialog(
            _FILE_DIALOGS[kind], directory=directory, allow_multiple=multiple, save_filename=file_name,
            file_types=tuple(file_types),
        )

    # *** FILES DROPPED ON THE WINDOW: the page knows only their names, pywebview their paths.

    def _listen_for_dropped_files(self):
        """WHY only when a FilePicker asks: pywebview keeps the paths of a drop only while something listens to it."""
        if self._is_listening_for_drops:
            return
        self._is_listening_for_drops = True
        self._window.dom.document.on("drop", self._on_files_dropped)

    def _on_files_dropped(self, event):
        received = time.monotonic()
        files = (event.get("dataTransfer") or {}).get("files") or []
        self.call_soon(lambda: self._keep_dropped_files(files, received))

    def _keep_dropped_files(self, files, received=None):
        for file in files:
            path = file.get("pywebviewFullPath")
            if path:
                paths = self._dropped_paths.setdefault((file.get("name"), file.get("size")), {})
                paths[file.get("lastModified")] = (path, time.monotonic() if received is None else received)

    def _note_drop(self, data):
        """The page told of a drop (bridge.js, before a FilePicker tells its new files)."""
        for file in data.get("files") or []:
            self._drop_times[(file.get("name"), file.get("size"), file.get("lastModified"))] = data["receivedAt"]

    def _dropped_path(self, name, size, last_modified=None):
        """The path pywebview gave for a file dropped on the window, or None (it has not come yet).
        WHY lastModified and the time: a file of the same name and size dropped before (from another folder) had its own
        path; a new drop got that one when the page told of it before pywebview did."""
        paths = self._dropped_paths.get((name, size)) or {}
        entry = paths.get(last_modified) or paths.get(None)
        if entry is None:
            return None
        path, received = entry
        dropped_at = self._drop_times.get((name, size, last_modified))
        if dropped_at is not None and received < dropped_at - _SAME_DROP_SECONDS:
            return None  # the path of an earlier drop: the one of this drop is on its way
        return path

    # *** THE APP THREAD:

    def _start_app_thread(self):
        # WHY daemon: the thread pywebview starts is not one, and a call to the page that never comes back
        #      (the window was closed in the meantime) kept the process open.
        threading.Thread(target=self._run_app_thread, name="ozdenui-app", daemon=True).start()

    def _run_app_thread(self):
        self._app_thread_id = threading.get_ident()
        if not self._ready.wait(_READY_TIMEOUT_SECONDS):
            print(f"ozdenui: the page is not ready yet (basic.js or the bridge did not load){_ready_hint()}", file=sys.stderr)
            self._show_window()
            self._window.load_url(_page_address())  # WHY: A load that never ends was seen: a new load is a new chance.
            # WHY it goes on waiting: a page that comes late on a slow computer must still start the program, not leave
            #      an empty window for ever.
            self._ready.wait()
        self._mark("page_ready")
        self._make_page()
        try:
            self._run_task(self._load_components)
            self._run_task(self._add_accent_packages)
            self._run_task(lambda: self._start(self.page))
            self._mark("first_draw_sent")
            self._show_window()
            self._run_tasks_until(lambda: False)
        except WindowClosed:
            return

    def _make_page(self):
        from .objects import Page

        self.page = Page(self, *self._page_size)
        if self.theme == "dark":
            self.page.color = _DARK_PAGE_COLOR

    def _run_tasks_until(self, is_done):
        while not is_done():
            task = self._tasks.get()
            if task is None:
                self._tasks.put(None)  # WHY: an outer loop (a dialog waits in a task) must stop too
                raise WindowClosed()
            self._run_task(task)

    def _run_task(self, task):
        # WHY its own "with" blocks: a task that runs while another one waits for a dialog (a click, a timer) made
        #      its objects in the open block of that one; a task that failed in a block leaves nothing open either.
        outer_containers = self._containers()
        self._thread_state.containers = []
        try:
            task()
        except WindowClosed:
            raise
        except Exception:
            traceback.print_exc()
        finally:
            self._thread_state.containers = outer_containers
        try:
            self.flush()
        except Exception:
            traceback.print_exc()

    def _wait_for(self, is_done):
        """Runs the other tasks until is_done(): the code that waits (app.confirm()) keeps the window working."""
        self._check_app_thread("waiting for an answer")
        self.flush()
        self._show_window()  # WHY: a dialog in start() was drawn in the hidden window: nobody could answer it
        self._run_tasks_until(is_done)

    def _show_window(self):
        """Shows the window once: it is hidden until the first drawing of start() is on the page."""
        if self._is_shown:
            return
        self._is_shown = True
        self._window.show()
        self._mark("shown")

    def _ask(self, object_id, method, page_args):
        """Calls a method on the page and returns its result."""
        self._check_app_thread("ask()")
        self.flush()
        script = f"__bp.ask({json.dumps(object_id)}, {json.dumps(method)}, {json.dumps(page_args, ensure_ascii=False)})"
        return self._python_value(self._window.evaluate_js(script))

    def _call_static(self, target, method, page_args, wait_for_answer=False, keep=None):
        """Calls a function of a component (Toast.show, Dialog.confirm). wait_for_answer: the function gives a
        Promise; its value is returned, and the window keeps working while the code waits for it.
        keep: the id of the Python object that stands for what the function returns (a bubble)."""
        command = {"op": "static", "target": target, "method": method, "args": page_args}
        if keep:
            command["keep"] = keep
        if not wait_for_answer:
            self._send(command)
            return None
        answer = _Answer()
        callback_id = f"answer-{id(answer)}"
        self._register_callback(callback_id, answer.give, None)
        command["answer"] = callback_id
        self._send(command)
        value = self._wait_for_answer(callback_id, answer)
        self._callbacks.pop(callback_id, None)
        return value

    def _wait_for_answer(self, key, answer):
        """Waits for an answer (the window keeps working). key: the callback id of the answer, or the id of the
        object that gives it (a Dialog). It is None when it can not come: the object could not be made, or the
        page was loaded again (WHY: the code waited for ever)."""
        self._pending_answers[key] = answer
        if key in self._failed_ids:
            answer.give(None)  # WHY: a background job: the page refused the object before the answer was kept
        try:
            self._wait_for_event(answer.is_given)
        finally:
            self._pending_answers.pop(key, None)
        return answer.value

    def _wait_for_event(self, event):
        """Waits until event is set: on the app thread the other tasks run meanwhile (the window keeps working)."""
        if threading.get_ident() == self._app_thread_id:
            self._wait_for(event.is_set)
        else:
            event.wait()  # WHY: a background job may wait: the app thread shows the dialog meanwhile

    def _check_app_thread(self, what):
        if threading.get_ident() != self._app_thread_id:
            raise RuntimeError(f"ozdenui: {what} works only in start(), an event or a timer, not in another thread")

    def _mark(self, name):
        self.timings[name] = round((time.perf_counter() - self.started_at) * 1000, 1)

    def _load_components(self):
        if not self._components:
            return
        script = "__bp.loadComponents(" + json.dumps(self._components) + ")"
        loaded = threading.Event()
        answer = {}

        def on_loaded(result):
            answer["result"] = result
            loaded.set()

        self._window.evaluate_js(script, on_loaded)
        loaded.wait(_READY_TIMEOUT_SECONDS)
        for problem in (answer.get("result") or {}).get("errors", []):
            print(f"ozdenui: {problem}", file=sys.stderr)

    def _add_accent_packages(self):
        """The packages of App(accent=...) on the page (comp/minimal-accent.js), after every component is loaded."""
        if not self.accent:
            return
        from .objects import ACCENT_STYLE_NAME

        self._call_static("MinimalAccent", "addPackages", [ACCENT_STYLE_NAME, self.accent, self.accent_dark])

    # *** FROM THE OBJECTS:

    def _containers(self):
        state = self._thread_state
        if not hasattr(state, "containers"):
            state.containers = []
        return state.containers

    def _register(self, obj):
        self._objects[obj._id] = obj

    def _register_callback(self, callback_id, handler, owner_id):
        self._callbacks[callback_id] = (handler, _values.positional_count(handler), owner_id)

    def _forget_callback(self, callback_id):
        self._callbacks.pop(callback_id, None)

    def _send(self, command):
        if threading.get_ident() == self._app_thread_id:
            self._commands.append(command)
            return
        # Another thread (a background job): the command goes to the app thread, in order.
        with self._other_thread_lock:
            self._other_thread_commands.append(command)
            if self._is_other_thread_flush_queued:
                return
            self._is_other_thread_flush_queued = True
        self.call_soon(self._take_other_thread_commands)

    def _take_other_thread_commands(self):
        with self._other_thread_lock:
            self._commands.extend(self._other_thread_commands)
            self._other_thread_commands = []
            self._is_other_thread_flush_queued = False

    def _container_id(self):
        containers = self._containers()
        return containers[-1] if containers else "page"

    def _open_container(self, object_id):
        self._containers().append(object_id)

    def _close_container(self, object_id):
        containers = self._containers()
        if containers and containers[-1] == object_id:
            containers.pop()

    def _read(self, object_id, key):
        self._check_app_thread("measure()")
        self.flush()
        return self._window.evaluate_js(f"__bp.read({json.dumps(object_id)}, {json.dumps(key)})")

    def _after_apply(self, answer):
        if not answer:
            return
        for error in answer.get("errors", []):
            where = f"{error.get('src', '')}: {error.get('op', '')} {error.get('id') or ''}"
            print(f"ozdenui: {where}: {error.get('message', '')}", file=sys.stderr)
            if error.get("op") == "create" and error.get("id"):
                self._give_up_answer_of(error["id"])
        removed = set(answer.get("removed", []))
        if not removed:
            return
        for object_id in removed:
            obj = self._objects.pop(object_id, None)
            if obj is not None:
                self._leaving[object_id] = obj
        # WHY later: a component sends an event and then leaves the page (a Dialog: onClose, then remove(); a
        #     LoadingScreen with remove_on_close). Its functions were forgotten before that event was handled:
        #     Dialog.ask() waited for ever and on_close did not run (seen in a real window, with a busy timer).
        forget = lambda: self._forget_removed(removed)  # noqa: E731
        self._event_order.when_delivered(answer.get("lastEvent", 0), lambda: self._tasks.put(forget))

    def _forget_removed(self, removed):
        """WHY: the functions given to a removed object were kept for ever (a list made again every second grew)."""
        for object_id in removed:
            self._leaving.pop(object_id, None)
        for callback_id, (handler, count, owner_id) in list(self._callbacks.items()):
            if owner_id in removed:
                self._callbacks.pop(callback_id, None)

    # *** FROM THE PAGE (pywebview threads):

    def _on_page_ready(self, basic_version, width, height, prefers_dark=False):
        self.basic_version = basic_version
        self._page_size = (width, height)
        self._prefers_dark = prefers_dark
        if self._wanted_theme == "auto":
            self.theme = "dark" if prefers_dark else "light"
        if not self._ready.is_set():
            self._ready.set()
            return
        # The page was loaded again (the reload of debug, a link): its objects are gone, start() makes them again.
        # WHY a new order at once: the numbers of the new page start at 1 again, the old order waited for the next one.
        self._event_order = _EventOrder(self._queue_event)
        self.call_soon(self._start_again)

    def _give_up_answer_of(self, object_id):
        """The page could not make an object: an answer that belongs to it (a Dialog) is None."""
        self._failed_ids.add(object_id)
        pending = self._pending_answers.get(object_id)
        if pending is not None:
            pending.give(None)

    def _change_theme(self, theme):
        """WHY the page is loaded again: a component takes its look when it is made, and a new page keeps nothing of the
        old one (an open menu or bubble, a listener of a component). The reload path makes the objects again.
        WHY window.name: it stays over the load, so the new page has the ground of its theme from its first drawing (it
        was light for a moment before start() drew it dark)."""
        if self._is_closed or theme == self._wanted_theme:
            return
        self._wanted_theme = theme
        if theme == "auto":
            theme = "dark" if self._prefers_dark else "light"  # the page tells it again when it is ready
        self.theme = theme
        for timer in list(self._timers):
            timer.stop()  # WHY: a tick sent its commands to a page that was being loaded
        page_color = _DARK_PAGE_COLOR if theme == "dark" else ""
        self._window.evaluate_js(f"window.name = {json.dumps(_EARLY_PAGE_COLOR_PREFIX + page_color)}")
        self._is_loading_for_theme = True
        self._window.load_url(_page_address())

    def _start_again(self):
        self._end_page_tasks()
        if self._is_loading_for_theme:
            self._is_loading_for_theme = False  # WHY no word: the program asked for the new page (set_theme)
        else:
            print("ozdenui: the page was loaded again: start() runs again", file=sys.stderr)
        # WHY: the dialogs of the old page are gone; the code that waits for one of them gets None (it waited for ever)
        for pending in list(self._pending_answers.values()):
            pending.give(None)
        self._failed_ids = set()
        self._is_listening_for_drops = False  # WHY: the listener was on the old page
        for timer in list(self._timers):
            timer.stop()
        self._commands = []
        self._objects = {}
        self._leaving = {}
        self._callbacks = {}
        self._make_page()
        self._load_components()
        self._add_accent_packages()
        self._start(self.page)

    def _on_page_event(self, number, target_id, event_name, data):
        if event_name == "__drop":
            data = dict(data or {}, receivedAt=time.monotonic())  # WHY: compared with when pywebview gave the paths
        self._event_order.add(number, (target_id, event_name, data))

    def _queue_event(self, event):
        self._tasks.put(lambda: self._dispatch(*event))

    def _dispatch(self, target_id, event_name, data):
        data = data or {}
        if event_name == "callback":
            self._run_callback(target_id, data)
            return
        if event_name == "__message":
            print(f"ozdenui (page {data.get('kind')}): {data.get('text')}", file=sys.stderr)
            return
        if event_name == "__drop":
            self._note_drop(data)
            return
        obj = self._objects.get(target_id)
        if obj is None:
            return  # WHY: an event of an object removed in the meantime
        obj._receive(event_name, data)

    def _run_callback(self, callback_id, data):
        entry = self._callbacks.get(callback_id)
        if entry is None:
            return
        handler, count, owner_id = entry
        owner = self._objects.get(owner_id) or self._leaving.get(owner_id)
        if owner is not None and data.get("state"):
            owner._values.update(data["state"])
            if hasattr(owner, "_state_changed"):
                owner._state_changed()
        args = [self._python_value(value) for value in data.get("args", [])]
        _values.call_with_count(handler, count, args)

    def _python_value(self, value):
        """A value from the page: a basic.js object becomes its Python object; JSON data that came whole (the wholeArgs of
        a callback) becomes its value."""
        if isinstance(value, dict):
            if "__bpObject" in value:
                return self._object_value(value)
            if "__bpJson" in value:
                return json.loads(value["__bpJson"])
            return {key: self._python_value(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._python_value(item) for item in value]
        return value

    def _object_value(self, value):
        """A basic.js object from the page: its Python object, or {"id", "data"} for a part of a component, or None."""
        obj = self._objects.get(value["__bpObject"]) or self._leaving.get(value["__bpObject"])
        if obj is not None:
            return obj
        rest = {key: self._python_value(item) for key, item in value.items() if key != "__bpObject"}
        return rest or None

    def _on_window_closed(self):
        self._is_closed = True
        self._end_page_tasks()
        self._tasks.put(None)

    def _end_page_tasks(self):
        """The tasks of _page_end_tasks, the last one first (two capture_print() give the streams back in order).
        WHY: print() went on into a LogView that was not there any more: after run() every print was a command for
        nobody (and lost with terminal=False); after a reload every print was an error of the page."""
        for task in reversed(list(self._page_end_tasks)):
            try:
                task()
            except Exception:
                traceback.print_exc()
