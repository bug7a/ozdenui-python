# Bismillah
"""window_check.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The shared part of the checks: an example from examples/, a picture of the window (macOS).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import importlib.util
import os
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
_DROP_STEP_SECONDS = 0.3
_DROP_UPDATES = 3
_DROP_STEP_TIMEOUT_SECONDS = 5
_FRONT_TIMEOUT_SECONDS = 6
# WHY: a message of the page comes a moment after the step that made it (the event goes to Python through the app
# thread); within this time after a new step, a message may still belong to the step before it.
_MESSAGE_DELAY_SECONDS = 0.3


def load_example(name):
    """The module of examples/<name>.py, or of a program file (a path that ends with .py): its start() is used; its
    window is not opened (App(...).run() under if __name__ == "__main__", as in the examples)."""
    path = name if name.endswith(".py") else os.path.join(HERE, "..", "examples", name + ".py")
    spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "start"):
        # WHY: an example written as a class (todo.py: App(TodoApp().start)) has its start() on an object of its class
        module.start = _app_class_of(module)().start
    return module


def _app_class_of(module):
    """The one class of the module with a start() method."""
    classes = [value for value in vars(module).values()
               if isinstance(value, type) and value.__module__ == module.__name__ and callable(getattr(value, "start", None))]
    if len(classes) != 1:
        raise ValueError(f"{module.__name__}: no start() and {len(classes)} classes with one")
    return classes[0]


class TerminalProblems:
    """Passes the terminal output on and keeps the lines of a problem: a message of ozdenui (a mistake of the page, a
    warning) or a traceback. Put it in place of sys.stderr while a window is checked.
    A check that names its steps (set_step()) gets the step at the end of each line: [after: play_todo line 40: ...].
    WHY: a page error said what went wrong, not which click made it; finding the step took a script of its own."""

    def __init__(self, stream):
        self.stream = stream
        self.lines = []
        self._step = ""
        self._step_before = ""
        self._step_time = 0.0

    def set_step(self, step):
        """What the check does now (Ex: "play_todo line 40: click 'Add'")."""
        if step == self._step:
            return
        self._step_before = self._step
        self._step = step
        self._step_time = time.monotonic()

    def write(self, text):
        self.stream.write(text)
        if "ozdenui" in text or "Traceback" in text:
            self.lines.append(text.strip() + self._when())

    def flush(self):
        self.stream.flush()

    def _when(self):
        if not self._step:
            return ""
        is_just_after = (time.monotonic() - self._step_time < _MESSAGE_DELAY_SECONDS)
        if is_just_after and self._step_before:
            return f"  [after: {self._step}; or the step before it: {self._step_before}]"
        return f"  [after: {self._step}]"


def snapshot_window(app, path, on_done):
    """A picture of the page in the window. on_done(error or None) is called when it is written.

    WHY WKWebView on a Mac: it draws its own page, so no screen recording permission is needed (screencapture needs
    one). On Windows: a picture of that part of the screen (Pillow), for a computer with nothing else on its screen
    (a test machine). WHY no picture with another engine on a Mac: that part of the screen showed the other windows.
    """
    if sys.platform == "win32":
        _snapshot_screen(app, path, on_done)
        return
    if os.environ.get("PYWEBVIEW_GUI"):
        on_done("no picture with this engine")
        return

    import AppKit
    from PyObjCTools import AppHelper
    from webview.platforms.cocoa import BrowserView

    def take():
        view = BrowserView.instances[app._window.uid].webview

        def handler(image, error):
            if image is None:
                on_done(f"no picture: {error}")
                return
            bitmap = AppKit.NSBitmapImageRep.imageRepWithData_(image.TIFFRepresentation())
            png = bitmap.representationUsingType_properties_(AppKit.NSBitmapImageFileTypePNG, {})
            png.writeToFile_atomically_(path, True)
            on_done(None)

        view.takeSnapshotWithConfiguration_completionHandler_(None, handler)

    AppHelper.callAfter(take)  # WHY: AppKit only on the main thread


def bring_to_front(app, ask_page):
    """Asks for the front and waits until the page has the focus. False: another program holds it (a person works on this
    computer): what needs the front can not be checked now. ask_page(script) runs JavaScript on the app thread.
    WHY: a window in the back stops requestAnimationFrame, so a ContextMenu is not drawn and a drop does not arrive."""
    if not can_drop_natively():
        return True
    import AppKit
    from PyObjCTools import AppHelper
    from webview.platforms.cocoa import BrowserView

    def activate():
        AppKit.NSApp.activateIgnoringOtherApps_(True)
        BrowserView.instances[app._window.uid].window.makeKeyAndOrderFront_(None)

    deadline = time.time() + _FRONT_TIMEOUT_SECONDS
    while time.time() < deadline:
        AppHelper.callAfter(activate)  # WHY: AppKit only on the main thread
        time.sleep(_DROP_STEP_SECONDS)
        if ask_page("document.hasFocus()"):
            return True
    return False


def can_drop_natively():
    """WHY only here: a drop through the web view of macOS needs no mouse and no permission (another system: the check
    gives pywebview the path by hand)."""
    return sys.platform == "darwin" and not os.environ.get("PYWEBVIEW_GUI")


_DRAG_INFO_CLASS = []  # WHY made once: a process can make an Objective-C class only once (a second drop failed)


def _drag_info_class():
    """The class of the drags of drop_file_natively(), made the first time."""
    if _DRAG_INFO_CLASS:
        return _DRAG_INFO_CLASS[0]
    import AppKit
    import objc

    class DragInfo(AppKit.NSObject):
        """What the web view asks a drag (NSDraggingInfo)."""

        def setUp_location_window_(self, board, point, window):
            self.board, self.point, self.destination = board, point, window
            return self

        def draggingDestinationWindow(self):
            return self.destination

        def draggingSourceOperationMask(self):
            return AppKit.NSDragOperationCopy

        @objc.typedSelector(AppKit.NSPoint.__typestr__ + b"@:")
        def draggingLocation(self):
            return self.point

        @objc.typedSelector(AppKit.NSPoint.__typestr__ + b"@:")
        def draggedImageLocation(self):
            return self.point

        def draggedImage(self):
            return None

        def draggingPasteboard(self):
            return self.board

        def draggingSource(self):
            return None

        def draggingSequenceNumber(self):
            return 1

        def namesOfPromisedFilesDroppedAtDestination_(self, _folder):
            return []

        def numberOfValidItemsForDrop(self):
            return 1

        def setNumberOfValidItemsForDrop_(self, _count):
            pass

        def draggingFormation(self):
            return AppKit.NSDraggingFormationDefault

        def setDraggingFormation_(self, _formation):
            pass

        def animatesToDestination(self):
            return False

        def setAnimatesToDestination_(self, _value):
            pass

        def springLoadingHighlight(self):
            return 0

        def resetSpringLoading(self):
            pass

        @objc.typedSelector(b"v@:q@@@@?")
        def enumerateDraggingItemsWithOptions_forView_classes_searchOptions_usingBlock_(self, _options, _view, _classes, _search, _block):
            pass

    _DRAG_INFO_CLASS.append(DragInfo)
    return DragInfo


def drop_file_natively(app, path, x, y):
    """Drops a file at a place of the page through the entry points macOS calls when a person drops one (draggingEntered,
    draggingUpdated, performDragOperation), with the file on a real pasteboard. Call it from a thread of its own."""
    import AppKit
    import Foundation
    from PyObjCTools import AppHelper
    from webview.platforms.cocoa import BrowserView

    DragInfo = _drag_info_class()
    web_view = BrowserView.instances[app._window.uid].webview
    finished = threading.Event()

    def on_main_thread(task):
        finished.clear()
        problem = []

        def run():
            try:
                task()
            except Exception as error:  # WHY: a method of the drag that is missing here is the usual reason
                problem.append(error)
            finally:
                finished.set()

        AppHelper.callAfter(run)  # WHY: AppKit only on the main thread
        if not finished.wait(_DROP_STEP_TIMEOUT_SECONDS):
            raise TimeoutError("the main thread did not answer")
        if problem:
            raise problem[0]

    made = {}

    def make_drag():
        board = AppKit.NSPasteboard.pasteboardWithUniqueName()
        board.declareTypes_owner_([AppKit.NSFilenamesPboardType, "public.file-url"], None)
        board.setPropertyList_forType_([path], AppKit.NSFilenamesPboardType)
        board.setString_forType_(Foundation.NSURL.fileURLWithPath_(path).absoluteString(), "public.file-url")
        # WHY: a window in the back does not take a drag
        AppKit.NSApp.activateIgnoringOtherApps_(True)
        web_view.window().makeKeyAndOrderFront_(None)
        point = web_view.convertPoint_toView_(Foundation.NSMakePoint(x, y), None)
        made["drag"] = DragInfo.alloc().init().setUp_location_window_(board, point, web_view.window())

    on_main_thread(make_drag)
    drag = made["drag"]
    on_main_thread(lambda: web_view.draggingEntered_(drag))
    # WHY the page first: it answers through another process, and a drop before it saw the "dragover" is lost. A person moves
    #     the mouse for much longer than this.
    for _ in range(_DROP_UPDATES):
        time.sleep(_DROP_STEP_SECONDS)
        on_main_thread(lambda: web_view.draggingUpdated_(drag))
    time.sleep(_DROP_STEP_SECONDS)
    on_main_thread(lambda: web_view.prepareForDragOperation_(drag))
    on_main_thread(lambda: web_view.performDragOperation_(drag))


def _snapshot_screen(app, path, on_done):
    try:
        from PIL import ImageGrab

        window = app._window
        box = (window.x, window.y, window.x + window.width, window.y + window.height)
        ImageGrab.grab(bbox=box).save(path)
        on_done(None)
    except Exception as error:  # WHY: a picture is an extra of a check: it must not fail the check.
        on_done(f"no picture: {error}")
