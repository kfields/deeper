import math
import glm
import arcade
import esper

from deeper import Block, Cuboid, Ray

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CELL_WIDTH = 222
CELL_HEIGHT = 16
CELL_DEPTH = 254

WORLD_TILT = math.radians(33)
WORLD_ROTATION = math.radians(-30)

WORLD_UP = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)

class WorldCamera:
    def __init__(self, window, target, zoom=1.0):
        self.window = window
        self.distance = zoom * 500
        self.target = target
        self.zoom = zoom

        self.proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)
        self.inv_proj = glm.inverse(self.proj)
        
        self.camera = arcade.Camera(zoom=zoom)

        self.update_matrices()
        self.look_at(target, self.distance)

    def update_matrices(self):
        self.view_matrix = glm.rotate(glm.mat4(1), WORLD_TILT, WORLD_AXIS_X)
        self.view_matrix = glm.rotate(
            self.view_matrix, WORLD_ROTATION, WORLD_AXIS_Y
        )
        scale = 1 / self.zoom
        self.view_matrix = glm.scale(self.view_matrix, glm.vec3(scale, scale, scale))

        self.inv_view = glm.inverse(self.view_matrix)

        self.direction = glm.normalize(self.inv_view * glm.vec3(0.0, 0.0, -1.0))
        self.orientation = glm.quatLookAt(self.direction, WORLD_UP)

    def use(self):
        self.camera.use()

    def project(self, point, model=glm.mat4(1)):
        return glm.vec3(self.proj * self.view_matrix * model * point)

    def unproject(self, point, model=glm.mat4(1)):
        return glm.vec3(self.inv_proj * self.inv_view * model * point)

    def look_at(self, target, distance):
        self.target = target
        self.position = target + (self.direction * -distance)
        focal_point = self.project(target).xy - glm.vec2(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        )
        print("target: ", target)
        print("focal_point: ", focal_point)
        self.camera.move(focal_point)
        self.update_matrices()

    def mouse_to_ray(self, mx, my):
        viewportWidth = 800
        viewPortHeight = 600
        glOrthoWidth = 800
        glOrthoHeight = 600

        x = (2.0 * mx / viewportWidth  - 1) * (glOrthoWidth  / 2)
        y = (2.0 * my / viewPortHeight - 1) * (glOrthoHeight / 2)

        camera_right = glm.normalize(glm.cross(self.direction, glm.vec3(0,1,0)))
        camera_up = glm.normalize(glm.cross(camera_right, self.direction))
        ray_origin = self.position + camera_right * x + camera_up * y
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

class Processor(esper.Processor):
    @property
    def scene(self) -> "Scene":
        return self.world

class SpriteVu:
    sprite: arcade.Sprite = None
    position: glm.vec3 = glm.vec3()
    def __init__(self, sprite: arcade.Sprite) -> None:
        self.sprite = sprite

class RenderingProcessor(Processor):
    def process(self):
        self.scene.tile_vu_list = []
        self.scene.tile_list = arcade.SpriteList()

        for ent, (block, vu) in self.scene.get_components(Block, SpriteVu):
            position = self.scene.camera.project(block.position)
            vu.position = position
            #print("position: ", position)
            vu.sprite.set_position(*position.xy)
            self.scene.tile_vu_list.append(vu)

        self.scene.tile_vu_list = sorted(self.scene.tile_vu_list, key=lambda vu: vu.position.z)
        for vu in self.scene.tile_vu_list:
            self.scene.tile_list.append(vu.sprite)


class Scene(arcade.View, esper.World):
    def __init__(self, window=None):
        super().__init__(window)
        esper.World.__init__(self)

        self.add_processor(RenderingProcessor())
        self.camera = WorldCamera(self, glm.vec3(), 1)
        #self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*4, 0, CELL_DEPTH*4), 1)
        #self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*8, 0, CELL_DEPTH*8), 1)
        self.tile_vu_list = []
        self.tile_list = arcade.SpriteList()
        self.block = Block()
        self.selection = None

        self.create_blocks()
        #self.create_sprites()

    def create_blocks(self):
        rotation = glm.vec3()
        shape = Cuboid(CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH)
        for ty in range(0, 8):
            y_distance = CELL_DEPTH * ty
            for tx in range(0, 8):
                x_distance = CELL_WIDTH * tx
                position = glm.vec3(x_distance, CELL_HEIGHT, y_distance)
                #print("position: ", position)
                block = Block(position, rotation, shape)
                self.block.add_child(block)
                vu = SpriteVu(arcade.Sprite(
                    ":deeper:tiles/FloorD3.png", scale=1 / self.camera.zoom
                ))
                self.create_entity(block, vu)

    def on_update(self, delta_time: float):
        self.process()
        return super().on_update(delta_time)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tile_list.draw()

        #self.draw_aabbs()

        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)

        if self.selection:
            pos = self.camera.project(self.selection.position).xy
            arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
        arcade.finish_render()

    def draw_aabbs(self):
        for block in self.block.children:
            self.draw_aabb(block)

    def draw_aabb(self, block):
        aabb = block.aabb
        bbl = self.camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.minz))
        bbr = self.camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.minz))
        fbl = self.camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.maxz))
        fbr = self.camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.maxz))

        btl = self.camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.minz))
        btr = self.camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.minz))
        ftl = self.camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.maxz))
        ftr = self.camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.maxz))

        arcade.draw_line(bbl.x, bbl.y, bbr.x, bbr.y, arcade.color.YELLOW)
        #arcade.draw_line(fbl.x, fbl.y, fbr.x, fbr.y, arcade.color.YELLOW)
        arcade.draw_line(bbl.x, bbl.y, fbl.x, fbl.y, arcade.color.YELLOW)

        arcade.draw_line(btl.x, btl.y, btr.x, btr.y, arcade.color.YELLOW)
        #arcade.draw_line(fbl.x, fbl.y, fbr.x, fbr.y, arcade.color.YELLOW)
        arcade.draw_line(btl.x, btl.y, ftl.x, ftl.y, arcade.color.YELLOW)

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        print("mouse: ", mouse_x, mouse_y)
        ray = self.camera.mouse_to_ray(mouse_x, mouse_y)
        result = self.block.cast_ray(ray)
        print(result)
        if result:
            block, contact = result
            print("contact: ", contact)
            self.selection = Selection(contact)
        else:
            self.selection = None

class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.scene = Scene(self)
        self.show_view(self.scene)


def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
