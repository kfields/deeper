from crunge import imgui
from crunge.engine.imgui.widget import Widget

from deeper.state import SnapOption
from deeper.widgets.button import RadioButton, RadioButtonGroup


class SnapOptionWidget(Widget):
    def __init__(self, edit_state, children=...):
        children = [
            RadioButtonGroup(
                [
                    RadioButton("None", lambda: self.set_snap(SnapOption.NONE)),
                    RadioButton(
                        "Center", lambda: self.set_snap(SnapOption.CENTER), True
                    ),
                    RadioButton("Size", lambda: self.set_snap(SnapOption.SIZE)),
                    RadioButton(
                        "1/2 Cell", lambda: self.set_snap(SnapOption.HALF_CELL)
                    ),
                    RadioButton(
                        "1/4 Cell", lambda: self.set_snap(SnapOption.QUARTER_CELL)
                    ),
                ]
            )
        ]
        super().__init__(children)
        self.edit_state = edit_state

    def set_snap(self, value):
        self.edit_state.snap_option = value

    def _draw(self):
        imgui.text("SnapOption")
        imgui.begin_child("SnapOption", (0, 0), imgui.ChildFlags.BORDERS)
        super()._draw()
        imgui.end_child()
