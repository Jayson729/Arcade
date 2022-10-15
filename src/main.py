import pygame
import pygame.freetype
from pygame import mixer

# Initializes the main menu
pygame.init()
pygame.font.init()
pygame.mixer.init()
# https://www.dropbox.com/sh/g1law0qmnf6pjwr/AACummg5fZJ5JIF4ReeRDxJia?dl=0&preview=Stardew_Valley.ttf\
font = pygame.font.Font('Stardew_Valley.ttf', 50)

# Creates a screen for main menu
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


# Creating button class for buttons
class Button:
    def __init__(self, text, x, y, image):
        # Creating button from image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Setting text
        # self.text = font.render(text, True, '#FFC300')
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.text, self.text_rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    # Gets mouse position
    pos = pygame.mouse.get_pos()


class text_brown:
    def __init__(self, text, x, y):
        self.text = font.render(text, True, '#DDA059')
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.text, self.text_rect)

    def check_hover(self):
        pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(pos):
            return True
        else:
            return False


class text_yellow:
    def __init__(self, text, x, y):
        self.text = font.render(text, True, '#FFD921')
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.text, self.text_rect)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                return True
            else:
                return False



# Checks if mouse is hovering over and if clicked

#    if pygame.mouse.get_pressed()[0] == 1:


# Background for main
# Artist - @NeerTrustABear, pixilart.com
# Publishing date - 2021
# Type (gif, converted to png)
# # Web address(https://www.pixilart.com/art/floating-island-7c40a7fbda173c5)
background = pygame.image.load('backgroundMain.png')
background = pygame.transform.scale(background, (800, 600))

# Background music for main
# Runescape - Dream(#36)
# Composer - Ian Taylor
# Published by - Jagex
# Publishing date - March 15, 2004
# Type (wav)
# Web address(https://oldschool.runescape.wiki/w/Dream_(music_track))
mixer.music.load('runescape_dream.wav')
mixer.music.play(-1)

# Sets title and icon and set for main menu
pygame.display.set_caption("Arcade Games")
icon = pygame.image.load('main.png')
pygame.display.set_icon(icon)
enter_text_brown = text_brown("ENTER ARCADE", 276, 110)
enter_text_yellow = text_yellow("ENTER ARCADE", 276, 110)

# Right facing small cloud movement
small_right = pygame.image.load('small_right.png')
small_right = pygame.transform.scale(small_right, (200, 170))
small_rX = 60
small_rY = 50
small_rY_change = 0.5

small_left = pygame.image.load('small_left.png')
small_left = pygame.transform.scale(small_left, (150, 100))
small_lX = 500
small_lY = 30
small_lY_change = 0.5

# Creating large cloud image for lower clouds
large_cloud = pygame.image.load('large_cloud.png')

cloud_1 = pygame.transform.scale(large_cloud, (700, 650))
cloud_1_x = -210
cloud_1_y = 150
cloud_1_change = 0.5

cloud_2 = pygame.transform.scale(large_cloud, (500, 450))
cloud_2_x = 500
cloud_2_y = 200
cloud_2_change = 0.5

cloud_3 = pygame.transform.scale(large_cloud, (800, 760))
cloud_3_x = 380
cloud_3_y = 175
cloud_3_change = 0.5

cloud_4 = pygame.transform.scale(large_cloud, (800, 760))
cloud_4_x = -375
cloud_4_y = 260
cloud_4_change = 0.5


def small_right_move(x, y):
    screen.blit(small_right, (x, y))


def small_left_move(x, y):
    screen.blit(small_left, (x, y))


def cloud_1_move(x, y):
    screen.blit(cloud_1, (x, y))


def cloud_2_move(x, y):
    screen.blit(cloud_2, (x, y))


def cloud_3_move(x, y):
    screen.blit(cloud_3, (x, y))


def cloud_4_move(x, y):
    screen.blit(cloud_4, (x, y))


# Creates a loop for main menu screen
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Small right facing cloud movement
    small_rY += small_rY_change

    if small_rY <= 46:
        small_rY_change = .025
    elif small_rY >= 50:
        small_rY_change = -.025

    # Small left facing cloud movement
    small_lY += small_lY_change

    if small_lY <= 26:
        small_lY_change = .025
    elif small_lY >= 30:
        small_lY_change = -.025

    cloud_1_y += cloud_1_change

    if cloud_1_y <= 146:
        cloud_1_change = .025
    elif cloud_1_y >= 150:
        cloud_1_change = -.025

    cloud_2_y += cloud_2_change

    if cloud_2_y <= 196:
        cloud_2_change = .025
    elif cloud_2_y >= 200:
        cloud_2_change = -.025

    cloud_3_y += cloud_3_change

    if cloud_3_y <= 171:
        cloud_3_change = .025
    elif cloud_3_y >= 175:
        cloud_3_change = -.025

    cloud_4_y += cloud_4_change

    if cloud_4_y <= 256:
        cloud_4_change = .025
    elif cloud_4_y >= 260:
        cloud_4_change = -.025

    # Color for main background
    screen.fill((135, 206, 235))
    # Background Image
    screen.blit(background, (0, 0))
    clock.tick(60)

    if enter_text_brown.check_hover():
        enter_text_yellow.draw()
    else:
        enter_text_brown.draw()

    if enter_text_yellow.check_click():
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('arcade_door.wav'))

    small_right_move(small_rX, small_rY)
    small_left_move(small_lX, small_lY)
    cloud_2_move(cloud_2_x, cloud_2_y)
    cloud_1_move(cloud_1_x, cloud_1_y)
    cloud_3_move(cloud_3_x, cloud_3_y)
    cloud_4_move(cloud_4_x, cloud_4_y)
    pygame.display.update()
