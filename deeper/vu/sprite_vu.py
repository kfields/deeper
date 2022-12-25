import arcade

from deeper.sprite import AnimatedSprite
from . import Vu

class SpriteVu(Vu):
    sprite: arcade.Sprite = None
    def __init__(self, sprite: arcade.Sprite) -> None:
        self.sprite = sprite

class AnimatedSpriteVu(Vu):
    sprite: AnimatedSprite = None
    def __init__(self, sprite: AnimatedSprite) -> None:
        self.sprite = sprite
