from deeper.dimgui import Widget
from deeper.builder import Builder

class BlueprintWidget(Widget):
    def __init__(self, blueprint):
        super().__init__()
        self.blueprint = blueprint
        self.visible = True

class BlueprintWidgetBuilder(Builder):
    def build(self, blueprint):
        return self.cls(blueprint)