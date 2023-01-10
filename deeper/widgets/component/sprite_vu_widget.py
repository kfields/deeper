import glm
import imgui
import pyglet

from deeper.setting import AttrSetting, Vec2SettingVType
from deeper.widgets.setting import DragWrapper
from ...kits.setting_widget_kit import SettingWidgetKit

from deeper.components.sprite_vu import SpriteVu, AnimatedSpriteVu
from .component_widget import ComponentWidget, ComponentWidgetBuilder
from .. import IconButton
from deeper.resources.icons.icons_material_design import IconsMaterialDesign


class SpriteVuWidget(ComponentWidget):
    """
    def __init__(self, vu):
        super().__init__(vu)
        self.vu = vu
        font = pyglet.font.load("Material Icons")
        self.drag_icon = IconButton(IconsMaterialDesign.ICON_DRAG_INDICATOR, font)

    def create(self, gui):
        super().create(gui)
        self.drag_icon.create(gui)
    """

    def __init__(self, vu):
        self.vu = vu
        children = []
        children.append(
            DragWrapper(
                SettingWidgetKit.instance.build(
                    AttrSetting("offset", self.vu, Vec2SettingVType),
                    change_speed=0.01
                )
            )
        )
        super().__init__(vu, children)

    """
    def draw(self):
        changed, offset = imgui.drag_float2(
            "Offset", *self.vu.offset, change_speed=0.1
        )
        if changed:
            self.vu.offset = glm.vec2(*offset)
    """
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
    """


class SpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = SpriteVu
    cls = SpriteVuWidget


class AnimatedSpriteVuWidget(ComponentWidget):
    def __init__(self, vu):
        super().__init__(vu)
        self.vu = vu

    def draw(self):
        changed, offset = imgui.drag_float2("Offset", *self.vu.offset, change_speed=0.1)
        if changed:
            self.vu.offset = glm.vec2(*offset)


class AnimatedSpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = AnimatedSpriteVu
    cls = AnimatedSpriteVuWidget
