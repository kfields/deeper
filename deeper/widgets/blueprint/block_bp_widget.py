import glm

from crunge import imgui
from crunge.engine import Renderer

from deeper.blueprints.component.block_blueprint import BlockBlueprint
from .blueprint_widget import BlueprintWidget, BlueprintWidgetBuilder


class BlockBpWidget(BlueprintWidget):
    def __init__(self, block):
        super().__init__(block)
        self.block = block

    def draw(self, renderer: Renderer):
        changed, size = imgui.drag_float3(
            'Size', tuple(self.block.size), change_speed=0.1
        )
        if changed:
            self.block.size = glm.vec3(*size)


class BlockBpWidgetBuilder(BlueprintWidgetBuilder):
    key = BlockBlueprint
    cls = BlockBpWidget
