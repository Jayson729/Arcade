import pygame
import pygame.display
import pygame.freetype
import pygame.mixer
import sprites
from states.base import BaseState
from sprites import Waterfall


# Initializes the main menu
# Creates a screen for main menu
class StartMenu(BaseState):
    def __init__(self):
        super(StartMenu, self).__init__()
        pygame.display.set_caption("Arcade Games")
        pygame.display.set_icon(pygame.image.load('main.png'))
        self.menu_sound = pygame.mixer.Sound('click.wav')
        self.menu_sound.set_volume(0.3)
        pygame.mixer.music.load('runescape_dream.wav')
        pygame.mixer.music.play(-1)
        self.count = 0
        self.index = 0
        self.curr_index = 0
        self.change = .025
        self.menu_items = ["ENTER ARCADE", "SETTINGS", "CREDITS"]
        self.font = pygame.font.Font('Stardew_Valley.ttf', 10)
        self.large_cloud = pygame.image.load("large_cloud.png")
        self.small_right = pygame.image.load("small_right.png")
        self.small_left = pygame.image.load("small_left.png")
        self.background_img = pygame.transform.scale(pygame.image.load("backgroundMain.png"), (800, 600))
        # Cloud y values from cloud_1 to small_cloud_2
        self.cloud_1 = self.transform_image(self.large_cloud, 700, 650)
        self.cloud_2 = self.transform_image(self.large_cloud, 500, 450)
        self.cloud_3 = self.transform_image(self.large_cloud, 800, 760)
        self.cloud_4 = self.transform_image(self.large_cloud, 800, 760)
        self.small_cloud_1 = self.transform_image(self.small_left, 150, 100)
        self.small_cloud_2 = self.transform_image(self.small_right, 200, 170)
        self.index = 0
        self.y = 0
        self.sprites = pygame.sprite.Group()
        waterfall = Waterfall(390, 350)
        self.sprites.add(waterfall)

    def which_state(self, event):
        for item in self.menu_items:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN and item == "ENTER ARCADE":
                    self.next_state = "ARCADE"
                elif event.key == pygame.K_RETURN and item == "SETTINGS":
                    self.next_state = "SETTINGS"
                elif event.key == pygame.K_RETURN and item == "CREDITS":
                    self.next_state = "ARCADE"

    def render_text(self, index):
        if index == 0:
            self.font = pygame.font.Font('Stardew_Valley.ttf', 50)
        elif index == 1:
            self.font = pygame.font.Font('Stardew_Valley.ttf', 40)
        elif index == 2:
            self.font = pygame.font.Font('Stardew_Valley.ttf', 30)

        color = '#FFD921' if index == self.curr_index else '#DDA059'
        return self.font.render(self.menu_items[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.topleft[0] + 410, self.screen_rect.topleft[1] + 125 + (index * 40))
        return text.get_rect(center=center)

    def handle_action(self):
        if self.curr_index == 0:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('arcade_door.wav'))
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

    def image_move(self, screen, image, x, y, low_y, high_y, change):
        if y <= low_y:
            y += change
        elif y >= high_y:
            y -= change

        screen.blit(image, (x, y))


    def draw(self, screen):
        screen.blit(self.background_img, (0, 0))
        # Small right facing cloud movement
        self.sprites.draw(screen)
        self.image_move(screen, self.cloud_1, -210, 150, 146, 150, 0.025)
        self.image_move(screen, self.cloud_2, 500, 200, 196, 200, 0.025)
        self.image_move(screen, self.cloud_3, 380, 175, 171, 175, 0.025)
        self.image_move(screen, self.cloud_4, -375, 260, 256, 260, 0.025)
        self.image_move(screen, self.small_cloud_1, 525, 30, 26, 30, 0.025)
        self.image_move(screen, self.small_cloud_2, 60, 50, 46, 50, 0.025)
        self.sprites.update()
        for index, option in enumerate(self.menu_items):
            text_render = self.render_text(index)
            screen.blit(text_render, self.get_text_position(text_render, index))
