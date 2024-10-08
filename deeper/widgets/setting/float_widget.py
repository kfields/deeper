from crunge import imgui
from crunge.engine import Renderer

from deeper.setting import FloatSetting, FloatSettingVType
from .setting_widget import SettingWidget, SettingWidgetBuilder


class FloatWidget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self, renderer: Renderer):
        changed, self.value = imgui.drag_float(self.name, self.value)
        

class FloatWidgetBuilder(SettingWidgetBuilder):
    #key = FloatSetting
    key = FloatSettingVType
    cls = FloatWidget
