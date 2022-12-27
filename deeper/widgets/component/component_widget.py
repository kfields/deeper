from PIL import Image
import imgui
from arcade.resources import resolve_resource_path

from deeper.dimgui import Widget
from deeper.builder import Builder

class ComponentWidget(Widget):
    def __init__(self, component):
        super().__init__()
        self.component = component
        self.visible = True

class ComponentWidgetBuilder(Builder):
    def build(self, component):
        return self.cls(component)