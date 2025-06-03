from loguru import logger

from crunge.engine import Renderer
from crunge.engine.d2.view_2d import View2D

from .tool import Tool


class View(View2D):

    def __init__(self, title=""):
        super().__init__()
        self.title = title
        #self._tool: Tool = None

    @property
    def tool(self) -> Tool:
        return self.controller

    @tool.setter
    def tool(self, tool: Tool):
        self.controller = tool

    '''
    @property
    def tool(self) -> Tool:
        return self._tool

    @tool.setter
    def tool(self, tool: Tool):
        if tool == self._tool:
            return
        if self._tool:
            self._tool.disable()
        self._tool = tool
        self.controller = tool
        tool.enable()
    '''

    '''
    @tool.setter
    def tool(self, tool):
        self._tool = tool
        self.controller = tool

    def use_tool(self, tool: Tool):
        if tool == self.tool:
            return
        if self.tool:
            self.tool.disable()

        self.tool = tool
        tool.enable()
    '''
    
    '''
    def draw(self, renderer: Renderer):
        # logger.debug('View.draw')
        if self.tool:
            self.tool.draw(renderer)
        super().draw(renderer)
    '''

    def pre_draw(self, renderer: Renderer):
        self.scene.pre_draw(self.renderer)
        super().pre_draw(self.renderer)

    def draw(self, renderer: Renderer):
        if self.tool:
            self.tool.draw(renderer)

        with self.renderer:
            self.scene.draw(self.renderer)
            super().draw(self.renderer)

    def post_draw(self, renderer: Renderer):
        self.scene.post_draw(self.renderer)
        super().post_draw(self.renderer)

    '''
    def on_show(self):
        super().on_show()
        if self.tool:
            self.tool.enable()

    def on_hide(self):
        super().on_hide()
        if self.tool:
            self.tool.disable()
    '''