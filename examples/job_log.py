# Bismillah
"""A job in the background and its output in the window: print(), the logging module and the levels of a LogView."""

import logging
import time

from ozdenui import App, CheckBox, HGroup, LogView, ProgressBar, SmartButton, StatusBar, VGroup, run_in_background

STEP_SECONDS = 0.15
FILES = ["photo.jpg", "notes.txt", "disk.bin", "report.pdf", "song.mp3", "backup.zip"]

view = {}
logger = logging.getLogger("job")


def start(page):
    page.color = "#FFFFFF"
    with VGroup(gap=0, align="left top"):
        with VGroup(width="100%", height="auto", gap=10, padding=12, align="left top", shrink=0):
            with HGroup(hug=True, gap=8, align="left center"):
                view["run"] = SmartButton(text="Run the job", tone="cyan", on_click=run_job)
                SmartButton(text="Clear", on_click=lambda: view["log"].clear())
                CheckBox(text="Only warnings and errors", on_change=show_levels)
            view["bar"] = ProgressBar(title_text="Files", max_value=len(FILES), width="100%")
        view["log"] = LogView(fill=True, framed=False, empty_text="Run the job: its output comes here.")
        view["status"] = StatusBar(message="Ready", items=[{"key": "files", "text": "0 files"}])
    # Everything a program writes goes into the view: print() and the logging module.
    view["log"].capture_print()
    logger.addHandler(view["log"].logging_handler())
    logger.setLevel(logging.INFO)


def show_levels(box):
    view["log"].set_levels(["warn", "error"] if box.checked else [])


def run_job():
    view["run"].enabled = False
    view["bar"].value = 0
    view["status"].set_busy(True)
    view["status"].set_message("The job is running...")
    run_in_background(job)


def job():
    print("The job started")
    for index, name in enumerate(FILES):
        time.sleep(STEP_SECONDS)
        if name.endswith(".bin"):
            logger.error("%s can not be read: permission denied", name)
        elif name.endswith(".zip"):
            logger.warning("%s is very large", name)
        else:
            logger.info("Copied %s", name)
        view["bar"].value = index + 1
        view["status"].set_item_text("files", f"{index + 1} files")
    print("The job ended")
    view["log"].success("Done")
    view["status"].set_busy(False)
    view["status"].set_message("Ready")  # the lasting message: "Done" goes back to it
    view["status"].set_message("Done", "success", 3000)
    view["run"].enabled = True


if __name__ == "__main__":
    App(start, title="A job and its log", size=(680, 520)).run()
