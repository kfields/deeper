import glm

from ..constants import *
from .. import Isometry, Cuboid
from .. import Component


class Block(Component):
    def __init__(
        self,
        position=DEFAULT_VEC3,
        size=glm.vec3(1, 1, 1),
        solid=True,
        blueprint=None,
    ) -> None:
        super().__init__(blueprint)
        self._position = position
        self.solid = solid
        self.rotation = DEFAULT_VEC3
        self.isometry = Isometry(*position, *self.rotation)
        self.shape = None
        self.size = size
        self.children = []

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self.isometry = Isometry(*position, *self.rotation)
        # if self.shape:
        #    self.aabb = self.shape.aabb(self.isometry)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        if self.solid:
            self.shape = Cuboid(size.x, size.y, size.z)
            # self.aabb = self.shape.aabb(self.isometry)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        # if shape:
        #    self.aabb = shape.aabb(self.isometry)
        self._shape = shape

    @property
    def aabb(self):
        return self.shape.aabb(self.isometry)

    def add_child(self, child):
        self.children.append(child)

    def cast_ray(self, ray, entity=0):
        if self.shape:
            contact = self.shape.cast_ray(self.isometry, ray)
            if contact:
                return entity, self, contact
            return None
