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
        # self.sprite_sheet = self.load_sprite_sheet()
        self.screen = self.create_screen()
        self.pacman = self.create_pacman()
        self.ghosts = self.create_ghosts()
        # self.buttons = self.create_buttons()
        # self.background = self.create_background()
        # self.map = self.create_map()

        pygame.display.set_caption('Pacman')
        super().__init__()

        self.game_manager = GameManager(self.screen, self.pacman, self.ghosts)
    
    def startup(self) -> None:
        while True:
            self.game_manager.do_input()
            self.game_manager.run_game()
            pygame.display.flip()
            self.clock.tick(Settings.fps)
            # print(f"fps: {self.clock.get_fps()}")

    # def load_sprite_sheet(self):
    #     filename = 'images/pacman_sprites.png'
    #     pacman_ss = SpriteSheet(filename)

    #     num_rows = 19
    #     num_cols = 19
    #     # the margin and padding values are wrong
    #     pacman_images = pacman_ss.load_grid_images(num_rows, num_cols, 
    #         x_margin=8,x_padding=8, y_margin=8, y_padding=8)
        
    #     #create a sprite for each image
    #     for i in range(num_rows):
    #         for j in range(num_cols):
    #             sprite = Sprite(pacman_images[i], j*50, i*50)
    
    def create_screen(self):
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def create_pacman(self):
        inputs = {
            'main': {
                'up': pygame.K_UP,
                'down': pygame.K_DOWN,
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'pause': pygame.K_ESCAPE,
            },
            'alt': {
                'up': pygame.K_w,
                'down': pygame.K_s,
                'left': pygame.K_a,
                'right': pygame.K_d,
                'pause': pygame.K_ESCAPE,
            }
        }
        pacman = PacmanSprite(600, 400, folder_path=f'{self.img_path}yellow_pacman/', speed=.15)
        return pacman
    
    def create_ghosts(self):
        ghosts = pygame.sprite.Group()
        # blue_ghost = AnimatedSprite(300, 100, f'{self.img_path}blue_ghost/', speed=0.05)
        # red_ghost = AnimatedSprite(400, 200, f'{self.img_path}red_ghost/', speed=0.05)
        # orange_ghost = AnimatedSprite(300, 300, f'{self.img_path}orange_ghost/', speed=0.05)
        # pink_ghost = AnimatedSprite(400, 400, f'{self.img_path}pink_ghost/', speed=0.05)
        
        blue_ghost = Ghost(300, 100, f'{self.img_path}blue_ghost/', animation_speed=0.15)
        red_ghost = Ghost(400, 200, f'{self.img_path}red_ghost/', animation_speed=0.15)
        orange_ghost = Ghost(300, 300, f'{self.img_path}orange_ghost/', animation_speed=0.15)
        pink_ghost = Ghost(400, 400, f'{self.img_path}pink_ghost/', animation_speed=0.15)

        ghosts.add(blue_ghost)
        ghosts.add(red_ghost)
        ghosts.add(orange_ghost)
        ghosts.add(pink_ghost)

        return ghosts

class GameManager:

    def __init__(self, screen, pacman, ghosts=None, buttons=None, background=None, map=None):
        self.screen = screen
        self.pacman = pacman
        self.ghosts = ghosts
        # self.background = background
        # self.map = map

        # self.buttons = buttons
        # self.NUM_BUTTONS = len(buttons)
        # self.cur_index = 0
        # first_button = self.buttons.sprites()[self.cur_index]
        # first_button.set_keyboard_hover(True)
    
    def change_button(self, dir: str) -> None:
        # plays click sound
        # self.menu_sound.play()

        # sets current button to not hovered
        cur_sprite = self.buttons.sprites()[self.curr_index]
        cur_sprite.set_keyboard_hover(False)

        # changes button
        if dir == 'up':
            self.cur_index = (self.cur_index - 1) % self.NUM_BUTTONS
        elif dir == 'down':
            self.cur_index = (self.cur_index + 1) % self.NUM_BUTTONS
        
        # sets new button to hovered
        cur_sprite = self.buttons.sprites()[self.curr_index]    
        cur_sprite.set_keyboard_hover(True)
    
    def move_pacman(self, dir: str) -> None:
        self.pacman.move_pacman(dir)

    def do_input(self):
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # for b in self.buttons:
            #     mouse = pygame.mouse.get_pos()
            #     if b.check_mouse_hover(mouse):
            #         if (event.type == pygame.MOUSEBUTTONDOWN 
            #                 and event.button == 1):
            #             b.do_action()
            #             # if clicking multiple buttons, 
            #             # only do one action
            #             break
            # if event.type == pygame.KEYDOWN:
            #     # pausing and buttons
            #     # if (event.key == pygame.K_UP 
            #     #         or event.key == pygame.K_w):
            #     #     # maybe something like this
            #     #     # if self.state == 'GAME':
            #     #     #     self.move_pacman('up')
            #     #     self.change_button('up')
            #     # if (event.key == pygame.K_DOWN 
            #     #         or event.key == pygame.K_s):
            #     #     self.change_button('down')
            #     # if event.key == pygame.K_RETURN:
            #     #     self.handle_action()
            #     pass
        
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.move_pacman('up')
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.move_pacman('down')
        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.move_pacman('left')
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.move_pacman('right')
    
    def draw_game_objects(self) -> None:
        # self.map.draw(self.screen)
        self.pacman.draw(self.screen)
        self.ghosts.draw(self.screen)
        # self.buttons.draw(self.screen)

    def run_game(self) -> None:
        # self.screen.blit(self.background.image, (0, 0))
        self.screen.fill((0, 0, 0))
        
        self.draw_game_objects()
        
        self.pacman.update()
        self.ghosts.update()
        # self.buttons.update()
        # self.map.update()

    def handle_action(self) -> None:
        # does action for current button
        cur_button = self.buttons.sprites()[self.curr_index]
        cur_button.do_action()

def main() -> None:
    pacman = Pacman()
    pacman.startup()

if __name__ == '__main__':
    main()
        
                