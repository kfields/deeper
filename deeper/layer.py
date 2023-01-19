import arcade

from deeper.constants import *
from deeper.effect import EffectList

class Layer:
    def __init__(self, scene, name):
        self.scene = scene
        self.name = name
        self.sprites = arcade.SpriteList()
        self.effects = EffectList()

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
