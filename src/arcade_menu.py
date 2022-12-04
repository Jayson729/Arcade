import pygame
from state import State
from people import People
from sprite import Sprite, AnimatedSprite
from button import Button, ButtonGroup
from settings import Settings


class ArcadeMenu(State):

    def __init__(self) -> None:

        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.img_path = 'images/arcade_menu/'
        self.global_img_path = 'images/'
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Select Game')
        pygame.display.set_icon(pygame.image.load(
            f'{self.global_img_path}main.png'))
        self.create_menu()

    def create_menu(self):
        self.background = self.get_background()
        self.pac = self.get_pac()
        self.anipac = self.get_anipac()
        self.buttons = self.get_buttons()
        self.people = self.get_people()

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume/100)

        pygame.mixer.music.load('music/runescape_dream.wav')
        pygame.mixer.music.set_volume(Settings.music_volume/100)
        # loops music
        pygame.mixer.music.play(-1)

    def get_screen(self) -> pygame.Surface:
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def get_pac(self):
        pacimg = pygame.image.load(f"{self.img_path}pac.png")
        pac = Sprite(200, 200, pacimg)
        pac.resize(200, 200)
        return pac

    def get_anipac(self):
        anipac = AnimatedSprite(
            200, 200, f'{self.img_path}anipac/', animation_speed=150)
        anipac.resize(200, 200)
        return anipac

    def get_background(self) -> Sprite:
        bg_image = pygame.image.load(f"{self.img_path}backgroundArcade.png")
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def get_people(self, move_horif: float = 1, move_horib = 1.1,
                   move_vert: float = 1) -> pygame.sprite.Group:
        # TO DO
        personf1Img = pygame.image.load(f"{self.img_path}peoplef1.png")
        personb1Img = pygame.image.load(f"{self.img_path}peopleb1.png")
        people = pygame.sprite.Group()

        people.add(People(personb1Img, -40, 760,
                    move_horib, move_vert).resize(155, 291))
        people.add(People(personf1Img, 895, -55,
                    move_horif, move_vert).resize(214, 430))

        return people

    def get_buttons(self) -> ButtonGroup:
        def back_action():
            print('back')
            self.next_state = 'START'
            self.done = True

        def pong_action():
            print('pong')
            self.next_state = 'PONG'
            self.done = True

        def pacman_action():
            print('pacman')
            self.next_state = 'PACMAN'
            self.done = True

        buttons = ButtonGroup()

        buttons.add(
            Button(50, 575, 'BACK', pygame.font.Font(
                'fonts/Stardew_Valley.ttf', 40), back_action))
        buttons.add(
            Button(350, 380, 'PONG', pygame.font.Font(
                'fonts/Stardew_Valley.ttf', 1), pong_action))
        buttons.add(
            Button(410, 205, 'PACMAN', pygame.font.Font(
                'fonts/Stardew_Valley.ttf', 50), pacman_action))

        return buttons

    def do_event(self, event):
        self.buttons.do_event(event, self.menu_sound)

    def draw(self, screen):
        self.background.draw(screen)
        self.people.draw(screen)
        self.buttons.draw(screen)
        self.pac.draw(screen)

    def draw_anipac(self, screen):
        self.anipac.draw(screen)

    def update(self):
        self.anipac.update()
        self.people.update()
        self.buttons.update()


def main() -> None:
    from main import main
    main('ARCADE')


if __name__ == '__main__':
    main()
