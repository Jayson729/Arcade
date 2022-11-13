import pygame
import time
from sprite import Sprite
import random

pygame.init()

display_width = 800
display_height = 600

black_color = (0, 0, 0)
white_color = (255, 255, 255)
light_blue_color = (0, 0, 230)

person_width = 150

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Select Game')
clock = pygame.time.Clock()

img_root = 'images/arcade_menu/'

person1Img = pygame.image.load(f'{img_root}people_sprite.png')
person1 = Sprite(person1Img, display_width * 0.45, display_height * 0.7)
person1.resize(100.7, 189.2)

person2Img = pygame.image.load(f'{img_root}/people_sprite2.png')
person2 = Sprite(person2Img, 700, 200)
person2.resize(100.7, 189.2)

def cabinetScreen(x, y, width, height, color):
    pygame.draw.rect(gameDisplay, color, (x, y, width, height))

# def person1(x,y):
#     gameDisplay.blit(person1.image, (x, y))

# def person2(x,y):
#     gameDisplay.blit(person2.image, (x, y))

def textObjects(text, font):
    textSurface = font.render(text, True, white_color)
    return textSurface, textSurface.get_rect()

def messageDisplay(text):
    # TO DO: Basically what I want to do is make it so once you hover it shows 
    # the title and a brief description as a text box on the bottom of the screen
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = textObjects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def gameHover():
    messageDisplay('Pong')

def game_loop():

    x1 = (display_width * 0.45)
    x2 = 700
    y1 = (display_height * 0.7)
    y2 = 200
    
    cabinetScreenStartX = 150
    cabinetScreenStartY = 300
    cabinetScreenWidth = 100
    cabinetScreenHeight = 100

    personSpriteSpeed = 1

    exit = False

    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        gameDisplay.fill(black_color)

        mouse = pygame.mouse.get_pos()

        if cabinetScreenStartX + cabinetScreenWidth > mouse[0] > cabinetScreenStartX and cabinetScreenStartY + cabinetScreenHeight > mouse[1] > cabinetScreenStartY:
            cabinetScreen(cabinetScreenStartX, cabinetScreenStartY, cabinetScreenWidth, cabinetScreenHeight, light_blue_color)
        else:
            cabinetScreen(cabinetScreenStartX, cabinetScreenStartY, cabinetScreenWidth, cabinetScreenHeight, white_color)
        
        gameDisplay.blit(person1.image, (x1, y1))
        gameDisplay.blit(person2.image, (x2, y2))

        x1 += personSpriteSpeed
        x2 -= personSpriteSpeed
        y1 -= personSpriteSpeed
        y2 += personSpriteSpeed

        # I want to make multiple family sprites that will walk up and down the screen
        if x1 > display_width:
            y1 = display_height * 0.7
            x1 = display_width * 0.45
            # person1(x1,y1)

        if y2 > display_height:
            y2 = 200
            x2 = 700
            # person2(x2, y2)

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
