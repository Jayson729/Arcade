import cProfile
import pygame
import sys
import random
import time
import os
import Block


"""Stores settings for Pong"""
class Settings:
    fps = 60
    aspect_ratio = 4/3
    window_width = 800
    window_height = 600
    player_buffer = 40


"""Stores fonts for Pong"""
class Fonts:
    pygame.font.init()
    score_font = pygame.font.Font(None, 50)
    pause_font = pygame.font.Font(None, 150)


"""Stores colors for Pong"""
class Colors:
    background_color = pygame.Color('turquoise4')
    light_grey = (200, 200, 200)


"""Handles all ball movements and scoring"""
class Ball(Block):

    """Initializes Ball"""
    def __init__(self, img_path: str, x_pos: int, y_pos: int,
                 players: pygame.sprite.Group = None,
                 ball_speed_x: int = 15, ball_speed_y: int = 15,
                 color: pygame.Color = pygame.Color(0, 0, 0)) -> None:
        super().__init__(img_path, x_pos, y_pos, color)
        self.ball_speed_x = ball_speed_x * random.choice((1, -1))
        self.ball_speed_y = ball_speed_y * random.choice((1, -1))
        self.players = players

    """Handles ball movements/collisions"""
    def update(self) -> None:
        self.rect.x += self.ball_speed_x
        self.rect.y += self.ball_speed_y
        self.check_collisions()
        self.update_score()

    """Moves ball back to center and sends to random side"""
    def reset_ball(self) -> None:
        self.rect.center = (Settings.window_width//2,
                            Settings.window_height//2)
        self.ball_speed_y *= random.choice((1, -1))
        self.ball_speed_x *= random.choice((1, -1))

    """Checks if the ball is colliding with walls or player"""
    def check_collisions(self) -> None:
        # checks for bouncing off ceiling/bottom
        if (self.rect.top <= 0
                or self.rect.bottom >= Settings.window_height):
            self.ball_speed_y *= -1

        players_hit = pygame.sprite.spritecollide(
            self, self.players, False
        )

        # checks for collisions with players
        # really players_hit should have exactly one element for normal pong, 
        # but if we ever decide to change anything this might be needed
        for p in players_hit:
            # hit side of player
            if p.side == 'left' and self.ball_speed_x < 0:
                self.ball_speed_x *= -1
            elif p.side == 'right' and self.ball_speed_x > 0:
                self.ball_speed_x *= -1

            # hit bottom or top of player respectively
            elif (self.rect.bottom >= p.rect.top
                    and self.rect.bottom <= p.rect.bottom
                    and self.ball_speed_y > 0):
                self.ball_speed_y *= -1
            elif (self.rect.top <= p.rect.bottom
                    and self.rect.top >= p.rect.top
                    and self.ball_speed_y < 0):
                self.ball_speed_y *= -1

    """updates player score and resets ball to middle"""
    def update_score(self) -> None:
        # scoring
        for p in self.players:
            if self.rect.left <= 0 and p.side == 'right':
                self.reset_ball()
                p.player_score += 1

            elif (self.rect.right >= Settings.window_width
                    and p.side == 'left'):
                self.reset_ball()
                p.player_score += 1


"""Controls all player movements"""
class Player(Block):

    """Initializes Player"""
    def __init__(self, img_path: str, x_pos: int, y_pos: int,
                 keybindings: dict, side: str, player_speed: int = 10,
                 player_score: int = 0,
                 color: pygame.Color = pygame.Color(0, 0, 0)) -> None:
        super().__init__(img_path, x_pos, y_pos, color)
        self.keybindings = keybindings
        self.player_speed = player_speed
        self.player_score = player_score
        self.movement = 0
        self.side = side

    """Sets movement value of player"""
    def move_player(self, dir: str) -> None:
        if dir == 'stop':
            self.movement = 0
        elif dir == 'up':
            self.movement = -self.player_speed
        else:
            self.movement = self.player_speed

    """Moves the player"""
    def update(self, balls) -> None:
        self.rect.y += self.movement
        self.check_collision()

    """Checks if the player is colliding with ceiling or floor """
    def check_collision(self) -> None:
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= Settings.window_height:
            self.rect.bottom = Settings.window_height


"""AI for pong"""
class Opponent(Player):

    """Moves player up or down"""
    def move_opponent(self, balls: pygame.sprite.Group) -> None:
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


""" Runs all parts of the game, including
resizing, drawing objects, updating objects, etc.
"""
class GameManager:
    # used for pausing game
    RUNNING, PAUSE = 0, 1

    """Initializes GameManager"""
    def __init__(self, balls: pygame.sprite.Group,
                 players: pygame.sprite.Group, screen: pygame.Surface,
                 goal_score: int = 10) -> None:
        self.balls = balls
        self.players = players
        self.screen = screen
        self.goal_score = goal_score
        self.state = GameManager.RUNNING

    """Deals with input"""
    def do_input(self) -> None:
        pressed = pygame.key.get_pressed()
        for p in self.players:
            if not isinstance(p, Player):
                print(f"{p} is not a player")
                break
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.VIDEORESIZE:
                    self.resize_game(e)
                if e.type == pygame.KEYDOWN:
                    if e.key == p.keybindings['pause']:
                        self.state = (self.state + 1) % 2
            if isinstance(p, Opponent):
                p.move_opponent(self.balls)
                continue
            if self.state == GameManager.RUNNING:
                if pressed[p.keybindings['up']]:
                    p.move_player('up')
                elif pressed[p.keybindings['down']]:
                    p.move_player('down')
                else:
                    p.move_player('stop')

    """Draws all game objects"""
    def draw_game_objects(self) -> None:
        pygame.draw.aaline(
            self.screen,
            Colors.light_grey,
            (Settings.window_width//2, 0),
            (Settings.window_width//2, Settings.window_height)
        )
        self.players.draw(self.screen)
        self.balls.draw(self.screen)

    """Draws scores"""
    def draw_scores(self) -> None:
        for p in self.players:
            score_text = Fonts.score_font.render(
                f'{p.player_score}',
                False,
                'grey67'
            )
            if p.side == 'left':
                self.screen.blit(
                    score_text,
                    (Settings.window_width//2 - 120, 50)
                )
            elif p.side == 'right':
                self.screen.blit(
                    score_text,
                    (Settings.window_width//2 + 120, 50)
                )

    """Returns player that won or None if no winner"""
    def check_win(self) -> Player:
        for p in self.players:
            if p.player_score >= self.goal_score:
                return p
        return None

    # TODO: timer after scoring
    """Main method that runs the game"""
    def run_game(self) -> None:
        # fill background
        self.screen.fill(Colors.background_color)

        if self.state is GameManager.PAUSE:
            self.pause_game()
            return

        self.draw_game_objects()
        self.draw_scores()

        # I like the look of the game objects still being on
        # screen so this is after drawing
        win = self.check_win()
        if win is not None:
            self.win_game(win)
            return

        # update game objects
        self.players.update(self.balls)
        self.balls.update()

    # TODO: Make a better pause screen
    #       quit to main menu, play again, change keybinds, etc.
    """Deals with pausing the game"""
    def pause_game(self) -> None:
        pause_text = Fonts.pause_font.render(
            "Game is paused", False, 'grey67'
        )
        self.screen.blit(pause_text, (0, Settings.window_height//2))

    # TODO: - Make a better win screen with the ability
    #         to play again or quit after game is done
    #       - play again should take allow you to 
    #         choose between player and AI
    """Deals with a player winning"""
    def win_game(self, player: Player) -> None:
        p_num = 1 if player.side == 'left' else 2
        win_text = Fonts.pause_font.render(
            f'Player {p_num} wins!', False, 'grey67'
        )
        self.screen.blit(win_text, (0, Settings.window_height//2))

    # TODO: - nothing scales completely right because of rounding errors 
    #         (things get smaller over time)
    #         maybe store original width?
    #       - add black bars to the side so that window 
    #         isn't restricted to 4:3 
    #       - scale font size/location
    """ Deals with resizing the game, scales all objects
    based on how much the screen was resized by
    Also changes Settings class based on new sizes
    """
    def resize_game(self, event: pygame.event.Event) -> None:
        if event.type != pygame.VIDEORESIZE:
            return

        ratio = event.w / Settings.window_width
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

        # resize screen
        # this only works for adjusting horizontally
        Settings.window_width = event.w
        Settings.window_height = event.w / Settings.aspect_ratio

        self.screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )


"""main function"""
def main():
    # initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # main window
    screen = pygame.display.set_mode(
        (Settings.window_width, Settings.window_height),
        pygame.RESIZABLE
    )
    pygame.display.set_caption('Pong')

    # sets keybindings
    left_inputs = {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'pause': pygame.K_ESCAPE
    }

    right_inputs = {
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'pause': pygame.K_ESCAPE
    }

    # creates players
    paddle_img_path = 'images/paddle.png'
    left_player = Opponent(
        paddle_img_path,
        Settings.player_buffer,
        Settings.window_height//2,
        left_inputs, 'left',
        color=pygame.Color(255, 0, 0)
    )

    right_player = Player(
        paddle_img_path,
        Settings.window_width - Settings.player_buffer,
        Settings.window_height//2,
        right_inputs, 'right',
        color=pygame.Color(0, 0, 255)
    )

    # creates sprite group of players
    players = pygame.sprite.Group()
    players.add(left_player)
    players.add(right_player)

    # resize players
    for p in players:
        p.resize(20, 160)

    # creates ball
    ball_img_path = 'images/ball1.png'
    ball1 = Ball(
        ball_img_path,
        Settings.window_width//2,
        Settings.window_height//2 - 100,
        players, color=pygame.Color(255, 255, 255)
    )

    # ball2 = Ball(ball_img_path,
    # Settings.window_width//2,
    # Settings.window_height//2 + 100,
    # players,
    # color=pygame.Color(255, 255, 255)
    # )

    # creates sprite group of ball(s)
    balls = pygame.sprite.Group()
    balls.add(ball1)
    # balls.add(ball2)

    # resize balls
    for b in balls:
        b.resize(40, 40)

    # creates game_manger
    game_manager = GameManager(balls, players, screen)

    # game loop
    while True:
        game_manager.do_input()
        game_manager.run_game()

        pygame.display.flip()

        clock.tick(Settings.fps)
        print(f"fps: {clock.get_fps()}")


if __name__ == "__main__":
    main()
