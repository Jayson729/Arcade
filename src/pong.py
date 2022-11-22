"""TODO: There's a bunch of TODO's already here if you wanna look"""
import sys
import random
import pygame
from player import StaticPlayer
from settings import Settings, Colors, Fonts
from state import State

class Ball(StaticPlayer):
    """Handles all ball movements and scoring"""

    def __init__(self, x: int, y: int, img: pygame.Surface,
                move_speed: int = 15,
                color: pygame.Color = pygame.Color(0, 0, 0),
                paddles: pygame.sprite.Group = None) -> None:
        """Initializes Ball"""
        super().__init__(x, y, img, move_speed, color)
        self.movement = (self.move_speed * random.choice((-1, 1)),
            self.move_speed * random.choice((-1, 1)))
        self.paddles = paddles

    def do_movement(self) -> None:
        collision = self.get_collision()
        # https://www.geeksforgeeks.org/python-tuple-multiplication/
        self.movement = tuple(
            ele1 * ele2 for ele1, ele2 in zip(self.movement, collision)
        )

    def check_x_collision(self, players_hit):
        for p in players_hit:
            if p.side == 'left' and self.movement[0] < 0:
                return True
            if p.side == 'right' and self.movement[0] > 0:
                return True
        return False

    def check_y_collision(self, players_hit):
        if (self.rect.top <= 0
                or self.rect.bottom >= Settings.window_height):
            return True
        for p in players_hit:
            # hit bottom of player
            if (self.rect.bottom >= p.rect.top
                    and self.rect.bottom <= p.rect.bottom
                    and self.movement[1] > 0):
                return True
            # hit top of player
            if (self.rect.top <= p.rect.bottom
                    and self.rect.top >= p.rect.top
                    and self.movement[1] < 0):
                return True
        return False

    def get_collision(self):
        players_hit = pygame.sprite.spritecollide(
            self, self.paddles, False
        )
        x = -1 if self.check_x_collision(players_hit) else 1
        y = -1 if self.check_y_collision(players_hit) else 1
        return (x, y)

    def update(self) -> None:
        """Handles ball movements/collisions"""
        self.do_movement()
        self.update_score()
        super().update()

    def reset_ball(self) -> None:
        """Moves ball back to center and sends to random side"""
        self.rect.center = (Settings.window_width//2,
                            Settings.window_height//2)
        self.movement = (self.move_speed * random.choice((-1, 1)),
            self.move_speed * random.choice((-1, 1)))

    def update_score(self) -> None:
        """updates player score and resets ball to middle"""
        # scoring
        for p in self.paddles:
            if self.rect.left <= 0 and p.side == 'right':
                self.reset_ball()
                p.score += 1
            elif (self.rect.right >= Settings.window_width
                    and p.side == 'left'):
                self.reset_ball()
                p.score += 1

    # """Checks if the ball is colliding with walls or player"""
    # def check_collisions(self) -> None:
    #     # checks for bouncing off ceiling/bottom
    #     if (self.rect.top <= 0
    #             or self.rect.bottom >= Settings.window_height):
    #         self.ball_speed_y *= -1

    #     players_hit = pygame.sprite.spritecollide(
    #         self, self.players, False
    #     )

    #     # checks for collisions with players
    #     # really players_hit should have exactly one element for normal pong,
    #     # but if we ever decide to change anything this might be needed
    #     for p in players_hit:
    #         # hit side of player
    #         if p.side == 'left' and self.ball_speed_x < 0:
    #             self.ball_speed_x *= -1
    #         elif p.side == 'right' and self.ball_speed_x > 0:
    #             self.ball_speed_x *= -1

    #         # hit bottom or top of player respectively
    #         elif (self.rect.bottom >= p.rect.top
    #                 and self.rect.bottom <= p.rect.bottom
    #                 and self.ball_speed_y > 0):
    #             self.ball_speed_y *= -1
    #         elif (self.rect.top <= p.rect.bottom
    #                 and self.rect.top >= p.rect.top
    #                 and self.ball_speed_y < 0):
    #             self.ball_speed_y *= -1


class Paddle(StaticPlayer):
    """Controls all player movements"""

    def __init__(self, x: int, y: int, img: pygame.Surface, side: str,
                move_speed: int = 10,
                color: pygame.Color = pygame.Color(0, 0, 0),
                score: int = 0) -> None:
        """Initializes Player"""
        super().__init__(x, y, img, move_speed, color)
        self.score = score
        self.side = side

    def get_direction(self, balls) -> str:
        return super().get_direction()

    def do_movement(self, balls) -> None:
        movements = {
            'stop': (0, 0),
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed),
            'left': (0, 0),
            'right': (0, 0),
        }
        direction = self.get_direction(balls)
        if direction is None:
            direction = 'stop'
        self.movement = movements[direction]

    def update(self, balls) -> None:
        """Moves the player"""
        self.do_movement(balls)
        super().update()


class Opponent(Paddle):
    """AI for pong"""
    def __init__(self, x: int, y: int, img: pygame.Surface, side: str,
            move_speed: int = 10, color: pygame.Color = pygame.Color(0, 0, 0),
            score: int = 0) -> None:
        super().__init__(x, y, img, side, move_speed, color, score)

    def get_direction(self, balls) -> str:
        first_ball = balls.sprites()[0]
        if self.rect.top < first_ball.rect.y:
            return 'down'
        if self.rect.bottom > first_ball.rect.y:
            return 'up'
        return 'stop'

class Pong(State):
    def __init__(self, p1=Paddle, p2=Paddle):
        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/pong/'
        self.clock = pygame.time.Clock()
        self.screen = self.get_screen()
        pygame.display.set_caption('Pong')
        self.create_game(p1, p2)
        super().__init__()

    @staticmethod
    def get_screen() -> pygame.Surface:
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def create_game(self, p1, p2):
        self.paddles = self.get_paddles(p1, p2)
        self.balls = self.get_balls()
        self.goal_score = 10

    def get_paddles(self, p1: Paddle, p2: Paddle) -> pygame.sprite.Group:
        paddle_settings = {
            'left': {
                'type': p1,
                'color': (255, 0, 0),
                'coords': (
                    Settings.player_buffer,
                    Settings.window_height//2
                )},
            'right': {
                'type': p2,
                'color': (0, 0, 255),
                'coords': (
                    Settings.window_width - Settings.player_buffer,
                    Settings.window_height//2
                )}
        }
        paddle_img = pygame.image.load(f'{self.img_path}paddle.png')
        paddles = pygame.sprite.Group()
        for side, settings in paddle_settings.items():
            paddle = settings['type'](settings['coords'][0],
                settings['coords'][1], paddle_img,
                side, color=settings['color']
            )
            paddle.resize(20, 160)
            paddles.add(paddle)

        return paddles

    def get_balls(self, num_balls: int=1) -> pygame.sprite.Group:
        ball_img = pygame.image.load(f'{self.img_path}ball1.png')
        balls = pygame.sprite.Group()
        for i in range(num_balls):
            ball = Ball(
                Settings.window_width//2,
                Settings.window_height//2,
                ball_img, color=(255, 255, 255), paddles=self.paddles
            )
            ball.resize(40, 40)
            balls.add(ball)
        return balls

    def startup(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            # print(f"fps: {self.clock.get_fps()}")

    @staticmethod
    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_scores(self) -> None:
        for p in self.paddles:
            score_text = Fonts.score_font.render(
                f'{p.score}',
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

    def update_scores(self) -> None:
        if (win := self.check_win) is not None:
            self.win_game(win)

    def win_game(self, winner):
        p_num = 1 if winner.side == 'left' else 2
        win_text = Fonts.pause_font.render(
            f'Player {p_num} wins!', False, 'grey67'
        )
        self.screen.blit(win_text, (0, Settings.window_height//2))

    def check_win(self) -> Paddle:
        for p in self.paddles:
            if p.score >= self.goal_score:
                return p
        return None

    def draw(self) -> None:
        self.screen.fill(Colors.background_color)
        pygame.draw.aaline(
            self.screen,
            Colors.light_grey,
            (Settings.window_width//2, 0),
            (Settings.window_width//2, Settings.window_height)
        )
        self.paddles.draw(self.screen)
        self.balls.draw(self.screen)
        self.draw_scores()

    def update(self) -> None:
        if (win := self.check_win()) is not None:
            self.win_game(win)
        else:
            self.paddles.update(self.balls)
            self.balls.update()
        # self.update_scores()
        pygame.display.flip()
        self.clock.tick(Settings.fps)


    # def run_game(self) -> None:
    #     # fill background
    #     self.screen.fill(Colors.background_color)

    #     if self.state is GameManager.PAUSE:
    #         self.pause_game()
    #         return

    #     self.draw_game_objects()
    #     self.draw_scores()

    #     # I like the look of the game objects still being on
    #     # screen so this is after drawing
    #     win = self.check_win()
    #     if win is not None:
    #         self.win_game(win)
    #         return

    #     # update game objects
    #     self.players.update(self.balls)
    #     self.balls.update()



# """ Runs all parts of the game, including
# resizing, drawing objects, updating objects, etc.
# """
# class GameManager:
#     # used for pausing game
#     RUNNING, PAUSE = 0, 1

#     """Initializes GameManager"""
#     def __init__(self, balls: pygame.sprite.Group,
#                  players: pygame.sprite.Group, screen: pygame.Surface,
#                  goal_score: int = 10) -> None:
#         self.balls = balls
#         self.players = players
#         self.screen = screen
#         self.goal_score = goal_score
#         self.state = GameManager.RUNNING

#     """Deals with input"""
#     def do_input(self) -> None:
#         pressed = pygame.key.get_pressed()
#         for p in self.players:
#             if not isinstance(p, Player):
#                 print(f"{p} is not a player")
#                 break
#             for e in pygame.event.get():
#                 if e.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 if e.type == pygame.VIDEORESIZE:
#                     self.resize_game(e)
#                 if e.type == pygame.KEYDOWN:
#                     if e.key == p.keybindings['pause']:
#                         self.state = (self.state + 1) % 2
#             if isinstance(p, Opponent):
#                 p.move_opponent(self.balls)
#                 continue
#             if self.state == GameManager.RUNNING:
#                 if pressed[p.keybindings['up']]:
#                     p.move_player('up')
#                 elif pressed[p.keybindings['down']]:
#                     p.move_player('down')
#                 else:
#                     p.move_player('stop')

#     """Draws all game objects"""
#     def draw_game_objects(self) -> None:
#         pygame.draw.aaline(
#             self.screen,
#             Colors.light_grey,
#             (Settings.window_width//2, 0),
#             (Settings.window_width//2, Settings.window_height)
#         )
#         self.players.draw(self.screen)
#         self.balls.draw(self.screen)

#     """Draws scores"""
#     def draw_scores(self) -> None:
#         for p in self.players:
#             score_text = Fonts.score_font.render(
#                 f'{p.player_score}',
#                 False,
#                 'grey67'
#             )
#             if p.side == 'left':
#                 self.screen.blit(
#                     score_text,
#                     (Settings.window_width//2 - 120, 50)
#                 )
#             elif p.side == 'right':
#                 self.screen.blit(
#                     score_text,
#                     (Settings.window_width//2 + 120, 50)
#                 )

#     """Returns player that won or None if no winner"""
#     def check_win(self) -> Player:
#         for p in self.players:
#             if p.player_score >= self.goal_score:
#                 return p
#         return None

#     # TODO: timer after scoring
#     """Main method that runs the game"""
#     def run_game(self) -> None:
#         # fill background
#         self.screen.fill(Colors.background_color)

#         if self.state is GameManager.PAUSE:
#             self.pause_game()
#             return

#         self.draw_game_objects()
#         self.draw_scores()

#         # I like the look of the game objects still being on
#         # screen so this is after drawing
#         win = self.check_win()
#         if win is not None:
#             self.win_game(win)
#             return

#         # update game objects
#         self.players.update(self.balls)
#         self.balls.update()

#     # TODO: Make a better pause screen
#     #       quit to main menu, play again, change keybinds, etc.
#     """Deals with pausing the game"""
#     def pause_game(self) -> None:
#         pause_text = Fonts.pause_font.render(
#             "Game is paused", False, 'grey67'
#         )
#         self.screen.blit(pause_text, (0, Settings.window_height//2))

#     # TODO: - Make a better win screen with the ability
#     #         to play again or quit after game is done
#     #       - play again should take allow you to
#     #         choose between player and AI
#     """Deals with a player winning"""
#     def win_game(self, player: Player) -> None:
#         p_num = 1 if player.side == 'left' else 2
#         win_text = Fonts.pause_font.render(
#             f'Player {p_num} wins!', False, 'grey67'
#         )
#         self.screen.blit(win_text, (0, Settings.window_height//2))

#     # TODO: - nothing scales completely right because of rounding errors
#     #         (things get smaller over time)
#     #         maybe store original width?
#     #       - add black bars to the side so that window
#     #         isn't restricted to 4:3
#     #       - scale font size/location
#     """ Deals with resizing the game, scales all objects
#     based on how much the screen was resized by
#     Also changes Settings class based on new sizes
#     """
#     def resize_game(self, event: pygame.event.Event) -> None:
#         if event.type != pygame.VIDEORESIZE:
#             return

#         ratio = event.w / Settings.window_width
#         for o in self.players.sprites() + self.balls.sprites():
#             new_width = o.image.get_width() * ratio
#             new_height = o.image.get_height() * ratio
#             o.resize(new_width, new_height)
#             o.rect.center = tuple(x * ratio for x in o.rect.center)

#         for p in self.players:
#             p.player_speed = p.player_speed * ratio

#         for b in self.balls:
#             b.ball_speed_x = b.ball_speed_x * ratio
#             b.ball_speed_y = b.ball_speed_y * ratio

#         # resize screen
#         # this only works for adjusting horizontally
#         Settings.window_width = event.w
#         Settings.window_height = event.w / Settings.aspect_ratio

#         self.screen = pygame.display.set_mode(
#             (Settings.window_width, Settings.window_height),
#             pygame.RESIZABLE
#         )


# """main class that calls everything else"""
# class Pong:
#     def __init__(self, p1=None, p2=None):
#         # initialize pygame
#         pygame.init()
#         self.clock = pygame.time.Clock()
#         self.img_path = 'images/pong/'
#         screen = self.create_screen()
#         pygame.display.set_caption('Pong')

#         players = self.create_players(p1, p2)
#         balls = self.create_balls(players)

#         # creates game_manager
#         self.game_manager = GameManager(balls, players, screen)

#     def create_screen(self) -> pygame.Surface:
#         screen = pygame.display.set_mode(
#             (Settings.window_width, Settings.window_height),
#             pygame.RESIZABLE
#         )
#         return screen

#     def create_players(self, p1=Player,
#             p2=Player) -> pygame.sprite.Group:
#         p1 = p1 if p1 is not None else Player
#         p2 = p2 if p2 is not None else Player
#         p_sides = ['left', 'right']
#         inputs = {
#             p_sides[0]: {
#                 'up': pygame.K_w,
#                 'down': pygame.K_s,
#                 'pause': pygame.K_ESCAPE
#             },
#             p_sides[1]: {
#                 'up': pygame.K_UP,
#                 'down': pygame.K_DOWN,
#                 'pause': pygame.K_ESCAPE
#             }
#         }
#         p_types = {p_sides[0]: p1, p_sides[1]: p2}
#         p_colors = {
#             p_sides[0]: (255, 0, 0),
#             p_sides[1]: (0, 0, 255)
#         }
#         p_coords = {
#             p_sides[0]: (
#                 Settings.player_buffer,
#                 Settings.window_height//2
#             ),
#             p_sides[1]: (
#                 Settings.window_width - Settings.player_buffer,
#                 Settings.window_height//2
#             )
#         }
#         players = pygame.sprite.Group()
#         paddle_img = pygame.image.load(f'{self.img_path}paddle.png')
#         for side in p_sides:
#             player = p_types[side](
#                 paddle_img,
#                 p_coords[side][0],
#                 p_coords[side][1],
#                 inputs[side], side,
#                 color=p_colors[side]
#             )
#             player.resize(20, 160)
#             players.add(player)
#         return players

#     def create_balls(self, players: pygame.sprite.Group,
#             colors: list=None, coords: list=None,
#             num_balls: int=1) -> pygame.sprite.Group:
#         colors = [(255, 255, 255)] if colors is None else colors
#         coords = [
#             (Settings.window_width//2, Settings.window_height//2)
#         ] if coords is None else coords

#         num_colors = len(colors)
#         num_coords = len(coords)
#         ball_img = pygame.image.load(f'{self.img_path}ball1.png')
#         balls = pygame.sprite.Group()
#         for b in range(num_balls):
#             ball = Ball(
#                 ball_img,
#                 coords[b % num_coords][0],
#                 coords[b % num_coords][1],
#                 players, color=colors[b % num_colors]
#             )
#             ball.resize(40, 40)
#             balls.add(ball)
#         return balls

#     def startup(self):
#         while True:
#             self.game_manager.do_input()
#             self.game_manager.run_game()

#             pygame.display.flip()

#             self.clock.tick(Settings.fps)
#             print(f"fps: {self.clock.get_fps()}")


def main():
    """main function"""
    pong = Pong(Opponent, Paddle)
    pong.startup()


if __name__ == "__main__":
    main()
