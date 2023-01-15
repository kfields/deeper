import glm
import imgui
import pyglet

from deeper.setting import AttrSetting
from deeper.widgets.setting import DropWrapper
from deeper.components.sprite_vu import SpriteVu, AnimatedSpriteVu
from .component_widget import ComponentWidget, ComponentWidgetBuilder
from .. import IconButton
from deeper.resources.icons.icons_material_design import IconsMaterialDesign

class SpriteVuWidget(ComponentWidget):
    def __init__(self, vu):
        super().__init__(vu)
        self.vu = vu
        font = pyglet.font.load("Material Icons")
        #self.drag_icon = Icon(IconsMaterialDesign.ICON_DRAG_INDICATOR, font)
        self.drag_icon = IconButton(IconsMaterialDesign.ICON_DRAG_INDICATOR, font)

    def create(self, gui):
        super().create(gui)
        self.drag_icon.create(gui)
        return self

    """
    def draw(self):
        changed, offset = imgui.drag_float2(
            "Offset", *self.vu.offset, change_speed=0.1
        )
        if changed:
            self.vu.offset = glm.vec2(*offset)
    """

    def draw(self):
        self.drag_icon.draw()
        if imgui.begin_drag_drop_source():
            #imgui.set_drag_drop_payload('itemtype', b'payload')
            self.gui.dropboard.value = self.vu.offset
            imgui.button(self.vu.offset.__repr__())
            imgui.end_drag_drop_source()

        imgui.same_line()

        changed, offset = imgui.drag_float2(
            "Offset", *self.vu.offset, change_speed=0.01
        )
        if changed:
            self.vu.offset = glm.vec2(*offset)

class SpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = SpriteVu
    cls = SpriteVuWidget


class AnimatedSpriteVuWidget(ComponentWidget):
    def __init__(self, vu):
        super().__init__(vu)
        self.vu = vu

    def draw(self):
        changed, offset = imgui.drag_float2(
            "Offset", *self.vu.offset, change_speed=0.1
        )
        if changed:
            self.vu.offset = glm.vec2(*offset)


class AnimatedSpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = AnimatedSpriteVu
    cls = AnimatedSpriteVuWidget