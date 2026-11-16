# Bismillah
"""_look.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
python -m ozdenui look: runs a program as it is, takes a picture of its window when its first drawing has stood for a
while, and closes the window. For an AI assistant (and a person in a hurry) that must see what a program draws: a
program that runs without an error can still have a part covered or cut.
WHY in the package: an assistant that wrote a window could only say "no error in the terminal"; in a check of two
assistants both left the same covered scroll bar, which one look at the picture shows.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import os
import runpy
import sys
import threading

from . import app as app_module

DEFAULT_WAIT_SECONDS = 1.5
NO_WINDOW_SECONDS = 30  # a program that never shows its window (an error in start(), no App) is not waited for longer
_NO_PILLOW = "a picture on this system needs Pillow: pip install pillow"


def _take_mac_picture(app, path, on_done):
    """WHY the web view itself: it draws its own page, so the picture needs no screen recording permission and holds
    no other window."""
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
            on_done(None if png.writeToFile_atomically_(path, True) else f"could not write {path}")

        view.takeSnapshotWithConfiguration_completionHandler_(None, handler)

    AppHelper.callAfter(take)  # WHY: AppKit only on the main thread


def _take_screen_picture(app, path, on_done):
    """That part of the screen: the window must be in front, with nothing over it."""
    try:
        from PIL import ImageGrab
    except ImportError:
        on_done(_NO_PILLOW)
        return
    try:
        window = app._window
        ImageGrab.grab(bbox=(window.x, window.y, window.x + window.width, window.y + window.height)).save(path)
        on_done(None)
    except Exception as error:  # WHY: any failure of the screen is told as a message, the window must still close
        on_done(f"no picture: {error}")


def take_picture(app, path, on_done):
    """A picture of the window into path (a PNG). on_done(None), or on_done(what went wrong)."""
    if sys.platform == "darwin" and not os.environ.get("PYWEBVIEW_GUI"):
        _take_mac_picture(app, path, on_done)
    else:
        _take_screen_picture(app, path, on_done)


def look(program, picture, wait_seconds=DEFAULT_WAIT_SECONDS, theme=""):
    """Runs the program file, saves the picture of its window and closes it. Returns None, or what went wrong."""
    program = os.path.abspath(program)
    picture = os.path.abspath(picture)
    result = {"error": "the program opened no window (no App(...).run()?)"}

    def on_picture(app, error):
        result["error"] = error
        app.close()

    def on_shown(app):
        result["error"] = "the window closed before the picture"
        # WHY a thread timer: the picture must come also while a function of the program keeps the app thread
        threading.Timer(wait_seconds, lambda: take_picture(app, picture, lambda error: on_picture(app, error))).start()

    def give_up():
        app = app_module._current
        if app is not None and not app._is_shown and app._window is not None:
            result["error"] = f"no window was shown in {NO_WINDOW_SECONDS} s (an error in start()? see above)"
            app.close()

    app_module._look = {"theme": theme, "on_shown": on_shown}
    guard = threading.Timer(NO_WINDOW_SECONDS, give_up)
    guard.daemon = True
    guard.start()
    old_argv, old_path = sys.argv, list(sys.path)
    sys.argv = [program]
    sys.path.insert(0, os.path.dirname(program))  # as python program.py does: the modules next to the program
    try:
        runpy.run_path(program, run_name="__main__")
    finally:
        guard.cancel()
        app_module._look = None
        sys.argv, sys.path[:] = old_argv, old_path
    return result["error"]
