from loguru import logger

import arcade

from deeper.constants import *
from deeper.event import DirtyEvent
from deeper.effect import EffectList

class Layer:
    def __init__(self, scene, name, group):
        self.scene = scene
        self.name = name
        self.group = group
        self.group_subscription = None
        self.sprites = arcade.SpriteList()
        self.effects = EffectList()
        self.dirty = True

    def enable(self):
        self.group_subscription = self.group.events.subscribe(self.on_group_event)

    def disable(self):
        self.group.events.unsubscribe(self.group_subscription)

    def on_group_event(self, event):
        logger.debug(event)
        match type(event):
            case DirtyEvent:
                self.mark()

    def mark(self):
        logger.debug('dirty')
        self.dirty = True

    def unmark(self):
        self.dirty = False

    def clear(self):
        self.sprites.clear()
        
    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        return sprite

    def add_effect(self, effect):
        self.effects.append(effect)
        return effect

    def update(self, delta_time):
        self.effects.update(delta_time)
        self.sprites.on_update(delta_time)

    def update_animation(self, delta_time):
        self.sprites.update_animation(delta_time)

    def draw(self):
        self.sprites.draw()
        self.effects.draw()
