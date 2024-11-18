from loguru import logger
import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu

from deeper.constants import DEFAULT_VEC2
from .vu import Vu
from .component_builder import ComponentBuilder

class SpriteVuComponent(Vu):
    def __init__(self, sprite_vu: SpriteVu, offset=DEFAULT_VEC2) -> None:
        super().__init__()
        self.sprite_vu = sprite_vu
        self._offset = offset
        self.layer = None

    def create(self, world, entity, layer):
        self.layer = layer
        self.sprite_vu.config(group=layer.sprites).create()

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
        #sprite = Sprite(material).create()
        vu = SpriteVu(sprite)
        return SpriteVuComponent(vu, offset)
