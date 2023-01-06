from ...setting import Setting, SettingGroup, StringSetting, IntSetting, FloatSetting, Vec2Setting

class SpriteVuSettings(SettingGroup):
    pass


SpriteVuSettings.setting_map = {
    "image": StringSetting,
    "offset": Vec2Setting
}


class AnimatedSpriteVuSettings(SettingGroup):
    pass


AnimatedSpriteVuSettings.setting_map = {
    "image": StringSetting,
    "offset": Vec2Setting,
    "width": IntSetting,
    "height": IntSetting,
    "frames": IntSetting,
    "rate": FloatSetting
}
