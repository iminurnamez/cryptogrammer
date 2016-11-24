from string import ascii_uppercase, punctuation, maketrans, translate
from random import shuffle

import pygame as pg

from ..import prepare
from ..components.labels import wrap_text, Label, Button, ButtonGroup


class Cryptogram(object):
    unencryptable = punctuation + " "
    font = prepare.FONTS["Perfect DOS VGA 437 Win"]
    move_time = 150
    def __init__(self, text):
        text = text.upper()
        self.move_keys = {
                pg.K_LEFT: -1,
                pg.K_RIGHT: 1}
        self.original_text = text
        self.original_lines = wrap_text(text, 32)
        self.encrypt()
        self.make_labels()
        self.current_index = 0
        self.encrypted_cursor = pg.Rect(0, 0, 20, 30)
        self.solution_cursor = pg.Rect(0, 0, 20, 30)
        r1 = self.encrypted_labels[self.current_index].rect
        self.encrypted_cursor.center = r1.centerx - 1, r1.centery - 1
        r2 = self.solution_labels[self.current_index].rect
        self.solution_cursor.center = r2.centerx -1, r2.centery -1
        self.move_timer = 0
        self.total_move_timer = 0
        self.adjusted_move_time = self.move_time
        self.buttons = ButtonGroup()
        self.hint_button = Button(
                    (890, 650), self.buttons, button_size=(120, 50),
                    text="HINT", hover_text="HINT", hover_text_color=(50, 168, 50),
                    call=self.give_hint, text_color=(25, 84, 25))
        pg.draw.rect(self.hint_button.idle_image, pg.Color(25, 84, 25),
                           (0, 0, 120, 50), 2)
        pg.draw.rect(self.hint_button.hover_image, pg.Color(50, 168, 50),
                           (0, 0, 120, 50), 2)
        self.hints_given = []
        self.hint_labels = pg.sprite.Group()
        self.hint_top = 20

    def encrypt(self):
        from_ = ascii_uppercase
        to_ = list(ascii_uppercase)
        shuffle(to_)
        to_ = "".join(to_)
        self.trans_table = maketrans(from_, to_)
        self.encrypted_lines = [translate(text, self.trans_table)
                                          for text in self.original_lines]

    def give_hint(self, *args):
        letters = [x for x in self.original_text if x not in self.unencryptable]
        shuffle(letters)
        for letter in letters:
            if letter not in self.hints_given:

                encrypted = translate(letter, self.trans_table)
                indx = self.encrypted.index(encrypted)
                while self.current_index != indx:
                    self.move_cursor(1)
                self.add_letter(letter)
                text = "{} = {}".format(encrypted, letter)
                Label(text, {"midtop": (950, self.hint_top)}, self.hint_labels,
                         font_path=self.font, font_size=32, text_color=(84, 84, 25))
                self.hint_top += 30
                self.hints_given.append(letter)
                return

    def make_labels(self):
        left = 120
        e_top = 100
        o_top = 400
        h_space = 20
        v_space = 50
        self.encrypted_labels = []
        self.solution_labels = []
        self.solution = []
        self.encrypted = []
        style = {"font_path": self.font, "font_size": 32,
                     "text_color": (25, 84, 25)}
        for original, encrypted in zip(self.original_lines, self.encrypted_lines):
            for o_char, e_char in zip(original, encrypted):
                char = o_char if o_char in self.unencryptable else "_"
                self.solution_labels.append(
                            Label(char, {"topleft": (left, o_top)}, **style))
                self.solution.append(char)
                self.encrypted_labels.append(
                            Label(e_char, {"topleft": (left, e_top)}, **style))
                self.encrypted.append(e_char)
                left += h_space
            left += h_space
            self.solution.append(" ")
            self.solution_labels.append(
                        Label(" ", {"topleft": (left, o_top)}, **style))
            self.encrypted_labels.append(
                        Label(" ", {"topleft": (left, e_top)}, **style))
            self.encrypted.append(" ")
            e_top += v_space
            o_top += v_space
            left = 120
        self.solution = self.solution[:-1]

    def move_cursor(self, direction):
        self.current_index += direction
        if self.current_index < 0:
            self.current_index = len(self.solution) - 1
        elif self.current_index > len(self.solution) - 1:
            self.current_index = 0
        r1 = self.solution_labels[self.current_index].rect
        r2 = self.encrypted_labels[self.current_index].rect
        self.solution_cursor.center = r1.centerx - 1, r1.centery - 1
        self.encrypted_cursor.center = r2.centerx - 1, r2.centery - 1
        if self.encrypted[self.current_index] in self.unencryptable:
            self.move_cursor(direction)

    def add_letter(self, letter):
        if letter not in self.trans_table:
            return
        current_solution = self.solution[self.current_index]
        current_encrypted = self.encrypted[self.current_index]
        if current_solution == letter:
            return
        if letter in self.solution:
            first = self.solution.index(letter)
            self.replace_letter(self.encrypted[first], "_")
            self.replace_letter(current_encrypted, letter)
        elif current_solution == "_":
            self.replace_letter(current_encrypted, letter)
        else:
            self.replace_letter(current_encrypted, letter)

    def replace_letter(self, to_replace, letter):
        for i, s in enumerate(self.encrypted):
            if s == to_replace:
                self.solution[i] = letter
                self.solution_labels[i].set_text(letter)

    def check_solved(self):
        if "".join(self.solution) == self.original_text:
            return True
        return False

    def get_event(self, event):
        self.buttons.get_event(event)
        if event.type == pg.KEYUP:
            if event.key in self.move_keys:
                self.move_cursor(self.move_keys[event.key])
                self.move_timer = 0
            else:
                letter = pg.key.name(event.key).upper()
                self.add_letter(letter)
                self.move_timer = 0

    def update(self, dt):
        keys = pg.key.get_pressed()
        for key in self.move_keys:
            if keys[key]:
                self.move_timer += dt
                self.total_move_timer += dt
                if self.move_timer >= self.adjusted_move_time:
                    self.move_cursor(self.move_keys[key])
                    self.move_timer -= self.adjusted_move_time
                if self.total_move_timer >= self.move_time * 2:
                    self.total_move_timer -= self.move_time * 2
                    self.adjusted_move_time -= 20
                break
        else:
            self.move_timer = 0
            self.adjusted_move_time = self.move_time
            self.total_move_timer = 0
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        for e in self.encrypted_labels:
            e.draw(surface)
        for l in self.solution_labels:
            l.draw(surface)
        pg.draw.rect(surface, pg.Color("yellow"), self.encrypted_cursor, 1)
        pg.draw.rect(surface, pg.Color("yellow"), self.solution_cursor, 1)
        self.buttons.draw(surface)
        self.hint_labels.draw(surface)