import arcade

from . import Vu

class SpriteVu(Vu):
    sprite: arcade.Sprite = None
    def __init__(self, sprite: arcade.Sprite) -> None:
        self.sprite = sprite
