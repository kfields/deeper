from loguru import logger
import glm

from crunge.engine.d2.camera_2d import Camera2D

from .constants import *
from . import Ray


class WorldCamera:
    def __init__(self, camera: Camera2D, target:glm.vec3=glm.vec3(), zoom=1.0):
        self.target = target
        self.distance = zoom * 10
        self._zoom = zoom

        self.world_matrix = glm.scale(glm.mat4(1), glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE))
        self.inv_world_matrix = glm.inverse(self.world_matrix)
        
        #self.camera = Camera2D(zoom=zoom)
        #self.camera = Camera2D()
        #self.camera = Camera2D(glm.vec3(0,0,0), glm.vec2(1024, 768))
        self.camera = camera

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
        self.camera.resize(size)
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
        self.camera.position = focal_point

    def mouse_to_ray(self, mx, my):
        viewport = self.camera.frustrum
        #print("viewport: ", viewport)
        viewportWidth = viewport.width
        viewPortHeight = viewport.height

        projection = self.camera.frustrum
        #print("projection: ", projection)
        inv_view = glm.inverse(glm.mat4(*self.camera.view_matrix))

        glOrthoWidth = projection.width
        glOrthoHeight = projection.height

        #x = (2.0 * mx / viewportWidth  - 1) * (glOrthoWidth  / 2)
        #y = (2.0 * my / viewPortHeight - 1) * (glOrthoHeight / 2)
        x = (2.0 * mx / viewportWidth  - 1) * (glOrthoWidth  / 2)
        y = (2.0 * my / viewPortHeight - 1) * (glOrthoHeight / 2)
        y = -y
        logger.debug(f"mouse: x={x}, y={y}")

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
