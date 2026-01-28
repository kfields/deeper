import glm

from crunge import imgui

from deeper.setting import Vec2SettingVType
from .setting_widget import SettingWidget, SettingWidgetBuilder


class Vec2Widget(SettingWidget):
    def __init__(self, setting, v_speed=1):
        super().__init__(setting)
        self.v_speed = v_speed

    def _draw(self):
        changed, value = imgui.drag_float2(
            self.name, tuple(self.value), v_speed=self.v_speed
        )
        if changed:
            self.value = glm.vec2(*value)


class Vec2WidgetBuilder(SettingWidgetBuilder):
    # key = Vec2Setting
    key = Vec2SettingVType
    cls = Vec2Widget
