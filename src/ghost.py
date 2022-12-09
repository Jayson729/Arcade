"""TODO: ghosts need to look in the direction they're moving
They need some kind of AI/pathfinding algorithm (probably BFS)
They'll all have the same algo, but they should ignore
tiles that have a ghost on them so that they naturally
go in different directions toward the player
"""
import random
from player import AnimatedPlayer
from settings import Settings


class Ghost(AnimatedPlayer):
    def __init__(self, x: int, y: int,
                 base_path: str, scared_blue_path='images/pacman/scared_ghost_blue/',
                 scared_white_path='images/pacman/scared_ghost_white/',
                 move_speed: float = 2.0, animation_speed: float = 150,
                 color=None) -> None:
        # first, calls super with all animations and sets instance variables
        super().__init__(x, y, base_path, move_speed, animation_speed, color)
        self.split_add_animations()
        self.add_animation('scared_blue', scared_blue_path, animation_speed)
        self.add_animation('scared_white', scared_white_path, animation_speed)
        self.scared = False
        self.scared_timer = 0
        self.current_direction = 'left'

        # this is only for random movements
        # get rid of this later
        self.temp_timer = 0

    def split_add_animations(self):
        right, down, left, up = self.split_animations('base', num_animations=4)
        self.add_animation_w_images('right', right)
        self.add_animation_w_images('down', down)
        self.add_animation_w_images('left', left)
        self.add_animation_w_images('up', up)
    
    def check_out_of_bounds(self):
        # use 1 because 0 can make clipping at the edge possible
        if self.rect.centerx < 1:
            self.rect.centerx = Settings.window_width
        elif self.rect.centerx >= Settings.window_width:
            self.rect.centerx = 1
        elif self.rect.centery < 1:
            self.rect.centery = Settings.window_height
        elif self.rect.centery >= Settings.window_height:
            self.rect.centery = 1

    def do_movement(self, game_map) -> None:
        if self.scared:
            self.do_scared()
            return
        movements = {
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed),
            'left': (-self.move_speed, 0),
            'right': (self.move_speed, 0),
        }
        if self.wall_in_direction(self.current_direction, game_map, movements[self.current_direction]):
            self.movement = (0, 0)
        
        direction = self.get_direction(movements)
        if self.wall_in_direction(direction, game_map, movements[direction]):
            return
        self.current_direction = direction
        self.movement = movements[direction]
        self.set_animation(direction)

    def get_direction(self, movements):
        # for now, random movements
        # in the future, I want to implement BFS toward pacman
        direction = self.current_direction if self.current_direction is not None else random.choice(list(movements.keys()))
        self.temp_timer += 1
        if self.temp_timer >= 25:
            direction = random.choice(list(movements.keys()))
            self.temp_timer = 0

        return direction
    
    def wall_in_direction(self, direction, game_map, movements):
        x, y = movements
        if direction == 'up':
            return game_map.is_wall((self.rect.left + 2, self.rect.top + y)) or game_map.is_wall((self.rect.right - 2, self.rect.top + y))
        elif direction == 'down':
            return game_map.is_wall((self.rect.left + 2, self.rect.bottom + y)) or game_map.is_wall((self.rect.right - 2, self.rect.bottom + y))
        elif direction == 'left':
            return game_map.is_wall((self.rect.left + x, self.rect.top + 2)) or game_map.is_wall((self.rect.left + x, self.rect.bottom - 2))
        elif direction == 'right':
            return game_map.is_wall((self.rect.right + x, self.rect.top + 2)) or game_map.is_wall((self.rect.right + x, self.rect.bottom - 2))

    def update(self, game_map):
        self.do_movement(game_map)
        super().update()

    def do_scared(self):
        self.do_scared_movement()
        self.scared_timer += 1
        if self.scared_timer < 150:
            self.set_animation('scared_blue')
        elif self.scared_timer < 250:
            self.set_animation('scared_white')
        else:
            self.scared = False
            self.scared_timer = 0

    def do_scared_movement(self):
        pass
