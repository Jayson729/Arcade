import pygame

class Waterfall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # This could be more efficient, resizing all images of sprite to same size
        img_root = 'images/start_menu/waterfall/'
        waterfall_0 = pygame.transform.scale(pygame.image.load(f'{img_root}0.png'), (60, 415))
        waterfall_1 = pygame.transform.scale(pygame.image.load(f'{img_root}1.png'), (60, 415))
        waterfall_2 = pygame.transform.scale(pygame.image.load(f'{img_root}2.png'), (60, 415))
        waterfall_3 = pygame.transform.scale(pygame.image.load(f'{img_root}3.png'), (60, 415))
        waterfall_4 = pygame.transform.scale(pygame.image.load(f'{img_root}4.png'), (60, 415))
        waterfall_5 = pygame.transform.scale(pygame.image.load(f'{img_root}5.png'), (60, 415))

        super().__init__()
        # Creating array with all images for the sprite
        self.sprites = []
        self.sprites.append(waterfall_0)
        self.sprites.append(waterfall_1)
        self.sprites.append(waterfall_2)
        self.sprites.append(waterfall_3)
        self.sprites.append(waterfall_4)
        self.sprites.append(waterfall_5)

        # Sets current sprite to the first image in the array
        self.current_sprite = 0
        # Sets image to whatever image index current_sprite is equal to
        self.image = self.sprites[self.current_sprite]

        # Creating a rectangle for screen placement
        self.rect = self.image.get_rect()
        # Setting how the image is drawn
        self.rect.topleft = [x, y]

    def update(self):
        # Incrementing the sprites with a decimal so the array will loop slower
        self.current_sprite += 0.15

        # Condition for current sprite to be set back to first image
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        # Sets image to the contents off the sprites array
        self.image = self.sprites[int(self.current_sprite)]