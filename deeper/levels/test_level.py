import arcade

from ..constants import *
from ..level import Level
from deeper import Entity, Block
from deeper.components.sprite_vu import SpriteVu
from deeper.catalog import Catalog

class TestLevel(Level):
    def __init__(self, timed=False):
        super().__init__(timed)
        self.create_grid()
        self.create_layer('Floor')
        self.create_layer('Default')

    def create_grid(self):
        catalog = Catalog.instance
        blueprint = catalog.find("Cell")
        size = glm.vec3(CELL_WIDTH, 0.01, 1)
        layer = self.create_layer('Grid')
        for ty in range(0, 16):
            for tx in range(0, 16):
                position = glm.vec3(tx * CELL_WIDTH, 0, ty)
                # position = glm.vec3(tx * CELL_WIDTH - CELL_HALF_WIDTH, 0, ty - CELL_HALF_DEPTH)
                # print("position: ", position)
                block = Block(position, size)
                vu = SpriteVu(
                    arcade.Sprite(
                        ":deeper:tiles/_Grid/GRID.png",
                    )
                )
                self.create_entity(layer, blueprint, block, vu)
                #self.create_entity(Entity(layer), layer, blueprint, block, vu)
