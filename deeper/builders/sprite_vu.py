import arcade

from deeper.constants import *
from deeper import Space, Cuboid
from deeper.vu.sprite_vu import SpriteVu, AnimatedSpriteVu
from deeper.sprite import AnimatedSprite

from ..builder import Builder


class SpriteVuBuilder(Builder):
    key = 'SpriteVu'

    def build(self, blueprint, world, target=None, components=[]):
        return SpriteVu(arcade.Sprite(blueprint.parent.image))


class AnimatedSpriteVuBuilder(Builder):
    key = 'AnimatedSpriteVu'

    def build(self, blueprint, world, target=None, components=[]):
        return AnimatedSpriteVu(
            AnimatedSprite(
                blueprint.image,
                image_width=blueprint.width,
                image_height=blueprint.height,
                frames=blueprint.frames,
                rate=blueprint.rate
            )
        )
