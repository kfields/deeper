from ...setting import Setting, SettingGroup, BoolSetting, StringSetting, IntSetting, FloatSetting, Vec2Setting


class SpriteAnimationSettings(SettingGroup):
    pass


SpriteAnimationSettings.setting_map = {
    "image": StringSetting,
    "offset": Vec2Setting,
    "width": IntSetting,
    "height": IntSetting,
    "frames": IntSetting,
    "rate": FloatSetting,
    "pingpong": BoolSetting, # Play forwards then backwards
}
