"""TODO: Fix collision with window borders (hitbox is wonky)
Make movements fixed to a grid (move like normal pacman)
Swintch to pacman death whe you touch a ghost 
(check for collisions with ghosts, switching animation done in animated_sprite.py)
"""

import pygame
from animated_sprite import AnimatedSprite
from settings import Settings
img_root = 'images/pacman/'
class PacmanSprite(AnimatedSprite):
    def __init__(self, x: int, y: int, player_speed=2.0, folder_path=f'{img_root}pacman_yellow/', death_folder_path=f'{img_root}pacman_death/', color=None, speed=0.3):
        super().__init__(x, y, folder_path, color, speed)
        self.add_animation('death', death_folder_path, speed*.5)
        self.f_centerx = float(self.rect.centerx)
        self.f_centery = float(self.rect.centery)
        self.player_speed = player_speed
        self.movement = 0
        self.pacman_movement = (self.player_speed, 0)
    
    def move_pacman(self, dir: str) -> None:
        if dir == 'right':
            self.pacman_movement = (0, 0)
            self.set_animation('death')
            return
        self.set_animation('base')
        # movement, rotation
        # movement multiplied by speeds later
        # x, y, '-' is up/left
        # rotation from facing right counter-clockwise in degrees
        movements = {
            'up': [(0, -self.player_speed), 90],
            'down': [(0, self.player_speed), 270],
            'left': [(-self.player_speed, 0), 180],
            'right': [(self.player_speed, 0), 0]
        }

        # sets movement and rotates pacman
        self.pacman_movement = movements[dir][0]
        self.rotate(movements[dir][1])

    def update(self):
        # self.f_centerx += self.pacman_movement[0]
        # self.f_centery += self.pacman_movement[1]
        # self.rect.centerx = self.f_centerx
        # self.rect.centery = self.f_centery

        self.rect.centerx += self.pacman_movement[0]
        self.rect.centery += self.pacman_movement[1]
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