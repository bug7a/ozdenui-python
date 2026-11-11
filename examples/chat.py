# Bismillah
"""A chat with an AI that is only a sample: for every message it writes a small plan, word by word, as an AI that streams
its answer does (in a background job, so the window keeps working). Stop ends the answer, New chat starts again.
Your AI goes into write_answer(): every piece it gives goes to chat.append_text(key, piece).
python chat.py dark: the same window in the dark theme.
"""

import re
import sys
import time

from ozdenui import App, ChatView, HGroup, Label, SmartButton, VGroup, run_in_background

COLORS = {"light": "#FFFFFF", "dark": "#1C1C1B"}  # the ground of the ChatView in each theme
THINK_SECONDS = 0.6  # before the first words: the dots
WORD_SECONDS = 0.04  # between two words
ANSWER = """Here is a small plan for **{topic}**:

1. Write down what you want to do
2. Split it into small steps
3. Do one step a day

| Day | Step |
|:---|:---|
| Monday | The list |
| Tuesday | The first step |

```python
steps = ["the list", "the first step"]
print(len(steps), "steps")
```

Ask again if something is not clear."""
FIRST_MESSAGES = [{"role": "system", "text": "A sample: the answers are written by this program, not by an AI"}]

view = {"stop": False}


def pieces_of(text):
    """The answer in pieces of one word (with the spaces before it), as a stream gives them."""
    return re.findall(r"\s*\S+|\s+$", text)


def write_answer(chat, key, topic):
    """In a background job: the window keeps working while the answer comes."""
    time.sleep(THINK_SECONDS)
    for piece in pieces_of(ANSWER.format(topic=topic)):
        if view["stop"]:
            return  # WHY no busy = False: Stop did it on the page
        chat.append_text(key, piece)
        time.sleep(WORD_SECONDS)
    chat.busy = False


def answer(chat, text):
    view["stop"] = False
    key = chat.add_message(role="assistant")
    chat.busy = True
    run_in_background(write_answer, chat, key, text)


def stop_answer(chat):
    view["stop"] = True


def new_chat():
    view["stop"] = True
    view["chat"].busy = False
    view["chat"].set_messages(FIRST_MESSAGES)


def start(page):
    page.color = COLORS[page.app.theme]
    with VGroup(gap=0):
        with HGroup(width="100%", height="auto", align="left center", gap=12, padding=[16, 10]):
            Label(text="A chat", font_size=17, bold=True, fill=True)
            SmartButton(text="New chat", on_click=new_chat)
        view["chat"] = ChatView(width="100%", fill=True, messages=FIRST_MESSAGES, empty_text="Ask something",
                                on_send=answer, on_stop=stop_answer)
        view["chat"].focus()


if __name__ == "__main__":
    App(start, title="A chat", size=(720, 760), theme=sys.argv[1] if len(sys.argv) > 1 else "light").run()
