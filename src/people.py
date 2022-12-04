import pygame
from sprite import Sprite


class People(Sprite):

    def __init__(self, img: pygame.Surface, x: int, y: int, 
                move_hori: float, move_vert: float) -> None:
        super().__init__(x, y, img)

        self.orig_top = self.rect.top
        self.orig_left = self.rect.left
        self.move_hori = move_hori
        self.move_vert = move_vert
        self.x = x

        self.f_top = float(self.orig_top)
        self.f_left = float(self.orig_left)

    def check_movement(self) -> None:
        if self.x < 100:
            self.f_top -= self.move_vert
            self.f_left += self.move_hori
        elif self.x > 100:
            self.f_top += self.move_vert
            self.f_left -= self.move_hori
    
    def update(self) -> None:
        self.check_movement()
        self.rect.top = self.f_top
        self.rect.left = self.f_left
