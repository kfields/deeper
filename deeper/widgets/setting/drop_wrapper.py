import pyglet
import imgui

from deeper.dimgui import Widget

from .. import Icon, IconButton
from deeper.resources.icons.icons_material_design import IconsMaterialDesign

class DropWrapper(Widget):
    drag_icon = None

    def __init__(self, wrapped):
        super().__init__([wrapped])
        self.wrapped = wrapped

    def create(self, gui):
        super().create(gui)
        if not DropWrapper.drag_icon:
            font = pyglet.font.load("Material Icons")
            DropWrapper.drag_icon = IconButton(IconsMaterialDesign.ICON_DRAG_INDICATOR, font)
            self.drag_icon.create(gui)
        return self

    """
    def draw(self):
        self.drag_icon.draw()
        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload('itemtype')
            if payload is not None:
                #print('Received:', payload)
                self.wrapped.value = self.gui.dropboard.value
            imgui.end_drag_drop_target()

        imgui.same_line()

        super().draw()
    """
    def draw(self):
        super().draw()
        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload('itemtype')
            if payload is not None:
                #print('Received:', payload)
                self.wrapped.value = self.gui.dropboard.value.value
            imgui.end_drag_drop_target()
