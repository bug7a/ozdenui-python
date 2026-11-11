# Bismillah
"""The dialogs: each one returns its answer (the code waits; the window keeps working meanwhile)."""

from ozdenui import App, Dialog, HGroup, Label, SmartButton, Toast, VGroup

PAGE_COLOR = "#F4F5F7"
TEXT_SOFT = "#5A6270"

view = {}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=16, padding=36, align="left top"):
        Label(text="Dialogs", font_size=24, bold=True)
        with HGroup(hug=True, gap=8):
            SmartButton(text="Alert", on_click=show_alert)
            SmartButton(text="Confirm", on_click=show_confirm)
            SmartButton(text="Prompt", on_click=show_prompt)
            SmartButton(text="Ask", on_click=show_ask)
            SmartButton(text="Toast", on_click=lambda: Toast.info("A short message.", title="Info"))
        Label(text="The answer:", font_size=13, text_color=TEXT_SOFT)
        view["answer"] = Label(text="-", font_size=20)


def tell(answer):
    view["answer"].text = repr(answer)


def show_alert():
    Dialog.alert("The file was saved.", title="Saved")
    tell("closed")


def show_confirm():
    tell(Dialog.confirm("The old copy will be replaced.", title="Replace it?", confirm_text="Replace"))


def show_prompt():
    tell(Dialog.prompt("A name for the new folder:", title="New folder", value="Photos", required=True))


def show_ask():
    tell(Dialog.ask("You have changes that are not saved.", title="Save them?",
                    buttons=["Save", "Don't save", "Cancel"]))


if __name__ == "__main__":
    App(start, title="Dialogs", size=(640, 420)).run()
