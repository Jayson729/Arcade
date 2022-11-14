"""TODO: We probably want keybindings here, 
then have them either be global (like now),
or have them initialized in a class like the commented out code
Also, I'm not sure if sounds/music should be here,
maybe those should be game specific since they'll only be used in a singular game
Also, if we want to do actual resizing just have a list of some 4:3 resolutions
that you can select between
"""

import pygame
# TODO: make these more general to be used in
# all games
# maybe something like this?
# class Settings:
#     def __init__(self, window_width=800, window_height=600, aspect_ratio=4/3, fps=60, fonts=None, colors=None):
#         self.window_width = window_width
#         self.window_height = window_height
#         self.aspect_ratio = aspect_ratio
#         self.fps = fps
#         self.fonts = self.default_fonts if fonts is None else fonts
#         self.colors = self.default_colors if colors is None else colors

"""Stores settings for Pong"""
class Settings:
    fps = 60
    aspect_ratio = 4/3
    window_width = 800
    window_height = 600
    player_buffer = 40


"""Stores fonts for Pong"""
class Fonts:
    pygame.font.init()
    score_font = pygame.font.Font(None, 50)
    pause_font = pygame.font.Font(None, 150)
    start_menu_font = 'fonts/Stardew_Valley.ttf'


"""Stores colors for Pong"""
class Colors:
    background_color = pygame.Color('turquoise4')
    light_grey = (200, 200, 200)
    start_menu_text = '#DDA059'
    start_menu_text_hover = '#FFD921'

# class Sounds:
#     pygame.mixer.init()
#     start_menu_sound = pygame.mixer.Sound('sounds/click.wav')
#     start_menu_sound.set_volume(0.3)

# class Music:
#     pygame.mixer.init()
#     start_menu_music = pygame.mixer.music.load('music/runescape_dream.wav')
    
