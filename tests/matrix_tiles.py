import math
import arcade
import glm

degRads = (math.pi*2)/360

SCALE = 1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.camera = arcade.Camera(zoom=1.5)
        self.tiles = arcade.SpriteList()
        ty = 0
        tile_width = 324
        tile_height = 200
        offset = (0, 100 * 8) 
        x_degrees = -17.33
        x_angle = x_degrees*degRads
        y_degrees = x_degrees - 120
        y_angle = y_degrees*degRads

        proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)
        view = glm.mat4(1)
        view = glm.rotate(view, x_angle, glm.vec3(0, 0, 1))

        for ty in range(0, 8):
            y_distance = 170 * ty
            for tx in range(0, 8):
                sprite = arcade.Sprite(":deeper:tiles/Floor8a.png", SCALE)
                x_distance = 200 * tx

                model = glm.mat4(1)
                pos = view * model * glm.vec4(x_distance, y_distance, 1, 1)
                #pos = proj * view * model * glm.vec4(x_distance, y_distance, y_distance, 1)

                sprite.set_position(pos[0] * SCALE, pos[1] * SCALE)
                self.tiles.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tiles.draw()


def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
