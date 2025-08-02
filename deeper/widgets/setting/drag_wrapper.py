from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.imgui.widget import Widget

from .. import Icon, IconButton
from deeper.resources.icons import IconsMaterialDesign

class DragWrapper(Widget):
    drag_icon = None

    def __init__(self, wrapped):
        super().__init__([wrapped])
        self.wrapped = wrapped

    def _create(self):
        super()._create()
        if not DragWrapper.drag_icon:
            DragWrapper.drag_icon = IconButton(IconsMaterialDesign.ICON_DRAG_INDICATOR)
            self.drag_icon.create()

    def _draw(self):
        self.drag_icon.draw()
        if imgui.begin_drag_drop_source():
            value = self.wrapped.setting
            self.gui.dropboard.value = value
            imgui.button(f"{value.__repr__()}##{str(self.id)}")
            imgui.end_drag_drop_source()
        
        imgui.same_line()

        super()._draw()
