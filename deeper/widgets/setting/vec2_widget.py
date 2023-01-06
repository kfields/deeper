import imgui

from deeper.setting import Vec2Setting
from .setting_widget import SettingWidget, SettingWidgetBuilder


class Vec2Widget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self):
        changed, self.value = imgui.drag_float2(self.name, self.value)
        

class Vec2WidgetBuilder(SettingWidgetBuilder):
    key = Vec2Setting
    cls = Vec2Widget
