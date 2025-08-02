from loguru import logger

from crunge.engine import Renderer
from crunge.engine.d2.sprite import SpriteVu, SpriteVuGroup
from crunge.engine.d2.sprite.dynamic import DynamicSpriteGroup
from crunge.engine.d2.sprite.instanced.instanced_sprite_vu_group import InstancedSpriteVuGroup
from crunge.engine.math import Rect2

from deeper.event import EventSource, LayerDirtyEvent

from .ecs.entity_group import EntityGroup
from .quad_tree import Quadtree


class SceneLayer(EntityGroup):
    def __init__(self, scene, name):
        super().__init__(name)
        self.scene = scene
        self.name = name
        #self.sprite_vu_group = SpriteVuGroup()
        self.sprite_group = DynamicSpriteGroup(1024).enable()
        self.sprite_vu_group = InstancedSpriteVuGroup(1024, self.sprite_group).enable()
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
        #logger.debug('dirty')
        self.dirty = True
        self.events.publish(LayerDirtyEvent())

    def unmark(self):
        self.dirty = False

    def clear(self):
        self.sprite_vu_group.clear()
        
    def add_sprite(self, vu: SpriteVu):
        #exit()
        #self.sprite_group.append(vu.sprite)
        self.sprite_vu_group.append(vu)
        self.quad_tree.insert(vu)
        return vu

    def update(self, delta_time: float):
        #self.effects.update(delta_time)
        self.sprite_vu_group.update(delta_time)

    def draw(self):
        if not self.visible:
            return
        #logger.debug(len(self.sprites.sprites))
        #logger.debug(renderer.camera.position)
        #logger.debug(renderer.camera.size)
        self.sprite_vu_group.draw()
        #logger.debug(f'visible_objects: {len(visible_objects)}')
