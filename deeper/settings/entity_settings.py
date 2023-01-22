from deeper.setting import SettingGroup, BoolSetting, StringSetting, Vec3Setting, Vec2Setting
from .component import BlockSettings, SpriteVuSettings, SpriteAnimationSettings

class ComponentsGroup(SettingGroup):
    pass


ComponentsGroup.setting_map = {
    "Block": BlockSettings,
    "SpriteVu": SpriteVuSettings,
    "SpriteAnimation": SpriteAnimationSettings
}

class EntitySettings(SettingGroup):
    pass


EntitySettings.setting_map = {
    "_abstract": BoolSetting,
    "extends": StringSetting,
    "category": StringSetting,
    "description": StringSetting,
    "components": ComponentsGroup,

    "size": Vec3Setting,
    "image": StringSetting,
    "offset": Vec2Setting
}
