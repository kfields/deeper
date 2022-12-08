import glm

from deeper import Isometry, Shape


class Space:
    def __init__(self, position=glm.vec3(), rotation=glm.vec3(), shape=None) -> None:
        self.position = position
        self.rotation = rotation
        self.shape = shape
        self.isometry = Isometry(*position, *rotation)
        if shape:
            self.aabb = shape.aabb(self.isometry)

        #print(self.isometry)
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def cast_ray(self, ray):
        if(self.shape):
            return self.shape.cast_ray(self.isometry, ray)
        for child in self.children:
            contact = child.cast_ray(ray)
            if contact:
                return contact