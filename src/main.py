"""TODO: Actually implement this into the menu"""

import sys
import pygame
from start_menu import StartMenu
from arcade_menu import ArcadeMenu
from pong import Pong
from game import Game
from pacman import Pacman
from settings_menu import SettingsMenu
from settings import Settings
from pause_menu import PauseMenu


def main(state):
    pygame.init()
    screen = pygame.display.set_mode(Settings.resolutions[0])

    states = {
        # "START": StartMenu,
        "START": StartMenu,
        "ARCADE" : ArcadeMenu,
        # "SETTINGS" : SettingsMenu(),
        # "CREDITS" : Credits(),
        "SETTINGS": SettingsMenu,
        'CREDITS': Pacman,
        'PACMAN': Pacman,
        'PAUSE': PauseMenu,
        'PONG': Pong,
    }

    game = Game(screen, states, state)
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main('START')
