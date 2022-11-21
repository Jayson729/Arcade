"""TODO: ghosts need to look in the direction they're moving
They need some kind of AI/pathfinding algorithm (probably BFS)
They'll all have the same algo, but they should ignore
tiles that have a ghost on them so that they naturally
go in different directions toward the player
"""
from player import AnimatedPlayer
import random
class Ghost(AnimatedPlayer):
    def __init__(self, x: int, y: int, 
            base_path: str, 
            move_speed: float=2.0, animation_speed: float=150,
            color=None) -> None:
        # first, calls super with all animations and sets instance variables
        super().__init__(x, y, base_path, move_speed, animation_speed, color)
        self.split_add_animations()
        
        # this is only for random movements
        # get rid of this later
        self.temp_timer = 0

    def split_add_animations(self):
        right, down, left, up = self.split_animations('base', num_animations=4)
        self.add_animation_w_images('right', right)
        self.add_animation_w_images('down', down)
        self.add_animation_w_images('left', left)
        self.add_animation_w_images('up', up)

    def do_movement(self) -> None:
        movements = {
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed),
            'left': (-self.move_speed, 0),
            'right': (self.move_speed, 0),
        }
        dir = self.get_direction(movements)
        self.movement = movements[dir]
        self.set_animation(dir)
    
    def get_direction(self, movements):
        # for now, random movements
        # in the future, I want to implement DFS toward pacman
        dir = self.current_animation if self.current_animation != 'base' else random.choice(list(movements.keys()))
        self.temp_timer += 1
        if self.temp_timer >= 25:
            dir = random.choice(list(movements.keys()))
            self.temp_timer = 0
        
        return dir
    
    def update(self):
        self.do_movement()
        super().update()