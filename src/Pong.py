import cProfile
import pygame, sys, random
import time

class settings:
    fps = 60
    aspect_ratio = 4/3
    window_width = 800
    window_height = 600
    player_buffer = 40

class fonts:
    pygame.font.init()
    score_font = pygame.font.Font(None, 50)
    pause_font = pygame.font.Font(None, 150)

class colors:
    background_color = pygame.Color('turquoise4')
    light_grey = (200, 200, 200)

class Block(pygame.sprite.Sprite):
    def __init__(self, img_path: str, color: pygame.Color, x_pos: int, y_pos: int):
        pygame.sprite.Sprite.__init__(self)
        # super().__init__()
        self.orig_image = pygame.image.load(img_path)
        self.orig_width = self.orig_image.get_width()
        self.orig_height = self.orig_image.get_height()
        
        self.image = self.orig_image
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.color = color

        color_image = pygame.Surface(self.image.get_size()).convert_alpha()
        color_image.fill(color)
        self.image.blit(color_image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
    
    def resize(self, new_width: int, new_height: int):
        #scales image
        self.image = pygame.transform.scale(self.orig_image, (new_width, new_height))

        #scales rect with center at old rect center
        self.rect = self.image.get_rect(center = self.rect.center)

        #honestly not sure if this is needed
        color_image = pygame.Surface(self.image.get_size()).convert_alpha()
        color_image.fill(self.color)
        self.image.blit(color_image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

class Ball(Block):
    """
    Initializes Ball
    """
    def __init__(self, img_path: str, x_pos: int, y_pos: int, players: pygame.sprite.Group = None, ball_speed_x: int = 15, ball_speed_y: int = 15, color: pygame.Color = pygame.Color(0, 0, 0)):
        super().__init__(img_path, color, x_pos, y_pos)
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
        self.rect.center = settings.window_width//2, settings.window_height//2
        self.ball_speed_y *= random.choice((1, -1))
        self.ball_speed_x *= random.choice((1, -1))

    def check_collisions(self):
        #checks for bouncing off ceiling/bottom
        if self.rect.top <= 0 or self.rect.bottom >= settings.window_height:
            self.ball_speed_y *= -1

        players_hit = pygame.sprite.spritecollide(self, self.players, False)

        #checks for collisions with players
        """
        really players_hit should have exactly one element for normal pong, 
        but if we ever decide to change anything this might be needed
        """
        for p in players_hit:
            #hit side of player
            if p.side == 'left' and self.ball_speed_x < 0:
                self.ball_speed_x *= -1
            elif p.side == 'right' and self.ball_speed_x > 0:
                self.ball_speed_x *= -1
            
            # hit top or bottom of player
            # these don't work
            # bottom
            elif self.rect.bottom >= p.rect.top and self.rect.bottom <= p.rect.bottom and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            # top
            elif self.rect.top <= p.rect.bottom and self.rect.top >= p.rect.top and self.ball_speed_y < 0:
                self.ball_speed_y *= -1
    
    def update_score(self):
        #scoring
        for p in self.players:
            if self.rect.left <= 0 and p.side == 'right':
                self.reset_ball()
                p.player_score += 1
            
            elif self.rect.right >= settings.window_width and p.side == 'left':
                self.reset_ball()
                p.player_score += 1

class Player(Block):
    """
    Initializes Player
    """
    def __init__(self, img_path: str, x_pos: int, y_pos: int, keybindings: dict, side: str, player_speed: int = 10, player_score: int = 0, color: pygame.Color = pygame.Color(0, 0, 0)):
        super().__init__(img_path, color, x_pos, y_pos)
        self.keybindings = keybindings
        self.player_speed = player_speed
        self.player_score = player_score
        self.movement = 0
        self.side = side

    """
    Sets movement value of player
    """
    def move_player(self, dir: str):
        if dir == 'stop':
            self.movement = 0
        elif dir == 'up':
            self.movement = -self.player_speed
        else:
            self.movement = self.player_speed

    """
    Moves the player
    """
    def update(self, balls):
        self.rect.y += self.movement
        self.check_collision()
    
    """
    Checks if the player is colliding with ceiling or floor
    """
    def check_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= settings.window_height:
            self.rect.bottom = settings.window_height

"""
AI for pong
"""
class Opponent(Player):
    """
    moves player up or down
    """
    def move_opponent(self, balls: pygame.sprite.Group):
        if len(balls) == 0:
            print('Balls is empty')
            return
        first_ball = balls.sprites()[0]
        if self.rect.top < first_ball.rect.y:
            self.move_player('down')
        elif self.rect.bottom > first_ball.rect.y:
            self.move_player('up')
        else:
            self.move_player('stop')

class Game_Manager:
    #used for pausing game
    RUNNING, PAUSE = 0, 1

    def __init__(self, balls: pygame.sprite.Group, players: pygame.sprite.Group, screen: pygame.display, goal_score: int = 10):
        self.balls = balls
        self.players = players
        self.screen = screen
        self.goal_score = goal_score
        self.state = Game_Manager.RUNNING

    def do_input(self):
        pressed = pygame.key.get_pressed()
        for p in self.players:
            if not isinstance(p, Player): print(f"{p} is not a player"); break
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.VIDEORESIZE:
                    self.resize_game(e)
                if e.type == pygame.KEYDOWN:
                    if e.key == p.keybindings['pause']: self.state = (self.state + 1) % 2
            if isinstance(p, Opponent): p.move_opponent(self.balls); continue
            if self.state == Game_Manager.RUNNING:
                if pressed[p.keybindings['up']]: p.move_player('up')
                elif pressed[p.keybindings['down']]: p.move_player('down')
                else: p.move_player('stop')

    def draw_game_objects(self):
        pygame.draw.aaline(self.screen, colors.light_grey, (settings.window_width//2, 0), (settings.window_width//2, settings.window_height))
        self.players.draw(self.screen)
        self.balls.draw(self.screen)

    def draw_scores(self):
        for p in self.players:
            score_text = fonts.score_font.render(f"{p.player_score}", False, 'grey67')
            if p.side == 'left':
                self.screen.blit(score_text, (settings.window_width//2 - 120, 50))
            elif p.side == 'right':
                self.screen.blit(score_text, (settings.window_width//2 + 120, 50))

    def check_win(self) -> Player:
        for p in self.players:
            if p.player_score >= self.goal_score:
                return p
        return None

    """
    TODO: timer after scoring
    """
    def run_game(self):
        #fill background
        self.screen.fill(colors.background_color)

        if self.state is Game_Manager.PAUSE:
            self.pause_game()
            return

        self.draw_game_objects()
        self.draw_scores()

        #I like the look of the game objects still being on screen so this is after drawing
        win = self.check_win()
        if win is not None:
            self.win_game(win)
            return

        #update game objects
        self.players.update(self.balls)
        self.balls.update()

    """
    TODO: Make a better pause screen
          quit to main menu, play again, change keybinds, etc.
    """
    def pause_game(self):
        pause_text = fonts.pause_font.render("Game is paused", False, 'grey67')
        self.screen.blit(pause_text, (0, settings.window_height//2))

    """
    TODO: Make a better win screen
          ability to play again or quit after game is done
          play again should take allow you to choose between player and AI
    """
    def win_game(self, player: Player):
        p_num = 1 if player.side == 'left' else 2
        win_text = fonts.pause_font.render(f'Player {p_num} wins!', False, 'grey67')
        self.screen.blit(win_text, (0, settings.window_height//2))
        # self.end_game()

    # def end_game(self):
    #     pass

    """
    TODO: nothing scales completely right because of rounding errors (things get smaller over time)
          maybe store original width?
          add black bars to the side so that window isn't restricted to 4:3 (also fullscreen later)
          scale font size/location
    """
    def resize_game(self, event: pygame.event):
        if event.type != pygame.VIDEORESIZE:
            return

        ratio = event.w / settings.window_width
        for o in self.players.sprites() + self.balls.sprites():
            new_width = o.image.get_width() * ratio
            new_height = o.image.get_height() * ratio
            o.resize(new_width, new_height)
            o.rect.center = tuple(x * ratio for x in o.rect.center)

        for p in self.players:
            p.player_speed = p.player_speed * ratio
        
        for b in self.balls:
            b.ball_speed_x = b.ball_speed_x * ratio
            b.ball_speed_y = b.ball_speed_y * ratio

        #resize screen
        #this only works for adjusting horizontally
        settings.window_width = event.w
        settings.window_height = event.w / settings.aspect_ratio
        
        self.screen = pygame.display.set_mode((settings.window_width, settings.window_height), pygame.RESIZABLE)
        
"""
main function
"""
def main():
    #initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    #main window
    screen = pygame.display.set_mode((settings.window_width, settings.window_height), pygame.RESIZABLE)
    pygame.display.set_caption('Pong')

    #sets keybindings
    left_inputs = {'up': pygame.K_w, 'down': pygame.K_s, 'pause': pygame.K_ESCAPE}
    right_inputs = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'pause': pygame.K_ESCAPE}

    #creates players
    paddle_img_path = 'images/paddle.png'
    left_player = Opponent(paddle_img_path, settings.player_buffer, settings.window_height//2, left_inputs, 'left', color=pygame.Color(255, 0, 0))
    # left_player = Player('left', left_inputs)
    # right_player = Opponent('right', right_inputs)
    right_player = Player(paddle_img_path, settings.window_width - settings.player_buffer, settings.window_height//2, right_inputs, 'right', color=pygame.Color(0, 0, 255))

    #creates sprite group of players
    players = pygame.sprite.Group()
    players.add(left_player)
    players.add(right_player)

    #resize players
    for p in players:
        p.resize(20, 160)

    #creates ball
    ball_img_path = 'images/ball1.png'
    ball1 = Ball(ball_img_path, settings.window_width//2, settings.window_height//2 - 100, players, color=pygame.Color(255, 255, 255))
    # ball2 = Ball(ball_img_path, settings.window_width//2, settings.window_height//2 + 100, players, color=pygame.Color(255, 255, 255))

    #creates sprite group of ball(s)
    balls = pygame.sprite.Group()
    balls.add(ball1)
    # balls.add(ball2)

    #resize balls
    for b in balls:
        b.resize(40, 40)
    
    #creates game_manger
    game_manager = Game_Manager(balls, players, screen)

    #game loop
    while True:
        game_manager.do_input()
        game_manager.run_game()

        pygame.display.flip()
        
        clock.tick(settings.fps)
        # print(f"fps: {clock.get_fps()}")

if __name__ == "__main__":
    main()