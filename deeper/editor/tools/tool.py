from deeper.tool import WorldTool


class WorldEditTool(WorldTool):
    def __init__(self, view, edit_state) -> None:
        super().__init__(view)
        self.edit_state = edit_state