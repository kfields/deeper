from ...setting import Setting, SettingGroup, StringSetting, IntSetting, FloatSetting, Vec2Setting

class SpriteVuSettings(SettingGroup):
    pass


SpriteVuSettings.setting_map = {
    "image": StringSetting,
    "offset": Vec2Setting
}
