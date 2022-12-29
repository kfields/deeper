import glm
import imgui

from deeper import Blueprint
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class BlueprintWidget(ComponentWidget):
    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.blueprint = blueprint

    def draw(self):
        expanded, self.visible = imgui.collapsing_header("Blueprint", self.visible)
        if not expanded:
            return
        """
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
      """

class BlueprintWidgetBuilder(ComponentWidgetBuilder):
    key = Blueprint
    cls = BlueprintWidget
