# import arcade

from crunge.engine.loader.texture_loader import TextureLoader
from crunge.engine.d2.sprite import Sprite, SpriteMaterial

from ..constants import *
from ..level import Level
from deeper import Block
from deeper.components.sprite_vu import SpriteVu
from deeper.catalog import Catalog


class BasicLevel(Level):
    def __init__(self, rows=32, cols=32, timed=False):
        # def __init__(self, rows=4, cols=4, timed=False):
        super().__init__("test", timed)
        self.rows = rows
        self.cols = cols
        self.create_grid()
        self.create_layer("Floor")
        self.create_layer("Default")

    def create_grid(self):
        catalog = Catalog.instance
        blueprint = catalog.find("Cell")
        size = glm.vec3(CELL_WIDTH, 0.01, 1)
        layer = self.create_layer("Grid")
        for ty in range(0, self.rows):
            for tx in range(0, self.cols):
                position = glm.vec3(tx * CELL_WIDTH, 0, ty)
                # logger.debug(f"position: {position}")
                block = Block(position, size)
                texture = TextureLoader().load(":deeper:/tiles/_Grid/GRID.png")
                material = SpriteMaterial(texture)
                vu = SpriteVu(Sprite(material).create())
                self.create_entity(layer, blueprint, block, vu)
