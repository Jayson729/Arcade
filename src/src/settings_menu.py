import sys
import pygame
from state import State
from cloud import Cloud
from button import Button
from sprite import Sprite, AnimatedSprite
from settings import Settings


class SettingsMenu(State):
    """Main class that calls everything else"""

    def __init__(self) -> None:
        """Initializes SettingsMenu"""

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/settings_menu/'
        self.global_path = 'images/start_menu/'
        self.clock = pygame.time.Clock()
        self.screen = self.get_screen()
        pygame.display.set_caption('Start Menu')
        pygame.display.set_icon(pygame.image.load(f'{self.global_path}main.png'))
        self.create_game()
        super().__init__()

    def create_game(self):
        self.background = self.get_background()

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(0.3)

        pygame.mixer.music.load('music/runescape_dream.wav')
        pygame.mixer.music.set_volume(0.2)
        # loops music
        pygame.mixer.music.play(-1)



        # starts first button as hovered


    @staticmethod
    def get_screen() -> pygame.Surface:
        """Returns a Surface to be used as a screen"""
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def get_background(self) -> Sprite:
        """Creates background as Sprite"""
        bg_image = pygame.image.load(f"{self.img_path}settings_menu_background.png")
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def startup(self) -> None:
        """Starts the game loop"""
        while True:
            self.draw()
            self.update()
            # self.clock.tick(Settings.fps)
            # print(f"fps: {self.clock.get_fps()}")

    def draw(self):
        self.background.draw(self.screen)

def main() -> None:
    """Main function"""
    settings_menu = SettingsMenu()
    settings_menu.startup()


if __name__ == '__main__':
    main()