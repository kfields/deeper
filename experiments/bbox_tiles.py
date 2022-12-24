import math
import arcade
import glm
from bbox import BBox3D

degRads = (math.pi * 2) / 360

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

"""
Let's try 3d bounding boxes where ty starts at the bottom and correlates to z
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
        self.grid = []
        self.camera = arcade.Camera(zoom=1.5)
        self.tiles = arcade.SpriteList()

        self.create_grid()
        self.create_sprites()

    def create_grid(self):
        for ty in range(0, 8):
            row = []
            y_distance = 252 * ty
            for tx in range(0, 8):
                x_distance = 216 * tx
                row.append(BBox3D(x_distance, 16, -y_distance))
            self.grid.append(row)

    def create_sprites(self):
        for row in reversed(self.grid):
            for box in row:
                sprite = arcade.Sprite(":deeper:tiles/Floor8a.png")
                center = box.center
                model = glm.mat4(1)
                pos = proj * view * model * glm.vec4(center[0], center[1], center[2], 1)
                sprite.set_position(pos[0], pos[2])
                self.tiles.append(sprite)

    def on_draw(self):
        arcade.start_render()
        #self.camera.use()
        self.tiles.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        #print(x,y)
        pass

def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
