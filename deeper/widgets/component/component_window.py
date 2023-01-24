from deeper.dimgui import Window
from deeper.kits.component_widget_kit import ComponentWidgetKit

class ComponentWindow(Window):
    def __init__(self, component):
        self.component = component
        children = []
        children.append(ComponentWidgetKit.instance.build(component))
        #super().__init__(component.__class__.__name__, children)
        super().__init__(component.__class__.__qualname__, children)
