import math
import arcade

degRads = (math.pi*2)/360

SCALE = 1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.camera = arcade.Camera(zoom=1.5)
        self.tiles = arcade.SpriteList()
        tile_width = 324
        tile_height = 200
        offset_x = 0
        offset_y = 100 * 8
        x_degrees = -17.33
        x_angle = x_degrees*degRads
        y_degrees = x_degrees - 120
        y_angle = y_degrees*degRads
        for ty in range(0, 8):
            y_distance = 170 * ty
            x1 = offset_x + (y_distance*(math.cos(y_angle)))
            y1 = offset_y + (y_distance*(math.sin(y_angle)))
            for tx in range(0, 8):
                sprite = arcade.Sprite(":deeper:tiles/Floor8a.png", SCALE)
                x_distance = 200 * tx
                x = x1 + (x_distance*(math.cos(x_angle)))
                y = y1 + (x_distance*(math.sin(x_angle)))

                sprite.set_position(x * SCALE, y * SCALE)
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
