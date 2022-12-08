"""TODO: Make a map for pacman
The actual map doesn't need to be customizable or in a class,
but there needs to be a map class to draw and create the map
https://github.com/StanislavPetrovV/DOOM-style-Game/blob/main/map.py
for example
"""
from settings import Settings
from pacman_sprite import PacmanSprite
from ghost import Ghost
import pygame
# 28 x 30
minimap = [
    '========================================',
    '=..................==..................=',
    '=.==========.=====.==.=====.==========.=',
    '=o=        =.=   =.==.=   =.=        =o=',
    '=.==========.=====.==.=====.==========.=',
    '=......................................=',
    '=.==========.==.========.==.==========.=',
    '=.==========.==.========.==.==========.=',
    '=............==....==....==............=',
    '=====.======.=====.==.=====.======.=====',
    '    =.=    =.===== == =====.=    =.=    ',
    '    =.=    =.==          ==.=    =.=    ',
    '    =.=    =.== ===  === ==.=    =.=    ',
    '=====.======.== =      = ==.======.=====',
    '     ........   =      =   ........     ',
    '=====.==.===.== = GGGG = ==.======.=====',
    '    =.==.===.== =      = ==.======.=    ',
    '    =........== ======== ==........=    ',
    '    =.======.==    P     ==.====.=.=    ',
    '    =.=    =.===== == =====.=  =.=.=    ',
    '=====.======.=====.==.=====.====.=======',
    '=............==....==....==............=',
    '=.==========.==.========.==.==========.=',
    '=.==========.==.========.==.==========.=',
    '=......................................=',
    '=.==========.=====.==.=====.==========.=',
    '=o=        =.=   =.==.=   =.=        =o=',
    '=.==========.=====.==.=====.==========.=',
    '=..................==..................=',
    '========================================',
]


class Map:
    def __init__(self, layout_text=minimap):
        self.width = len(layout_text[0])
        self.height = len(layout_text)
        self.tile_width = Settings.window_width // self.width
        self.tile_height = Settings.window_height // self.height

        self.game_objects = self.find_game_objects(layout_text)
        # self.wall_locations = self.game_objects['walls']
        # self.pacman_locations = self.game_objects['pacman']
        # self.ghost_locations = self.game_objects['ghosts']
        # self.food_locations = self.game_objects['food']
        # self.capsule_locations = self.game_objects['capsules']

    def find_game_objects(self, layout_text):
        game_objects = {
            'walls': [],
            'pacman': [],
            'ghosts': [],
            'food': [],
            'capsules': [],
            'empty': []
        }
        for x, row in enumerate(layout_text):
            for y, c in enumerate(row):
                if c == '=':
                    game_objects['walls'].append((y, x))
                elif c == '.':
                    game_objects['food'].append((y, x))
                elif c == 'P':
                    game_objects['pacman'].append((y, x))
                elif c == 'G':
                    game_objects['ghosts'].append((y, x))
                elif c == 'o':
                    game_objects['capsules'].append((y, x))
                else:
                    game_objects['empty'].append((y, x))
        return game_objects

    def find_object_locations_on_screen(self):
        locations_on_screen = {
            'walls': [],
            'pacman': [],
            'ghosts': [],
            'food': [],
            'capsules': [],
            'empty': []
        }
        for key, value in self.game_objects.items():
            for (x, y) in value:
                locations_on_screen[key].append(
                    (x * self.tile_width, y * self.tile_height))
        return locations_on_screen

    def draw(self, screen: pygame.Surface):
        locations_on_screen = self.find_object_locations_on_screen()
        for (x, y) in locations_on_screen['walls']:
            wall_rect = pygame.Rect(x, y, self.tile_width, self.tile_height)
            pygame.draw.rect(screen, (40, 40, 70), wall_rect)

        for (x, y) in locations_on_screen['food']:
            pygame.draw.circle(screen, (255, 255, 204), (x + (self.tile_width*0.5), y + (self.tile_height*0.5)),
                               3)

        for (x, y) in locations_on_screen['capsules']:
            pygame.draw.circle(screen, (255, 255, 204), (x + (self.tile_width*0.5), y + (self.tile_height*0.5)),
                               9)
        pygame.draw.circle(screen, (100, 20, 20), (self.game_objects['pacman'][0][0] * self.tile_width, self.game_objects['pacman'][0][1] * self.tile_height), 5)
        for i, _ in enumerate(self.game_objects['ghosts']):
            pygame.draw.circle(screen, (100, 20, 20), (self.game_objects['ghosts'][i][0] * self.tile_width, self.game_objects['ghosts'][i][1] * self.tile_height), 5)

    def update(self, pacman: PacmanSprite, ghosts: pygame.sprite.Group):
        """This entire function is gross but hopefully it works
        It's purpose is to track the current location of pacman/ghosts on a grid
        """

        # track pacman
        self.game_objects['pacman'][0] = (pacman.rect.centerx//self.tile_width, pacman.rect.centery//self.tile_height)

        # track ghosts
        for i, ghost in enumerate(ghosts):
            self.game_objects['ghosts'][i] = (ghost.rect.centerx//self.tile_width, ghost.rect.centery//self.tile_height)
            # ghost_x, ghost_y = ghost_on_grid
            # if ghost.current_direction == 'left':
            #     ghost_on_grid = (
            #         ghost.rect.right//self.tile_width, ghost_y)
            # elif ghost.current_direction == 'right':
            #     ghost_on_grid = (
            #         ghost.rect.left//self.tile_width, ghost_y)
            # elif ghost.current_direction == 'up':
            #     ghost_on_grid = (
            #         ghost_x, ghost.rect.bottom//self.tile_height)
            # elif ghost.current_direction == 'down':
            #     ghost_on_grid = (
            #         ghost_x, ghost.rect.top//self.tile_height)

        # delete food from game_objects if pacman is on tile
        if (x := self.game_objects['pacman'][0]) in self.game_objects['food']:
            self.game_objects['food'].remove(x)
        if (x := self.game_objects['pacman'][0]) in self.game_objects['capsules']:
            self.game_objects['capsules'].remove(x)
    
    def is_pacman_in_ghost(self):
        return self.game_objects['pacman'][0] in self.game_objects['ghosts']

    def is_wall(self, screen_coordinates: tuple[int, int]):
        """Returns if a given screen location is a wall based on tile size"""
        return (screen_coordinates[0]//self.tile_width, screen_coordinates[1]//self.tile_height) in self.game_objects['walls']
