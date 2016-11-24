from . import prepare,tools
from .states import title_screen, gameplay, menu, solved_screen

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
                   "MENU": menu.Menu(),
                   "GAMEPLAY": gameplay.Gameplay(),
                   "SOLVED_SCREEN": solved_screen.SolvedScreen()}
    controller.setup_states(states, "TITLE")
    controller.main()
