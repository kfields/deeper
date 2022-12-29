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

        imgui.text("name: ")
        imgui.same_line()
        imgui.text(self.blueprint.name)

        imgui.text("extends: ")
        imgui.same_line()
        imgui.text(self.blueprint.extends)

        imgui.text("category: ")
        imgui.same_line()
        imgui.text(self.blueprint.category)

        changed, extents = imgui.drag_float3(
            "Extents", *self.blueprint.extents, change_speed=0.1
        )
        if changed:
            self.block.extents = extents


class BlueprintWidgetBuilder(ComponentWidgetBuilder):
    key = Blueprint
    cls = BlueprintWidget
