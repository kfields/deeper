import math
import arcade
import glm

from deeper import Space, Cuboid, Ray
'''
body = Body((0, 1, 2))
space = Space()
space.add_body(body)
print(space.bodies)
'''

degRads = (math.pi * 2) / 360

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CELL_WIDTH = 216
CELL_HEIGHT = 216
CELL_DEPTH = 252
"""
Let's try creating sprites and batching them according to bounding box z-order
Thinking about doing away with the grid ...
"""

proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)
inv_proj = glm.inverse(proj)

view = glm.mat4(1)
view = glm.rotate(view, -57 * degRads, glm.vec3(1, 0, 0))
view = glm.rotate(view, -30 * degRads, glm.vec3(0, 1, 0))
inv_view = glm.inverse(view)

class Eye:
    def __init__(self, position):
        self.position = position

class Selection:
    def __init__(self, position):
        self.position = position

class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.camera = arcade.Camera(zoom=1.5)
        self.tiles = arcade.SpriteList()

        self.space = Space()
        self.eye = Eye(glm.vec3(0, 1000, 1000))
        self.selection = None

        self.create_boxes()
        self.create_sprites()

    def create_boxes(self):
        rotation = glm.vec3()
        shape = Cuboid(CELL_WIDTH, 16, CELL_DEPTH)
        for ty in range(0, 8):
            y_distance = CELL_DEPTH * ty
            for tx in range(0, 8):
                x_distance = CELL_WIDTH * tx
                self.space.add_child(Space(glm.vec3(x_distance, 16, -y_distance), rotation, shape))

    def create_sprites(self):
        sorted_spaces = sorted(self.space.children, key=lambda space: space.position[2])
        for space in sorted_spaces:
            sprite = arcade.Sprite("../resources/tiles/Floor8a.png")
            model = glm.mat4(1)
            pos = proj * view * model * space.position
            sprite.set_position(pos[0], pos[2])
            self.tiles.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tiles.draw()
        if self.selection:
            model = glm.mat4(1)
            pos = proj * view * model * self.selection.position
            arcade.draw_line(0, 0, pos[0], pos[1], arcade.color.YELLOW, 2)
        arcade.finish_render()
    '''
    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        #print(x,y)
        width, height = self.get_size()
        #normalize device coordinates
        x = (2.0 * mouse_x) / width - 1.0
        #x = mouse_x
        y = 1.0 - (2.0 * mouse_y) / height
        #y = mouse_y
        z = 1.0
        #z = 1000.0
        #print(x, y, z)
        ray_nds = glm.vec3(x, y, z)
        ray_clip = glm.vec4(ray_nds.xy, -1.0, 1.0)
        #ray_clip = glm.vec3(ray_nds.xy, -1.0)
        ray_eye = inv_proj * ray_clip
        print("ray_eye: ", ray_eye)
        ray_world = (inv_view * ray_eye).xyz
        #ray_world = glm.vec3(ray_world[0]*width, ray_world[1]*height, ray_world[2])
        #ray_world = inv_view * ray_eye
        ray_world = glm.normalize(ray_world)
        print("ray_world: ", ray_world)
        #ray = Ray(0.0, 100.0, 100.0, *ray_world)
        ray = Ray(ray_world[0]*width, ray_world[1]*height, ray_world[2], ray_eye[0], ray_eye[1], ray_eye[2])
        #ray = Ray(0, 1000, 1000, ray_eye[0], ray_eye[1], ray_eye[2])
        contact = self.space.cast_ray(ray)
        print(contact)
        '''

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        #print(x,y)
        width, height = self.get_size()
        #normalize device coordinates
        x = (2.0 * mouse_x) / width - 1.0
        #x = mouse_x
        y = 1.0 - (2.0 * mouse_y) / height
        #y = mouse_y
        z = 1.0
        #z = 1000.0
        #print(x, y, z)
        ray_nds = glm.vec3(x, y, z)
        #ray_clip = glm.vec4(ray_nds.xy, -1.0, 1.0)
        ray_clip = glm.vec3(ray_nds.xy, -1.0)
        #ray_eye = glm.normalize(inv_proj * ray_clip)
        ray_eye = inv_proj * ray_clip
        print("ray_eye: ", ray_eye)

        model = glm.mat4(1)
        pos = inv_proj * inv_view * model * self.eye.position

        #ray_world = (pos).xyz
        ray_world = pos
        #ray_world = glm.vec3(ray_world[0]*width, ray_world[1]*height, ray_world[2])
        #ray_world = inv_view * ray_eye
        #ray_world = glm.normalize(ray_world)
        print("ray_world: ", ray_world)
        #ray = Ray(0.0, 100.0, 100.0, *ray_world)
        ray = Ray(ray_world[0], ray_world[1], ray_world[2], ray_eye[0], ray_eye[1], ray_eye[2])
        #ray = Ray(0, 1000, 1000, ray_eye[0], ray_eye[1], ray_eye[2])
        contact = self.space.cast_ray(ray)
        print(contact)
        if contact:
            self.selection = Selection(glm.vec3(contact))
        else:
            self.selection = None

def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
