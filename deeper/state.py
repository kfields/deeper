from enum import Enum


class SnapOption(Enum):
    NONE = 0
    CENTER = 1
    SIZE = 2
    CELL = 3
    HALF_CELL = 4
    QUARTER_CELL = 5

class EditState:
    def __init__(self, scene) -> None:
        self.scene = scene
        self.current_blueprint = None

class LevelEditState(EditState):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.snap_option = SnapOption.CENTER
        self.current_layer = None

class EntityEditState(EditState):
    def __init__(self, scene, entity) -> None:
        super().__init__(scene)
        self.entity = entity
