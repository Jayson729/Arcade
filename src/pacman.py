import pygame
from sprite import Sprite
from settings import Settings, Colors, Fonts
from spritesheet import SpriteSheet

class Pacman:

    def __init__(self):
        # initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.sprite_sheet = self.load_sprite_sheet()
        self.screen = self.create_screen()
        self.pacman = self.create_pacman()
        self.ghosts = self.create_ghosts()
        # self.maps = self.create_maps()
        # self.game_manager = GameManager(screen, pacman, ghosts)

    def load_sprite_sheet(self):
        filename = 'images/pacman_sprites.png'
        pacman_ss = SpriteSheet(filename)

        num_rows = 19
        num_cols = 19
        # the margin and padding values are wrong
        pacman_images = pacman_ss.load_grid_images(num_rows, num_cols, 
            x_margin=8,x_padding=8, y_margin=8, y_padding=8)
        
        #create a sprite for each image
        for i in range(num_rows):
            for j in range(num_cols):
                sprite = Sprite(pacman_images[i], j*50, i*50)
    
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
        pacman = pygame.sprite.GroupSingle()
        pacman_img_path = ''

