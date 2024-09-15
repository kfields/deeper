from crunge.engine.view import View

from ..tool import Tool

class SceneTool(Tool):
    def __init__(self, view: View, title='') -> None:
        super().__init__(view, title)
        self.scene = view.scene
        self.camera = self.scene.camera

class SceneEditTool(SceneTool):
    def __init__(self, view, edit_state, title='') -> None:
        super().__init__(view, title)
        self.edit_state = edit_state