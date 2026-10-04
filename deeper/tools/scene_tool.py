from ..scene_view import SceneView

from ..tool import Tool
from ..state import SceneEditState


class SceneTool(Tool):
    def __init__(self, view: SceneView, title="") -> None:
        super().__init__(view, title)
        self.scene = view.scene
        self.camera = view.scene_camera

    def draw(self):
        pass


class SceneEditTool(SceneTool):
    def __init__(self, view, edit_state: SceneEditState, title="") -> None:
        super().__init__(view, title)
        self.edit_state = edit_state
