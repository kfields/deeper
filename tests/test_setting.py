import json
from pydantic.json import pydantic_encoder

from deeper.setting import Vec3Setting

#setting = Vec3Setting('position').parse_obj([1, 2, 3])
setting = Vec3Setting.parse_obj({ 'name': 'position', 'value': [1, 2, 3]})
print(setting)
#print(json.dumps(setting, indent=4, default=pydantic_encoder))
print(setting.json())