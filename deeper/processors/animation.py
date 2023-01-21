from loguru import logger

import arcade

from ..constants import *
from deeper import Block
from deeper.components.sprite_animation import SpriteAnimation
from . import Processor

class AnimationProcessor(Processor):
    def __init__(self, scene=None) -> None:
        super().__init__()
        self.scene = scene

    def process(self, delta_time: float):
        for ent, (animation, ) in self.world.get_components(SpriteAnimation):
          animation.update(delta_time)

