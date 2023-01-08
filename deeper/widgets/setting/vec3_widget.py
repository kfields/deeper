import glm
import imgui

from deeper.setting import Vec3Setting, Vec3SettingVType
from .setting_widget import SettingWidget, SettingWidgetBuilder


class Vec3Widget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self):
        changed, value = imgui.drag_float3(self.name, *self.value)
        if changed:
            self.value = glm.vec3(*value)
        

class Vec3WidgetBuilder(SettingWidgetBuilder):
    #key = Vec3Setting
    key = Vec3SettingVType
    cls = Vec3Widget
