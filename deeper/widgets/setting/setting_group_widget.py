import imgui

from deeper.setting import SettingGroup
from .setting_widget import SettingWidget, SettingWidgetBuilder


class SettingGroupWidget(SettingWidget):
    def __init__(self, setting, children=[]):
        from ...kits.setting_widget_kit import SettingWidgetKit
        children = []
        for subsetting in setting.value:
            children.append(SettingWidgetKit.instance.build(subsetting))
        super().__init__(setting, children)

    def draw(self):
        expanded, visible = imgui.collapsing_header(self.name, self.visible)
        if expanded:
            super().draw()

class SettingGroupWidgetBuilder(SettingWidgetBuilder):
    key = SettingGroup
    cls = SettingGroupWidget
