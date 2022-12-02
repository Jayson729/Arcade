import pygame
import time
from state import State
from people import People
from sprite import Sprite
from button import Button, ButtonGroup
from settings import Settings
import random

class ArcadeMenu(State):

    def __init__(self) -> None:
        
        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        display_width = 800
        display_height = 600
        
        pygame.display.set_caption('Select Game')
        pygame.display.set_icon(pygame.image.load(f'{self.global_img_path}main.png'))
        self.create_menu()
        super().__init__()

        img_root = 'images/arcade_menu/'

        
        person1 = Sprite(person1Img, display_width * 0.45, display_height * 0.7)
        person1.resize(100.7, 189.2)

        person2Img = pygame.image.load(f'{img_root}/people_sprite2.png')
        person2 = Sprite(person2Img, 700, 200)
        person2.resize(100.7, 189.2)

    def create_menu(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()
        self.people = self.get_people()

        self.menu_sound = pygame.mixer.Sound()
        self.menu_sound.set_volume(Settings.effects_volume/100)

        pygame.mixer.music.load()
        pygame.mixer.music.set_volume(Settings.music_volume/100)
        # loops music
        pygame.mixer.music.play(-1)

    def get_screen(self) -> pygame.Surface:
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def get_background(self) -> Sprite:
        bg_image = pygame.image.load()
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def get_people(self) -> pygame.sprite.Group:
        #TO DO
        person1Img = pygame.image.load(f"{self.img_path}people_sprite.png")
        people = pygame.sprite.Group()

        people.add(People(person1Img, 100, 100).resize(650, 650))

        return people

    def get_buttons(self) -> ButtonGroup:
        buttons = ButtonGroup()
        return buttons
    def cabinetScreen(x, y, width, height, color):
        pygame.draw.rect(gameDisplay, color, (x, y, width, height))

    def draw(self, screen):
        self.background.draw(screen)
        self.people.draw(screen)
        self.buttons.draw(screen)

    def update(self):
        self.background.update()
        self.people.update()
        self.buttons.update()

    

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
                cabinetScreen(cabinetScreenStartX, cabinetScreenStartY,
                            cabinetScreenWidth, cabinetScreenHeight, light_blue_color)
            else:
                cabinetScreen(cabinetScreenStartX, cabinetScreenStartY,
                            cabinetScreenWidth, cabinetScreenHeight, white_color)

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


    def main() -> None:
        game_loop()
        pygame.quit()
        quit()


    if __name__ == '__main__':
        main()
