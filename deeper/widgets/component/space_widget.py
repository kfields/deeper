import glm
import imgui

from deeper.space import Space
from .component_widget import ComponentWidget, ComponentWidgetBuilder

class SpaceWidget(ComponentWidget):
    def __init__(self, space):
        super().__init__(space)
        self.space = space

    def draw(self):
        #imgui.begin_group()
        #imgui.text("Position")
        #imgui.begin_child("Space", -1, -1, border=True)
        expanded, self.visible = imgui.collapsing_header("Space", self.visible)
        if not expanded:
            return
        changed, position = imgui.drag_float3(
            "Position", *self.space.position, change_speed=.1
        )
        if changed:
            self.space.position = glm.vec3(*position)
        #imgui.end_child()
        #imgui.end_group()

class SpaceWidgetBuilder(ComponentWidgetBuilder):
    key = Space
    cls = SpaceWidget