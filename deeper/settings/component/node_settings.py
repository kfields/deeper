from ...setting import SettingGroup, Vec3Setting


class NodeSettings(SettingGroup):
    pass


NodeSettings.setting_map = {
    'size': Vec3Setting,
    'position': Vec3Setting
}
