import sys
import pygame
from state import State
from waterfall import Waterfall
from cloud import Cloud
from button import Button
from sprite import Sprite
from settings import Settings, Fonts, Colors#, Music, Sounds

# Initializes the main menu
# Creates a screen for main menu
class StartMenu(State):
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        screen = self.create_screen()
        clouds = self.create_clouds()
        buttons = self.create_buttons()
        waterfall = Waterfall(390, 350)
        background = self.create_background()

        pygame.display.set_caption('Start Menu')
        self.game_manager = GameManager(screen, clouds, waterfall, buttons, background)

    def startup(self):
        while True:
            self.game_manager.do_input()
            self.game_manager.run_game()

            pygame.display.flip()

            self.clock.tick(Settings.fps)
            # print(f"fps: {self.clock.get_fps()}")

    def create_screen(self) -> pygame.Surface:
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def create_background(self):
        bg_image = pygame.image.load("images/backgroundMain.png")
        background = Sprite(bg_image, 0, 0)
        background.resize(800, 600)
        return background

    def create_clouds(self, large_clouds=None, small_clouds=None, 
        sway_distance=1.5, sway_speed=0.025):
        # load images
        large_cloud_img = pygame.image.load('images/large_cloud.png')
        small_cloud_img = pygame.image.load('images/small_cloud.png')

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
                cloud.image = pygame.transform.flip(cloud.image, True, False)
            clouds.add(cloud)
        
        for c in small_clouds:
            cloud = Cloud(small_cloud_img,
                c['coords'][0], c['coords'][1], 
                sway_distance, sway_speed
            )
            cloud.resize(c['size'][0], c['size'][1])
            if c['mirrored']:
                cloud.image = pygame.transform.flip(cloud.image, True, False)
            clouds.add(cloud)

        return clouds

    """I think I want buttons to be sprites
    rendered fonts should count as images
    """
    def create_buttons(self) -> pygame.sprite.Group:
        def arcade_action():
            print('arcade')
            # pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/arcade_door.wav'))
        def settings_action():
            print('settings')
        def credits_action():
            print('credits')

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

class GameManager:
    def __init__(self, screen: pygame.Surface, 
            clouds: pygame.sprite.Group, waterfall: Waterfall,
            buttons: pygame.sprite.Group, 
            background: Sprite):
        self.screen = screen
        self.clouds = clouds
        self.waterfall = waterfall
        self.background = background
        

        self.buttons = buttons
        self.NUM_BUTTONS = len(buttons)

        # self.menu_sound = Sounds.start_menu_sound
        # self.menu_music = Music.start_menu_music
        
        # pygame.mixer.music.load('music/runescape_dream.wav')
        # pygame.mixer.music.play(-1)

        self.curr_index = 0
        self.buttons.sprites()[self.curr_index].set_keyboard_hover(True)
    
    def change_button(self, dir: str):
        self.buttons.sprites()[self.curr_index].set_keyboard_hover(False)
        if dir == 'up':
            self.curr_index = (self.curr_index - 1) % self.NUM_BUTTONS
        else:
            self.curr_index = (self.curr_index + 1) % self.NUM_BUTTONS
        self.buttons.sprites()[self.curr_index].set_keyboard_hover(True)
        
    def do_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for b in self.buttons:
                mouse = pygame.mouse.get_pos()
                if b.check_mouse_hover(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        b.do_action()
                        # if clicking multiple buttons, only do one action
                        break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.change_button('up')
                    # self.menu_sound.play()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.change_button('down')
                    # self.menu_sound.play()
                if event.key == pygame.K_RETURN:
                    self.handle_action()
            

    def draw_game_objects(self):
        self.clouds.draw(self.screen)
        self.waterfall.draw(self.screen)
        self.buttons.draw(self.screen)

    def run_game(self):
        self.screen.blit(self.background.image, (0, 0))
        self.draw_game_objects()

        self.clouds.update()
        self.waterfall.update()
        self.buttons.update()

    def handle_action(self):
        # maybe?
        self.buttons.sprites()[self.curr_index].do_action()


def main():
    start_menu = StartMenu()
    start_menu.startup()

if __name__ == '__main__':
    main()

# class StartMenu(State):
#     def __init__(self):
#         # not gonna mess with it but what does this mean?
#         super(StartMenu, self).__init__()
#         self.clock = pygame.time.Clock()
#         self.fps = 60
#         self.clock.tick(self.fps)
#         pygame.display.set_caption("Arcade Games")
#         pygame.display.set_icon(pygame.image.load('images/main.png'))
#         self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
#         self.menu_sound.set_volume(0.3)
#         pygame.mixer.music.load('music/runescape_dream.wav')
#         pygame.mixer.music.play(-1)
#         self.curr_index = 0
#         # Cloud movement items
#         self.move_1 = 0
#         self.move_2 = 0
#         self.move_3 = 0
#         self.move_4 = 0
#         self.move_5 = 0
#         self.move_6 = 0
#         self.change = [0.025, - 0.025]
#         self.menu_items = ["ENTER ARCADE", "SETTINGS", "CREDITS"]
        # self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 10)
#         self.large_cloud = pygame.image.load("images/large_cloud.png").convert_alpha()
#         self.small_right = pygame.image.load("images/small_right.png").convert_alpha()
#         self.small_left = pygame.image.load("images/small_left.png").convert_alpha()
#         self.background_img = pygame.transform.scale(pygame.image.load("images/backgroundMain.png"), (800, 600))
#         # Cloud y values from cloud_1 to small_cloud_2
#         self.list = [140, 190, 145, 190, 30, 50]
#         self.cloud_1 = self.transform_image(self.large_cloud, 650, 650)
#         self.cloud_2 = self.transform_image(self.large_cloud, 500, 450)
#         self.cloud_3 = self.transform_image(self.large_cloud, 800, 760)
#         self.cloud_4 = self.transform_image(self.large_cloud, 760, 760)
#         self.small_cloud_1 = self.transform_image(self.small_left, 150, 100)
#         self.small_cloud_2 = self.transform_image(self.small_right, 200, 170)
#         self.index = 0
#         self.y = 0
#         self.sprites = pygame.sprite.Group()
#         waterfall = Waterfall(390, 350)
#         self.sprites.add(waterfall)

#     def which_state(self, event):
#         for item in self.menu_items:
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_RETURN and item == "ENTER ARCADE":
#                     self.next_state = "ARCADE"
#                 elif event.key == pygame.K_RETURN and item == "SETTINGS":
#                     self.next_state = "SETTINGS"
#                 elif event.key == pygame.K_RETURN and item == "CREDITS":
#                     self.next_state = "ARCADE"

#     def render_text(self, index):
#         if index == 0:
#             self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 50)
#         elif index == 1:
#             self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 40)
#         elif index == 2:
#             self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 30)

#         color = '#FFD921' if index == self.curr_index else '#DDA059'
#         return self.font.render(self.menu_items[index], True, color)

#     def get_text_position(self, text, index):
#         center = (self.screen_rect.topleft[0] + 410, self.screen_rect.topleft[1] + 125 + (index * 40))
#         return text.get_rect(center=center)

#     def handle_action(self):
#         if self.curr_index == 0:
#             pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/arcade_door.wav'))
#         elif self.curr_index == 1:
#             self.done = True
#         elif self.curr_index == 2:
#             self.done = True

#     def get_event(self, event):
#         if event.type == pygame.QUIT:
#             self.quit = True
#         elif event.type == pygame.KEYUP:
#             if event.key == pygame.K_ESCAPE:
#                 self.quit = True
#             if event.key == pygame.K_UP:
#                 self.menu_sound.play()
#                 if self.curr_index <= 0:
#                     self.curr_index = 2
#                 elif self.curr_index == 2:
#                     self.curr_index = 1
#                 else:
#                     self.curr_index = 0
#             elif event.key == pygame.K_w:
#                 self.menu_sound.play()
#                 if self.curr_index <= 0:
#                     self.curr_index = 2
#                 elif self.curr_index == 2:
#                     self.curr_index = 1
#                 else:
#                     self.curr_index = 0
#             elif event.key == pygame.K_DOWN:
#                 self.menu_sound.play()
#                 if self.curr_index == 0:
#                     self.curr_index = 1
#                 elif self.curr_index >= 2:
#                     self.curr_index = 0
#                 else:
#                     self.curr_index = 2
#             elif event.key == pygame.K_s:
#                 self.menu_sound.play()
#                 if self.curr_index == 0:
#                     self.curr_index = 1
#                 elif self.curr_index >= 2:
#                     self.curr_index = 0
#                 else:
#                     self.curr_index = 2

#             elif event.key == pygame.K_RETURN:
#                 self.handle_action()

#     def transform_image(self, image, scalex, scaley):
#         return pygame.transform.scale(image, (scalex, scaley))

#     def update_count(self, count):
#         if count <= 0:
#             count += 0.25

#     def draw(self, screen):
#         screen.blit(self.background_img, (0, 0))

#         self.list[0] += self.move_1
#         if self.list[0] <= 137:
#             self.move_1 = self.change[0]
#         elif self.list[0] >= 140:
#             self.move_1 = self.change[1]

#         self.list[1] += self.move_2
#         if self.list[1] <= 187:
#             self.move_2 = self.change[0]
#         elif self.list[1] >= 190:
#             self.move_2 = self.change[1]

#         self.list[2] += self.move_3
#         if self.list[2] <= 142:
#             self.move_3 = self.change[0]
#         elif self.list[2] >= 145:
#             self.move_3 = self.change[1]

#         self.list[3] += self.move_4
#         if self.list[3] <= 187:
#             self.move_4 = self.change[0]
#         elif self.list[3] >= 190:
#             self.move_4 = self.change[1]

#         self.list[4] += self.move_5
#         if self.list[4] <= 27:
#             self.move_5 = self.change[0]
#         elif self.list[4] >= 30:
#             self.move_5 = self.change[1]

#         self.list[5] += self.move_6
#         if self.list[5] <= 47:
#             self.move_6 = self.change[0]
#         elif self.list[5] >= 50:
#             self.move_6 = self.change[1]

#         self.sprites.draw(screen)
#         screen.blit(self.cloud_1, (-170, self.list[0]))
#         screen.blit(self.cloud_2, (500, self.list[1]))
#         screen.blit(self.cloud_3, (380, self.list[2]))
#         screen.blit(self.cloud_4, (-290, self.list[3]))
#         screen.blit(self.small_cloud_1, (525, self.list[4]))
#         screen.blit(self.small_cloud_2, (60, self.list[5]))
#         self.sprites.update()
#         for index, option in enumerate(self.menu_items):
#             text_render = self.render_text(index)
#             screen.blit(text_render, self.get_text_position(text_render, index))
