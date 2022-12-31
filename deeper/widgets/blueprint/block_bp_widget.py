import glm
import imgui

from deeper.components.block import Block
from .blueprint_widget import BlueprintWidget, BlueprintWidgetBuilder


class BlockBpWidget(BlueprintWidget):
    def __init__(self, block):
        super().__init__(block)
        self.block = block

    def draw(self):
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


class BlockBpWidgetBuilder(BlueprintWidgetBuilder):
    key = Block
    cls = BlockWidget
