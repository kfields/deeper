import arcade

from deeper import Space
from deeper.vu.sprite_vu import SpriteVu, AnimatedSpriteVu
from . import Processor

class RenderingProcessor(Processor):
    def __init__(self, scene=None) -> None:
        super().__init__()
        self.scene = scene

    def process(self, delta_time: float):
        self.scene.tile_vu_list = []
        self.scene.tile_list = arcade.SpriteList()

        for ent, (space, vu) in self.world.get_components(Space, SpriteVu):
            position = self.scene.camera.project(space.position)
            vu.position = position
            vu.aabb = space.aabb
            #print("position: ", position)
            vu.sprite.set_position(*position.xy)
            self.scene.tile_vu_list.append(vu)

        for ent, (space, vu) in self.world.get_components(Space, AnimatedSpriteVu):
            position = self.scene.camera.project(space.position)
            vu.position = position
            vu.aabb = space.aabb
            #print("position: ", position)
            vu.sprite.set_position(*position.xy)
            vu.sprite.update_animation(delta_time)
            self.scene.tile_vu_list.append(vu)

        #self.scene.tile_vu_list = sorted(self.scene.tile_vu_list, key=lambda vu: vu.position.z + vu.position.y)
        self.scene.tile_vu_list = sorted(self.scene.tile_vu_list, key=lambda vu: vu.position.z)
        #self.scene.tile_vu_list = sorted(self.scene.tile_vu_list, key=lambda vu: vu.aabb.maxz)

        for vu in self.scene.tile_vu_list:
            self.scene.tile_list.append(vu.sprite)
