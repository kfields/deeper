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
        self.target = target
        self.zoom = zoom

        self.proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)
        self.inv_proj = glm.inverse(self.proj)
        
        self.camera = arcade.Camera(zoom=zoom)
        # self.camera = arcade.Camera()
        self.position = glm.vec3(95, 295, 165)
        self.zoom_unit = glm.length(self.position)
        self.distance = zoom * self.zoom_unit
        self.direction = glm.normalize(self.position * -1)
        self.orientation = glm.quatLookAt(self.direction, glm.vec3(0, 1, 0))
        self.view_matrix = glm.lookAt(self.position, glm.vec3(0, 0, 0), glm.vec3(0.0, 1.0, 0.0))

        self.scale = 1/zoom
        self.view_matrix = glm.scale(self.view_matrix, glm.vec3(self.scale, self.scale, self.scale))
        self.view_matrix_zy = glm.mat4(self.view_matrix)
        self.view_matrix_zy[2][1] = .00025 #m9 = z -> y offset

        self.inv_view = glm.inverse(self.view_matrix)

        self.look_at(target, self.distance)

    def use(self):
        self.camera.use()

    def view(self, point, model=glm.mat4(1)):
        return glm.vec3(self.view_matrix * model * point)

    def projectxy(self, point, model=glm.mat4(1)):
        #p = self.proj * self.view_matrix_zy * model * point
        p = self.proj * self.view_matrix * model * point
        return glm.vec2(p.x, p.z + ((p.z * .10) + (p.y * .25)))
        #return (self.proj * self.view_matrix * model * point).xz

    def projectxz(self, point, model=glm.mat4(1)):
        return (self.proj * self.view_matrix * model * point).xz

    def unproject(self, point, model=glm.mat4(1)):
        return glm.vec3(self.inv_proj * self.inv_view * model * point).xz

    def look_at(self, target, distance):
        self.target = target
        self.position = target + (self.direction * -distance)
        #self.position = target + (self.direction * -distance) + glm.vec3(CELL_WIDTH/2, 0, CELL_DEPTH/2)

        focal_point = self.projectxz(target) - glm.vec2(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        )
        print("focal_point: ", focal_point)
        self.camera.move(focal_point)

    def mouse_to_ray(self, mx, my):
        viewportWidth = 800
        viewPortHeight = 600
        glOrthoWidth = 800
        glOrthoHeight = 600

        x = +(2.0 * mx / viewportWidth  - 1) * (glOrthoWidth  / 2)
        y = -(2.0 * my / viewPortHeight - 1) * (glOrthoHeight / 2)

        camera_right = glm.normalize(glm.cross(self.direction, glm.vec3(0,1,0)))
        camera_up = glm.normalize(glm.cross(camera_right, self.direction))
        ray_origin = self.position + camera_right * x + camera_up * -y
        ray_direction = self.direction

        print("viewport: ", self.camera.viewport)
        print("camera position: ", self.position)
        print("ray origin: ", ray_origin)
        print("ray direction: ", ray_direction)
        ray = Ray(*ray_origin, *ray_direction)
        return ray


class Selection:
    def __init__(self, position):
        self.position = position


class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        #self.camera = WorldCamera(self, glm.vec3(0, 0, 0), 1)
        self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*4, 0, CELL_DEPTH*4), 1)
        #self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*8, 0, CELL_DEPTH*8), 1.25)
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
            position = self.camera.projectxz(space.position)
            #print("position: ", pos)
            sprite.set_position(*position)
            self.tiles.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tiles.draw()

        pos = self.camera.projectxy(self.camera.target)
        #print("target screen pos: ", pos)
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.projectxy(self.camera.position)
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)

        if self.selection:
            pos = self.camera.projectxy(self.selection.position)
            #print("contact screen pos: ", pos)
            arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
        arcade.finish_render()

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        print("mouse: ", mouse_x, mouse_y)
        ray = self.camera.mouse_to_ray(mouse_x, mouse_y)
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
