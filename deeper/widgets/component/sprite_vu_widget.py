from PIL import Image
import imgui
from arcade.resources import resolve_resource_path

from deeper.vu.sprite_vu import SpriteVu, AnimatedSpriteVu
from .component_widget import ComponentWidget, ComponentWidgetBuilder

class SpriteVuWidget(ComponentWidget):
    def __init__(self, vu):
        super().__init__(vu)
        self.vu = vu
    """
    def draw(self):
        #imgui.begin_group()
        #imgui.text("Position")
        changed, self.space.position = imgui.drag_float3(
            "Position", *self.space.position
        )
        #imgui.end_group()
    """

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
        changed, self.space.position = imgui.drag_float3(
            "Position", *self.space.position
        )
        #imgui.end_group()
    """

class AnimatedSpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = AnimatedSpriteVu
    cls = AnimatedSpriteVuWidget