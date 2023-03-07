import glm

from .. import Node
from .component_builder import ComponentBuilder

class Block(Node):
    pass

class BlockBuilder(ComponentBuilder):
    key = 'Block'

    def build(self, blueprint, world):
        # TODO: Shouldn't blueprint size already be a vec3?
        size = glm.vec3(blueprint.size)
        return Block(size=size)
