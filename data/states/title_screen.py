from random import shuffle
from string import ascii_uppercase, maketrans, translate

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.font = prepare.FONTS["Perfect DOS VGA 437 Win"]
        self.next = "MENU"
        self.text = "CRYPTOGRAMMER"
        self.encrypt()
        self.letters = list(set((x for x in self.text)))
        shuffle(self.letters)
        self.timer = 0
        self.switch_span = 300
        self.make_labels()

    def encrypt(self):
        from_ = ascii_uppercase
        to_ = list(ascii_uppercase)
        shuffle(to_)
        to_ = "".join(to_)
        self.trans_table = maketrans(from_, to_)
        self.encrypted = translate(self.text, self.trans_table)

    def make_labels(self):
        top = 200
        left = 200
        self.labels = []
        style = {"font_path": self.font, "font_size": 64, "text_color": (25, 84, 25)}
        for char in self.encrypted:
            self.labels.append(Label(char, {"topleft": (left, top)}, **style))
            left += 50

    def choose_letter(self):
        try:
            letter = self.letters.pop()
        except IndexError:
            letter = None
        return letter

    def change_letter(self, indx, letter):
        to_replace = self.encrypted[indx]
        for i, label in enumerate(self.labels):
            if self.encrypted[i] == to_replace:
                label.set_text(letter)

    def switch_letter(self):
        if not self.letters:
            return
        letter = self.choose_letter()
        indx = self.text.index(letter)
        self.change_letter(indx, letter)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            else:
                self.done = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.switch_span:
            self.timer -= self.switch_span
            self.switch_letter()

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for label in self.labels:
            label.draw(surface)
