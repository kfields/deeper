from loguru import logger

from crunge.engine import Renderer
from crunge.engine.d2 import Sprite, SpriteList

from deeper.constants import *
from deeper.event import Event, EventSource, LayerDirtyEvent

from .ecs.entity_group import EntityGroup

class SceneLayer(EntityGroup):
    def __init__(self, scene, name):
        super().__init__(name)
        self.scene = scene
        self.name = name
        self.sprites = SpriteList()
        self.visible = True
        self.locked = False
        self.dirty = True
        self.events = EventSource()

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
        
    def add_sprite(self, sprite: Sprite):
        self.sprites.append(sprite)
        return sprite

    def update(self, delta_time: float):
        #self.effects.update(delta_time)
        self.sprites.update(delta_time)

    def update_animation(self, delta_time: float):
        self.sprites.update_animation(delta_time)

    def draw(self, renderer: Renderer):
        if not self.visible:
            return
        #logger.debug(len(self.sprites.sprites))
        #logger.debug(renderer.camera.position)
        #logger.debug(renderer.camera.size)
        self.sprites.draw(renderer)
