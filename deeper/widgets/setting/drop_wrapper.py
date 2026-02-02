from loguru import logger
from crunge import imgui

from crunge.engine.imgui.widget import Widget

from .. import IconButton
from deeper.resources.icons.icons_material_design import IconsMaterialDesign


class DropWrapper(Widget):
    drag_icon = None

    def __init__(self, wrapped):
        super().__init__([wrapped])
        self.wrapped = wrapped

    """
    def _create(self):
        super()._create()
        self.drag_icon = IconButton(IconsMaterialDesign.ICON_DRAG_INDICATOR)
        self.drag_icon.create()
    """

    def _create(self):
        super()._create()
        if not DropWrapper.drag_icon:
            DropWrapper.drag_icon = IconButton(IconsMaterialDesign.ICON_DRAG_INDICATOR)
            self.drag_icon.enable()

    """
    def _draw(self):
        self.drag_icon.draw()
        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload("itemtype")
            logger.debug(f'Received: {payload}')
            if payload is not None:
                self.wrapped.value = self.gui.dropboard.value.value
            imgui.end_drag_drop_target()

        imgui.same_line()
        
        super()._draw()
    """

    def _draw(self):
        super()._draw()
        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload("itemtype")
            logger.debug(f'Received: {payload}')
            if payload is not None:
                self.wrapped.value = self.gui.dropboard.value.value
            imgui.end_drag_drop_target()
