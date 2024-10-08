"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scene import Scene
"""

from loguru import logger

from ..processor import Processor
from ..scene import Scene

class SceneProcessor(Processor):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene)
        self.scene = scene
