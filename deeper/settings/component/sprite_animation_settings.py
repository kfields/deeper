from ...setting import Setting, SettingGroup, StringSetting, IntSetting, FloatSetting, Vec2Setting


class SpriteAnimationSettings(SettingGroup):
    pass


SpriteAnimationSettings.setting_map = {
    "image": StringSetting,
    "offset": Vec2Setting,
    "width": IntSetting,
    "height": IntSetting,
    "frames": IntSetting,
    "rate": FloatSetting
}
