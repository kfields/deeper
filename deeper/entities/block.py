from loguru import logger

import arcade

from deeper.constants import *
from deeper import Block

from ..builder import EntityBuilder

class BlockBuilder(EntityBuilder):
    key = 'Block'

    def build(self, blueprint, world, position = DEFAULT_VEC3, components=[]):
        #print(blueprint)
        logger.debug(f"position: {position}")
        block = None
        for component in components:
            if component.__class__ == Block:
                block = component
                break
        block.position = position
        world.create_entity(*components)

    """
    def build(self, blueprint, world, target=None, components=[]):
        #print(blueprint)
        position = self.compute_position(blueprint, world, target)
        #print("position: ", position)
        #size = glm.vec3(*blueprint.size)
        #block = Block(position, size, blueprint=blueprint)
        block = None
        for component in components:
            if component.__class__ == Block:
                block = component
                break
        block.position = position
        #world.create_entity(block, *components)
        world.create_entity(*components)

    def compute_position(self, blueprint, world, target):
        if not target:
            return glm.vec3()
        target_space = world.component_for_entity(target, Block)
        target_pos = target_space.position
        target_aabb = target_space.aabb

        size = blueprint.size
        return glm.vec3(target_pos.x, target_aabb.maxy + size[1]/2, target_pos.z)
    """