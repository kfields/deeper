import glm
import imgui

from deeper.space import Space
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class SpaceWidget(ComponentWidget):
    def __init__(self, space):
        super().__init__(space)
        self.space = space

    def draw(self):
        expanded, self.visible = imgui.collapsing_header("Space", self.visible)
        if not expanded:
            return
        changed, position = imgui.drag_float3(
            "Position", *self.space.position, change_speed=0.1
        )
        if changed:
            self.space.position = glm.vec3(*position)


class SpaceWidgetBuilder(ComponentWidgetBuilder):
    key = Space
    cls = SpaceWidget
