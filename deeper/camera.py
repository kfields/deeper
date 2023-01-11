import arcade
import glm

from .constants import *
from . import Ray

"""
class ScreenCamera(arcade.Camera):
    def __enter__(self):
        self._prev_viewport = self._window.ctx.viewport
        self._prev_projection_2d_matrix =  self._window.ctx.projection_2d_matrix
        self._prev_view_matrix_2d = self._window.ctx.view_matrix_2d
        self.use()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._window.ctx.viewport = self._prev_viewport
        self._window.ctx.projection_2d_matrix = self._prev_projection_2d_matrix
        self._window.ctx.view_matrix_2d = self._prev_view_matrix_2d
"""

class WorldCamera:
    def __init__(self, window, target, zoom=1.0):
        self.window = window
        self.distance = zoom * 10
        self.target = target
        self._zoom = zoom

        self.world_matrix = glm.scale(glm.mat4(1), glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE))
        self.inv_world_matrix = glm.inverse(self.world_matrix)
        
        self.camera = arcade.Camera(zoom=zoom)
        #self.camera = ScreenCamera(zoom=zoom)

        self.update_matrices()
        self.look_at(target, self.distance)

    def __enter__(self):
        self.window.save_ctx_state()
        self.use()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.window.restore_ctx_state()

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

    def resize(self, viewport_width: int, viewport_height: int, *,
               resize_projection: bool = True) -> None:
        self.camera.resize(viewport_width, viewport_height, resize_projection=resize_projection)
        self.look_at(self.target, self.distance)

    def project(self, point):
        return glm.vec3(self.view_matrix * point)

    def unproject(self, point):
        return glm.vec3(self.inv_view * point)

    def look_at(self, target, distance):
        self.target = target
        self.position = target + (self.direction * -distance)

        focal_point = self.project(target).xy - glm.vec2(
            self.camera.viewport[2] / 2, self.camera.viewport[3] / 2
        )
        #print("focal_point: ", focal_point)
        self.camera.move(focal_point)
        self.update_matrices()

    def mouse_to_ray(self, mx, my):
        viewport = self.camera.viewport
        print("viewport: ", viewport)
        viewportWidth = viewport[2]
        viewPortHeight = viewport[3]

        projection = self.camera.projection
        print("projection: ", projection)

        glOrthoWidth = projection[1]
        glOrthoHeight = projection[3]

        x = (2.0 * mx / viewportWidth  - 1) * (glOrthoWidth  / 2)
        y = (2.0 * my / viewPortHeight - 1) * (glOrthoHeight / 2)

        inv_view = glm.inverse(glm.mat4(*self.camera._view_matrix))
        #inv_view = glm.inverse(glm.mat4(*self.window.ctx._view_matrix_2d))
        mouse_vec = glm.vec3(x, y, 0)
        mouse_vec = self.inv_world_matrix * inv_view * mouse_vec
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
