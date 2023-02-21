from loguru import logger

import arcade

from deeper.constants import *
from deeper.sprite import AnimatedSprite
from .vu import Vu
from .block import Block
from .component_builder import ComponentBuilder

class SpriteVu(Vu):
    sprite: arcade.Sprite = None
    def __init__(self, sprite: arcade.Sprite, offset=DEFAULT_VEC2) -> None:
        super().__init__()
        self.sprite = sprite
        self._offset = offset
        self.layer = None

    def create(self, world, entity, layer):
        self.layer = layer

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset
        self.layer.mark()


class SpriteVuBuilder(ComponentBuilder):
    key = 'SpriteVu'

    def build(self, blueprint, world):
        offset = glm.vec2(blueprint.offset) if hasattr(blueprint, 'offset') else DEFAULT_VEC2
        sprite = arcade.Sprite()
        sprite.texture = blueprint.texture
        return SpriteVu(sprite, offset)
