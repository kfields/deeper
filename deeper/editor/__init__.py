import arcade

from deeper.dimgui import Gui
from deeper.constants import *
from deeper.world import World

from .state import WorldEditState
from .views import WorldEditView


class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.world = World()
        self.edit_state = WorldEditState(self.world)
        view = WorldEditView(self, self.edit_state)
        self.show_view(view)

    def on_update(self, delta_time: float):
        self.world.process()
        return super().on_update(delta_time)

    def show_view(self, new_view):
        super().show_view(new_view)

def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
