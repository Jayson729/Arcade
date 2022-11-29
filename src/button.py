import pygame
from sprite import Sprite
from settings import Fonts, Colors

class Button(Sprite):
    """Button class that works with keyboard and mouse"""

    def __init__(self, x: int, y: int, text, font, action, color=None, hover_color=None) -> None:
        """Initializes Button"""
        # set defaults
        # self.fonts = Fonts()
        default_color = Colors.start_menu_text
        default_hover_color = Colors.start_menu_text_hover

        # set instance variables
        self.color = default_color if color is None else color
        self.hover_color = default_hover_color if hover_color is None else hover_color
        self.currently_hovered = False
        self.currently_keyboard_hovered = False
        self.currently_mouse_hovered = False
        self.text = text
        self.font = font
        self.action = action

        # render font
        self.font_render = self.font.render(self.text, True, self.color)

        # call super with rendered font
        super().__init__(x, y, self.font_render)

    def check_mouse_hover(self, mouse: tuple) -> bool:
        """Checks if the mouse is hovering
        return True if colliding, False if not
        """
        collision = self.rect.collidepoint(mouse[0], mouse[1])
        self.currently_mouse_hovered = collision
        return self.currently_mouse_hovered

    def set_keyboard_hover(self, val: bool) -> None:
        """Sets keyboard hover to val"""
        self.currently_keyboard_hovered = val

    def update(self) -> None:
        """Updates button"""
        self.currently_hovered = (self.currently_keyboard_hovered
            or self.currently_mouse_hovered)
        if self.currently_hovered:
            #re-render font to hover
            self.font_render = self.font.render(
                self.text, True, self.hover_color)
        elif not self.currently_hovered:
            #re-render font to not hovered
            self.font_render = self.font.render(
                self.text, True, self.color)

        self.image = self.font_render

    def do_action(self) -> None:
        """Another way to call b.action()"""
        self.action()
