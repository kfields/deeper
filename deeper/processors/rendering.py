from loguru import logger

import arcade

from ..constants import *
from deeper import Block
from deeper.components.sprite_vu import SpriteVu
from . import SceneProcessor

class RenderingProcessor(SceneProcessor):
    def process(self, delta_time: float):
        for layer in self.scene.layers:
            self.process_layer(layer, delta_time)

    def process_layer(self, layer, delta_time: float):
        # if not layer.dirty or not layer.visible:
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
            vu.sprite.position = sprite_position.xy
            vu_list.append(vu)

        vu_list = sorted(vu_list, key=lambda vu: vu.position.z)

        for vu in vu_list:
            layer.sprites.append(vu.sprite)

        layer.unmark()
