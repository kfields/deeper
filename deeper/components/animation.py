from enum import Enum

from .. import Component

class AnimationDirection(Enum):
    FORWARD = 0
    REVERSE = 1

class Animation(Component):
    def __init__(self) -> None:
        super().__init__()
        self.animation_direction = AnimationDirection.FORWARD