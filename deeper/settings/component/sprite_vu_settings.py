from ...setting import Setting, SettingGroup, Vec2Setting

class SpriteVuSettings(SettingGroup):
    pass


SpriteVuSettings.setting_map = {"offset": Vec2Setting}


class AnimatedSpriteVuSettings(SettingGroup):
    pass


AnimatedSpriteVuSettings.setting_map = {"offset": Vec2Setting}
