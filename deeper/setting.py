#from pydantic import BaseModel, ValidationError, validator
from dataclasses import dataclass

import glm
from .data_transfer import DataTransfer


def decompose(d):
    a = []
    for key, value in d.items():
        if not value:
            value = []
        elif type(value) is dict:
            value = decompose(value)
        a.append({"name": key, "value": value})
    return a


#class Setting(DataTransfer):
@dataclass
class Setting:
    name: str
    _value: object = None
    vtype: object = None
    # value: object
    # def __init__(self, name) -> None:
    #    self.name = name
    @classmethod
    def parse_obj(cls, obj):
        v = cls.validate(obj["value"])
        #return cls(obj["name"], obj["value"])
        return cls(obj["name"], v)

    def get_vtype(self):
        return self.__annotations__["_value"]

    @classmethod
    def validate(cls, value):
        return value

    @property
    def value(self):
        #return getattr(self.obj, self.name)
        return self._value

    @value.setter
    def value(self, value):
        self._value =  value

class AttrSetting(Setting):
    #obj: object

    def get_vtype(self):
        return self.vtype

    @property
    def value(self):
        #return getattr(self.obj, self.name)
        return getattr(self._value, self.name)

    @value.setter
    def value(self, value):
        #setattr(self.obj, self.name, value)
        setattr(self._value, self.name, value)


SettingGroupVType = list[Setting]


class SettingGroup(Setting):
    _value: SettingGroupVType

    @classmethod
    def validate(cls, v):
        result = []
        for item in v:
            result.append(cls.setting_map[item["name"]].parse_obj(item))
        return result

BoolSettingVType = bool

class BoolSetting(Setting):
    _value: BoolSettingVType

IntSettingVType = int

class IntSetting(Setting):
    _value: IntSettingVType

FloatSettingVType = float

class FloatSetting(Setting):
    _value: FloatSettingVType

StringSettingVType = str

class StringSetting(Setting):
    _value: StringSettingVType

Vec2SettingVType = glm.vec2

class Vec2Setting(Setting):
    _value: Vec2SettingVType
    # value: list
    @classmethod
    def validate(cls, v):
        return glm.vec2(*v)

Vec3SettingVType = glm.vec3

class Vec3Setting(Setting):
    _value: Vec3SettingVType
    # value: list
    @classmethod
    def validate(cls, v):
        return glm.vec3(*v)
