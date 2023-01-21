from deeper.constants import *
from deeper import Block

from .entity_builder import EntityBuilder

class BlockBuilder(EntityBuilder):
    key = 'Block'

    def build(self, blueprint, world, layer, position = DEFAULT_VEC3):
        ent = super().build(blueprint, world, layer)
        block = world.component_for_entity(ent, Block)
        block.position = position
        return ent
