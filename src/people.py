import pygame
from sprite import Sprite


class People(Sprite):

    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        super().__init__(x, y, img)

        # TO DO
