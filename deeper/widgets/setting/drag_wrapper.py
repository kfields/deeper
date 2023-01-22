import pyglet
import imgui

from deeper.dimgui import Widget

from .. import Icon, IconButton
from deeper.resources.icons import IconsMaterialDesign

class DragWrapper(Widget):
    drag_icon = None

    def __init__(self, wrapped):
        super().__init__([wrapped])
        self.wrapped = wrapped

    def create(self, gui):
        super().create(gui)
        if not DragWrapper.drag_icon:
            font = pyglet.font.load("Material Icons")
            DragWrapper.drag_icon = IconButton(IconsMaterialDesign.ICON_DRAG_INDICATOR, font)
            self.drag_icon.create(gui)
        return self

    def draw(self):
        self.drag_icon.draw()
        if imgui.begin_drag_drop_source():
            #value = self.wrapped.value
            value = self.wrapped.setting
            self.gui.dropboard.value = value
            imgui.button(value.__repr__())
            imgui.end_drag_drop_source()
        
        imgui.same_line()

        super().draw()
