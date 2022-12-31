import arcade

from deeper.constants import *
from deeper import Block

from ..builder import EntityBuilder

class BlockBuilder(EntityBuilder):
    key = 'Block'

    def build(self, blueprint, world, target=None, components=[]):
        #print(blueprint)
        position = self.compute_position(blueprint, world, target)
        #print("position: ", position)
        size = glm.vec3(*blueprint.size)
        block = Block(position, size, blueprint=blueprint)
        world.create_entity(block, *components)


    def compute_position(self, blueprint, world, target):
        if not target:
            return glm.vec3()
        target_space = world.component_for_entity(target, Block)
        target_pos = target_space.position
        target_aabb = target_space.aabb

        size = blueprint.size
        return glm.vec3(target_pos.x, target_aabb.maxy + size[1]/2, target_pos.z)
