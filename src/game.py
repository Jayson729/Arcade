"""TODO: Actually implement this into the game
Maybe have each menu extend Game and then have Game extend State
that way they'd all have the same screen/states and stuff like that
This should also store the settings if we decide to
have a class for settings instead
The self.screen here should be used for all games
"""

import sys
import pygame
from settings import Settings


class Game:
    def __init__(self, screen, states, start_state):
        self.delta_time = 1
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.count = 0
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.state.do_event(event)

    def flip_state(self):
        self.state_name = self.state.next_state
        # persistent = self.state.persist.pop()
        pygame.mixer.music.stop()
        # self.state = self.states[persistent](screen=self.screen)
        self.state = self.states[self.state_name]()
        self.state.done = False
        # self.state.startup(persistent)

    def update(self, dt):
        self.state.update()
        if self.state.done:
            self.flip_state()

    def draw(self, screen):
        self.state.draw(screen)

    def run(self):
        # while not self.done:
        #     dt = self.clock.tick(self.fps)
        #     self.event_loop()
        #     self.update(dt)
        #     self.draw()
        #     if self.count <= 0:
        #         self.count += 0.025
        #     elif self.count >= 4:
        #         self.count -= 0.025
        #     pygame.display.update()
        self.state = self.state()
        while not self.state.done:
            delta_time = self.clock.tick(Settings.fps)
            self.check_events()
            self.update(delta_time)
            self.draw(self.screen)
            pygame.display.update()
