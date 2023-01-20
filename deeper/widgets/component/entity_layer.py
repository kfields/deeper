import glm
import imgui

from deeper.components.entity_group import EntityLayer
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class EntityLayerWidget(ComponentWidget):
    def __init__(self, group):
        super().__init__(group)
        self.group = group

    def draw(self):
        super().draw()

class EntityLayerWidgetBuilder(ComponentWidgetBuilder):
    key = EntityLayer
    cls = EntityLayerWidget
