from crunge import imgui
from crunge.engine import Renderer

from deeper.setting import BoolSetting, BoolSettingVType
from .setting_widget import SettingWidget, SettingWidgetBuilder


class BoolWidget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self, renderer: Renderer):
        changed, value = imgui.checkbox(self.name, self.value)
        if changed:
            self.value = value

class BoolWidgetBuilder(SettingWidgetBuilder):
    #key = BoolSetting
    key = BoolSettingVType
    cls = BoolWidget
