import glm
import imgui

from deeper.dimgui import Widget, Window

class BlueprintPanel(Widget):
    def __init__(self, blueprint):
        super().__init__()
        self.blueprint = blueprint

    def draw(self):
        pass

class BlueprintWindow(Window):
    def __init__(self, blueprint):
        super().__init__("Blueprint", [BlueprintPanel(blueprint)])
        self.blueprint = blueprint