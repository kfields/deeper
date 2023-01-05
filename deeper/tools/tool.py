from deeper.tool import WorldTool


class WorldEditTool(WorldTool):
    def __init__(self, view, edit_state, title='') -> None:
        super().__init__(view, title)
        self.edit_state = edit_state