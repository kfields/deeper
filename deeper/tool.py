class Tool:
    def __init__(self, view) -> None:
        self.view = view
        self.window = view.window

    def enable(self):
        self.window.push_handlers(self)

    def disable(self):
        self.window.remove_handlers(self)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        pass

class WorldTool(Tool):
    def __init__(self, view) -> None:
        super().__init__(view)
        self.world = view.world
        self.camera = view.camera