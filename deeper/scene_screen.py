from loguru import logger
import glm

from crunge import sdl
from crunge.engine import colors
from crunge.engine.d2.screen import Screen2D
from crunge.engine.d2.camera_2d import Camera2D

from .scene import Scene

from .scene_camera import SceneCamera
from .tool import Tool

from .scene_view import SceneView


class SceneScreen(Screen2D):
    scene: Scene = None

    def __init__(self, scene, title=""):
        super().__init__()
        self.title = title
        self.scene = scene
        # self.scene_camera: SceneCamera = None
        self.dragging = False

    @property
    def ppu(self) -> float:
        return self.camera.ppu

    @property
    def camera(self) -> Camera2D:
        return self.view.camera

    @property
    def scene_camera(self) -> SceneCamera:
        return self.view.scene_camera

    def create_views(self):
        logger.debug("Creating screen views")
        self.view = SceneView(self.scene)
        self.add_child(self.view)

    """
    def _created(self):
        super()._created()
        self.scene_camera = SceneCamera(self.camera)
    """

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

    """
    def on_size(self):
        super().on_size()
        size = self.size
        if self.scene_camera is not None:
            self.scene_camera.resize(size)
    """

    """
    def update(self, delta_time: float):
        self.scene.update(delta_time)
        return super().update(delta_time)
    """

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        down = event.down

        if key == sdl.SDLK_KP_PLUS:
            self.camera.zoom = self.camera.zoom - 0.1
        elif key == sdl.SDLK_KP_MINUS:
            self.camera.zoom = self.camera.zoom + 0.1

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        # logger.debug(f"{self.view.title}:{self.title}:on_mouse_press")
        button = event.button

        if button != 3:
            return
        if event.down:
            self.dragging = True
        else:
            self.dragging = False

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        super().on_mouse_motion(event)
        if not self.dragging:
            return
        zoom = self.scene_camera.zoom
        sensitivity = 0.1
        dx = -event.xrel * zoom * sensitivity
        dy = event.yrel * zoom * sensitivity
        self.scene_camera.pan(dx, dy)

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        # logger.debug(f"{self.title}:on_mouse_wheel")
        self.camera.zoom_pct = self.scene_camera.zoom_pct + event.y * 10
