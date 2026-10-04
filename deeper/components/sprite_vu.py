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

        # Before enable, deliberately. The vu is not seated on a node, so
        # its own find_render_group has nothing to walk — this is the only
        # way it learns it is grouped, and _enable reads that to decide
        # whether to allocate a program, buffers and bind groups. Assigning
        # after would mean every sprite in the scene allocates a full set it
        # never draws through.
        self.sprite_vu.render_group = layer.render_group
        self.sprite_vu.enable()

        # No group assignment here. It used to set sprite_vu.group directly,
        # which never added the vu to the group's members — membership comes
        # from the layer's ordered rebuild calling add_sprite_vu, which is
        # also what assigns the buffer and, now, the append sequence the
        # draw order is derived from. Setting group by hand would skip all
        # three and leave a vu that looks grouped and never draws.

    def destroy(self, world, entity, layer):
        # ASSUMPTION: the ECS calls a teardown hook with this shape. If it
        # doesn't, this needs wiring up — without it a despawned entity
        # leaves its vu in the group, holding a slot and drawing, until the
        # next full clear happens to sweep it out.
        self.sprite_vu.disable()
        self.layer = None

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset
        # Guarded: a blueprint can set offset before create runs, and the
        # unguarded version raised on None.
        if self.layer is not None:
            self.layer.mark()


class SpriteVuBuilder(ComponentBuilder):
    key = 'SpriteVu'

    def build(self, blueprint, world):
        offset = glm.vec2(blueprint.offset) if hasattr(blueprint, 'offset') else DEFAULT_VEC2
        sprite = Sprite(blueprint.texture)
        vu = SpriteVu(sprite)
        return SpriteVuComponent(vu, offset)