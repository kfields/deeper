from deeper.setting import SettingGroup, BoolSetting, StringSetting, DictSetting, Vec3Setting, Vec2Setting
from .component import NodeSettings, BlockSettings, SpriteVuSettings, SpriteAnimationSettings

class ComponentsGroup(SettingGroup):
    pass


ComponentsGroup.setting_map = {
    'Node': NodeSettings,
    'Block': BlockSettings,
    'SpriteVu': SpriteVuSettings,
    'SpriteAnimation': SpriteAnimationSettings
}

class EntitySettings(SettingGroup):
    pass


EntitySettings.setting_map = {
    '_abstract': BoolSetting,
    'extends': StringSetting,
    'category': StringSetting,
    'description': StringSetting,
    'components': ComponentsGroup,
    'children': DictSetting,

    'transform': Vec3Setting,
    'size': Vec3Setting,
    'image': StringSetting,
    'offset': Vec2Setting
}
