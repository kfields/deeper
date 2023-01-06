from ...setting import Setting, SettingGroup, Vec3Setting, Vec2Setting


class BlockSettings(SettingGroup):
    pass


BlockSettings.setting_map = {
    "size": Vec3Setting,
    "position": Vec3Setting
}
