import pygame
from sprite import Sprite

class Cloud(Sprite):

    """sway is how much to vary from center point"""
    def __init__(self, img, x, y, sway_distance, sway_speed):
        super().__init__(img, x, y)

        self.orig_y = self.rect.y
        self.sway_distance = sway_distance
        self.sway_speed = sway_speed
        self.movement = sway_speed
    
    def check_sway(self):
        if self.rect.y <= self.orig_y - self.sway_distance:
            self.movement = -self.sway_speed
        elif self.rect.y >= self.orig_y + self.sway_distance:
            self.movement = self.sway_speed

    def update(self):
        self.rect.y += self.movement
        self.check_sway()