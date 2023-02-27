import pyglet.window.mouse as mouse
import arcade
from arcade import key
from arcade.gui import UIManager

from .dimgui import ViewGui
from .tool import Tool

class View(arcade.View):
    current_tool: Tool = None
    title: str = None

    def __init__(self, window, title=''):
        super().__init__(window)
        self.title = title
        #self.ui_manager = UIManager(window)
        self.gui = ViewGui(self, auto_enable=False)
        
    def use_tool(self, tool: Tool):
        if tool == self.current_tool:
            return
        if self.current_tool:
            self.current_tool.disable()
                        
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

        #self.ui_manager.draw()

        self.draw()

        if self.current_tool:
            self.current_tool.draw()

        self.gui.finish_render()
        arcade.finish_render()


    def on_show_view(self):
        super().on_show_view()
        #self.ui_manager.enable()
        self.gui.show()
        if self.current_tool:
            self.current_tool.enable()
        self.gui.enable()

    def on_hide_view(self):
        super().on_hide_view()
        #self.ui_manager.disable()
        if self.current_tool:
            self.current_tool.disable()
        self.gui.disable()
        self.gui.hide()
