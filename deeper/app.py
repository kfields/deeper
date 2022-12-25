import arcade

from .window import Window
from .constants import *
from .world import World

from .state import WorldEditState
from .views import WorldEditor


class Deeper(Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.world = World()
        #self.edit_state = WorldEditState(self.world)
        #view = WorldEditor(self, self.edit_state)
        view = WorldEditor(self, WorldEditState(self.world))
        self.show_view(view)

    """
    def on_update(self, delta_time: float):
        self.world.process()
        return super().on_update(delta_time)
    """

    def show_view(self, new_view):
        super().show_view(new_view)

def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
