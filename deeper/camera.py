import math
import arcade
import glm

from .constants import *
from . import Ray

class WorldCamera:
    def __init__(self, window, target, zoom=1.0):
        self.window = window
        self.distance = zoom * 300
        self.target = target
        self.zoom = zoom

        self.proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)
        self.inv_proj = glm.inverse(self.proj)
        
        self.camera = arcade.Camera(zoom=zoom)

        self.update_matrices()
        self.look_at(target, self.distance)

    def update_matrices(self):
        """
        tx = self.target[0] + self.target[0] / 2
        ty = self.target[1] + self.target[1] / 2
        self.view_matrix = glm.translate(glm.mat4(1), glm.vec3(tx, 0, ty))
        """
        self.view_matrix = glm.rotate(glm.mat4(1), math.radians(-ROT_X), WORLD_AXIS_X)
        self.view_matrix = glm.rotate(
            self.view_matrix, math.radians(-ROT_Y), WORLD_AXIS_Y
        )
        scale = 1 / self.zoom
        self.view_matrix = glm.scale(self.view_matrix, glm.vec3(scale, scale, scale))
        #self.view_matrix[2][1] = .00025 #m9 = z -> y offset

        self.inv_view = glm.inverse(self.view_matrix)

        self.orientation = glm.rotate(
            glm.quat(), math.radians(ROT_X), WORLD_AXIS_X
        )
        self.orientation = glm.rotate(
            self.orientation, math.radians(ROT_Y), WORLD_AXIS_Y
        )
        #self.direction = glm.normalize(self.orientation * glm.vec3(0.0, 0.0, 1.0))
        self.direction = glm.normalize(self.inv_view * glm.vec3(0.0, 0.0, 1.0))

    def use(self):
        self.camera.use()

    def project(self, point, model=glm.mat4(1)):
        return glm.vec3(self.proj * self.view_matrix * model * point)

    def unproject(self, point, model=glm.mat4(1)):
        return glm.vec3(self.inv_proj * self.inv_view * model * point)

    def look_at(self, target, distance):
        self.target = target
        self.position = target + (self.direction * -distance)
        #self.position = target + (self.direction * -distance) + glm.vec3(CELL_WIDTH/2, 0, CELL_DEPTH/2)

        focal_point = self.project(target).xy - glm.vec2(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        )
        print("focal_point: ", focal_point)
        self.camera.move(focal_point)
        self.update_matrices()

    def mouse_to_ray(self, mx, my):
        viewportWidth = 800
        viewPortHeight = 600
        glOrthoWidth = 800
        glOrthoHeight = 600

        x = -(2.0 * mx / viewportWidth  - 1) * (glOrthoWidth  / 2)
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
