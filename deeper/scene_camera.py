from loguru import logger
import glm

from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.math.rect import Rect2

from .constants import WORLD_SCALE, WORLD_TILT, WORLD_ROTATION, WORLD_AXIS_X, WORLD_AXIS_Y, WORLD_UP
from . import Ray


class SceneCamera:
    """
    Orthographic scene camera. Zoom semantics: higher zoom = more zoomed in.

    Zoom is owned entirely by the underlying Camera2D (its frustum shrinks as
    zoom grows). Nothing in this class scales by zoom directly; screen-space
    deltas are converted through the frustum/viewport ratio, so they're
    zoom-correct automatically.
    """

    # How far behind the target rays start (and where `position` sits).
    # Orthographic, so this has no visual effect -- it just needs to clear the scene.
    RAY_BACKOFF = 1000.0

    def __init__(self, camera: Camera2D = None, target: glm.vec3 = None, zoom: float = 1.0):
        self.camera = camera
        self.target = glm.vec3(target) if target is not None else glm.vec3()
        self.distance = self.RAY_BACKOFF
        self._zoom = zoom

        self.world_matrix = glm.scale(glm.mat4(1), glm.vec3(WORLD_SCALE))
        self.inv_world_matrix = glm.inverse(self.world_matrix)

        self.update_matrices()

        if self.camera is not None:
            self.camera.zoom = zoom
        self.look_at(self.target)

    # --- zoom -------------------------------------------------------------

    @property
    def zoom(self) -> float:
        return self._zoom

    @zoom.setter
    def zoom(self, zoom: float):
        if zoom <= 0:
            zoom = 0.1
        self._zoom = zoom
        if self.camera is not None:
            self.camera.zoom = zoom
        self.look_at(self.target)

    @property
    def zoom_pct(self) -> float:
        return self._zoom * 100.0

    @zoom_pct.setter
    def zoom_pct(self, pct: float):
        if pct <= 0:
            pct = 10
        self.zoom = pct / 100.0

    # --- matrices ---------------------------------------------------------

    def update_matrices(self):
        # The view orientation is fixed (doesn't depend on target or zoom),
        # so this only needs to run when the WORLD_* constants change.
        self.view_matrix = glm.rotate(glm.mat4(1), WORLD_TILT, WORLD_AXIS_X)
        self.view_matrix = glm.rotate(self.view_matrix, WORLD_ROTATION, WORLD_AXIS_Y)
        self.view_matrix = glm.scale(self.view_matrix, glm.vec3(WORLD_SCALE))
        self.inv_view = glm.inverse(self.view_matrix)

        # Camera basis in world space, taken straight from the inverse view.
        self.direction = glm.normalize(self.view_to_world_vector(0.0, 0.0, -1.0))
        self.right = glm.normalize(self.view_to_world_vector(1.0, 0.0, 0.0))
        self.up = glm.normalize(self.view_to_world_vector(0.0, 1.0, 0.0))
        self.orientation = glm.quatLookAt(self.direction, WORLD_UP)

    def update(self, delta_time: float):
        self.camera.update(delta_time)

    def resize(self, size: glm.ivec2) -> None:
        # Camera2D is resized by the view.
        self.look_at(self.target)

    # --- space conversions ------------------------------------------------

    def project(self, point):
        return glm.vec3(self.view_matrix * point)

    def unproject(self, point):
        return glm.vec3(self.inv_view * point)

    def view_to_world_vector(self, x: float, y: float, z: float = 0.0) -> glm.vec3:
        """Direction/offset in view units -> world units (undoes rotation and WORLD_SCALE)."""
        return glm.vec3(self.inv_view * glm.vec4(x, y, z, 0.0))

    def pixels_per_view_unit(self) -> glm.vec2 | None:
        """Screen pixels per view unit, or None before the camera has a viewport.

        Camera2D's frustum is viewport_size / ppu / zoom, so this equals
        ppu * zoom: zoomed out = fewer pixels per unit = more world per pixel.
        """
        size = self.camera.viewport_size
        frustum = self.camera.frustum
        if frustum is None or frustum.width <= 0 or frustum.height <= 0:
            return None
        return glm.vec2(size.x / frustum.width, size.y / frustum.height)

    def screen_to_view_offset(self, mx: float, my: float) -> glm.vec2:
        """Mouse position -> offset from screen center, in view units (+y up)."""
        ppu = self.pixels_per_view_unit()
        if ppu is None:
            return glm.vec2(0.0, 0.0)
        size = self.camera.viewport_size
        x = (mx - size.x * 0.5) / ppu.x
        y = (size.y * 0.5 - my) / ppu.y  # flip Y: screen down, view up
        return glm.vec2(x, y)

    # --- navigation -------------------------------------------------------

    def pan(self, dx: float, dy: float):
        """Pan by a screen-space delta in pixels. Zoomed out pans farther per pixel."""
        ppu = self.pixels_per_view_unit()
        if ppu is None:
            return
        offset = self.view_to_world_vector(dx / ppu.x, dy / ppu.y)
        self.look_at(self.target + offset)

    def look_at(self, target):
        self.target = glm.vec3(target)
        self.position = self.target - self.direction * self.distance
        if self.camera is None:
            return
        self.camera.position = self.project(self.target).xy

    # --- picking ----------------------------------------------------------

    def mouse_to_ray(self, mx: float, my: float) -> Ray:
        offset = self.screen_to_view_offset(mx, my)
        point = self.target + self.view_to_world_vector(offset.x, offset.y)
        origin = point - self.direction * self.distance
        return Ray(*origin, *self.direction)