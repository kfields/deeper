import arcade

from deeper.constants import *
from deeper import Space, Cuboid
from deeper.vu.sprite_vu import SpriteVu

from ..builder import Builder

class BlockBuilder(Builder):
    def __init__(self) -> None:
        super().__init__('Block')

    def build(self, world, target, blueprint):
        #print(blueprint)
        target_space = world.component_for_entity(target, Space)
        target_pos = target_space.position
        target_aabb = target_space.aabb

        extents = blueprint.extents
        position = glm.vec3(target_pos.x, target_aabb.maxy + extents[1]/2, target_pos.z)
        rotation = glm.vec3()
        shape = Cuboid(*extents)
        #print("position: ", position)
        block = Space(position, rotation, shape)
        vu = SpriteVu(arcade.Sprite(blueprint.image))
        world.create_entity(block, vu)
