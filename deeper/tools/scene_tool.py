#from crunge.engine.view import View
from ..scene_view import SceneView

from ..tool import Tool
from ..state import EditState
class SceneTool(Tool):
    def __init__(self, view: SceneView, title='') -> None:
        super().__init__(view, title)
        self.scene = view.scene
        self.camera = view.scene_camera

class SceneEditTool(SceneTool):
    def __init__(self, view, edit_state: EditState, title='') -> None:
        super().__init__(view, title)
        self.edit_state = edit_state