import math
import arcade
import glm

from deeper import Space, Cuboid, Ray

degRads = (math.pi * 2) / 360

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CELL_WIDTH = 216
CELL_DEPTH = 252

ROT_X = 57
ROT_Y = 30


class WorldCamera:
    def __init__(self, window, target, zoom=1.0):
        self.window = window
        self.distance = zoom * 300
        self.target = target
        self.zoom = zoom

        self.proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)
        self.inv_proj = glm.inverse(self.proj)
        
        self.camera = arcade.Camera(zoom=zoom)
        # self.camera = arcade.Camera()
        self.update_view_matrix()
        self.look_at(target, self.distance)

    def update_view_matrix(self):
        """
        tx = self.target[0] + self.target[0] / 2
        ty = self.target[1] + self.target[1] / 2
        self.view_matrix = glm.translate(glm.mat4(1), glm.vec3(tx, 0, ty))
        """
        self.view_matrix = glm.rotate(glm.mat4(1), -ROT_X * degRads, glm.vec3(1, 0, 0))
        self.view_matrix = glm.rotate(
            self.view_matrix, -ROT_Y * degRads, glm.vec3(0, 1, 0)
        )
        scale = 1 / self.zoom
        self.view_matrix = glm.scale(self.view_matrix, glm.vec3(scale, scale, scale))
        self.inv_view = glm.inverse(self.view_matrix)

        self.orientation = glm.rotate(
            glm.quat(), ROT_X * degRads, glm.vec3(1, 0, 0)
        )
        self.orientation = glm.rotate(
            self.orientation, ROT_Y * degRads, glm.vec3(0, 1, 0)
        )
        self.direction = glm.normalize(self.orientation * glm.vec3(0.0, 0.0, 1.0))
        #self.direction = glm.normalize(self.inv_view * glm.vec3(0.0, 0.0, 1.0))
        """        
        self.camera_matrix = glm.rotate(glm.mat4(1), ROT_X * degRads, glm.vec3(1, 0, 0))
        self.camera_matrix = glm.rotate(
            self.camera_matrix, ROT_Y * degRads, glm.vec3(0, 1, 0)
        )
        #self.direction = self.camera_matrix * glm.vec3(0.0, 0.0, 1.0)
        self.direction = self.inv_view * glm.vec3(0.0, 0.0, 1.0)
        """
    def use(self):
        self.camera.use()

    def view(self, point, model=glm.mat4(1)):
        return glm.vec3(self.view_matrix * model * point)

    def project(self, point, model=glm.mat4(1)):
        return glm.vec3(self.proj * self.view_matrix * model * point).xz

    def unproject(self, point, model=glm.mat4(1)):
        return glm.vec3(self.inv_proj * self.inv_view * model * point).xz

    def look_at(self, target, distance):
        self.target = target
        self.position = target + (self.direction * -distance)
        #self.position = target + (self.direction * -distance) + glm.vec3(CELL_WIDTH/2, 0, CELL_DEPTH/2)

        focal_point = self.project(target) - glm.vec2(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        )
        print("focal_point: ", focal_point)
        self.camera.move(focal_point)
        self.update_view_matrix()

    def mouse_to_ray(self, mouse_nds):
        ray_clip = glm.vec4(mouse_nds.xy, -1.0, 1.0)
        ray_eye = self.inv_proj * ray_clip
        print("camera position: ", self.position)
        print("camera direction: ", self.direction)
        print("camera target: ", self.target)
        print("ray_eye: ", ray_eye)
        ray_world = glm.normalize((self.inv_view * ray_eye).xyz)
        print("ray_world: ", ray_world)
        ray = Ray(*self.position, *ray_world)
        return ray


class Selection:
    def __init__(self, position):
        self.position = position


class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.camera = WorldCamera(self, glm.vec3(0, 0, 0), 1.25)
        #self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*4, 0, CELL_DEPTH*4), 1.25)
        # self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*8, 0, CELL_DEPTH*8), 1.25)
        self.tiles = arcade.SpriteList()

        self.space = Space()
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
                position = glm.vec3(x_distance, 16, y_distance)
                print("position: ", position)
                self.space.add_child(
                    Space(position, rotation, shape)
                )

    def create_sprites(self):
        sorted_spaces = sorted(self.space.children, key=lambda space: space.position[2])
        for space in sorted_spaces:
            sprite = arcade.Sprite(
                "../resources/tiles/FloorD3.png", scale=1 / self.camera.zoom
            )
            position = self.camera.project(space.position)
            #print("position: ", pos)
            sprite.set_position(*position)
            self.tiles.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tiles.draw()

        pos = self.camera.project(self.camera.target)
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position)
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)

        if self.selection:
            pos = self.camera.project(self.selection.position)
            arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
        arcade.finish_render()

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        print("mouse: ", mouse_x, mouse_y)
        width, height = self.get_size()
        # normalize device coordinates
        x = (2.0 * mouse_x) / width - 1.0
        y = 1.0 - (2.0 * mouse_y) / height
        z = 1.0
        print("nds: ", x, y, z)
        ray_nds = glm.vec3(x, y, z)
        ray = self.camera.mouse_to_ray(ray_nds)
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
