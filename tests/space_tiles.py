import math
import arcade
import glm

from deeper import Space, Body
'''
body = Body((0, 1, 2))
space = Space()
space.add_body(body)
print(space.bodies)
'''

degRads = (math.pi * 2) / 360

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

"""
Let's try creating sprites and batching them according to bounding box z-order
Thinking about doing away with the grid ...
"""

tile_width = 324
tile_height = 200

proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)

view = glm.mat4(1)
view = glm.rotate(view, -57 * degRads, glm.vec3(1, 0, 0))
view = glm.rotate(view, -30 * degRads, glm.vec3(0, 1, 0))

class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.space = Space()
        self.camera = arcade.Camera(zoom=1.5)
        self.tiles = arcade.SpriteList()

        self.create_boxes()
        self.create_sprites()

    def create_boxes(self):
        for ty in range(0, 8):
            y_distance = 252 * ty
            for tx in range(0, 8):
                x_distance = 216 * tx
                self.space.add_body(Body((x_distance, 16, -y_distance)))

    def create_sprites(self):
        sorted_bodies = sorted(self.space.bodies, key=lambda box: box.get_center()[2])
        for box in sorted_bodies:
            sprite = arcade.Sprite("../resources/tiles/Floor8a.png")
            center = box.get_center()
            model = glm.mat4(1)
            pos = proj * view * model * glm.vec4(center[0], center[1], center[2], 1)
            sprite.set_position(pos[0], pos[2])
            self.tiles.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tiles.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        #print(x,y)
        pass

def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
