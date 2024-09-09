import glm

from crunge import imgui
from crunge.engine import Renderer

from deeper.components.block import Block
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class BlockWidget(ComponentWidget):
    def __init__(self, block):
        super().__init__(block)
        self.block = block

    def draw(self, renderer: Renderer):
        changed, position = imgui.drag_float3(
            'Position', *self.block.position, change_speed=0.1
        )
        if changed:
            self.block.position = glm.vec3(*position)

        changed, size = imgui.drag_float3(
            'Size', *self.block.size, change_speed=0.1
        )
        if changed:
            self.block.size = glm.vec3(*size)

        changed, transform = imgui.drag_float3(
            'Transform', *self.block.transform, change_speed=0.1
        )
        if changed:
            self.block.transform = glm.vec3(*transform)


class BlockWidgetBuilder(ComponentWidgetBuilder):
    key = Block
    cls = BlockWidget
