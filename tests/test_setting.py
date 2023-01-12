import json
from pydantic.json import pydantic_encoder

from deeper.setting import Setting, SettingGroup, Vec3Setting

# setting = Vec3Setting('position').parse_obj([1, 2, 3])
setting = Vec3Setting.parse_obj({"name": "position", "value": [1, 2, 3]})
print(setting)
# print(json.dumps(setting, indent=4, default=pydantic_encoder))
#print(setting.json())


class BlockSettings(SettingGroup):
    pass


BlockSettings.setting_map = {"position": Vec3Setting}


group = BlockSettings.parse_obj(
    {"name": "Block", "value": [{"name": "position", "value": [1, 2, 3]}]}
)
print(group)


class ComponentsGroup(SettingGroup):
    pass


ComponentsGroup.setting_map = {"Block": BlockSettings}

components_group = ComponentsGroup.parse_obj(
    {
        "name": "components",
        "value": [
            {"name": "Block", "value": [{"name": "position", "value": [1, 2, 3]}]}
        ],
    }
)
print(components_group)


class EntitySettings(SettingGroup):
    pass


EntitySettings.setting_map = {"components": ComponentsGroup}

entity_settings = EntitySettings.parse_obj(
    {
        "name": "Floor1",
        "value": [
            {
                "name": "components",
                "value": [
                    {
                        "name": "Block",
                        "value": [{"name": "position", "value": [1, 2, 3]}],
                    }
                ],
            }
        ],
    }
)
print(entity_settings)

vtype = entity_settings.get_vtype()
print(vtype)

d = entity_settings.to_dict()
print(d)