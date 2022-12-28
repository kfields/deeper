import arcade

from deeper.constants import *
from deeper.vu.sprite_vu import SpriteVu, AnimatedSpriteVu
from deeper.sprite import AnimatedSprite

from ..builder import Builder


class SpriteVuBuilder(Builder):
    key = 'SpriteVu'

    def build(self, blueprint, world, target=None, components=[]):
        offset = glm.vec2(blueprint.offset[0], blueprint.offset[1]) if hasattr(blueprint, 'offset') else DEFAULT_VEC2
        return SpriteVu(arcade.Sprite(blueprint.parent.image), offset)


class AnimatedSpriteVuBuilder(Builder):
    key = 'AnimatedSpriteVu'

    def build(self, blueprint, world, target=None, components=[]):
        offset = glm.vec2(*blueprint.offset) if hasattr(blueprint, 'offset') else DEFAULT_VEC2
        return AnimatedSpriteVu(
            AnimatedSprite(
                blueprint.image,
                image_width=blueprint.width,
                image_height=blueprint.height,
                frames=blueprint.frames,
                rate=blueprint.rate
            ),
            offset
        )
