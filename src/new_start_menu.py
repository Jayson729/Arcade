import sys
import pygame
from state import State
from cloud import Cloud
from button import Button
from sprite import Sprite, AnimatedSprite
from settings import Settings


class StartMenu(State):
    """Main class that calls everything else"""

    def __init__(self) -> None:
        """Initializes StartMenu"""

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/start_menu/'
        self.clock = pygame.time.Clock()
        self.screen = self.get_screen()
        pygame.display.set_caption('Start Menu')
        pygame.display.set_icon(pygame.image.load(f'{self.img_path}main.png'))
        self.create_game()
        super().__init__()

    def create_game(self):
        self.background = self.get_background()
        self.waterfall = self.get_waterfall()
        self.clouds = self.get_clouds()
        self.buttons = self.get_buttons()
        self.NUM_BUTTONS = len(self.buttons)

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(0.3)

        pygame.mixer.music.load('music/runescape_dream.wav')
        pygame.mixer.music.set_volume(0.2)
        # loops music
        pygame.mixer.music.play(-1)

        self.curr_index = 0

        # starts first button as hovered
        first_sprite = self.buttons.sprites()[self.curr_index]
        first_sprite.set_keyboard_hover(True)

    def get_waterfall(self):
        waterfall = AnimatedSprite(390, 350, f'{self.img_path}waterfall/', animation_speed=150)
        waterfall.resize(60, 415)
        return waterfall

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
        bg_image = pygame.image.load(f"{self.img_path}backgroundMain.png")
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def get_clouds(self, sway_distance: float=1.5,
            sway_speed: float=0.025) -> pygame.sprite.Group:
        """Creates a group of clouds"""
        # load images
        large_cloud_img = pygame.image.load(f'{self.img_path}large_cloud.png')
        small_cloud_img = pygame.image.load(f'{self.img_path}small_cloud.png')
        small_cloud_mirrored = pygame.transform.flip(small_cloud_img, True, False)

        # add all clouds to a sprite group
        clouds = pygame.sprite.Group()
        # clouds.add(Cloud(large_cloud_img, 155, 465, sway_distance, sway_speed).resize(650, 650))
        # clouds.add(Cloud(large_cloud_img, 750, 415, sway_distance, sway_speed).resize(500, 450))
        # clouds.add(Cloud(large_cloud_img, 780, 525, sway_distance, sway_speed).resize(800, 760))
        # clouds.add(Cloud(large_cloud_img, 90, 570, sway_distance, sway_speed).resize(760, 760))
        # clouds.add(Cloud(small_cloud_img, 600, 80, sway_distance, sway_speed).resize(150, 100))
        # clouds.add(Cloud(small_cloud_mirrored, 160, 135, sway_distance, sway_speed).resize(200, 170))

        clouds.add(Cloud(large_cloud_img, -170, 140, sway_distance, sway_speed).resize(650, 650))
        clouds.add(Cloud(large_cloud_img, 500, 190, sway_distance, sway_speed).resize(500, 450))
        clouds.add(Cloud(large_cloud_img, 380, 145, sway_distance, sway_speed).resize(800, 760))
        clouds.add(Cloud(large_cloud_img, -290, 190, sway_distance, sway_speed).resize(760, 760))
        clouds.add(Cloud(small_cloud_img, 525, 30, sway_distance, sway_speed).resize(150, 100))
        clouds.add(Cloud(small_cloud_mirrored, 60, 50, sway_distance, sway_speed).resize(200, 170))

        return clouds

    def get_buttons(self) -> pygame.sprite.Group:
        """Creates a group of buttons"""
        def arcade_action():
            print('arcade')
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound('sounds/arcade_door.wav')
            )
            # self.next_state = 'ARCADE'
            # self.done = True
        def settings_action():
            print('settings')
            self.next_state = 'SETTINGS'
            self.done = True
        def credits_action():
            print('credits')
            self.next_state = 'CREDITS'
            self.done = True
        buttons = pygame.sprite.Group()
        buttons.add(Button(410, 125, 'ENTER ARCADE', pygame.font.Font('fonts/Stardew_Valley.ttf', 50), arcade_action))
        buttons.add(Button(410, 165, 'SETTINGS', pygame.font.Font('fonts/Stardew_Valley.ttf', 40), settings_action))
        buttons.add(Button(410, 205, 'CREDITS', pygame.font.Font('fonts/Stardew_Valley.ttf', 30), credits_action))

        return buttons

    def startup(self) -> None:
        """Starts the game loop"""
        while True:
            self.draw()
            self.update()
            self.check_events()
            # self.clock.tick(Settings.fps)
            # print(f"fps: {self.clock.get_fps()}")

    def check_events(self) -> None:
        """Accepts and deals with inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for b in self.buttons:
                mouse = pygame.mouse.get_pos()
                if b.check_mouse_hover(mouse):
                    # if the mouse is hovered, 
                    # set the keyboard hover for all buttons to false
                    for b in self.buttons:
                            b.set_keyboard_hover(False)

                    # if the mouse if hovered, check for mouse press
                    # if mouse press, do the button's action
                    if (event.type == pygame.MOUSEBUTTONDOWN
                            and event.button == 1):
                        b.do_action()
                        # if clicking multiple buttons,
                        # only do one action
                        break
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.change_button('up')
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.change_button('down')
                if event.key == pygame.K_RETURN:
                    self.handle_action()

    def draw(self):
        self.background.draw(self.screen)
        self.waterfall.draw(self.screen)
        self.clouds.draw(self.screen)
        self.buttons.draw(self.screen)

    def update(self):
        self.waterfall.update()
        self.clouds.update()
        self.buttons.update()
        pygame.display.flip()
        self.clock.tick(Settings.fps)

    def change_button(self, direction: str) -> None:
        """Changes the selected button and updates hover"""
        # if the mouse is currently hovering a button,
        # ignore all keyboard inputs
        for b in self.buttons:
            if b.currently_mouse_hovered:
                return

        # plays click sound
        self.menu_sound.play()

        # sets current button to not hovered
        cur_sprite = self.buttons.sprites()[self.curr_index]
        cur_sprite.set_keyboard_hover(False)

        # changes button
        if direction == 'up':
            self.curr_index = (self.curr_index - 1) % self.NUM_BUTTONS
        else:
            self.curr_index = (self.curr_index + 1) % self.NUM_BUTTONS

        # sets new button to hovered
        cur_sprite = self.buttons.sprites()[self.curr_index]
        cur_sprite.set_keyboard_hover(True)

    def handle_action(self) -> None:
        """Handles button actions for keyboard"""
        # does action for current button
        cur_button = self.buttons.sprites()[self.curr_index]
        cur_button.do_action()

def main() -> None:
    """Main function"""
    start_menu = StartMenu()
    start_menu.startup()


if __name__ == '__main__':
    main()
