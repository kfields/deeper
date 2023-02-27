from enum import Enum


class SnapOption(Enum):
    NONE = 0
    CENTER = 1
    SIZE = 2
    CELL = 3
    HALF_CELL = 4
    QUARTER_CELL = 5

class EditState:
    def __init__(self, world) -> None:
        self.world = world
        self.current_blueprint = None

class WorldEditState(EditState):
    def __init__(self, world) -> None:
        super().__init__(world)
        self.snap_option = SnapOption.CENTER
        self.current_layer = None

class EntityEditState(EditState):
    def __init__(self, world, entity) -> None:
        super().__init__(world)
        self.entity = entity
