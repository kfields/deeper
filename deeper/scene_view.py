from loguru import logger
import glm

from crunge import sdl
from crunge.engine import colors
from crunge.engine.d2.view import View2D

from .scene import Scene

from .scene_camera import SceneCamera
from .tool import Tool


# Each wheel notch / keypress multiplies or divides zoom by this.
# Multiplicative steps feel the same at every zoom level and can't reach zero.
ZOOM_STEP = 1.1


class SceneView(View2D):
    scene: Scene = None

    def __init__(self, scene, title=""):
        super().__init__()
        self.title = title
        self.scene = scene
        self.scene_camera: SceneCamera = None
        self.dragging = False

    def _reset(self):
        super()._reset()
        scratch = self.scratch  # initialize the Scratch overlay

    def _created(self):
        super()._created()
        self.scene_camera = SceneCamera(self.camera)

    @property
    def tool(self) -> Tool:
        return self.controller

    @tool.setter
    def tool(self, tool: Tool):
        self.controller = tool

    def enable(self):
        super().enable()
        self.scene.enable()

    def disable(self):
        super().disable()
        self.scene.disable()

    def on_size(self):
        super().on_size()
        size = self.size
        if self.scene_camera is not None:
            self.scene_camera.resize(size)

    def update(self, delta_time: float):
        self.scene.update(delta_time)
        return super().update(delta_time)

    # -- zoom --------------------------------------------------------------

    def zoom_by(self, steps: float):
        """Zoom in (steps > 0) or out (steps < 0). Always goes through
        SceneCamera so its zoom and Camera2D's stay in sync."""
        if self.scene_camera is None:
            return
        self.scene_camera.zoom = self.scene_camera.zoom * (ZOOM_STEP ** steps)

    def on_key(self, event: sdl.KeyboardEvent):
        if not event.down:
            return  # otherwise key release zooms a second time

        key = event.key
        if key == sdl.SDLK_KP_PLUS:
            self.zoom_by(1)
        elif key == sdl.SDLK_KP_MINUS:
            self.zoom_by(-1)

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        self.zoom_by(event.y)

    # -- pan ---------------------------------------------------------------

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        if event.button != 3:
            return
        self.dragging = event.down

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        super().on_mouse_motion(event)
        if not self.dragging:
            return
        # Raw pixel delta. SceneCamera.pan converts pixels to world units using
        # the zoomed frustum, so the scene tracks the cursor 1:1 at any zoom.
        # Negated X: dragging right moves the view left, so the scene follows the mouse.
        # Y is not negated because screen Y points down and view Y points up.
        self.scene_camera.pan(-event.xrel, event.yrel)

    # -- drawing -----------------------------------------------------------

    def _draw(self):
        super()._draw()
        if self.tool is not None:
            self.tool.draw()

        with self.renderer.render_pass():
            self.scene.draw()

    def draw_aabb(self, aabb, color=colors.YELLOW):
        bbl = self.scene_camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.minz)).xy
        bbr = self.scene_camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.minz)).xy
        fbl = self.scene_camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.maxz)).xy
        fbr = self.scene_camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.maxz)).xy

        btl = self.scene_camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.minz)).xy
        btr = self.scene_camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.minz)).xy
        ftl = self.scene_camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.maxz)).xy
        ftr = self.scene_camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.maxz)).xy

        # Bottom
        self.scratch.draw_segment(bbl, bbr, color)
        self.scratch.draw_segment(fbl, fbr, color)
        self.scratch.draw_segment(bbl, fbl, color)
        self.scratch.draw_segment(bbr, fbr, color)
        # Top
        self.scratch.draw_segment(btl, btr, color)
        self.scratch.draw_segment(ftl, ftr, color)
        self.scratch.draw_segment(btl, ftl, color)
        self.scratch.draw_segment(btr, ftr, color)
        # Sides
        self.scratch.draw_segment(bbl, btl, color)
        self.scratch.draw_segment(fbl, ftl, color)
        self.scratch.draw_segment(bbr, btr, color)
        self.scratch.draw_segment(fbr, ftr, color)