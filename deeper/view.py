from loguru import logger

from crunge.engine import Renderer
from crunge.engine.d2.view_2d import View2D

from .tool import Tool


class View(View2D):
    #tool: Tool = None
    title: str = None

    def __init__(self, title=''):
        super().__init__()
        self.title = title
        self._tool: Tool = None

    @property
    def tool(self):
        return self._tool
    
    @tool.setter
    def tool(self, tool):
        self._tool = tool
        self.controller = tool
        #self.use_tool(tool)

    
    def use_tool(self, tool: Tool):
        if tool == self.tool:
            return
        if self.tool:
            self.tool.disable()
                        
        self.tool = tool
        #self.gui.disable()
        tool.enable()
        #self.gui.enable()

    def draw(self, renderer: Renderer):
        #logger.debug('View.draw')
        if self.tool:
            self.tool.draw(renderer)
        super().draw(renderer)

    def on_show(self):
        super().on_show()
        #self.gui.show()
        if self.tool:
            self.tool.enable()
        #self.gui.enable()

    def on_hide_view(self):
        super().on_hide()
        if self.tool:
            self.tool.disable()
        #self.gui.disable()
        #self.gui.hide()
