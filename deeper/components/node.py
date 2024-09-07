import glm

from ..constants import *
from .. import Isometry, Cuboid
from ..ecs.entity import Entity

from .component_builder import ComponentBuilder
from ..scene_layer import SceneLayer
class Node(Entity):
    def __init__(
        self,
        position=DEFAULT_VEC3,
        size=glm.vec3(CELL_WIDTH, 1, 1),
        transform=DEFAULT_VEC3
    ) -> None:
        super().__init__()
        self._position = position
        self.transform = transform
        self.rotation = DEFAULT_VEC3
        self.isometry = Isometry(*position, *self.rotation)
        self.shape = None
        self.size = size
        self.layer: SceneLayer = None

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
        for child in self.children:
            child.position = position + child.transform

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self.shape = Cuboid(size.x, size.y, size.z)

    @property
    def aabb(self):
        return self.shape.aabb(self.isometry)

    def cast_ray(self, ray) -> tuple:
        if self.shape:
            contact = self.shape.cast_ray(self.isometry, ray)
            if contact:
                return self, glm.vec3(contact)
            return None

class NodeBuilder(ComponentBuilder):
    key = 'Node'

    def build(self, blueprint, world):
        # TODO: Shouldn't blueprint size already be a vec3?
        size = glm.vec3(blueprint.size)
        return Node(size=size)
