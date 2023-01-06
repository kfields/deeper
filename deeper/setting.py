from pydantic import BaseModel, ValidationError, validator
import glm
from .data import Data


def decompose(d):
    a = []
    for key, value in d.items():
        if not value:
            value = []
        elif type(value) is dict:
            value = decompose(value)
        a.append({'name': key, 'value': value})
    return a

class Setting(Data):
    name: str
    # value: object
    # def __init__(self, name) -> None:
    #    self.name = name


class SettingGroup(Setting):
    value: list[Setting]

    @validator("value", pre=True)
    def validate_value(cls, v):
        result = []
        for item in v:
            result.append(cls.setting_map[item["name"]].parse_obj(item))
        return result

class BoolSetting(Setting):
    value: bool

class IntSetting(Setting):
    value: int

class FloatSetting(Setting):
    value: float

class StringSetting(Setting):
    value: str

class Vec2Setting(Setting):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            glm.vec2: lambda v: list(v),
        }

    value: glm.vec2
    # value: list
    @validator("value", pre=True)
    def validate_value(cls, v):
        return glm.vec2(*v)

class Vec3Setting(Setting):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            glm.vec3: lambda v: list(v),
        }

    value: glm.vec3
    # value: list
    @validator("value", pre=True)
    def validate_value(cls, v):
        return glm.vec3(*v)
