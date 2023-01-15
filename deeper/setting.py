import glm


def decompose(d):
    a = []
    for key, value in d.items():
        if not value:
            value = []
        elif type(value) is dict:
            value = decompose(value)
        a.append({"name": key, "value": value})
    return a

class Subscription:
    def __init__(self, callback) -> None:
        self.callback = callback

class Setting:
    name: str
    _value: object = None
    vtype: object = None

    def __init__(self, name, value=None, vtype=None) -> None:
        self.name = name
        if not value:
            value = self.default()
        self._value = value
        if vtype:
            self.vtype = vtype
        self.subscriptions = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} value={self.value}>"

    @classmethod
    def parse_obj(cls, obj):
        v = cls.validate(obj["value"])
        return cls(obj["name"], v)

    def get_vtype(self):
        return self.__annotations__["_value"]

    @classmethod
    def validate(cls, value):
        return value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for subscription in self.subscriptions:
            subscription.callback(self)

    def subscribe(self, callback):
        self.subscriptions.append(Subscription(callback))

    def unsubscribe(self, subscription):
        self.subscriptions.remove(subscription)

    def to_dict(self):
        #return { self.name, self.value }
        return self.value

class AttrSetting(Setting):
    def get_vtype(self):
        return self.vtype

    @property
    def value(self):
        return getattr(self._value, self.name)

    @value.setter
    def value(self, value):
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

    def default(self):
        return []

    def add_setting(self, setting):
        value = self.value
        value.append(setting)
        self.value = value
        #TODO: Temporary hack until I can figure it out
        setting.subscriptions = self.subscriptions
    
    def subscribe(self, callback):
        super().subscribe(callback)
        for setting in self.value:
            setting.subscribe(callback)

    def to_dict(self):
        d = {}
        for setting in self.value:
            #d[setting.name] = setting.value
            d[setting.name] = setting.to_dict()
        return d

BoolSettingVType = bool


class BoolSetting(Setting):
    _value: BoolSettingVType
    def default(self):
        return False

IntSettingVType = int


class IntSetting(Setting):
    _value: IntSettingVType
    def default(self):
        return 0


FloatSettingVType = float


class FloatSetting(Setting):
    _value: FloatSettingVType
    def default(self):
        return 0.0


StringSettingVType = str


class StringSetting(Setting):
    _value: StringSettingVType
    def default(self):
        return ""


Vec2SettingVType = glm.vec2


class Vec2Setting(Setting):
    _value: Vec2SettingVType

    @classmethod
    def validate(cls, v):
        return glm.vec2(*v)

    def default(self):
        return glm.vec2()

    def to_dict(self):
        return list(self._value)
        
Vec3SettingVType = glm.vec3


class Vec3Setting(Setting):
    _value: Vec3SettingVType

    @classmethod
    def validate(cls, v):
        return glm.vec3(*v)

    def default(self):
        return glm.vec3()

    def to_dict(self):
        return list(self._value)
