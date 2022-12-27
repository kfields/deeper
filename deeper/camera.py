import arcade
import glm

from .constants import *
from . import Ray

class WorldCamera:
    def __init__(self, window, target, zoom=1.0):
        self.window = window
        self.distance = zoom * 10
        self.target = target
        self._zoom = zoom

        self.world_matrix = glm.scale(glm.mat4(1), glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE))
        self.inv_world_matrix = glm.inverse(self.world_matrix)

        self.proj = glm.ortho(-1, 1, -1, 1, -1.0, 1.0)
        self.inv_proj = glm.inverse(self.proj)
        
        self.camera = arcade.Camera(zoom=zoom)

        self.update_matrices()
        self.look_at(target, self.distance)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        self._zoom = zoom
        self.camera.zoom = zoom

    def update_matrices(self):
        self.view_matrix = glm.rotate(glm.mat4(1), WORLD_TILT, WORLD_AXIS_X)
        self.view_matrix = glm.rotate(
            self.view_matrix, WORLD_ROTATION, WORLD_AXIS_Y
        )
        self.view_matrix = glm.scale(self.view_matrix, glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE))
        self.inv_view = glm.inverse(self.view_matrix)

        self.direction = glm.normalize(self.inv_view * glm.vec3(0.0, 0.0, -1.0))
        self.orientation = glm.quatLookAt(self.direction, WORLD_UP)

    def use(self):
        self.camera.use()

    def project(self, point, model=glm.mat4(1)):
        return glm.vec3(self.proj * self.view_matrix * model * point)
        #return glm.vec3(self.proj * self.view_matrix * self.world_matrix * model * point)

    def unproject(self, point, model=glm.mat4(1)):
        return glm.vec3(self.inv_proj * self.inv_view * model * point)
        #return glm.vec3(self.inv_proj * self.inv_view * self.inv_world_matrix * model * point)

    def look_at(self, target, distance):
        self.target = target
        self.position = target + (self.direction * -distance)

        focal_point = self.project(target).xy - glm.vec2(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        )
        #print("focal_point: ", focal_point)
        self.camera.move(focal_point)
        self.update_matrices()

    def mouse_to_ray(self, mx, my):
        viewport = self.camera.viewport
        #print("viewport: ", viewport)
        viewportWidth = viewport[2]
        viewPortHeight = viewport[3]

        projection = self.camera.projection
        #print("projection: ", projection)

        glOrthoWidth = projection[1]
        glOrthoHeight = projection[3]

        #mx = mx + SCREEN_WIDTH / 2
        #my = my + SCREEN_HEIGHT / 2

        x = (2.0 * mx / viewportWidth  - 1) * (glOrthoWidth  / 2)
        y = (2.0 * my / viewPortHeight - 1) * (glOrthoHeight / 2)

        #TODO: A little better, but not quite there
        inv_view = glm.inverse(glm.mat4(*self.camera._view_matrix))
        mouse_vec = glm.vec3(x, y, 0)
        mouse_vec = self.inv_world_matrix * inv_view * mouse_vec
        #mouse_vec = self.inv_world_matrix * mouse_vec
        #x, y = (inv_view * mouse_vec).xy
        x, y = mouse_vec.xy * self.zoom

        camera_right = glm.normalize(glm.cross(self.direction, WORLD_UP))
        camera_up = glm.normalize(glm.cross(camera_right, self.direction))
        ray_origin = (self.position + (camera_right * x) + (camera_up * y))
        ray_direction = self.direction

        #print("viewport: ", self.camera.viewport)
        #print("camera position: ", self.position)
        #print("ray origin: ", ray_origin)
        #print("ray direction: ", ray_direction)
        ray = Ray(*ray_origin, *ray_direction)
        return ray
