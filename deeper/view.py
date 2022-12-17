import arcade
from arcade.gui import UIManager

from .dimgui import Gui

from .tool import Tool

class View(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.ui_manager = UIManager(window)
        self.gui = Gui(window, auto_enable=False)
        self.current_tool: Tool = None
        
    def use_tool(self, tool: Tool):
        self.current_tool = tool
        self.gui.disable()
        tool.enable()
        self.gui.enable()

    def draw(self):
        pass

    def on_draw(self):
        super().on_draw()
        arcade.start_render()
        self.gui.start_render()

        self.ui_manager.draw()

        self.draw()

        if self.current_tool:
            self.current_tool.draw()

        self.gui.finish_render()
        arcade.finish_render()


    def on_show_view(self):
        super().on_show_view()
        self.ui_manager.enable()
        self.gui.enable()

    def on_hide_view(self):
        super().on_hide_view()
        self.ui_manager.disable()
        self.gui.disable()