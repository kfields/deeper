from loguru import logger

from crunge.engine import Renderer
from crunge.engine.d2 import SpriteVu, SpriteVuGroup
from crunge.engine.d2.sprite.group.instanced_sprite_vu_group import InstancedSpriteVuGroup
from crunge.engine.math import Rect2

from deeper.event import EventSource, LayerDirtyEvent

from .ecs.entity_group import EntityGroup
from .quad_tree import Quadtree


class SceneLayer(EntityGroup):
    def __init__(self, scene, name):
        super().__init__(name)
        self.scene = scene
        self.name = name
        #self.sprites = SpriteVuGroup()
        self.sprites = InstancedSpriteVuGroup(1024)
        self.visible = True
        self.locked = False
        self.dirty = True
        self.events = EventSource()
        self.quad_tree = Quadtree(Rect2(-1000, -1000, 2000, 2000))

    def __str__(self) -> str:
        return f"Layer({self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def enable(self):
        pass

    def disable(self):
        pass

    def mark(self):
        logger.debug('dirty')
        self.dirty = True
        self.events.publish(LayerDirtyEvent())

    def unmark(self):
        self.dirty = False

    def clear(self):
        self.sprites.clear()
        
    def add_sprite(self, sprite: SpriteVu):
        self.sprites.append(sprite)
        self.quad_tree.insert(sprite)
        return sprite

    def update(self, delta_time: float):
        #self.effects.update(delta_time)
        self.sprites.update(delta_time)

    '''
    def draw(self, renderer: Renderer):
        if not self.visible:
            return
        #logger.debug(len(self.sprites.sprites))
        #logger.debug(renderer.camera.position)
        #logger.debug(renderer.camera.size)
        #self.sprites.draw(renderer)
        frustrum = renderer.camera.frustrum
        #logger.debug(f'frustrum: {frustrum}')
        visible_objects = []
        self.quad_tree.query(frustrum, visible_objects)
        #logger.debug(f'visible_objects: {len(visible_objects)}')

        for obj in visible_objects:
            obj.draw(renderer)
    '''
    def pre_draw(self, renderer: Renderer):
        pass

    def draw(self, renderer: Renderer):
        if not self.visible:
            return
        #logger.debug(len(self.sprites.sprites))
        #logger.debug(renderer.camera.position)
        #logger.debug(renderer.camera.size)
        self.sprites.draw(renderer)
        #logger.debug(f'visible_objects: {len(visible_objects)}')

    def post_draw(self, renderer: Renderer):
        pass
