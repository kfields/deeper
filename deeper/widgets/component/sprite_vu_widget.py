import glm
import imgui
import pyglet

from deeper.setting import AttrSetting, Vec2SettingVType
from deeper.widgets.setting import DragWrapper
from ...kits.setting_widget_kit import SettingWidgetKit

from deeper.components.sprite_vu import SpriteVu
from .component_widget import ComponentWidget, ComponentWidgetBuilder
from .. import IconButton
from deeper.resources.icons.icons_material_design import IconsMaterialDesign


class SpriteVuWidget(ComponentWidget):
    def __init__(self, vu):
        self.vu = vu
        children = []
        children.append(
            DragWrapper(
                SettingWidgetKit.instance.build(
                    AttrSetting("offset", self.vu, Vec2SettingVType), change_speed=0.01
                )
            )
        )
        super().__init__(vu, children)


class SpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = SpriteVu
    cls = SpriteVuWidget
