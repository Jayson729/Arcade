import sys
import pygame
from state import State
from cloud import Cloud
from button import Button, ButtonGroup
from sprite import Sprite, AnimatedSprite
from settings import Settings


class SettingsMenu(State):
    """Main class that calls everything else"""

    def __init__(self, screen=None) -> None:
        """Initializes SettingsMenu"""

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/settings_menu/'
        self.global_path = 'images/'
        self.default_color = Settings.settings_menu_text_color
        self.default_font = Settings.settings_menu_font
        self.clock = pygame.time.Clock()
        self.screen = screen
        if screen is None:
            self.screen = self.get_screen()
        # self.menu_items = {1: [self.music_int, self.effects_int], 2: ["MUSIC VOLUME", "EFFECTS VOLUME"]}
        pygame.display.set_caption('Settings')
        pygame.display.set_icon(pygame.image.load(
            f'{self.global_path}main.png'))
        self.create_game()
        super().__init__()

    # def get_text_position(self, text, index):
    #     top_left = 0

    #     for i, j in self.menu_items.items():
    #         if i == 0:
    #             top_left = (self.screen_rect.topleft[0] + 500, self.screen_rect.topleft[1] + 150 + (index * 30))
    #         elif i == 1:
    #             top_left = (self.screen_rect.topleft[0] + 500, self.screen_rect.topleft[1] + 150 + (index * 30))
    #     return text.get_rect(topleft=top_left)

    # def render_text(self, index):
    #     for i, j in self.menu_items.items():
    #         if j:
    #             self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 30)

    #     return self.font.render(f'{self.menu_items[j]}', True, self.default_color)

    def create_game(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()
        self.menu_items = self.get_menu_items()

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume/100)

        pygame.mixer.music.load('music/runescape_dream.wav')
        pygame.mixer.music.set_volume(Settings.music_volume/100)
        # loops music
        pygame.mixer.music.play(-1)

    def get_screen(self) -> pygame.Surface:
        """Returns a Surface to be used as a screen"""
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def get_menu_items(self):
        font = pygame.font.Font(self.default_font, 30)
        menu_items = pygame.sprite.Group()
        menu_items.add(Sprite(280, 190, font.render(
            'MUSIC VOLUME', True, self.default_color)))
        menu_items.add(Sprite(280, 240, font.render(
            'EFFECTS VOLUME', True, self.default_color)))
        return menu_items

    def get_background(self) -> Sprite:
        """Creates background as Sprite"""
        bg_image = pygame.image.load(
            f"{self.img_path}settings_menu_background.png")
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def get_buttons(self) -> ButtonGroup:
        """Creates a group of buttons"""

        def music_action_down():
            print('music down')
            if Settings.music_volume > 0:
                Settings.music_volume -= 5
                # self.music_int -= 1
                pygame.mixer.music.set_volume(Settings.music_volume/100)
                self.menu_sound.play()

        def music_action_up():
            print('music up')
            if Settings.music_volume < 100:
                Settings.music_volume += 5
                # self.music_int += 1
                pygame.mixer.music.set_volume(Settings.music_volume/100)
                self.menu_sound.play()

        def effects_action_down():
            print('effects down')
            if Settings.effects_volume > 0:
                Settings.effects_volume -= 5
                # self.effects_int -= 1
                self.menu_sound.set_volume(Settings.effects_volume/100)
                self.menu_sound.play()

        def effects_action_up():
            print('effects up')
            if Settings.effects_volume < 100:
                Settings.effects_volume += 5
                # self.effects_int += 1
                self.menu_sound.set_volume(Settings.effects_volume/100)
                self.menu_sound.play()

        def back_action():
            print('back')
            self.next_state = 'START'
            self.done = True

        buttons = ButtonGroup()
        buttons.add(
            Button(490, 205, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   music_action_down).rotate(180)
        )
        buttons.add(
            Button(550, 205, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   music_action_up)
        )
        buttons.add(
            Button(490, 250, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   effects_action_down).rotate(180)
        )
        buttons.add(
            Button(550, 250, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   effects_action_up)
        )
        buttons.add(
            Button(50, 575, 'BACK', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   back_action)
        )

        return buttons

    def startup(self) -> None:
        """Starts the game loop"""
        while True:
            self.draw()
            self.update()
            self.check_events()
            # print(f"fps: {self.clock.get_fps()}")

    def check_events(self) -> None:
        """Accepts and deals with inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.buttons.do_event(event, self.menu_sound)

    def draw_volumes(self, screen):
        font = pygame.font.Font('fonts/Stardew_Valley.ttf', 30)
        music_vol_render = font.render(
            repr(Settings.music_volume), True, self.default_color)
        effects_vol_render = font.render(
            repr(Settings.effects_volume), True, self.default_color)
        screen.blit(music_vol_render, (500, 190))
        screen.blit(effects_vol_render, (500, 235))

    def draw(self):
        self.background.draw(self.screen)
        self.buttons.draw(self.screen)
        self.menu_items.draw(self.screen)
        self.draw_volumes(self.screen)

    def update(self):
        self.buttons.update()
        pygame.display.flip()
        self.clock.tick(Settings.fps)


def main() -> None:
    """Main function"""
    settings_menu = SettingsMenu()
    settings_menu.startup()


if __name__ == '__main__':
    main()
