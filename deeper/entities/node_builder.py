from deeper.constants import *
from deeper import Block

from .entity_builder import EntityBuilder

class NodeBuilder(EntityBuilder):
    key = 'Node'

    def build(self, blueprint, world, layer, position = DEFAULT_VEC3):
        #ent = super().build(blueprint, world, layer)
        #block = world.component_for_entity(ent, Block)
        block = super().build(blueprint, world, layer)
        block.position = position
        #return ent
        return block
