import glm
import imgui
import pyglet

from deeper.setting import AttrSetting, Vec2SettingVType
from deeper.widgets.setting import DragWrapper
from ...kits.setting_widget_kit import SettingWidgetKit

from deeper.components.sprite_animation import SpriteAnimation
from .component_widget import ComponentWidget, ComponentWidgetBuilder
from .. import IconButton
from deeper.resources.icons.icons_material_design import IconsMaterialDesign


class SpriteAnimationWidget(ComponentWidget):
    def __init__(self, animation):
        super().__init__(animation)
        self.animation = animation

    def draw(self):
        changed, rate = imgui.drag_float(
            "Rate",
            self.animation.rate,
            change_speed=0.01,
            min_value=0.01,
            max_value=1.0,
        )
        if changed:
            self.animation.rate = rate


class SpriteAnimationWidgetBuilder(ComponentWidgetBuilder):
    key = SpriteAnimation
    cls = SpriteAnimationWidget
