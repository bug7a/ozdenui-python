# Bismillah
"""bench.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
P0 measurements (2026-11-03).

1. 1000 objects made at once: the commands go to the page in one call (batched), and in one call each.
2. A click on the page -> the Python handler -> the change on the page and on the screen.
3. A question to the page (measure()).

The window opens, measures for about 15 seconds and closes itself. The results are printed and written to
bench/results.json. Usage: .venv/bin/python bench/bench.py

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import json
import os
import platform
import statistics
import threading
import time
from importlib.metadata import version

from ozdenui import App, Box, Button, HGroup, Label, VGroup

ROWS = 250  # a row = an HGroup, a color Box, a Label and a Button: 4 objects
RUNS = 5
CLICKS = 50
CLICK_GAP_MS = 40
READS = 100
FRAME_WAIT_SECONDS = 0.4
TIMEOUT_SECONDS = 60
SHOW_WAIT_MS = 500
RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

# The measuring code of the page: it wraps __bp.apply to see when Python's commands arrive and when the next
# frame is drawn after them, and clicks a button many times.
BENCH_JS = r"""
(function () {
    const bench = window.__bench = { applyStartedAt: 0, frameAt: 0, applyWaiter: null };
    const originalApply = __bp.apply;
    __bp.apply = function (commands) {
        bench.applyStartedAt = performance.now();
        const result = originalApply(commands);
        bench.frameAt = 0;
        requestAnimationFrame(function () {
            setTimeout(function () { bench.frameAt = performance.now(); }, 0);
        });
        if (bench.applyWaiter) {
            const waiter = bench.applyWaiter;
            bench.applyWaiter = null;
            waiter();
        }
        return result;
    };
    const nextApply = function () {
        return new Promise(function (resolve) { bench.applyWaiter = resolve; });
    };
    const nextFrame = function () {
        return new Promise(function (resolve) {
            requestAnimationFrame(function () { setTimeout(resolve, 0); });
        });
    };
    const wait = function (ms) {
        return new Promise(function (resolve) { setTimeout(resolve, ms); });
    };
    bench.frameTime = function () {
        return (bench.frameAt) ? bench.frameAt - bench.applyStartedAt : null;
    };
    bench.clicks = async function (button, label, reporter, count, gapMs) {
        const toApply = [];
        const toFrame = [];
        for (let i = 0; i < count; i++) {
            const applied = nextApply();
            const startedAt = performance.now();
            button.elem.click();
            await applied;
            toApply.push(performance.now() - startedAt);
            await nextFrame();
            toFrame.push(performance.now() - startedAt);
            await wait(gapMs);
        }
        const detail = { toApply: toApply, toFrame: toFrame, text: label.text };
        reporter.elem.dispatchEvent(new CustomEvent("report", { detail: detail }));
    };
    return "ready";
})()
"""

results = {}


def milliseconds(seconds):
    return round(seconds * 1000, 1)


def summary(values):
    ordered = sorted(values)
    p95_index = min(len(ordered) - 1, round(0.95 * (len(ordered) - 1)))
    return {
        "median": round(statistics.median(ordered), 1),
        "p95": round(ordered[p95_index], 1),
        "min": round(ordered[0], 1),
        "max": round(ordered[-1], 1),
    }


def make_rows(flush_each=False):
    """ROWS rows in a scrolling box: 2 + ROWS * 4 objects. flush_each: one call to the page for every object."""
    made = []

    def keep(obj):
        made.append(obj)
        if flush_each:
            app.flush()
        return obj

    with keep(Box(0, 0, "100%", "100%", color="transparent", scroll_y=1)) as holder:
        with keep(VGroup(width="100%", height="auto", align="left top", gap=4, padding=10)):
            for number in range(ROWS):
                with keep(HGroup(width="100%", height=28, align="left center", gap=8)):
                    keep(Box(width=16, height=16, round=4, color="#2F6FED"))
                    keep(Label(text=f"Row {number + 1}", font_size=14))
                    keep(Button(text="Open", width=64, height=24))
    return holder, len(made)


def measure_batched():
    runs = []
    for _ in range(RUNS):
        started = time.perf_counter()
        holder, count = make_rows()
        built = time.perf_counter()
        answer = app.flush()
        finished = time.perf_counter()
        time.sleep(FRAME_WAIT_SECONDS)
        frame_ms = app.evaluate("__bench.frameTime()")
        total_ms = milliseconds(finished - started)
        runs.append({
            "objects": count,
            "python_build_ms": milliseconds(built - started),
            "page_apply_ms": round(answer["ms"], 1),
            "total_ms": total_ms,
            "apply_to_frame_ms": round(frame_ms, 1) if frame_ms else None,
            "total_to_screen_ms": round(total_ms - answer["ms"] + frame_ms, 1) if frame_ms else None,
            "errors": len(answer["errors"]),
        })
        holder.remove()
        app.flush()
    results["create_batched"] = runs


def measure_one_call_each():
    started = time.perf_counter()
    holder, count = make_rows(flush_each=True)
    results["create_one_call_each"] = {"objects": count, "total_ms": milliseconds(time.perf_counter() - started)}
    holder.remove()
    app.flush()


def measure_reads(label):
    times = []
    for _ in range(READS):
        started = time.perf_counter()
        label.measure("width")
        times.append((time.perf_counter() - started) * 1000)
    results["measure_round_trip_ms"] = summary(times)


def start_click_test():
    with VGroup(gap=16, padding=40):
        count = Label(text="0", font_size=48, bold=1)
        button = Button(text="+1", width=80, height=44, on_click=lambda: count.set(text=str(int(count.text) + 1)))
        reporter = Label(text="", width=1, height=1, opacity=0)
    reporter.on("report", lambda obj, event: finish(event["detail"], count))
    measure_reads(count)
    app.evaluate(f"setTimeout(function () {{ __bench.clicks({button.js}, {count.js}, {reporter.js}, {CLICKS}, {CLICK_GAP_MS}); }}, 0)")


def finish(report, count):
    results["click_to_page_ms"] = summary(report["toApply"])
    results["click_to_frame_ms"] = summary(report["toFrame"])
    results["clicks"] = {"sent": CLICKS, "text_on_page": report["text"], "text_in_python": count.text}
    results["machine"] = {
        "python": platform.python_version(),
        "pywebview": version("pywebview"),
        "os": f"{platform.system()} {platform.mac_ver()[0] or platform.release()}",
        "basic_js": app.basic_version,
    }
    with open(RESULTS_FILE, "w") as file:
        json.dump(results, file, indent=2)
    print(json.dumps(results, indent=2))
    app.close()


def stop_after_timeout():
    # WHY: a page that stops drawing (a hidden window) never sends the report: the window must still close.
    print("bench: timeout, the results so far:")
    print(json.dumps(results, indent=2))
    app.close()


def measure_all():
    results["startup"] = dict(app.timings)
    app.evaluate(BENCH_JS)
    measure_batched()
    measure_one_call_each()
    start_click_test()


def start(page):
    watchdog = threading.Timer(TIMEOUT_SECONDS, stop_after_timeout)
    watchdog.daemon = True
    watchdog.start()
    # WHY after: the window is shown when start() has drawn; a hidden window draws no frames to measure
    app.after(SHOW_WAIT_MS, measure_all)


app = App(start, title="OzdenUI bench", size=(900, 700))

if __name__ == "__main__":
    app.run()
