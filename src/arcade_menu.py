import pygame
from state import State
from people import People
from sprite import Sprite
from button import Button, ButtonGroup
from settings import Settings


class ArcadeMenu(State):

    def __init__(self) -> None:

        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.img_path = 'images/arcade_menu'
        self.global_img_path = 'images/'
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Select Game')
        pygame.display.set_icon(pygame.image.load(
            f'{self.global_img_path}main.png'))
        self.create_menu()

    def create_menu(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()
        self.people = self.get_people()

        self.menu_sound = pygame.mixer.Sound()
        self.menu_sound.set_volume(Settings.effects_volume/100)

        pygame.mixer.music.load()
        pygame.mixer.music.set_volume(Settings.music_volume/100)
        # loops music
        pygame.mixer.music.play(-1)

    def get_screen(self) -> pygame.Surface:
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def get_background(self) -> Sprite:
        bg_image = pygame.image.load(f"{self.img_path}backgroundAMenu.png")
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def get_people(self) -> pygame.sprite.Group:
        # TO DO
        person1Img = pygame.image.load(f"{self.img_path}people_sprite.png")
        person2Img = pygame.image.load(f"{self.img_path}people_sprite2.png")
        people = pygame.sprite.Group()

        people.add(People(person1Img, 100, 100).resize(650, 650))
        people.add(People(person2Img, 200, 200).resize(650, 650))

        return people

    def get_buttons(self) -> ButtonGroup:
        # TO DO
        def back_action():
            print('back')
            self.next_state = 'START'
            self.done = True

        def pong_action():
            print('pong')

        def pacman_action():
            print('pacman')

        buttons = ButtonGroup()

        buttons.add(
            Button(50, 575, 'BACK', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   back_action)
        )

        return buttons

    def cabinetScreen(x, y, width, height, color):
        pygame.draw.rect(gameDisplay, color, (x, y, width, height))

    def draw(self, screen):
        self.background.draw(screen)
        self.people.draw(screen)
        self.buttons.draw(screen)

    def update(self):
        self.people.update()
        self.buttons.update()

def main() -> None:
    from main import main
    main('START')

if __name__ == '__main__':
    main()
