import pygame
from sprite import Sprite

class Cloud(Sprite):

    """sway is how much to vary from center point"""
    def __init__(self, img, x, y, sway_distance, sway_speed):
        super().__init__(img, x, y)

        self.orig_centery = self.rect.centery
        self.f_centery = float(self.orig_centery)
        self.sway_distance = sway_distance
        self.sway_speed = sway_speed
        self.movement = sway_speed
    
    def check_sway(self):
        if self.f_centery <= self.orig_centery - self.sway_distance:
            self.movement += self.sway_speed
        elif self.f_centery >= self.orig_centery + self.sway_distance:
            self.movement += -self.sway_speed

    def update(self):
        self.check_sway()
        self.f_centery += self.movement
        self.rect.centery = self.f_centery
        