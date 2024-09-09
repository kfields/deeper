from loguru import logger

#from crunge.engine.imgui import ImGuiView
from crunge.engine import Renderer
from crunge.engine.d2.view_2d import View2D

from .tool import Tool

#class View(ImGuiView):
class View(View2D):
    current_tool: Tool = None
    title: str = None

    def __init__(self, title=''):
        super().__init__()
        self.title = title
    
    def use_tool(self, tool: Tool):
        if tool == self.current_tool:
            return
        if self.current_tool:
            self.current_tool.disable()
                        
        self.current_tool = tool
        #self.gui.disable()
        tool.enable()
        #self.gui.enable()

    def draw(self, renderer: Renderer):
        #logger.debug('View.draw')
        if self.current_tool:
            self.current_tool.draw(renderer)
        super().draw(renderer)

    def on_show(self):
        super().on_show()
        #self.gui.show()
        if self.current_tool:
            self.current_tool.enable()
        #self.gui.enable()

    def on_hide_view(self):
        super().on_hide()
        if self.current_tool:
            self.current_tool.disable()
        #self.gui.disable()
        #self.gui.hide()
