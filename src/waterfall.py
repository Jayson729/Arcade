import pygame
from sprite import Sprite

class Waterfall(Sprite):
    def __init__(self, x, y, folder_path='images/waterfall'):

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

    def update(self):
        # Incrementing the sprites with a decimal so the array will loop slower
        self.current_sprite += 0.15

        # Condition for current sprite to be set back to first image
        if self.current_sprite >= len(self.waterfall_images):
            self.current_sprite = 0

        # Sets image to the contents off the sprites array
        self.image = self.waterfall_images[int(self.current_sprite)]
