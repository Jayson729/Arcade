import pygame
import time
import pygame.display
import pygame.freetype
import pygame.mixer

pygame.init()

display_width = 809
display_height = 600

black_color = (0, 0, 0)
white_color = (255, 255, 255)

person_width = 150

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Select Game')
clock = pygame.time.Clock()

peopleImg = pygame.image.load('images/people_sprite.png')

def person(x,y):
    gameDisplay.blit(peopleImg, (x, y))

def game_loop():

    x = (display_width * 0.45)
    y = (display_height * 0.7)

    exit = False
    delete = False

    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True


        gameDisplay.fill(black_color)
        person(x,y)

        if x > display_width - person_width or x < 0:
             delete = True

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
