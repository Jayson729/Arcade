import pygame, sys
import random


# ball movement, collision, and stay inbounds
def ball_annimation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if(ball.top <= 0 or ball.bottom >= height):
        ball_speed_y *= -1

    if(ball.colliderect(player) or ball.colliderect(opponent)):
        ball_speed_x *= -1

    if(ball.left <= 0):
        restart()
        player_score += 1
        
    if(ball.right >= width):
        restart()
        opponent_score += 1

        
        
# player stay inbounds
def player_inbounds():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >=  height:
        player.bottom = height

# opponent AI and stay inbounds
def opponent_move():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >=  height:
        player.bottom = height

# if scored ball restart in middle
def restart():
    global ball_speed_x, ball_speed_y
    ball.center = width/2, height/2
    ball_speed_y *= random.choice((1,-1))
    ball_speed_x *= random.choice((1,-1))

# make window
width = 1280
height = 960
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Pong')

pygame.init()
clock = pygame.time.Clock()

# make window
width = 1280
height = 960
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Pong')


# creates ball, player, and opponent
ball = pygame.Rect(width/2 - 15,height/2 - 15,30,30)
player = pygame.Rect(width - 20,height/2 - 70,10,140)
opponent = pygame.Rect(10,height/2 - 70,10,140)


background = pygame.Color('turquoise4')
grey = (200,200,200)
ball_speed_x = 10 * random.choice((1,-1))
ball_speed_y = 10 * random.choice((1,-1))
player_speed = 0
opponent_speed = 10

player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 50)

# game loop and working up/down keys
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 10
            if event.key == pygame.K_UP:
                player_speed -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 10
            if event.key == pygame.K_UP:
                player_speed += 10
    

    ball_annimation()
    player_inbounds()
    opponent_move()
    
    screen.fill(background)
    pygame.draw.rect(screen,grey, player)
    pygame.draw.rect(screen,grey, opponent)
    pygame.draw.ellipse(screen,grey, ball)
    player_text = game_font.render(f"{player_score}", False, 'grey67')
    screen.blit(player_text, (760, 50))
    opponent_text = game_font.render(f"{opponent_score}", False, 'grey67')
    screen.blit(opponent_text, (560, 50))
        

    pygame.display.flip()
    clock.tick(60)

