from deeper.dimgui import Widget
from deeper.builder import Builder

class SettingWidget(Widget):
    def __init__(self, setting, children=[]):
        super().__init__(children)
        self.setting = setting
        self.visible = True

    @property
    def name(self):
        return self.setting.name

    @property
    def value(self):
        return self.setting.value

    @value.setter
    def value(self, value):
        self.setting.value = value

class SettingWidgetBuilder(Builder):
    def build(self, setting, **kwargs):
        return self.cls(setting, **kwargs)

class GenericWidgetBuilder(Builder):
    def build(self, setting):
        return self.cls(setting)