from deeper import Space, Body

body = Body((0, 1, 2))
space = Space()
space.add_body(body)
print(space.bodies)