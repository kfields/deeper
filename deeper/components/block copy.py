import glm

from ..constants import *
from .. import Isometry, Cuboid
from .. import Component
from .component_builder import ComponentBuilder

class Block(Component):
    def __init__(
        self,
        position=DEFAULT_VEC3,
        size=glm.vec3(CELL_WIDTH, 1, 1),
        solid=True
    ) -> None:
        super().__init__()
        self._position = position
        self.solid = solid
        self.rotation = DEFAULT_VEC3
        self.isometry = Isometry(*position, *self.rotation)
        self.shape = None
        self.size = size
        self.children = []
        self.layer = None

    def create(self, world, entity, layer):
        self.layer = layer

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self.isometry = Isometry(*position, *self.rotation)
        self.layer.mark()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        if self.solid:
            self.shape = Cuboid(size.x, size.y, size.z)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
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
                return entity, self, glm.vec3(contact)
            return None

class BlockBuilder(ComponentBuilder):
    key = 'Block'

    def build(self, blueprint, world):
        # TODO: Shouldn't blueprint size already be a vec3?
        size = glm.vec3(blueprint.size)
        return Block(size=size)
