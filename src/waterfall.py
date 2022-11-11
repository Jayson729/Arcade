import pygame
from sprite import Sprite


"""Waterfall class that switches between images in a given folder"""
class Waterfall(Sprite):
    def __init__(self, x: int, y: int, 
            folder_path: str='images/waterfall') -> None:

        # load images
        self.NUM_WATERFALLS = 6
        self.waterfall_images = []
        for num in range(self.NUM_WATERFALLS):
            img = pygame.image.load(f'{folder_path}/waterfall_{num}.png')
            img = pygame.transform.scale(img, (60, 415))
            self.waterfall_images.append(img)

        super().__init__(self.waterfall_images[0], x, y)

        # Sets current sprite to the first image in the array
        self.current_sprite = 0

    """Updates waterfall"""
    def update(self) -> None:
        # Incrementing the sprites with a decimal so the array will loop slower
        self.current_sprite += 0.15

        # Condition for current sprite to be set back to first image
        if self.current_sprite >= self.NUM_WATERFALLS:
            self.current_sprite = 0

        # Sets image to the contents off the sprites array
        self.image = self.waterfall_images[int(self.current_sprite)]

    """Blits the current image to a given screen """
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect.center)
