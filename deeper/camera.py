from loguru import logger
import arcade
import glm

from .constants import *
from . import Ray


class WorldCamera:
    def __init__(self, window, target, zoom=1.0):
        self.window = window
        self.target = target
        self.distance = zoom * 10
        self._zoom = zoom

        self.world_matrix = glm.scale(glm.mat4(1), glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE))
        self.inv_world_matrix = glm.inverse(self.world_matrix)
        
        self.camera = arcade.Camera(zoom=zoom)

        self.update_matrices()
        self.look_at(target)

    def __enter__(self):
        self.window.push_ctx_state()
        self.use()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.window.pop_ctx_state()

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        self._zoom = zoom
        self.distance = zoom * 10
        self.camera.zoom = zoom
        self.look_at(self.target)

    @property
    def zoom_pct(self):
        return  1 / self._zoom * 100

    @zoom_pct.setter
    def zoom_pct(self, pct):
        if pct <= 0:
            pct = 10
        self.zoom = 100 / pct

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

    def update(self):
        self.camera.update()

    def resize(self, viewport_width: int, viewport_height: int, *,
               resize_projection: bool = True) -> None:
        self.camera.resize(viewport_width, viewport_height, resize_projection=resize_projection)
        self.look_at(self.target)

    def project(self, point):
        return glm.vec3(self.view_matrix * point)

    def unproject(self, point):
        return glm.vec3(self.inv_view * point)

    def pan(self, dx, dy):
        camera_right = glm.normalize(glm.cross(self.direction, WORLD_UP))
        camera_up = glm.normalize(glm.cross(camera_right, self.direction))
        #vector = (camera_right * dx) + (camera_up * dy) * self.zoom
        vector = (camera_right * dx) + (camera_up * dy)
        target = self.target + vector / self.distance
        self.look_at(target)

    def look_at(self, target):
        self.target = target
        self.position = target + (self.direction * -self.distance)
        self.update_matrices()
        #focal_point = self.project(target).xy * 1/self.zoom
        focal_point = self.project(target).xy
        #print("focal_point: ", focal_point)
        self.camera.center(focal_point)

    def mouse_to_ray(self, mx, my):
        viewport = self.camera.viewport
        #print("viewport: ", viewport)
        viewportWidth = viewport[2]
        viewPortHeight = viewport[3]

        projection = self.camera.projection
        #print("projection: ", projection)

        glOrthoWidth = projection[1]
        glOrthoHeight = projection[3]

        x = (2.0 * mx / viewportWidth  - 1) * (glOrthoWidth  / 2)
        y = (2.0 * my / viewPortHeight - 1) * (glOrthoHeight / 2)

        inv_view = glm.inverse(glm.mat4(*self.camera._view_matrix))
        mouse_vec = glm.vec3(x, y, 0)
        mouse_vec = self.inv_world_matrix * inv_view * mouse_vec
        #x, y = mouse_vec.xy * self.zoom
        x, y = mouse_vec.xy

        camera_right = glm.normalize(glm.cross(self.direction, WORLD_UP))
        camera_up = glm.normalize(glm.cross(camera_right, self.direction))
        ray_origin = self.position + (camera_right * x) + (camera_up * y)
        ray_direction = self.direction

        #print("viewport: ", self.camera.viewport)
        #print("camera position: ", self.position)
        #print("ray origin: ", ray_origin)
        #print("ray direction: ", ray_direction)
        ray = Ray(*ray_origin, *ray_direction)
        return ray
