import arcade

from deeper.constants import *
from deeper import Space, Cuboid
from deeper.vu.sprite_vu import SpriteVu

from ..builder import Builder

class SpriteVuBuilder(Builder):
    def __init__(self) -> None:
        super().__init__('SpriteVu')

    def build(self, blueprint, world, target=None, components=[]):
        print("blueprint.__dict__", blueprint.parent.__dict__)
        #exit()
        return SpriteVu(arcade.Sprite(blueprint.parent.image))
