from crunge import imgui
from crunge.engine import Renderer

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

    def draw(self, renderer: Renderer):
        changed, rate = imgui.drag_float(
            'Rate',
            self.animation.rate,
            v_speed=0.01,
            v_min=0.01,
            v_max=1.0,
        )
        if changed:
            self.animation.rate = rate


class SpriteAnimationWidgetBuilder(ComponentWidgetBuilder):
    key = SpriteAnimation
    cls = SpriteAnimationWidget
