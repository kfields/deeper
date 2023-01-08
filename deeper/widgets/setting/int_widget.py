import imgui

from deeper.setting import IntSetting, IntSettingVType
from .setting_widget import SettingWidget, SettingWidgetBuilder


class IntWidget(SettingWidget):
    def __init__(self, setting):
        super().__init__(setting)

    def draw(self):
        changed, self.value = imgui.drag_int(self.name, self.value)
        

class IntWidgetBuilder(SettingWidgetBuilder):
    #key = IntSetting
    key = IntSettingVType
    cls = IntWidget
