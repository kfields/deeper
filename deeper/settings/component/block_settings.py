from ...setting import Setting, SettingGroup, Vec3Setting

class BlockSettings(SettingGroup):
    pass


BlockSettings.setting_map = {"position": Vec3Setting}
