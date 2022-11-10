import pygame
from sprite import Sprite

class Cloud(Sprite):

    """sway is how much to vary from center point"""
    def __init__(self, img, x, y, sway_distance, sway_speed):
        super().__init__(img, x, y)

        self.orig_center = self.rect.center
        self.sway_distance = sway_distance
        self.sway_speed = sway_speed
        self.movement = sway_speed
    
    def check_sway(self, sway_distance, sway_speed):
        if self.rect.center <= self.orig_center - sway_distance:
            self.movement = -sway_speed
        elif self.rect.center >= self.orig_center + sway_distance:
            self.movement = sway_speed

    def update(self):
        self.rect.center += self.movement
        self.check_sway()