from loguru import logger

from deeper.builder import Builder
import deeper.widgets.setting

from .kit import Kit

class SettingWidgetKit(Kit):
    builders_path = deeper.widgets.setting
    #builder_type = Builder

    def find(self, setting, cls=None):
        if not cls:
            #cls = setting.__class__
            cls = setting.get_vtype()
        if cls in self.builders:
            return self.builders[cls]
        else:
            base = cls.__bases__[0]
            if base == object:
                return None
            #print(base)
            return self.find(setting, base) #TODO: What if multiple bases?

    def build(self, setting, **kwargs):
        #print(setting.__dict__)
        builder = self.find(setting)
        return builder.build(setting, **kwargs)