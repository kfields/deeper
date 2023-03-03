from loguru import logger

from ..constants import *
from deeper.components.sprite_animation import SpriteAnimation
from . import SceneProcessor

class AnimationProcessor(SceneProcessor):
    def process(self, delta_time: float):
        for ent, (animation, ) in self.world.get_components(SpriteAnimation):
          animation.update(delta_time)

