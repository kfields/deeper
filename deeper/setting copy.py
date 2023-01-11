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
        a.append({"name": key, "value": value})
    return a


class Setting(Data):
    name: str
    # value: object
    # def __init__(self, name) -> None:
    #    self.name = name

    def get_vtype(self):
        return self.__annotations__["value"]


class AttrSetting(Setting):
    obj: object
    vtype: object = None

    def get_vtype(self):
        return self.vtype

    @property
    def value(self):
        return getattr(self.obj, self.name)

    @value.setter
    def value(self, value):
        setattr(self.obj, self.name, value)


SettingGroupVType = list[Setting]


class SettingGroup(Setting):
    value: SettingGroupVType

    @validator("value", pre=True)
    def validate_value(cls, v):
        result = []
        for item in v:
            result.append(cls.setting_map[item["name"]].parse_obj(item))
        return result

BoolSettingVType = bool

class BoolSetting(Setting):
    value: BoolSettingVType

IntSettingVType = int

class IntSetting(Setting):
    value: IntSettingVType

FloatSettingVType = float

class FloatSetting(Setting):
    value: FloatSettingVType

StringSettingVType = str

class StringSetting(Setting):
    value: StringSettingVType

Vec2SettingVType = glm.vec2

class Vec2Setting(Setting):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            glm.vec2: lambda v: list(v),
        }

    value: Vec2SettingVType
    # value: list
    @validator("value", pre=True)
    def validate_value(cls, v):
        return glm.vec2(*v)

Vec3SettingVType = glm.vec3

class Vec3Setting(Setting):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            glm.vec3: lambda v: list(v),
        }

    value: Vec3SettingVType
    # value: list
    @validator("value", pre=True)
    def validate_value(cls, v):
        return glm.vec3(*v)
