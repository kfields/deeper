from pydantic import BaseModel, ValidationError, validator
import glm
from .data import Data

class Setting(Data):
    name: str
    #value: object
    #def __init__(self, name) -> None:
    #    self.name = name

class Settings(Setting):
    def __init__(self, name) -> None:
        super().__init__(name)

class Vec3Setting(Setting):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            glm.vec3: lambda v: list(v),
        }

    value: glm.vec3
    #value: list
    @validator('value', pre=True)
    def validate_value(cls, v):
        return glm.vec3(*v)