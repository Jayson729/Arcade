import pygame


"""Resizable sprite class"""
class Block(pygame.sprite.Sprite):

    """Initializes Block"""
    def __init__(self, img_path: str, x_pos: int, 
            y_pos: int, color: pygame.Color = None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.image.load(img_path)
        self.orig_width = self.orig_image.get_width()
        self.orig_height = self.orig_image.get_height()

        self.image = self.orig_image
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        if color is not None:
            self.color = color
            color_image = pygame.Surface(
                self.image.get_size()
            ).convert_alpha()
            color_image.fill(color)
            self.image.blit(
                color_image,
                (0, 0),
                special_flags=pygame.BLEND_RGBA_MULT
            )

    """Resizes a block based on new width/height"""
    def resize(self, new_width: int, new_height: int) -> None:
        # scales image
        self.image = pygame.transform.scale(
            self.orig_image,
            (new_width, new_height)
        )
        self.rect = self.image.get_rect(center=self.rect.center)