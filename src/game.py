"""TODO: Actually implement this into the game Maybe have each menu extend Game and then have Game extend State
that way they'd all have the same screen/states and stuff like that
This should also store the settings if we decide to
have a class for settings instead
The self.screen here should be used for all games
"""

import pygame
from state import State

class Game:
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.count = 0
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        next_state = self.state.next_state
        self.state_name = next_state
        # persistent = self.state.persist
        pygame.mixer.music.stop()
        self.state = self.states[self.state_name]()
        self.state.done = False
        # self.state.startup(persistent)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

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
            self.state.game_manager.do_input()
            self.state.game_manager.run_game()
            pygame.display.update()
            self.clock.tick(self.fps)
            if self.state.done:
                self.flip_state()
