import sys
import pygame
from state import State
from animated_sprite import AnimatedSprite
from cloud import Cloud
from button import Button
from sprite import Sprite
from pacman import Pacman
from pong import Pong
from settings import Settings, Fonts, Colors


"""Main class that calls everything else"""
class StartMenu(State):

    """Initializes StartMenu"""
    def __init__(self) -> None:
       
        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()
        
        # create game objects
        self.img_root = 'images/start_menu/'
        self.clock = pygame.time.Clock()
        screen = self.create_screen()
        clouds = self.create_clouds()
        buttons = self.create_buttons()
        waterfall = AnimatedSprite(390, 350, folder_path=f'{self.img_root}waterfall/', speed=0.15)
        waterfall.resize(60, 415, True)
        background = self.create_background()
        pygame.display.set_caption('Start Menu')
        pygame.display.set_icon(pygame.image.load(f'{self.img_root}main.png'))
        super().__init__()

        # create GameManager
        self.game_manager = GameManager(screen, clouds, 
            waterfall, buttons, background)

    """Starts the game loop"""
    def startup(self) -> None:
        while True:
            self.game_manager.do_input()
            self.game_manager.run_game()

            pygame.display.flip()

            self.clock.tick(Settings.fps)
            # print(f"fps: {self.clock.get_fps()}")

    """Returns a Surface to be used as a screen"""
    def create_screen(self) -> pygame.Surface:
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    """Creates background as Sprite"""
    def create_background(self) -> Sprite:
        bg_image = pygame.image.load(f"{self.img_root}backgroundMain.png")
        background = Sprite(bg_image, 0, 0)
        background.resize(800, 600)
        return background

    """Creates a group of clouds"""
    def create_clouds(self, large_clouds: list=None, 
            small_clouds: list=None, sway_distance: float=1.5, 
            sway_speed: float=0.025) -> pygame.sprite.Group:
        # load images
        large_cloud_img = pygame.image.load(f'{self.img_root}large_cloud.png')
        small_cloud_img = pygame.image.load(f'{self.img_root}small_cloud.png')

        large_clouds = [
            {'coords': (155, 465), 'mirrored': False, 
                'size': (650, 650)},
            {'coords': (750, 415), 'mirrored': False, 
                'size': (500, 450)},
            {'coords': (780, 525), 'mirrored': False, 
                'size': (800, 760)},
            {'coords': (90, 570), 'mirrored': False, 
                'size': (760, 760)}
        ] if large_clouds is None else large_clouds
        small_clouds = [
            {'coords': (600, 80), 'mirrored': False, 
                'size': (150, 100)},
            {'coords': (160, 135), 'mirrored': True, 
                'size': (200, 170)}
        ] if small_clouds is None else small_clouds

        # add all clouds to a sprite group
        clouds = pygame.sprite.Group()
        for c in large_clouds:
            cloud = Cloud(large_cloud_img, 
                c['coords'][0], c['coords'][1], 
                sway_distance, sway_speed
            )
            cloud.resize(c['size'][0], c['size'][1])
            if c['mirrored']:
                cloud.image = pygame.transform.flip(
                    cloud.image, True, False)
            clouds.add(cloud)
        
        for c in small_clouds:
            cloud = Cloud(small_cloud_img,
                c['coords'][0], c['coords'][1], 
                sway_distance, sway_speed
            )
            cloud.resize(c['size'][0], c['size'][1])
            if c['mirrored']:
                cloud.image = pygame.transform.flip(
                    cloud.image, True, False)
            clouds.add(cloud)

        return clouds

    """Creates a group of buttons"""
    def create_buttons(self) -> pygame.sprite.Group:
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

        menu_items = {
            'ENTER ARCADE': {
                'coords': (410, 125),
                'action': arcade_action,
                'size': 50
            }, 
            'SETTINGS': {
                'coords': (410, 165),
                'action': settings_action,
                'size': 40
            },
            'CREDITS': {
                'coords': (410, 205),
                'action': credits_action,
                'size': 30
            } 
        }

        buttons = pygame.sprite.Group()
        for text, vals in menu_items.items():
            button = Button(text, vals['action'], 
                vals['coords'][0], vals['coords'][1],
                size=vals['size']
            )
            buttons.add(button)

        return buttons


"""Runs all parts of the menu, including
handling buttons, drawing and updating objects
"""
class GameManager:

    """Initializes a GameManager"""
    def __init__(self, screen: pygame.Surface, 
            clouds: pygame.sprite.Group, waterfall: AnimatedSprite,
            buttons: pygame.sprite.Group, 
            background: Sprite) -> None:
        self.screen = screen
        self.clouds = clouds
        self.waterfall = waterfall
        self.background = background
        self.buttons = buttons
        self.NUM_BUTTONS = len(buttons)

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
    
    """Changes the selected button and updates hover"""
    def change_button(self, dir: str) -> None:
        # plays click sound
        self.menu_sound.play()

        # sets current button to not hovered
        cur_sprite = self.buttons.sprites()[self.curr_index]
        cur_sprite.set_keyboard_hover(False)

        # changes button
        if dir == 'up':
            self.curr_index = (self.curr_index - 1) % self.NUM_BUTTONS
        else:
            self.curr_index = (self.curr_index + 1) % self.NUM_BUTTONS
        
        # sets new button to hovered
        cur_sprite = self.buttons.sprites()[self.curr_index]    
        cur_sprite.set_keyboard_hover(True)

    """Accepts and deals with inputs"""
    def do_input(self) -> None:
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
                if (event.key == pygame.K_UP 
                        or event.key == pygame.K_w):
                    self.change_button('up')
                if (event.key == pygame.K_DOWN 
                        or event.key == pygame.K_s):
                    self.change_button('down')
                if event.key == pygame.K_RETURN:
                    self.handle_action()
            
    """Draws game objects"""
    def draw_game_objects(self) -> None:
        self.waterfall.draw(self.screen)
        self.clouds.draw(self.screen)
        self.buttons.draw(self.screen)

    """Runs the Game, draws/updates game objects"""
    def run_game(self) -> None:
        self.screen.blit(self.background.image, (0, 0))
        self.draw_game_objects()

        self.clouds.update()
        self.waterfall.update()
        self.buttons.update()

    """Handles button actions for keyboard"""
    def handle_action(self) -> None:
        # does action for current button
        cur_button = self.buttons.sprites()[self.curr_index]
        cur_button.do_action()


"""Main function"""
def main() -> None:
    start_menu = StartMenu()
    start_menu.startup()


if __name__ == '__main__':
    main()
