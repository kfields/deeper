from deeper import Isometry, Space

child = Space(Isometry(0, 1, 2))
space = Space(Isometry())
space.add_child(child)
print(space.children)