import sys
import pygame
from state import State
from cloud import Cloud
from button import Button
from sprite import Sprite, AnimatedSprite
from settings import Settings, Colors


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
        self.default_color = Colors.start_menu_text
        self.clock = pygame.time.Clock()
        self.screen = self.get_screen()
        self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 40)
        self.music_vol = 0.2
        self.music_int = 2
        self.effects_vol = 0.3
        self.effects_int = 3
        self.menu_items = {1: [self.music_int, self.effects_int], 2: ["MUSIC VOLUME", "EFFECTS VOLUME"]}
        pygame.display.set_caption('Settings')
        pygame.display.set_icon(pygame.image.load(f'{self.global_path}main.png'))
        self.create_game()
        super().__init__()

    def get_text_position(self, text, index):
        top_left = 0

        for i, j in self.menu_items.items():
            if i == 0:
                top_left = (self.screen_rect.topleft[0] + 500, self.screen_rect.topleft[1] + 150 + (index * 30))
            elif i == 1:
                top_left = (self.screen_rect.topleft[0] + 500, self.screen_rect.topleft[1] + 150 + (index * 30))
        return text.get_rect(topleft=top_left)

    def render_text(self, index):
        for i, j in self.menu_items.items():
            if j:
                self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 30)

        return self.font.render(f'{self.menu_items[j]}', True, self.default_color)


    def create_game(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()
        self.NUM_BUTTONS = len(self.buttons)

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(self.effects_vol)

        pygame.mixer.music.load('music/runescape_dream.wav')
        pygame.mixer.music.set_volume(self.music_vol)
        # loops music
        pygame.mixer.music.play(-1)

        self.curr_index = 0

        # starts first button as hovered
        # first_sprite = self.buttons.sprites()[self.curr_index]
        # first_sprite.set_keyboard_hover(True)

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

    def get_buttons(self) -> pygame.sprite.Group:
        """Creates a group of buttons"""

        def music_action_down():
            print('music down')
            if self.music_vol > 0:
                self.music_vol -= 0.1
                self.music_int -= 1
                pygame.mixer.music.set_volume(self.music_vol)

        def music_action_up():
            print('music up')
            if self.music_vol < 1.0:
                self.music_vol += 0.1
                self.music_int += 1
                pygame.mixer.music.set_volume(self.music_vol)

        def effects_action_down():
            print('effects down')
            if self.effects_vol > 0:
                self.effects_vol -= 0.1
                self.effects_int -= 1
                self.menu_sound.set_volume(self.effects_vol)

        def effects_action_up():
            print('effects up')
            if self.effects_vol < 1.0:
                self.effects_vol += 0.1
                self.effects_int += 1
                self.menu_sound.set_volume(self.effects_vol)

        def back_action():
            print('back')
            self.next_state = 'START'
            self.done = True

        buttons = pygame.sprite.Group()
        buttons.add(
            Button(500, 205, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   music_action_down).rotate(180)
        )
        buttons.add(
            Button(520, 205, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   music_action_up)
        )
        buttons.add(
            Button(500, 250, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   effects_action_down).rotate(180)
        )
        buttons.add(
            Button(520, 250, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   effects_action_up)
        )

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
        self.buttons.draw(self.screen)
        for index, option in enumerate(self.menu_items):
            text_render = self.render_text(index)
            self.screen.blit(text_render, self.get_text_position(text_render, index))

    def update(self):
        self.buttons.update()
        pygame.display.flip()
        self.clock.tick(Settings.fps)

    def change_button(self, direction: str) -> None:
        """Changes the selected button and updates hover"""
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
    settings_menu = SettingsMenu()
    settings_menu.startup()


if __name__ == '__main__':
    main()

