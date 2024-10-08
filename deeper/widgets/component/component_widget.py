from crunge.engine.imgui.widget import Widget

from deeper.builder import Builder

class ComponentWidget(Widget):
    def __init__(self, component, children=[]):
        super().__init__(children)
        self.component = component
        self.name = component.__class__.__name__

class ComponentWidgetBuilder(Builder):
    def build(self, component):
        return self.cls(component)