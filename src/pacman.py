"""TODO: Ghosts need to move
Ghosts need to interact with pacman
Pacman hitbox is all messed up for some reason (probably in pacman_sprite.py)
Add some sounds/music
Maybe some buttons for settings/pausing? 
or maybe those will be part of the eventual pause menu

"""

import sys
import pygame
from sprite import Sprite
from pacman_sprite import PacmanSprite
from state import State
from settings import Settings, Colors, Fonts
# from spritesheet import SpriteSheet
from animated_sprite import AnimatedSprite
from ghost import Ghost

class Pacman(State):

    def __init__(self):
        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/pacman/'
        self.clock = pygame.time.Clock()
        self.screen = self.create_screen()
        pygame.display.set_caption('Pacman')
        self.create_game()
        super().__init__()

    def create_screen(self):
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def create_game(self):
        self.map = self.get_map()
        self.pacman = self.get_pacman()
        self.ghosts = self.get_ghosts()
    
    def get_map(self):
        return None
    
    def get_pacman(self):
        return PacmanSprite(600, 400, 
            f'{self.img_path}yellow_pacman/', 
            f'{self.img_path}pacman_death/',
        )
    
    def get_ghosts(self):
        ghosts = pygame.sprite.Group()
        blue_ghost = Ghost(300, 100, f'{self.img_path}blue_ghost/', animation_speed=0.15)
        red_ghost = Ghost(400, 200, f'{self.img_path}red_ghost/', animation_speed=0.15)
        orange_ghost = Ghost(300, 300, f'{self.img_path}orange_ghost/', animation_speed=0.15)
        pink_ghost = Ghost(400, 400, f'{self.img_path}pink_ghost/', animation_speed=0.15)

        ghosts.add(blue_ghost)
        ghosts.add(red_ghost)
        ghosts.add(orange_ghost)
        ghosts.add(pink_ghost)

        return ghosts
    
    def startup(self) -> None:
        while True:
            self.check_events()
            self.update()
            self.draw()
            # pygame.display.flip()
            # self.clock.tick(Settings.fps)
            # print(f"fps: {self.clock.get_fps()}")

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def draw(self) -> None:
        # self.screen.blit(self.background.image, (0, 0))
        self.screen.fill((0, 0, 0))
        # self.map.draw(self.screen)
        self.pacman.draw(self.screen)
        self.ghosts.draw(self.screen)
        # self.buttons.draw(self.screen)

    def update(self) -> None:
        self.pacman.update()
        self.ghosts.update()
        # self.buttons.update()
        # self.map.update()
        pygame.display.flip()
        self.clock.tick(Settings.fps)

def main() -> None:
    pacman = Pacman()
    pacman.startup()

if __name__ == '__main__':
    main()
        
                