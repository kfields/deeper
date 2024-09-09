from crunge.engine.imgui.widget import Widget

from deeper.builder import Builder

class BlueprintWidget(Widget):
    def __init__(self, blueprint):
        super().__init__()
        self.blueprint = blueprint

class BlueprintWidgetBuilder(Builder):
    def build(self, blueprint):
        return self.cls(blueprint)