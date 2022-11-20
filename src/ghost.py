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
    def __init__(self, x: int, y: int, 
            base_path: str, 
            move_speed: float=2.0, animation_speed: float=0.3,
            color=None) -> None:
        # first, calls super with all animations and sets instance variables
        super().__init__(x, y, base_path, animation_speed)

        # move these probably
        right, down, left, up = self.split_animations('base', num_animations=4)
        self.add_animation_w_images('right', right, animation_speed)
        self.add_animation_w_images('down', down, animation_speed)
        self.add_animation_w_images('left', left, animation_speed)
        self.add_animation_w_images('up', up, animation_speed)

        # move these to sprite.py
        self.f_centerx = float(self.rect.centerx)
        self.f_centery = float(self.rect.centery)

        # move these to new class?
        self.move_speed = move_speed
        self.movement = (0, 0)

        # this is only for random movements
        # get rid of this later
        self.temp_timer = 0
        
    # move to animatedsprite
    def split_animations(self, name, num_animations):
        all_images = self.orig_animations[name]

        # split into right=0, down=1, left=2, up=3
        split_images = split_list(all_images, len(all_images)//num_animations)

        return split_images

    # good I think
    def move_ghost(self):
        movements = {
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed),
            'left': (-self.move_speed, 0),
            'right': (self.move_speed, 0),
        }
        dir = self.get_move(movements)
        self.movement = movements[dir]
        self.set_animation(dir)
    
    # good location, code is junk
    def get_move(self, movements):
        # for now, random movements
        # in the future, I want to implement DFS toward pacman
        dir = self.current_animation if self.current_animation != 'base' else random.choice(list(movements.keys()))
        self.temp_timer += 1
        if self.temp_timer >= 25:
            dir = random.choice(list(movements.keys()))
            self.temp_timer = 0
        
        return dir
    
    # move parts
    def update(self):
        self.move_ghost()

        # move this, probably sprite.py
        self.rect.centerx += self.movement[0]
        self.rect.centery += self.movement[1]
        self.check_out_of_bounds()
        super().update()
    
    # move
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

# possibly move
# from https://predictivehacks.com/?all-tips=how-to-split-a-list-into-equal-elements-in-python
# don't really know how it works but it does
def split_list(input, num_elem):
    output = []
    for i in range(0, len(input), num_elem):
        output.append(input[i:i + num_elem])

    return output