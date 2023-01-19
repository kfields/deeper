import glm
import imgui

from deeper.components.group import LayerGroup
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class LayerGroupWidget(ComponentWidget):
    def __init__(self, group):
        super().__init__(group)
        self.group = group

    def draw(self):
        super().draw()

class LayerGroupWidgetBuilder(ComponentWidgetBuilder):
    key = LayerGroup
    cls = LayerGroupWidget
