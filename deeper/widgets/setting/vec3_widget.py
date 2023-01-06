import imgui

from deeper.setting import Vec3Setting
from .setting_widget import SettingWidget, SettingWidgetBuilder


class Vec3Widget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self):
        changed, self.value = imgui.drag_float3(self.name, self.value)
        

class Vec3WidgetBuilder(SettingWidgetBuilder):
    key = Vec3Setting
    cls = Vec3Widget
