import arcade

from deeper.constants import *
from deeper.sprite import AnimatedSprite
from .vu import Vu
from ..builder import ComponentBuilder

class SpriteVu(Vu):
    sprite: arcade.Sprite = None
    def __init__(self, sprite: arcade.Sprite, offset=DEFAULT_VEC2) -> None:
        self.sprite = sprite
        self.offset = offset


class SpriteVuBuilder(ComponentBuilder):
    key = 'SpriteVu'

    def build(self, blueprint, world, target=None, components=[]):
        offset = glm.vec2(*blueprint.offset) if hasattr(blueprint, 'offset') else DEFAULT_VEC2
        #return SpriteVu(arcade.Sprite(blueprint.parent.image), offset)
        return SpriteVu(arcade.Sprite(blueprint.image), offset)


class AnimatedSpriteVu(Vu):
    sprite: AnimatedSprite = None
    def __init__(self, sprite: AnimatedSprite, offset=DEFAULT_VEC2) -> None:
        self.sprite = sprite
        self.offset = offset

class AnimatedSpriteVuBuilder(ComponentBuilder):
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
