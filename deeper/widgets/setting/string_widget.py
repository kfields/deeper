from crunge import imgui
from crunge.engine import Renderer

from deeper.setting import StringSetting, StringSettingVType
from .setting_widget import SettingWidget, SettingWidgetBuilder


class StringWidget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self, renderer: Renderer):
        changed, value = imgui.input_text(
            self.name,
            self.value,
            256
        )
        if changed:
            self.value = value
        

class StringWidgetBuilder(SettingWidgetBuilder):
    #key = StringSetting
    key = StringSettingVType
    cls = StringWidget
