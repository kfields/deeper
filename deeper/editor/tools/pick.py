import glm

import arcade

from deeper.tool import WorldTool

class Hover:
    def __init__(self, space, position):
        self.space = space
        self.position = position

class PickTool(WorldTool):
    def __init__(self, view) -> None:
        super().__init__(view)
        self.hover = None

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        print("mouse: ", mouse_x, mouse_y)
        ray = self.camera.mouse_to_ray(mouse_x, mouse_y)
        result = self.world.cast_ray(ray)
        print(result)
        if result:
            space, contact = result
            print("contact: ", contact)
            self.hover = Hover(space, glm.vec3(contact))
        else:
            self.hover = None

    def draw(self):
        if self.hover:
            pos = self.camera.project(self.hover.position).xy
            arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
