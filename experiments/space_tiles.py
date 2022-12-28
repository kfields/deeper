import math
import arcade
import glm

from deeper import Isometry, Block
'''
body = Body((0, 1, 2))
block = Block()
block.add_body(body)
print(block.bodies)
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
        self.block = Block()
        self.camera = arcade.Camera(zoom=1.5)
        self.tiles = arcade.SpriteList()

        self.create_boxes()
        self.create_sprites()

    def create_boxes(self):
        for ty in range(0, 8):
            y_distance = 252 * ty
            for tx in range(0, 8):
                x_distance = 216 * tx
                self.block.add_child(Block(glm.vec3(x_distance, 16, -y_distance)))

    def create_sprites(self):
        sorted_spaces = sorted(self.block.children, key=lambda block: block.position[2])
        for block in sorted_spaces:
            sprite = arcade.Sprite(":deeper:tiles/Floor8a.png")
            model = glm.mat4(1)
            pos = proj * view * model * block.position
            sprite.set_position(pos[0], pos[2])
            self.tiles.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tiles.draw()

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        pass

def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
