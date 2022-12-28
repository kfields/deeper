import glm
import imgui

from deeper.vu.sprite_vu import SpriteVu, AnimatedSpriteVu
from .component_widget import ComponentWidget, ComponentWidgetBuilder

class SpriteVuWidget(ComponentWidget):
    def __init__(self, vu):
        super().__init__(vu)
        self.vu = vu

    def draw(self):
        expanded, self.visible = imgui.collapsing_header("Sprite", self.visible)
        if not expanded:
            return
        changed, offset = imgui.drag_float2(
            "Offset", *self.vu.offset, change_speed=0.1
        )
        if changed:
            self.vu.offset = glm.vec2(*offset)

class SpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = SpriteVu
    cls = SpriteVuWidget


class AnimatedSpriteVuWidget(ComponentWidget):
    def __init__(self, vu):
        super().__init__(vu)
        self.vu = vu
    """
    def draw(self):
        #imgui.begin_group()
        #imgui.text("Position")
        changed, self.block.position = imgui.drag_float3(
            "Position", *self.block.position
        )
        #imgui.end_group()
    """

class AnimatedSpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = AnimatedSpriteVu
    cls = AnimatedSpriteVuWidget