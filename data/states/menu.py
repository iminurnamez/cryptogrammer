import os
import json
from string import punctuation

import pygame as pg

from .. import tools, prepare
from ..components.labels import Button
from ..components.cryptogram import Cryptogram


def judge_difficulty(text):
    words = [w.strip(punctuation) for w in text.split(" ")]
    num_words = len(words)
    doubles = 0
    one_letter = len([x for x in words if len(x) == 1])
    two_letters = len([x for x in words if len(x) == 2])
    three_letters = len([x for x in words if len(x) == 3])
    four_letters = len([x for x in words if len(x) == 4])
    for w in words:
        for i, c in enumerate(w):
            try:
                next_letter = w[i + 1]
                if next_letter == c:
                    doubles += 1
            except IndexError:
                pass
    score = sum((one_letter * 5, two_letters * 4, three_letters * 3,
                        four_letters * 1, doubles * 2, num_words))
    return score


class Menu(tools._State):
    def __init__(self):
        super(Menu, self).__init__()

    def load_puzzles(self):
        p = os.path.join("resources", "quotes.txt")
        with open(p, "r") as f:
            self.puzzles = []
            for line in f.readlines():
                stripped = line.strip()
                self.puzzles.append(stripped.upper())

    def load_solved(self):
        p = os.path.join("resources", "solved.json")
        try:
            with open(p, "r") as f:
                self.solved = json.load(f)
        except IOError:
            self.solved = []

    def make_buttons(self):
        w, h  = 200, 80
        start_left = 140
        left = start_left
        top = 30
        self.buttons = []
        style = {"button_size": (200, 80), "text_color": "gray80",
                     "font_size": 32, "fill_color": "gray20",
                     "hover_fill_color": "gray40", "hover_text_color": "gray80"}
        for i, p in enumerate(self.puzzles, start=1):
            b = Button((left, top), text="{}".format(i), hover_text="{}".format(i),
                       call=self.choose_puzzle, args=p, **style)
            self.buttons.append(b)
            left += 300
            if not i % 3:
                top += 100
                left = start_left

    def choose_puzzle(self, puzzle):
        self.persist["text"] = puzzle
        self.done = True
        self.next = "GAMEPLAY"

    def startup(self, persistent):
        self.persist = persistent
        self.load_puzzles()
        self.puzzles = sorted(self.puzzles, key=judge_difficulty, reverse=True)
        self.load_solved()
        self.current_index = 0
        self.make_buttons()
        current = self.buttons[self.current_index]
        current.image = current.hover_image

    def move_cursor(self, direction):
        self.current_index += direction
        if self.current_index < 0:
                    self.current_index = len(self.puzzles) - 1
        elif self.current_index > len(self.puzzles) - 1:
                    self.current_index = 0
        for b in self.buttons:
            b.image = b.idle_image
        current = self.buttons[self.current_index]
        current.image = current.hover_image

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_LEFT:
                self.move_cursor(-1)
            elif event.key == pg.K_RIGHT:
                self.move_cursor(1)
            elif event.key == pg.K_RETURN:
                self.puzzle = self.buttons[self.current_index].args
                self.persist["text"] = self.puzzle
                self.done = True
                self.next = "GAMEPLAY"

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for b in self.buttons:
            b.draw(surface)

