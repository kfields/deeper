import arcade

from deeper.constants import *
from deeper.sprite import AnimatedSprite
from . import Vu

class SpriteVu(Vu):
    sprite: arcade.Sprite = None
    def __init__(self, sprite: arcade.Sprite, offset=DEFAULT_VEC2) -> None:
        self.sprite = sprite
        self.offset = offset

class AnimatedSpriteVu(Vu):
    sprite: AnimatedSprite = None
    def __init__(self, sprite: AnimatedSprite, offset=DEFAULT_VEC2) -> None:
        self.sprite = sprite
        self.offset = offset
