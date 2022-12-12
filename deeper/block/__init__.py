import glm

from deeper import Space
from deeper import Cuboid

class Block(Space):
    def __init__(self, position=glm.vec3(), rotation=glm.vec3(), extents=glm.vec3(1,1,1)) -> None:
        super().__init__(position, rotation)
        self.shape = Cuboid(extents.x, extents.y, extents.z)