from deeper import Isometry, Ray, HalfSpace, Cuboid

hit_ray = Ray(0.0, 1.0, 0.0, 0.0, -1.0, 0.0)
print(hit_ray)

miss_ray = Ray(0.0, 1.0, 0.0, 0.0, 1.0, 0.0)
print(miss_ray)

shape = HalfSpace(1.0, 1.0, 1.0)
print(shape)

isometry = Isometry()

contact = shape.cast_ray(isometry, hit_ray)
print(f'hit: {contact}')

contact = shape.cast_ray(isometry, miss_ray)
print(f'miss: {contact}')

# Cuboid
shape = Cuboid(1.0, 0.5, 1.0)
print(shape)

isometry = Isometry()

contact = shape.cast_ray(isometry, hit_ray)
print(f'hit: {contact}')

contact = shape.cast_ray(isometry, miss_ray)
print(f'miss: {contact}')