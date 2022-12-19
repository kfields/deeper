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
        position = glm.vec3(target_pos.x, target_pos.y + CELL_HEIGHT, target_pos.z)
        rotation = glm.vec3()
        shape = Cuboid(CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH)
        #print("position: ", position)
        block = Space(position, rotation, shape)
        vu = SpriteVu(arcade.Sprite(
            blueprint.image, scale=1
        ))
        world.create_entity(block, vu)
