from loguru import logger

import arcade

from ..constants import *
from deeper import Block
from deeper.components.sprite_vu import SpriteVu, AnimatedSpriteVu
from . import Processor

class RenderingProcessor(Processor):
    def __init__(self, scene=None) -> None:
        super().__init__()
        self.scene = scene

    def process(self, delta_time: float):
        for layer in self.scene.layers:
            self.process_layer(layer, delta_time)

    def process_layer(self, layer, delta_time: float):
        if not layer.dirty:
            return
        logger.debug(f"processing {layer.name}")
        layer_group = layer.group
        vu_list = []

        layer.clear()

        for ent, (_, block, vu) in self.world.get_components(layer_group.__class__, Block, SpriteVu):
            position = self.scene.camera.project(block.position)
            vu.position = position
            #print("position: ", position)
            sprite_position = position.xy + (vu.offset * WORLD_SCALE)
            vu.sprite.set_position(*sprite_position)
            vu_list.append(vu)

        for ent, (_, block, vu) in self.world.get_components(layer_group.__class__, Block, AnimatedSpriteVu):
            position = self.scene.camera.project(block.position)
            vu.position = position
            #print("position: ", position)
            sprite_position = position.xy + (vu.offset * WORLD_SCALE)
            vu.sprite.set_position(*sprite_position)
            vu.sprite.update_animation(delta_time)
            vu_list.append(vu)

        vu_list = sorted(vu_list, key=lambda vu: vu.position.z)

        for vu in vu_list:
            layer.sprites.append(vu.sprite)

        layer.unmark()

    """
    def process(self, delta_time: float):
        self.scene.tile_vu_list = []
        self.scene.tile_list = arcade.SpriteList()

        for ent, (block, vu) in self.world.get_components(Block, SpriteVu):
            position = self.scene.camera.project(block.position)
            vu.position = position
            vu.aabb = block.aabb
            #print("position: ", position)
            #sprite_position = position.xy + vu.offset
            sprite_position = position.xy + (vu.offset * WORLD_SCALE)
            vu.sprite.set_position(*sprite_position)
            self.scene.tile_vu_list.append(vu)

        for ent, (block, vu) in self.world.get_components(Block, AnimatedSpriteVu):
            position = self.scene.camera.project(block.position)
            vu.position = position
            vu.aabb = block.aabb
            #print("position: ", position)
            sprite_position = position.xy + vu.offset
            vu.sprite.set_position(*sprite_position)
            vu.sprite.update_animation(delta_time)
            self.scene.tile_vu_list.append(vu)

        self.scene.tile_vu_list = sorted(self.scene.tile_vu_list, key=lambda vu: vu.position.z)

        for vu in self.scene.tile_vu_list:
            self.scene.tile_list.append(vu.sprite)
    """