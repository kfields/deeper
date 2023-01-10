from deeper.widgets.tool import ToolWidget
from deeper.widgets.state import SnapOptionWidget

class StampToolWidget(ToolWidget):
    def __init__(self, tool, children=...):
        # children = [RadioButton('Test', lambda: None, True)]
        children = [SnapOptionWidget(tool.edit_state)]
        super().__init__(tool, children)
