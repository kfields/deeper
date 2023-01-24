from loguru import logger

from . import Processor

class SceneProcessor(Processor):
    def __init__(self, scene) -> None:
        super().__init__(scene.world)
        self.scene = scene
