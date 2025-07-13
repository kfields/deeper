from loguru import logger
import glm

from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.math.rect import Rect2

from .constants import WORLD_SCALE, WORLD_TILT, WORLD_ROTATION, WORLD_AXIS_X, WORLD_AXIS_Y, WORLD_UP
from . import Ray


class SceneCamera:
    def __init__(self, camera: Camera2D = None, target:glm.vec3=glm.vec3(), zoom=1.0):
        self.camera = camera
        self.target = target
        self.distance = zoom * 10
        self._zoom = zoom

        self.world_matrix = glm.scale(glm.mat4(1), glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE))
        self.inv_world_matrix = glm.inverse(self.world_matrix)
        
        self.update_matrices()
        self.look_at(target)

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

    def update(self, delta_time: float):
        self.camera.update(delta_time)

    def resize(self, size: glm.ivec2) -> None:
        #self.camera.resize(size) # Resized by the view
        self.look_at(self.target)

    def project(self, point):
        return glm.vec3(self.view_matrix * point)

    def unproject(self, point):
        return glm.vec3(self.inv_view * point)

    def pan(self, dx, dy):
        camera_right = glm.normalize(glm.cross(self.direction, WORLD_UP))
        camera_up = glm.normalize(glm.cross(camera_right, self.direction))
        vector = (camera_right * dx) + (camera_up * dy)
        target = self.target + vector / self.distance
        self.look_at(target)

    def look_at(self, target):
        self.target = target
        self.position = target + (self.direction * -self.distance)
        self.update_matrices()
        if self.camera is None:
            return
        focal_point = self.project(target).xy
        #logger.debug("focal_point: {focal_point}")
        self.camera.position = focal_point

    def mouse_to_ray(self, mx, my):
        # Get viewport dimensions
        viewport = self.camera.viewport
        viewportWidth = viewport.width
        viewPortHeight = viewport.height

        frustum = self.camera.frustum
        glOrthoWidth = frustum.width
        glOrthoHeight = frustum.height

        # Convert mouse coordinates to NDC
        x_ndc = (2.0 * mx / viewportWidth) - 1.0
        y_ndc = (2.0 * my / viewPortHeight) - 1.0
        y_ndc = -y_ndc  # Flip Y for WebGPU's coordinate system

        # Convert NDC to world coordinates using the adjusted projection size
        x_world = x_ndc * (glOrthoWidth / 2.0)
        y_world = y_ndc * (glOrthoHeight / 2.0)

        # Transform mouse vector to world space
        inv_view = glm.inverse(glm.mat4(*self.camera.view_matrix))
        mouse_vec = glm.vec3(x_world, y_world, 0)
        mouse_vec = self.inv_world_matrix * inv_view * mouse_vec
        x, y = mouse_vec.xy

        # Compute ray origin and direction
        camera_right = glm.normalize(glm.cross(self.direction, WORLD_UP))
        camera_up = glm.normalize(glm.cross(camera_right, self.direction))
        ray_origin = self.position + (camera_right * x) + (camera_up * y)
        ray_direction = self.direction

        # Return the ray
        ray = Ray(*ray_origin, *ray_direction)
        return ray
