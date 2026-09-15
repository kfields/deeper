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

    def __init__(self, scene, name = "SceneScreen", title = "Scene Screen"):
        super().__init__(name, title)
        self.scene = scene
    
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
    
    def enable(self):
        super().enable()
        self.scene.enable()

    def disable(self):
        super().disable()
        self.scene.disable()
