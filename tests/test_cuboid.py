from deeper import Cuboid, Isometry, Aabb

shape = Cuboid(1.0, 1.0, 1.0)
print(shape)

pos = Isometry(1, 1, 1)

aabb = shape.aabb(pos)
print(aabb)