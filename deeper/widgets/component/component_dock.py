from crunge.engine.imgui.widget import Dock

from deeper.kits.component_widget_kit import ComponentWidgetKit

class ComponentDock(Dock):
    def __init__(self, component):
        self.component = component
        children = []
        children.append(ComponentWidgetKit.instance.build(component))
        super().__init__(component.__class__.__qualname__, children)
