import pygame as pg

from .. import tools, prepare
from ..components.labels import MultiLineLabel, Blinker


class SolvedScreen(tools._State):
    font = prepare.FONTS["Perfect DOS VGA 437 Win"]
    def __init__(self):
        super(SolvedScreen, self).__init__()
        self.next = "MENU"
                
    def startup(self, persistent):
        self.persist = persistent
        self.cryptogram = self.persist["cryptogram"]
        text = self.cryptogram.original_text        
        self.solution_label = MultiLineLabel(
                    self.font, 32, text, (25, 84, 25),
                    {"center": (prepare.SCREEN_RECT.center)}, char_limit=32)
        self.proceed = Blinker(
                    "Press ENTER to continue", {"midbottom":
                    (prepare.SCREEN_RECT.centerx,
                    prepare.SCREEN_RECT.bottom - 10)}, 500, 
                    font_path=self.font, font_size=48, 
                    text_color=(50, 168, 50))
                    
    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                self.done = True

                
    def update(self, dt):
        self.proceed.update(dt)
        

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.solution_label.draw(surface)
        self.proceed.draw(surface)