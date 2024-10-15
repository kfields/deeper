from loguru import logger
import glm

from crunge.engine.math.rect import Rect2
from crunge.engine.d2.sprite import Sprite

from ..constants import WORLD_SCALE
from ..scene import Scene
from ..scene_layer import SceneLayer
from ..scene_camera import SceneCamera

from deeper import Block
from deeper.components.sprite_vu import SpriteVu
from . import SceneProcessor

class RenderingProcessor(SceneProcessor):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene)
        self.scene = scene
        self.scene_camera = SceneCamera()

    def process(self, delta_time: float):
        for layer in self.scene.layers:
            self.process_layer(layer, delta_time)

    def process_layer(self, layer: SceneLayer, delta_time: float):
        if not layer.dirty:
            return
        logger.debug(f'processing {layer.name}')
        vu_list = []

        layer.clear()

        for ent, (_, block, vu) in self.world.get_components(layer.__class__, Block, SpriteVu):
            #position = self.scene.camera.project(block.position)
            position = self.scene_camera.project(block.position)
            #logger.debug(f'position: {position}')
            vu.position = position
            sprite_position = position.xy + (vu.offset * WORLD_SCALE)
            #logger.debug(f'sprite_position: {sprite_position}')
            #vu.sprite.position = sprite_position.xy
            sprite = vu.sprite
            size = sprite.texture.size
            #size = block.size
            self.update_sprite_transform(vu.sprite, sprite_position, size)
            vu_list.append(vu)

        vu_list = sorted(vu_list, key=lambda vu: vu.position.z)
        #logger.debug(f'vu_list: {vu_list}')

        for vu in vu_list:
            layer.add_sprite(vu.sprite)

        layer.unmark()

    def update_sprite_transform(self, sprite: Sprite, position: glm.vec3, size: glm.vec2, rotation=0.0, scale=glm.vec3(1,1,1), depth=0.0):
        x = position.x
        y = position.y
        z = depth

        model = glm.mat4(1.0)  # Identity matrix
        model = glm.translate(model, glm.vec3(x, y, z))
        model = glm.scale(
            model,
            glm.vec3(size.x * scale.x, size.y * scale.y, 1),
        )
        '''
        model = glm.rotate(model, rotation, glm.vec3(0, 0, 1))
        model = glm.scale(
            model,
            glm.vec3(size.x * scale.x, size.y * scale.y, 1),
        )
        '''
        sprite.transform = model

            
        sprite.aabb = Rect2(
            x - size.x / 2,
            y - size.y / 2,
            size.x,
            size.y,
        )
        #logger.debug(f'sprite.aabb: {sprite.aabb}')