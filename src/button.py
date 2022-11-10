import pygame
from sprite import Sprite
from settings import Fonts, Colors

class Button(Sprite):
    def __init__(self, text, action, x, y, style=None, 
            size=None, color=None, hover_color=None):
        # set defaults
        default_style = Fonts.start_menu_font
        default_size = 10
        default_color = Colors.start_menu_text
        default_hover_color = Colors.start_menu_text_hover

        # set instance variables
        self.text = text
        self.action = action
        self.style = default_style if style is None else style
        self.size = default_size if size is None else size
        self.color = default_color if color is None else color
        self.hover_color = default_hover_color if hover_color is None else hover_color
        self.currently_hovered = False

        # set font
        self.font = pygame.font.Font(self.style, self.size)

        # render font
        self.font_render = self.font.render(self.text, True, self.color)

        # call super with rendered font
        super().__init__(self.font_render, x, y)
    
    def check_hover(self, mouse) -> bool:
        collision = self.rect.collidepoint(mouse[0], mouse[1])
        self.currently_hovered = collision
        return collision
        # if collision and not self.currently_hovered:
        #     #re-render font to hover
        #     self.font_render = self.font.render(self.text, True, self.hover_color)
        #     self.currently_hovered = True
        # elif not collision and self.currently_hovered:
        #     #re-render font to not hovered
        #     self.font_render = self.font.render(self.text, True, self.color)
        #     self.currently_hovered = False
        
        # self.image = self.font_render
        # return collision
    
    def update(self, index):
        if self.currently_hovered:
            #re-render font to hover
            self.font_render = self.font.render(self.text, True, self.hover_color)
            self.currently_hovered = True
        elif not self.currently_hovered:
            #re-render font to not hovered
            self.font_render = self.font.render(self.text, True, self.color)
            self.currently_hovered = False
        
        self.image = self.font_render

    def do_action(self):
        self.action()
        