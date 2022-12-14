import math
import arcade
import glm
import imgui

from deeper.dimgui import Gui

from deeper.constants import *
from deeper.world import World
from deeper.scene import Scene


class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.world = World()
        self.scene = Scene(self, self.world)
        self.show_view(self.scene)

    def on_update(self, delta_time: float):
        self.world.process()
        return super().on_update(delta_time)


def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
