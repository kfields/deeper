from loguru import logger

import imgui

from deeper.dimgui import Window
from deeper.widgets import Selectable, SelectableGroup

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
                children.append(
                    DropWrapper(SettingWidgetKit.instance.build(subsetting))
                )
        super().__init__(setting, children)

    def draw(self):
        if imgui.tree_node(self.name):
            self.draw_context_popup()
            super().draw()
            imgui.tree_pop()

    def draw_context_popup(self):
            if imgui.begin_popup_context_item(self.name):
                clicked, selected = imgui.selectable("Add Setting")
                if clicked:
                    selectables = []
                    for name, cls in self.setting.setting_map.items():
                        selectables.append(
                            Selectable(name, lambda name=name, cls=cls: self.add_setting(name, cls))
                        )
                    win = self.gui.add_child(
                        Window(
                            "Settings",
                            [
                                SelectableGroup(
                                    selectables, lambda: self.gui.remove_child(win)
                                ).create(self.gui)
                            ],
                        )
                    )
                imgui.end_popup()

    def add_setting(self, name, cls):
        from ...kits.setting_widget_kit import SettingWidgetKit
        setting = cls(name)
        self.setting.add_setting(setting)
        if isinstance(setting, SettingGroup):
            self.children.append(
                SettingWidgetKit.instance.build(setting).create(self.gui)
            )
        else:
            self.children.append(
                DropWrapper(SettingWidgetKit.instance.build(setting)).create(self.gui)
            )


class SettingGroupWidgetBuilder(SettingWidgetBuilder):
    # key = SettingGroup
    key = SettingGroupVType
    cls = SettingGroupWidget
