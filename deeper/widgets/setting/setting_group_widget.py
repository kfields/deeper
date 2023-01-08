import imgui

from deeper.setting import SettingGroup, SettingGroupVType
from .setting_widget import SettingWidget, SettingWidgetBuilder
from .drop_wrapper import DropWrapper

class SettingGroupWidget(SettingWidget):
    def __init__(self, setting, children=[]):
        from ...kits.setting_widget_kit import SettingWidgetKit
        children = []
        for subsetting in setting.value:
            if isinstance(subsetting, SettingGroup):
                children.append(SettingWidgetKit.instance.build(subsetting))
            else:
                children.append(DropWrapper(SettingWidgetKit.instance.build(subsetting)))
        super().__init__(setting, children)
    """
    def draw(self):
        expanded, visible = imgui.collapsing_header(self.name, self.visible)
        if expanded:
            super().draw()
    """
    def draw(self):
        if imgui.tree_node(self.name):
            super().draw()
            imgui.tree_pop()

class SettingGroupWidgetBuilder(SettingWidgetBuilder):
    #key = SettingGroup
    key = SettingGroupVType
    cls = SettingGroupWidget
