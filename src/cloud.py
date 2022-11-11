import pygame
from sprite import Sprite


"""Cloud class that makes an image sway a 
certain distance at a certain speed
"""
class Cloud(Sprite):

    """Initializes cloud"""
    def __init__(self, img: pygame.Surface, x: int, y: int, 
            sway_distance: float, sway_speed: float) -> None:
        super().__init__(img, x, y)

        self.orig_centery = self.rect.centery
        self.sway_distance = sway_distance
        self.sway_speed = sway_speed
        self.movement = sway_speed

        # stores as float to have a smooth animation
        self.f_centery = float(self.orig_centery)
    
    """Sets the movement value based on location and sway speed"""
    def check_sway(self) -> None:
        if self.f_centery <= self.orig_centery - self.sway_distance:
            self.movement += self.sway_speed
        elif self.f_centery >= self.orig_centery + self.sway_distance:
            self.movement += -self.sway_speed

    """Updates cloud based on centery as float and movement"""
    def update(self) -> None:
        self.check_sway()
        self.f_centery += self.movement
        self.rect.centery = self.f_centery
        