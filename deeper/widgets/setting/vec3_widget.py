import glm

from crunge import imgui
from crunge.engine import Renderer

from deeper.setting import Vec3Setting, Vec3SettingVType
from .setting_widget import SettingWidget, SettingWidgetBuilder


class Vec3Widget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self, renderer: Renderer):
        changed, value = imgui.drag_float3(self.name, tuple(self.value))
        if changed:
            self.value = glm.vec3(*value)
        

class Vec3WidgetBuilder(SettingWidgetBuilder):
    #key = Vec3Setting
    key = Vec3SettingVType
    cls = Vec3Widget
