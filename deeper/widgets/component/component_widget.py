from deeper.dimgui import Widget
from deeper.builder import Builder

class ComponentWidget(Widget):
    def __init__(self, component):
        super().__init__()
        self.component = component
        self.name = component.__class__.__name__
        self.visible = True

class ComponentWidgetBuilder(Builder):
    def build(self, component):
        return self.cls(component)