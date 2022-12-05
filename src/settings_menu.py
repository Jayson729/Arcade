import pygame
from state import State
from button import Button, ButtonGroup
from sprite import Sprite
from settings import Settings
from music_player import MusicPlayer


class SettingsMenu(State):
    """Main class that calls everything else"""

    def __init__(self, music_player: MusicPlayer) -> None:
        """Initializes SettingsMenu"""
        super().__init__()

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
        self.music_player = music_player

        pygame.display.set_caption('Settings')
        pygame.display.set_icon(pygame.image.load(
            f'{self.global_path}main.png'))
        self.create_game()

    def create_game(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()
        self.menu_items = self.get_menu_items()
        self.music_player.load_play_music('music/runescape_dream.wav')

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume/100)

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
            self.next_state = 'PREVIOUS'
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

    def do_event(self, event):
        self.buttons.do_event(event)

    def draw_volumes(self, screen):
        font = pygame.font.Font('fonts/Stardew_Valley.ttf', 30)
        # render fonts
        music_vol_render = font.render(
            str(Settings.music_volume), True, self.default_color)
        effects_vol_render = font.render(
            str(Settings.effects_volume), True, self.default_color)

        # get rects for blitting
        music_vol_rect = music_vol_render.get_rect(center=(520, 205))
        effects_vol_rect = effects_vol_render.get_rect(center=(520, 250))

        # blit renders to screen
        screen.blit(music_vol_render, music_vol_rect)
        screen.blit(effects_vol_render, effects_vol_rect)

    def draw(self, screen):
        self.background.draw(screen)
        self.buttons.draw(screen)
        self.menu_items.draw(screen)
        self.draw_volumes(screen)

    def update(self):
        self.buttons.update()


def main() -> None:
    """Main function"""
    from main import main
    main('SETTINGS')


if __name__ == '__main__':
    main()
