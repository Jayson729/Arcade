"""TODO: Actually implement this into the menu"""

import sys
import pygame
from new_start_menu import StartMenu
from pong import Pong
from game import Game
from pacman import Pacman


pygame.init()
screen = pygame.display.set_mode((800, 600))

states = {
    # "START": StartMenu,
    "START": StartMenu,
    # "ARCADE" : ArcadeMenu(),
    # "SETTINGS" : SettingsMenu(),
    # "CREDITS" : Credits(),
    "SETTINGS": Pong,
    'CREDITS': Pacman,

}

game = Game(screen, states, "START")
game.run()


pygame.quit()
sys.exit()
