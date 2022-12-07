"""TODO: Fix collision with window borders (hitbox is wonky)
Make movements fixed to a grid (move like normal pacman)
Switch to pacman death when you touch a ghost
(check for collisions with ghosts, switching animation done in animated_sprite.py)
"""

from player import AnimatedPlayer
# from map import Map


class PacmanSprite(AnimatedPlayer):
    def __init__(self, x: int, y: int,
                 base_path: str, death_path: str,
                 move_speed: float = 2.0, animation_speed: float = 100,
                 color=None) -> None:
        super().__init__(x, y, base_path, move_speed, animation_speed, color=color)
        self.add_animation('death', death_path, animation_speed*2)

    # def get_direction(self):
    #     current_direction = super().get_direction()
    #     if self.is_wall(current_direction):
    #         return None
    #     return current_direction
    
    # def is_wall(self, current_direction, map):
    #     x, y = map.game_objects['pacman'][0]
    #     if current_direction == 'left':
    #         if not (x-1, y) in map.game_objects['walls']:
    #             return True
    #     elif current_direction == 'right':
    #         if not (x+1, y) in map.game_objects['walls']:
    #             return True
    #     elif current_direction == 'up':
    #         if not (x, y-1) in map.game_objects['walls']:
    #             return True
    #     elif current_direction == 'down':
    #         if not (x, y+1) in map.game_objects['walls']:
    #             return True
    #     return False

    # good I think
    def do_movement(self) -> None:
        # movement, rotation
        # x, y, '-' is up/left
        # rotation in degrees from facing right
        # counter-clockwise in degrees
        movements = {
            'up': [(0, -self.move_speed), 90],
            'down': [(0, self.move_speed), 270],
            'left': [(-self.move_speed, 0), 180],
            'right': [(self.move_speed, 0), 0]
        }

        # find direction based on keys pressed
        # sets movement and rotates pacman
        if (direction := self.get_direction()) is not None:
            self.set_animation('base')
            self.rotate(movements[direction][1])
            self.movement = movements[direction][0]
    
    # def check_is_wall(self, map):
    #     new_movement_x = 0
    #     new_movement_y = 0
    #     x, y = self.movement
    #     if not map.is_wall((self.rect.centerx + x, self.rect.centery)):
    #         new_movement_x = x
    #     elif not map.is_wall((self.rect.centerx, self.rect.centery + y)):
    #         new_movement_y = y
    #     self.movement = (new_movement_x, new_movement_y)

    # move parts
    def update(self, map):
        self.old_movement = self.movement
        self.do_movement()
        # self.check_is_wall(map)
        if map.is_wall((self.rect.centerx + self.movement[0], self.rect.centery + self.movement[1])):
            self.movement = (0, 0)
        super().update()
        if map.is_pacman_in_ghost():
            self.set_animation('death')
            self.movement = (0, 0)
            self.allow_player_movement = False
        
        # if map.is_pacman_in_wall():
        #     self.movement = self.old_movement
        #     super().update()
