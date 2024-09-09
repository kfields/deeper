from loguru import logger

from crunge.engine.d2.sprite import Sprite

from deeper.constants import *
from .vu import Vu
from .component_builder import ComponentBuilder

class SpriteVu(Vu):
    sprite: Sprite = None
    def __init__(self, sprite: Sprite, offset=DEFAULT_VEC2) -> None:
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
        sprite = Sprite(blueprint.texture)
        return SpriteVu(sprite, offset)
