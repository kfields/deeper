import arcade

from deeper.constants import *
from deeper import Space, Cuboid
from deeper.vu.sprite_vu import SpriteVu, AnimatedSpriteVu
from deeper.sprite import AnimatedSprite

from ..builder import Builder


class SpriteVuBuilder(Builder):
    def __init__(self) -> None:
        super().__init__("SpriteVu")

    def build(self, blueprint, world, target=None, components=[]):
        print("blueprint.__dict__", blueprint.parent.__dict__)
        return SpriteVu(arcade.Sprite(blueprint.parent.image))


class AnimatedSpriteVuBuilder(Builder):
    def __init__(self) -> None:
        super().__init__("AnimatedSpriteVu")

    def build(self, blueprint, world, target=None, components=[]):
        print("blueprint.__dict__", blueprint.__dict__)
        return AnimatedSpriteVu(
            AnimatedSprite(
                blueprint.image,
                image_width=blueprint.width,
                image_height=blueprint.height,
                frames=blueprint.frames,
                rate=blueprint.rate
            )
        )
