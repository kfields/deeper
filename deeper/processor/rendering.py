import arcade

from deeper import Space
from deeper.vu.sprite_vu import SpriteVu
from . import Processor

class RenderingProcessor(Processor):
    def __init__(self, scene=None) -> None:
        super().__init__()
        self.scene = scene

    def process(self):
        self.scene.tile_vu_list = []
        self.scene.tile_list = arcade.SpriteList()

        for ent, (space, vu) in self.world.get_components(Space, SpriteVu):
            position = self.scene.camera.project(space.position)
            vu.position = position
            #print("position: ", position)
            vu.sprite.set_position(*position.xy)
            self.scene.tile_vu_list.append(vu)

        #self.scene.tile_vu_list = sorted(self.scene.tile_vu_list, key=lambda vu: -vu.position.z)
        self.scene.tile_vu_list = sorted(self.scene.tile_vu_list, key=lambda vu: -vu.position.z + vu.position.y)
        
        for vu in self.scene.tile_vu_list:
            self.scene.tile_list.append(vu.sprite)
