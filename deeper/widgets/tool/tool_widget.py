from crunge.engine.imgui.widget import Widget

class ToolWidget(Widget):
    def __init__(self, tool, children=...):
        super().__init__(children)
        self.tool = tool