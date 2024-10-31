from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.imgui.widget import Widget

from .. import IconButton
from deeper.resources.icons.icons_material_design import IconsMaterialDesign

class DropWrapper(Widget):
    drag_icon = None

    def __init__(self, wrapped):
        super().__init__([wrapped])
        self.wrapped = wrapped

    #def _create(self, gui):
    def _create(self):
        #super()._create(gui)
        super()._create()
        if not DropWrapper.drag_icon:
            DropWrapper.drag_icon = IconButton(IconsMaterialDesign.ICON_DRAG_INDICATOR)
            #self.drag_icon.create(self.gui)
            self.drag_icon.config(gui=self.gui).create()
        return self

    def draw(self, renderer: Renderer):
        super().draw(renderer)
        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload('itemtype')
            if payload is not None:
                #print('Received:', payload)
                self.wrapped.value = self.gui.dropboard.value.value
            imgui.end_drag_drop_target()
