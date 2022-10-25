import cProfile
import pygame, sys, random
import time

_WINDOW_WIDTH = 1280
_WINDOW_HEIGHT = 960

class Block(pygame.sprite.Sprite):
    def __init__(self, img_path: str, x_pos: int, y_pos: int):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

class Ball(Block):
    """
    Initializes Ball
    """
    def __init__(self, img_path: str, x_pos: int, y_pos: int, players: pygame.sprite.Group = None, ball_speed_x: int = 15, ball_speed_y: int = 15):
        super().__init__(img_path, x_pos, y_pos)
        self.ball_speed_x = ball_speed_x * random.choice((1, -1))
        self.ball_speed_y = ball_speed_y * random.choice((1, -1))
        self.players = players

    """
    Handles ball movements/collisions
    """
    def update(self):
        self.rect.x += self.ball_speed_x
        self.rect.y += self.ball_speed_y
        self.check_collisions()
        self.update_score()

    """
    Moves ball back to center and sends to random side
    """
    def reset_ball(self):
        self.rect.center = _WINDOW_WIDTH//2, _WINDOW_HEIGHT//2
        self.ball_speed_y *= random.choice((1, -1))
        self.ball_speed_x *= random.choice((1, -1))

    def check_collisions(self):
        #checks for bouncing off ceiling/bottom
        if self.rect.top <= 0 or self.rect.bottom >= _WINDOW_HEIGHT:
            self.ball_speed_y *= -1

        players_hit = pygame.sprite.spritecollide(self, self.players, False)

        #checks for collisions with players
        """
        really players_hit should have exactly one element for normal pong, 
        but if we ever decide to change anything this might be needed
        """
        for p in players_hit:
            #hit side of player
            if p.side == 'left' and self.ball_speed_x > 0:
                self.ball_speed_x *= -1
            elif p.side == 'right' and self.ball_speed_x < 0:
                self.ball_speed_x *= -1
            
            #hit top or bottom of player
            #bottom
            if self.rect.bottom >= p.rect.top and self.rect.bottom <= p.rect.bottom and self.ball_speed_y < 0:
                self.ball_speed_y *= -1
            #top
            elif self.rect.top <= p.rect.bottom and self.rect.top >= p.rect.top and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
    
    def update_score(self):
        #scoring
        for p in self.players:
            if self.rect.left <= 0 and p.side == 'right':
                self.reset_ball()
                p.player_score += 1
            
            elif self.rect.right >= _WINDOW_WIDTH and p.side == 'left':
                self.reset_ball()
                p.player_score += 1

class Player(Block):
    """
    Initializes Player
    """
    def __init__(self, img_path: str, x_pos: int, y_pos: int, keybindings: dict, player_speed: int = 10, player_score: int = 0):
        super().__init__(img_path, x_pos, y_pos)
        self.keybindings = keybindings
        self.player_speed = player_speed
        self.player_score = player_score

    """
    Moves the player
    """
    def move_player(self, dir: str):
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
    moves player up or down
    """
    def move_opponent(self, ball: Ball):
        if self.rect.top < ball.rect.y:
            self.move_player('down')
        else:
            self.move_player('up')

class GameManager:
    grey = (200, 200, 200)

    def __init__(self, balls: pygame.sprite.Group, players: pygame.sprite.Group, screen: pygame.display):
        self.balls = balls
        self.players = players
        self.screen = screen
    
    def run_game(self):
        
    
    def reset_ball(self):
        i

"""
main function
"""
def main():
    #initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    #main window
    screen = pygame.display.set_mode((_WINDOW_WIDTH, _WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Pong')

    #sets keybindings
    left_inputs = {'up': pygame.K_w, 'down': pygame.K_s, 'pause': pygame.K_ESCAPE}
    right_inputs = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'pause': pygame.K_ESCAPE}

    #creates ball
    ball = Ball()

    #creates sprite group of ball(s)
    balls = pygame.sprite.Group()
    balls.add(ball)

    #creates players
    left_player = Opponent('left', left_inputs)
    # left_player = Player('left', left_inputs)
    # right_player = Opponent('right', right_inputs)
    right_player = Player('right', right_inputs)

    #creates sprite group of players
    players = pygame.sprite.Group()
    players.add(left_player)
    players.add(right_player)
    
    #sets colors and fonts
    grey = (200, 200, 200)
    score_font = pygame.font.Font(None, 50)
    pause_font = pygame.font.Font(None, 150)
    background_color = pygame.Color('turquoise4')
    
    #used for pausing game
    RUNNING, PAUSE = 0, 1
    state = RUNNING
    
    #game loop
    while True:
        # start_time = time.perf_counter()
        #move players
        pressed = pygame.key.get_pressed()
        for p in players:
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

        #run the game
        if state == RUNNING:
            #draw game objects
            players.draw(screen)
            balls.draw(screen)
            pygame.draw.aaline(screen, GameManager.grey, (_WINDOW_WIDTH//2, 0), (_WINDOW_WIDTH//2, _WINDOW_HEIGHT))

            #update balls
            balls.update()

            #move and draw ball
            ball.move_ball(players)
            pygame.draw.ellipse(screen, grey, ball)

            #multiple balls
            # for ball in balls:
            #     ball.move_ball(players)
            #     pygame.draw.ellipse(screen, grey, ball)

            #draw middle line
            

            #draw players and scores
            for p in players.values():
                pygame.draw.rect(screen, grey, p.rect)
                score_text = score_font.render(f"{p.player_score}", False, 'grey67')
                if p.side == 'left':
                    screen.blit(score_text, (_WINDOW_WIDTH//2 - 120, 50))
                elif p.side == 'right':
                    screen.blit(score_text, (_WINDOW_WIDTH//2 + 120, 50))
        else:
            pause_text = pause_font.render("Game is paused", False, 'grey67')
            screen.blit(pause_text, (0, _WINDOW_HEIGHT//2))
        
        # end_time = time.perf_counter()
        # print(f"Execution Time: {end_time - start_time:0.6f}")
    
        pygame.display.flip()
        
        clock.tick(60)
        print(f"fps: {clock.get_fps()}")

if __name__ == "__main__":
    main()