from loguru import logger

import arcade

from deeper.constants import *
from deeper.event import Event, EventSource, LayerDirtyEvent

from .ecs.entity_group import EntityGroup

class SceneLayer(EntityGroup):
    def __init__(self, scene, name):
        super().__init__(name)
        self.scene = scene
        self.name = name
        self.sprites = arcade.SpriteList()
        self.visible = True
        self.locked = False
        self.dirty = True
        self.events = EventSource()

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
        
    def add_sprite(self, sprite: arcade.Sprite):
        self.sprites.append(sprite)
        return sprite

    def update(self, delta_time: float):
        #self.effects.update(delta_time)
        self.sprites.on_update(delta_time)

    def update_animation(self, delta_time: float):
        self.sprites.update_animation(delta_time)

    def draw(self):
        if not self.visible:
            return
        self.sprites.draw()
