import glm
import imgui

from deeper.setting import Vec2Setting, Vec2SettingVType
from .setting_widget import SettingWidget, SettingWidgetBuilder


class Vec2Widget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self):
        changed, value = imgui.drag_float2(self.name, *self.value)
        if changed:
            self.value = glm.vec2(*value)
        

class Vec2WidgetBuilder(SettingWidgetBuilder):
    #key = Vec2Setting
    key = Vec2SettingVType
    cls = Vec2Widget
