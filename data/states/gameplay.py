import pygame as pg

from .. import tools, prepare
from ..components.cryptogram import Cryptogram


class Gameplay(tools._State):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.next = "SOLVED_SCREEN"

    def startup(self, persistent):
        self.persist = persistent
        text = self.persist["text"]
        self.cryptogram = Cryptogram(text)
        self.current_index = 0

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.cryptogram.get_event(event)

    def update(self, dt):
        self.cryptogram.update(dt)
        if self.cryptogram.check_solved():
            self.done = True
            self.persist["cryptogram"] = self.cryptogram

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.cryptogram.draw(surface)

