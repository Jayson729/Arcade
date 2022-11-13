import pygame


"""General resizable sprite class"""
class Sprite(pygame.sprite.Sprite):

    """Initializes a Sprite, 
    takes an actual image, not a path to the image
    """
    def __init__(self, img: pygame.Surface, x_pos: int, 
            y_pos: int, color: tuple=None) -> None:
        super().__init__()
        self.orig_image = img.copy()
        self.orig_size = img.get_size()

        self.image = self.orig_image
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        if color is not None:
            self.color = color
            color_image = pygame.Surface(
                self.orig_size
            ).convert_alpha()
            color_image.fill(color)
            self.image.blit(
                color_image,
                (0, 0),
                special_flags=pygame.BLEND_RGBA_MULT
            )
        
    """Resizes a sprite based on new width/height
    if original is True, resizes original image too
    """
    def resize(self, new_width: int, new_height: int, original=False) -> None:
        if original:
            self.orig_image = pygame.transform.scale(
            self.orig_image,
            (new_width, new_height)
            )
            self.orig_size = self.orig_image.get_size()
        # scales image
        self.image = pygame.transform.scale(
            self.orig_image,
            (new_width, new_height)
        )
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def rotate(self, degrees):
        self.image = pygame.transform.rotate(self.orig_image, degrees)
