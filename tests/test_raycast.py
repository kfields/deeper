from deeper import Isometry, Ray, HalfSpace

ray = Ray(1.0, 1.0, 1.0, 0.0, -1.0, 0.0)
print(ray)

shape = HalfSpace(1.0, 1.0, 1.0)
print(shape)

isometry = Isometry()
contact = shape.cast_ray(isometry, ray)
print(contact)