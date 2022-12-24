import arcade
import imgui
from deeper.dimgui import Gui


class BasicExample(arcade.Window):

    def __init__(self):
        super().__init__(800, 600, "Basic Example", resizable=True)
        self.gui = Gui(self)

    def on_draw(self):
        self.clear()

        imgui.new_frame()

        imgui.show_demo_window(False)

        self.gui.draw()

if __name__ == '__main__':
    window = BasicExample()
    arcade.run()