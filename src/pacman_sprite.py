"""TODO: Fix collision with window borders (hitbox is wonky)
Make movements fixed to a grid (move like normal pacman)
Switch to pacman death when you touch a ghost
(check for collisions with ghosts, switching animation done in animated_sprite.py)
"""

from player import AnimatedPlayer
class PacmanSprite(AnimatedPlayer):
    def __init__(self, x: int, y: int,
            base_path: str, death_path: str,
            move_speed: float=2.0, animation_speed: float=100,
            color=None) -> None:
        super().__init__(x, y, base_path, move_speed, animation_speed, color=color)
        self.add_animation('death', death_path, animation_speed*.3)

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
            if direction == 'right':
                self.movement = (0, 0)
                self.set_animation('death')
                return
            self.set_animation('base')
            self.movement = movements[direction][0]
            self.rotate(movements[direction][1])

    # move parts
    def update(self):
        self.do_movement()
        super().update()
