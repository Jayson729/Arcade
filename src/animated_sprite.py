"""TODO: Ability to switch between animations easily
resize function looks gross, probably a better way to do this
"""

import pygame
from sprite import Sprite
import os


"""AnimatedSprite class that switches between images in a given folder"""
class AnimatedSprite(Sprite):
    def __init__(self, x: int, y: int, 
            folder_path: str='images/start_menu/waterfall/', 
            color=None, speed=1.0) -> None:

        # load images
        self.orig_images = self.get_images(folder_path)
        self.images = self.orig_images

        self.NUM_IMAGES = len(self.images)

        super().__init__(self.images[0], x, y, color)

        # Sets current sprite to the first image in the array
        self.current_sprite = 0
        self.speed = speed
    
    def get_images(self, path: str):
        images = []
        for file_name in sorted(os.listdir(path)):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pygame.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images

    """Updates sprite"""
    def update(self) -> None:
        # Incrementing the sprites with a decimal so the array will loop slower
        self.current_sprite += self.speed

        # Condition for current sprite to be set back to first image
        if self.current_sprite >= self.NUM_IMAGES:
            self.current_sprite = 0

        # Sets image to the contents off the sprites array
        self.image = self.images[int(self.current_sprite)]

    """Blits the current image to a given screen """
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect.center)

    def resize(self, new_width, new_height, original=False):
        if original:
            for key, value in enumerate(self.images):
                self.orig_images[key] = pygame.transform.scale(
                self.orig_images[key],
                (new_width, new_height)
                )
            self.orig_image = self.orig_images[0]
            self.orig_size = self.orig_image.get_size()

        for key, value in enumerate(self.images):
            # scales image
            self.images[key] = pygame.transform.scale(
                self.orig_images[key],
                (new_width, new_height)
            )
            self.image = self.images[int(self.current_sprite)]
            self.rect = self.images[0].get_rect(center=self.rect.center)