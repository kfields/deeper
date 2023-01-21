import arcade

from deeper.constants import *
from .animation import Animation
from .component_builder import ComponentBuilder
from .sprite_vu import SpriteVu

class SpriteAnimation(Animation):
    def __init__(self, filename, image_width, image_height, frames, rate=1):
        super().__init__()
        self.image_width = image_width
        self.image_height = image_height
        self.frames = frames
        self.rate = rate
        # Animation timing
        self.time = 1
        self.update_time = 0

        # Load Textures
        texture_coords = []
        for i in range(frames):
            texture_coords.append( (i*image_width, 0, image_width, image_height) )

        self.textures = arcade.load_textures(filename, texture_coords)
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.sprite = None

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate
        self.interval = 1/(60*rate)

    def create(self, world, entity, layer):
        vu = world.component_for_entity(entity, SpriteVu)
        self.sprite = vu.sprite
        self.sprite.texture = self.texture

    def update(self, delta_time: float = 1/60):
        self.time += delta_time

        if self.time < self.update_time:
            return

        self.update_time = self.time + self.interval

        self.cur_texture_index += 1

        if self.cur_texture_index > self.frames-1:
            self.cur_texture_index = 0

        self.texture = self.textures[self.cur_texture_index]
        self.sprite.texture = self.texture

class SpriteAnimationBuilder(ComponentBuilder):
    key = 'SpriteAnimation'

    def build(self, blueprint, world):
        return SpriteAnimation(
                blueprint.image,
                image_width=blueprint.width,
                image_height=blueprint.height,
                frames=blueprint.frames,
                rate=blueprint.rate
        )
