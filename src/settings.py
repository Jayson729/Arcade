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


"""Stores colors for Pong"""
class Colors:
    background_color = pygame.Color('turquoise4')
    light_grey = (200, 200, 200)