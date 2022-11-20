"""TODO: ghosts need to look in the direction they're moving
They need some kind of AI/pathfinding algorithm (probably BFS)
They'll all have the same algo, but they should ignore
tiles that have a ghost on them so that they naturally
go in different directions toward the player
"""
from animated_sprite import AnimatedSprite
import pygame
from itertools import islice
import random
from settings import Settings
class Ghost(AnimatedSprite):
    def __init__(self, x: int, y: int, path: str, move_speed: float=2.0, animation_speed: float=0.3):
        # first, calls super with all animations and sets instance variables
        super().__init__(x, y, folder_path=path, speed=animation_speed)
        self.f_centerx = float(self.rect.centerx)
        self.f_centery = float(self.rect.centery)
        self.move_speed = move_speed
        self.movement = 0
        self.ghost_movement = (self.move_speed, 0)

        # this is only for random movements
        # get rid of this later
        self.temp_timer = 0

        # then, splits into different animations
        NUM_ANIMATIONS = 4
        all_images = self.orig_animations['base']

        # split into right=0, down=1, left=2, up=3
        split_images = split_list(all_images, len(all_images)//NUM_ANIMATIONS)

        # then, adds animations
        self.add_animation_w_images('right', split_images[0], animation_speed)
        self.add_animation_w_images('down', split_images[1], animation_speed)
        self.add_animation_w_images('left', split_images[2], animation_speed)
        self.add_animation_w_images('up', split_images[3], animation_speed)

    def move_ghost(self):
        # for now, random movements
        # in the future, I want to implement DFS toward pacman
        movements = {
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed),
            'left': (-self.move_speed, 0),
            'right': (self.move_speed, 0),
        }
        dir = self.current_animation if self.current_animation != 'base' else random.choice(list(movements.keys()))
        self.temp_timer += 1
        if self.temp_timer >= 25:
            dir = random.choice(list(movements.keys()))
            self.temp_timer = 0
        # print(dir)
        self.ghost_movement = movements[dir]
        self.set_animation(dir)
    
    def update(self):
        self.move_ghost()
        self.rect.centerx += self.ghost_movement[0]
        self.rect.centery += self.ghost_movement[1]
        self.check_out_of_bounds()
        super().update()
        
    """doesn't work, stops too late on bottom/right and too early on top/left"""
    def check_out_of_bounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > Settings.window_height:
            self.rect.bottom = Settings.window_height
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > Settings.window_width:
            self.rect.right = Settings.window_width

# from https://predictivehacks.com/?all-tips=how-to-split-a-list-into-equal-elements-in-python
# don't really know how it works but it does
def split_list(input, num_elem):
    output = []
    for i in range(0, len(input), num_elem):
        output.append(input[i:i + num_elem])

    return output