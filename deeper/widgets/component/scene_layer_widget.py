import glm
import imgui

from deeper.scene_layer import SceneLayer
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class SceneLayerWidget(ComponentWidget):
    def __init__(self, group):
        super().__init__(group)
        self.group = group

    def draw(self):
        super().draw()

class SceneLayerWidgetBuilder(ComponentWidgetBuilder):
    key = SceneLayer
    cls = SceneLayerWidget
