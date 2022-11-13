import sys
import pygame
from start_menu import StartMenu
from new_start_menu import StartMenu as StartMenu2
#from states.settings_menu import SettingsMenu
#from states.credits import Credits
#from states.arcade_menu import ArcadeMenu
from pong import Pong
from game import Game


pygame.init()
screen = pygame.display.set_mode((800, 600))

states = {
    "START": StartMenu(),
    # "START": StartMenu2()
    # "ARCADE" : ArcadeMenu(),
    # "SETTINGS" : SettingsMenu(),
    # "CREDITS" : Credits(),
    # "PONG": Pong()

}

game = Game(screen, states, "START")
game.run()


pygame.quit()
sys.exit()
