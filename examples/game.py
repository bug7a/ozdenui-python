# Bismillah
"""Catch the dots: move the square with the arrow keys and touch the dot before the time is over.
Objects at a place of their own (left, top), the keys of the page and a timer."""

import random

from ozdenui import App, Box, HGroup, Label, SmartButton, VGroup, every

PAGE_COLOR = "#14213D"
FIELD_COLOR = "#1F2E52"
PLAYER_COLOR = "#FCA311"
DOT_COLOR = "#2EC4B6"
TEXT_LIGHT = "#E5E5E5"
FIELD_WIDTH = 560
FIELD_HEIGHT = 360
PLAYER_SIZE = 34
DOT_SIZE = 18
STEP = 22
GAME_SECONDS = 30
MOVES = {"ArrowLeft": (-STEP, 0), "ArrowRight": (STEP, 0), "ArrowUp": (0, -STEP), "ArrowDown": (0, STEP)}

view = {}
game = {"score": 0, "left": GAME_SECONDS, "running": False, "stop_timer": None}


def start(page):
    page.color = PAGE_COLOR
    with VGroup(gap=14, padding=24):
        with HGroup(hug=True, gap=40):
            view["score"] = Label(text="Score: 0", font_size=20, bold=True, text_color=TEXT_LIGHT)
            view["time"] = Label(text=f"Time: {GAME_SECONDS}", font_size=20, bold=True, text_color=TEXT_LIGHT)
        with Box(width=FIELD_WIDTH, height=FIELD_HEIGHT, color=FIELD_COLOR, round=10):
            view["dot"] = Box(0, 0, DOT_SIZE, DOT_SIZE, color=DOT_COLOR, round=DOT_SIZE // 2)
            view["player"] = Box(0, 0, PLAYER_SIZE, PLAYER_SIZE, color=PLAYER_COLOR, round=6)
        view["button"] = SmartButton(text="Play", style_name="ozdenDark", on_click=play)
    view["player"].call("setMotion", "left 0.08s, top 0.08s")
    page.on("keydown", lambda page_, event: move(event.get("key")))
    place_player_in_middle()
    place_dot()


def place_player_in_middle():
    view["player"].set(left=(FIELD_WIDTH - PLAYER_SIZE) // 2, top=(FIELD_HEIGHT - PLAYER_SIZE) // 2)


def place_dot():
    view["dot"].set(left=random.randint(0, FIELD_WIDTH - DOT_SIZE), top=random.randint(0, FIELD_HEIGHT - DOT_SIZE))


def play():
    if game["running"]:
        return
    game.update(score=0, left=GAME_SECONDS, running=True)
    view["score"].text = "Score: 0"
    view["time"].text = f"Time: {GAME_SECONDS}"
    view["button"].enabled = False
    place_player_in_middle()
    place_dot()
    game["stop_timer"] = every(1000, tick)


def tick():
    game["left"] -= 1
    view["time"].text = f"Time: {game['left']}"
    if game["left"] > 0:
        return
    game["running"] = False
    game["stop_timer"]()
    view["time"].text = "Time is over"
    view["button"].enabled = True


def move(key):
    if not game["running"] or key not in MOVES:
        return
    step_x, step_y = MOVES[key]
    player = view["player"]
    left = min(max(player.left + step_x, 0), FIELD_WIDTH - PLAYER_SIZE)
    top = min(max(player.top + step_y, 0), FIELD_HEIGHT - PLAYER_SIZE)
    player.set(left=left, top=top)
    if touches(player, view["dot"]):
        game["score"] += 1
        view["score"].text = f"Score: {game['score']}"
        place_dot()


def touches(a, b):
    """Two boxes overlap (their places are kept in Python: no question to the page)."""
    return (a.left < b.left + DOT_SIZE and b.left < a.left + PLAYER_SIZE
            and a.top < b.top + DOT_SIZE and b.top < a.top + PLAYER_SIZE)


if __name__ == "__main__":
    App(start, title="Catch the dots", size=(620, 520)).run()
