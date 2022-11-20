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
            color=None, speed=1.0, name: str='base') -> None:

        # load images
        self.orig_animations = {name: self.get_images(folder_path)}
        self.animations = {name: self.orig_animations[name]}
        self.images = self.animations[name]
        

        self.NUM_IMAGES = len(self.images)

        super().__init__(self.images[0], x, y, color)

        # Sets current sprite to the first image in the array
        self.current_sprite = 0
        self.current_animation = name
        self.speeds = {name: speed}
    
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
        
        # this almost works, but is hard to read and doesn't ignore non-numeric filenames
        # for file_name in sorted(os.listdir(path), key = lambda x: (len(x), x.split('.')[0])):
        #     if os.path.isfile(os.path.join(path, file_name)):
        #         img = pygame.image.load(path + '/' + file_name).convert_alpha()
        #         images.append(img)

        return images

    """Updates sprite"""
    def update(self) -> None:
        # Incrementing the sprites with a decimal so the array will loop slower
        self.current_sprite += self.speeds[self.current_animation]

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
                self.orig_animations[self.current_animation][key] = pygame.transform.scale(
                    self.orig_animations[self.current_animation][key],
                    (new_width, new_height)
                )
            self.orig_image = self.orig_animations[self.current_animation][0]
            self.orig_size = self.orig_image.get_size()

        for key, value in enumerate(self.images):
            # scales image
            self.images[key] = pygame.transform.scale(
                self.orig_animations[self.current_animation][key],
                (new_width, new_height)
            )
            self.image = self.images[int(self.current_sprite)]
            self.rect = self.images[0].get_rect(center=self.rect.center)
        
    def rotate(self, degrees):
        self.images = [pygame.transform.rotate(i, degrees) for i in self.animations[self.current_animation]]
        
    def add_animation(self, name: str, folder_path: str, speed: float):
        self.orig_animations[name] = self.get_images(folder_path)
        self.animations[name] = self.orig_animations[name]
        self.speeds[name] = speed
    
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