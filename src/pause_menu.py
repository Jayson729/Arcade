"""TODO: Make a general pause menu for every game
Should be pretty simple, no fancy art just some buttons
for settings/quit game (go to another menu)
Code should be pretty similar to start menu for buttons
"""
import pygame
import pygame.mixer
import pygame.freetype
import pygame.display
from state import State
from game import Game


class PauseMenu(State):
    def __init__(self):
        super(PauseMenu, self).__init__()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.clock.tick(self.fps)
        pygame.display.set_caption("Arcade Games")
        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(0.3)
        pygame.mixer.music.load('music/runescape_dream.wav')
        pygame.mixer.music.play(-1)
        self.curr_index = 0
        self.menu_items = ["RESUME", "SETTINGS", "QUIT GAME"]
        img_root = 'images/pause_menu/'
        self.background_img = pygame.transform.scale(pygame.image.load(f"{img_root}Myproject-1.png"), (800, 600))


    def which_state(self, event):
        for item in self.menu_items:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN and item == "RESUME":
                    self.next_state = "RESUME"
                elif event.key == pygame.K_RETURN and item == "SETTINGS":
                    self.next_state = "SETTINGS"
                elif event.key == pygame.K_RETURN and item == "QUIT GAME":
                    self.next_state = "QUIT GAME"
                
    def render_text(self, index):
        if index == 0:
            self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 50)
        elif index == 1:
            self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 50)
        elif index == 2:
            self.font = pygame.font.Font('fonts/Stardew_Valley.ttf', 50)

        color = '#845916'
        return self.font.render(self.menu_items[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.topleft[0] + 410, self.screen_rect.topleft[1] + 125 + (index * 40))
        return text.get_rect(center=center)

    def handle_action(self):
        if self.curr_index == 0:
            self.done = True
        elif self.curr_index == 1:
            self.done = True
        elif self.curr_index == 2:
            self.done = True 
        
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
            if event.key == pygame.K_UP:
                self.menu_sound.play()
                if self.curr_index <= 0:
                    self.curr_index = 2
                elif self.curr_index == 2:
                    self.curr_index = 1
                else:
                    self.curr_index = 0
            elif event.key == pygame.K_w:
                self.menu_sound.play()
                if self.curr_index <= 0:
                    self.curr_index = 2
                elif self.curr_index == 2:
                    self.curr_index = 1
                else:
                    self.curr_index = 0
            elif event.key == pygame.K_DOWN:
                self.menu_sound.play()
                if self.curr_index == 0:
                    self.curr_index = 1
                elif self.curr_index >= 2:
                    self.curr_index = 0
                else:
                    self.curr_index = 2
            elif event.key == pygame.K_s:
                self.menu_sound.play()
                if self.curr_index == 0:
                    self.curr_index = 1
                elif self.curr_index >= 2:
                    self.curr_index = 0
                else:
                    self.curr_index = 2

            elif event.key == pygame.K_RETURN:
                self.handle_action()

    def transform_image(self, image, scalex, scaley):
        return pygame.transform.scale(image, (scalex, scaley))

    def update_count(self, count):
        if count <= 0:
            count += 0.25

    def draw(self, screen):
        screen.blit(self.background_img, (0, 0))
        for index, option in enumerate(self.menu_items):
            text_render = self.render_text(index)
            screen.blit(text_render, self.get_text_position(text_render, index))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game = Game(screen, {'PAUSE': PauseMenu()}, 'PAUSE')
    game.run()
    PauseMenu()

if __name__ == '__main__':
    main()