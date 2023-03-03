from ...setting import SettingGroup, StringSetting, Vec2Setting

class SpriteVuSettings(SettingGroup):
    pass


SpriteVuSettings.setting_map = {
    'image': StringSetting,
    'offset': Vec2Setting
}
