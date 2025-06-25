from loguru import logger

from crunge.engine import Renderer
from crunge.engine.d2.view_2d import View2D

from .tool import Tool


class View(View2D):

    def __init__(self, title=""):
        super().__init__()
        self.title = title

    @property
    def tool(self) -> Tool:
        return self.controller

    @tool.setter
    def tool(self, tool: Tool):
        self.controller = tool

    def draw(self, renderer: Renderer):
        if self.tool:
            self.tool.draw(renderer)

        with self.renderer:
            self.scene.draw(self.renderer)
        
        super().draw(self.renderer)
