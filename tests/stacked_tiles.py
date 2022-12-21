import math
import arcade
import glm
from bbox import BBox3D

degRads = (math.pi * 2) / 360

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

"""
Let's see if things stack properly
"""

tile_width = 324
tile_height = 200

proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)

view = glm.mat4(1)
view = glm.rotate(view, -57 * degRads, glm.vec3(1, 0, 0))
view = glm.rotate(view, -30 * degRads, glm.vec3(0, 1, 0))

class Block(BBox3D):
    def __init__(self, x, y, z, path, **kwargs):
        super().__init__(x, y, z, **kwargs)
        self.path = path

class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.blocks = []
        self.camera = arcade.Camera(zoom=1.5)
        self.tiles = arcade.SpriteList()

        self.create_blocks()
        self.create_sprites()

    def create_blocks(self):
        for ty in range(0, 8):
            y_distance = 252 * ty
            for tx in range(0, 8):
                x_distance = 216 * tx
                self.blocks.append(Block(x_distance, 0, -y_distance, ":deeper:tiles/Floor2.png"))
                #self.blocks.append(Block(x_distance, 64, -y_distance, ":deeper:tiles/TileStone5.png"))
                self.blocks.append(Block(x_distance - 40, 100, -y_distance, ":deeper:tiles/Door3/Door30005.png"))

    def create_sprite(self, box, path):
        sprite = arcade.Sprite(path)
        center = box.center
        model = glm.mat4(1)
        pos = proj * view * model * glm.vec4(center[0], center[1], center[2], 1)
        sprite.set_position(pos[0], pos[2])
        self.tiles.append(sprite)

    def create_sprites(self):
        sorted_blocks = sorted(self.blocks, key=lambda box: box.center[2] + box.center[1])
        for box in sorted_blocks:
            #self.create_sprite(box, ":deeper:tiles/Floor2.png")
            self.create_sprite(box, box.path)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tiles.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # print(x,y)
        pass


def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
