import glm

from deeper import Isometry, Shape


class Space:
    def __init__(self, position=glm.vec3(), rotation=glm.vec3(), shape=None) -> None:
        self._position = position
        self.rotation = rotation
        self.isometry = Isometry(*position, *rotation)
        self.children = []
        self.shape = shape

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self.isometry = Isometry(*position, *self.rotation)
        if self.shape:
            self.aabb = self.shape.aabb(self.isometry)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        if shape:
            self.aabb = shape.aabb(self.isometry)
        self._shape = shape

    def add_child(self, child):
        self.children.append(child)

    def cast_ray(self, ray, entity=0):
        if(self.shape):
            contact = self.shape.cast_ray(self.isometry, ray)
            if contact:
                return entity, self, contact
            return None
