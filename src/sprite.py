import os
import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, img, color=None):
        super().__init__()
        self.image = img
        self.ORIGINAL_IMAGE = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.IMAGE_RATIO = self.image.get_width() / self.image.get_height()

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
    
    def resize(self, multiplier) -> None:
        height = self.ORIGINAL_IMAGE.get_height() * multiplier
        width = height * self.IMAGE_RATIO
        self.image = pygame.transform.scale(
            self.ORIGINAL_IMAGE,
            (width, height)
        )
        self.rect = self.image.get_rect(center=self.rect.center)
    
    # rounding errors if not rotating by 90 degree increments
    # I think
    def rotate(self, degrees):
        self.image = pygame.transform.rotate(self.image, degrees)
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect.center)


class AnimatedSprite(Sprite):
    def __init__(self, x, y, path, animation_speed, name='base', color=None):
        self.images = self.get_images(path)
        super().__init__(x, y, self.images[0], color)
        self.animation_speed = animation_speed
        self.NUM_IMAGES = len(self.images)

        self.animations = {name: self.images}
        self.animation_speeds = {name: animation_speed}
        self.original_animations = {name: self.images}
        
        self.animation_time_prev = pygame.time.get_ticks()
        self.animation_trigger = False

        self.current_sprite = 0
        self.current_animation = name

    def update(self):
        self.check_animation_speed()
        self.animate()

    def animate(self):
        if not self.animation_trigger:
            return

        self.current_sprite = (self.current_sprite + 1) % self.NUM_IMAGES

        # Sets image to the contents off the sprites array
        self.image = self.images[self.current_sprite]

    def check_animation_speed(self):
        self.animation_trigger = False
        time_now = pygame.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_speed:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path: str):
        images = []
        files = {}
        # finds all files in path (ignores folders)
        # also ignores any files not named a digit
        for f in os.listdir(path):
            if not os.path.isfile(os.path.join(path, f)):
                continue
            
            # splits file_name from extension
            file_name, file_extension = os.path.splitext(f)
            if not file_name.isnumeric(): 
                continue
            
            # adds file_extension to a dict at key file_name 
            # this way, we can sort later and still
            # know what the file name is
            files[file_name] = file_extension

        for file_name in sorted(files, key=int):
            img = pygame.image.load(f'{path}/{file_name}{files[file_name]}').convert_alpha()
            images.append(img)

        return images

    # from https://predictivehacks.com/?all-tips=how-to-split-a-list-into-equal-elements-in-python
    # don't really know how it works but it does    
    def split_list(self, input: list, num_elem):
        output = []
        for i in range(0, len(input), num_elem):
            output.append(input[i:i + num_elem])

        return output

    def resize(self, multiplier):
        for key, value in enumerate(self.images):
            height = self.ORIGINAL_IMAGE.get_height() * multiplier
            width = height * self.IMAGE_RATIO
            self.images[key] = pygame.transform.scale(
                self.ORIGINAL_IMAGE,
                (width, height)
            )
        self.image = self.images[int(self.current_sprite)]
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def rotate(self, degrees):
        self.images = [pygame.transform.rotate(i, degrees) for i in self.animations[self.current_animation]]

    def add_animation(self, name: str, folder_path: str, speed: float):
        self.original_animations[name] = self.get_images(folder_path)
        self.animations[name] = self.original_animations[name]
        self.animation_speeds[name] = speed
    
    def add_animation_w_images(self, name: str, images: list, speed: float):
        self.original_animations[name] = images
        self.animations[name] = images
        self.animation_speeds[name] = speed

    def set_animation(self, name):
        if name not in self.animations:
            print(f'{name} not in animations')
            return
        # ignore if it's already at that animation
        if name == self.current_animation:
            return
        self.current_sprite = 0
        self.current_animation = name
        self.images = self.animations[name]
        self.NUM_IMAGES = len(self.images)