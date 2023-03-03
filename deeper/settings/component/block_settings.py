from ...setting import SettingGroup, Vec3Setting


class BlockSettings(SettingGroup):
    pass


BlockSettings.setting_map = {
    'size': Vec3Setting,
    'position': Vec3Setting
}
