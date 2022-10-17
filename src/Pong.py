import cProfile
import pygame, sys, random
import time

_WINDOW_WIDTH = 500
_WINDOW_HEIGHT = 360

class Ball:
    """
    Initializes Ball
    """
    def __init__(self, ball_speed_x = 10, ball_speed_y = 10, ball_width = 30, ball_height = 30):
        self.rect = pygame.Rect(_WINDOW_WIDTH//2 - ball_width//2, _WINDOW_HEIGHT//2 - ball_height//2, ball_width, ball_height)
        self.ball_speed_x = ball_speed_x * random.choice((1, -1))
        self.ball_speed_y = ball_speed_y * random.choice((1, -1))

    """
    Moves ball back to center and sends to random side
    """
    def restart(self):
        self.rect.center = _WINDOW_WIDTH//2, _WINDOW_HEIGHT//2
        self.ball_speed_y *= random.choice((1, -1))
        self.ball_speed_x *= random.choice((1, -1))

    """
    Handles ball movements/collisions
    """
    def move_ball(self, players):
        self.rect.x += self.ball_speed_x
        self.rect.y += self.ball_speed_y

        #checks for bouncing off ceiling/bottom
        if self.rect.top <= 0 or self.rect.bottom >= _WINDOW_HEIGHT:
            self.ball_speed_y *= -1

        for p in players.values():
            #checks for collisions with players
            if self.rect.colliderect(p):
                self.ball_speed_x *= -1
                break

            elif self.rect.left <= 0 and p.side == 'right':
                self.restart()
                p.player_score += 1
            
            elif self.rect.right >= _WINDOW_WIDTH and p.side == 'left':
                self.restart()
                p.player_score += 1

class Player:
    """
    Initializes Player
    """
    def __init__(self, side, keybindings, player_speed = 10, player_score = 0, player_width = 10, player_height = 140):
        PLAYER_BUFFER = 10
        rect_left = PLAYER_BUFFER
        if side == 'right':
            rect_left = _WINDOW_WIDTH - PLAYER_BUFFER - player_width
        self.rect = pygame.Rect(rect_left, _WINDOW_HEIGHT//2 - player_height//2, player_width, player_height)

        self.keybindings = keybindings
        self.player_speed = player_speed
        self.player_score = player_score
        self.side = side

    """
    Moves the player
    """
    def move_player(self, dir):
        if dir == 'up':
            self.rect.y -= self.player_speed
        else:
            self.rect.y += self.player_speed
        
        self.check_collision()
    
    """
    Checks if the player is colliding with ceiling or floor
    """
    def check_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= _WINDOW_HEIGHT:
            self.rect.bottom = _WINDOW_HEIGHT

"""
AI for pong
"""
class Opponent(Player):
    """
    returns either 'up' or 'down'
    """
    def move_opponent(self, ball):
        if self.rect.top < ball.rect.y:
            self.move_player('down')
        else:
            self.move_player('up')

"""
main function
"""
def main():
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((_WINDOW_WIDTH, _WINDOW_HEIGHT))
    pygame.display.set_caption('Pong')

    #fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background_color = pygame.Color('turquoise4')
    background.fill(background_color)

    #sets keybindings
    left_inputs = {'up': pygame.K_w, 'down': pygame.K_s, 'pause': pygame.K_ESCAPE}
    right_inputs = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'pause': pygame.K_ESCAPE}

    #creates ball, player, and opponent
    ball = Ball()
    # ball1 = Ball()
    # ball2 = Ball()
    # balls = [ball1, ball2]

    left_player = Opponent('left', left_inputs)
    # left_player = Player('left', left_inputs)
    # right_player = Opponent('right', right_inputs)
    right_player = Player('right', right_inputs)

    #creates dict of players
    players = {'left': left_player, 'right': right_player}
    
    #sets colors and fonts
    grey = (200, 200, 200)
    score_font = pygame.font.Font(None, 50)
    pause_font = pygame.font.Font(None, 150)
    
    #used for pausing game
    RUNNING, PAUSE = 0, 1
    state = RUNNING
    clock = pygame.time.Clock()
    
    #game loop
    while True:
        # start_time = time.perf_counter()
        #move players
        pressed = pygame.key.get_pressed()
        for p in players.values():
            if not isinstance(p, Player): print(f"{p} is not a player"); break
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == p.keybindings['pause']: state = (state + 1) % 2
            # if isinstance(p, Opponent): p.move_player(ball1); continue
            if isinstance(p, Opponent): p.move_opponent(ball); continue
            if state == RUNNING:
                if pressed[p.keybindings['up']]: p.move_player('up')
                elif pressed[p.keybindings['down']]: p.move_player('down')
        

        #fill background
        screen.fill(background_color)

        if state == RUNNING:
            #move and draw ball
            # for ball in balls:
            #     ball.move_ball(players)
            #     pygame.draw.ellipse(screen, grey, ball)

            ball.move_ball(players)
            pygame.draw.ellipse(screen, grey, ball)

            #draw players and scores
            for p in players.values():
                pygame.draw.rect(screen, grey, p.rect)
                score_text = score_font.render(f"{p.player_score}", False, 'grey67')
                if p.side == 'left':
                    screen.blit(score_text, (_WINDOW_WIDTH//2 - 120, 50))
                elif p.side == 'right':
                    screen.blit(score_text, (_WINDOW_WIDTH//2 + 120, 50))
            
        elif state == PAUSE:
            pause_text = pause_font.render("Game is paused", False, 'grey67')
            screen.blit(pause_text, (0, _WINDOW_HEIGHT//2))
        
        # end_time = time.perf_counter()
        # print(f"Execution Time: {end_time - start_time:0.6f}")
    
        pygame.display.flip()
        
        clock.tick(60)
        print(f"fps: {clock.get_fps()}")

if __name__ == "__main__":
    main()