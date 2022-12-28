import glm
import imgui

from deeper.block import Block
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class BlockWidget(ComponentWidget):
    def __init__(self, block):
        super().__init__(block)
        self.block = block

    def draw(self):
        expanded, self.visible = imgui.collapsing_header("Block", self.visible)
        if not expanded:
            return
        changed, position = imgui.drag_float3(
            "Position", *self.block.position, change_speed=0.1
        )
        if changed:
            self.block.position = glm.vec3(*position)

        changed, extents = imgui.drag_float3(
            "Extents", *self.block.extents, change_speed=0.1
        )
        if changed:
            self.block.extents = glm.vec3(*extents)


class BlockWidgetBuilder(ComponentWidgetBuilder):
    key = Block
    cls = BlockWidget
