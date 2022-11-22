"""Stores basic state information for every game
TODO: Actually implement this into the code
Also, i'm not sure if the functions that do nothing
are supposed to be finished
"""

import pygame

class State:
    """Stores basic state information for every game"""

    def __init__(self):
        """Initalizes State"""
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
