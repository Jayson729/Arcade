from abc import abstractmethod
import pygame
from sprite import Sprite, AnimatedSprite
from settings import Settings


class AnimatedPlayer(AnimatedSprite):
    def __init__(self, x: int, y: int,
            base_path: str, move_speed: float,
            animation_speed: float, color=None):
        super().__init__(x, y, base_path, animation_speed, color=color)
        self.move_speed = move_speed
        self.movement = (0, 0)

    @staticmethod
    def get_direction() -> str:
        direction = None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = 'down'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = 'right'
        return direction

    def check_out_of_bounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > Settings.window_height:
            self.rect.bottom = Settings.window_height
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > Settings.window_width:
            self.rect.right = Settings.window_width

    @abstractmethod
    def do_movement(self) -> None:
        pass

    def update(self) -> None:
        self.rect.centerx += self.movement[0]
        self.rect.centery += self.movement[1]
        self.check_out_of_bounds()
        super().update()

# copy of AnimatedPlayer except for single img
class StaticPlayer(Sprite):
    def __init__(self, x: int, y: int,
            img: pygame.Surface, move_speed: float,
            color=None) -> None:
        super().__init__(x, y, img, color)
        self.move_speed = move_speed
        self.movement = (0, 0)

    @staticmethod
    def get_direction() -> str:
        direction = None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = 'down'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = 'right'
        return direction

    def check_out_of_bounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > Settings.window_height:
            self.rect.bottom = Settings.window_height
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > Settings.window_width:
            self.rect.right = Settings.window_width

    @abstractmethod
    def do_movement(self) -> None:
        pass

    def update(self) -> None:
        self.rect.centerx += self.movement[0]
        self.rect.centery += self.movement[1]
        self.check_out_of_bounds()
        super().update()
