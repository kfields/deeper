from enum import Enum

class SnapOption(Enum):
    NONE = 0
    CENTER = 1
    SIZE = 2
    CELL = 3
    HALF_CELL = 4
    QUARTER_CELL = 5

class WorldEditState:
    def __init__(self, world) -> None:
        self.world = world
        self.current_blueprint = None
        self.snap_option = SnapOption.CENTER
        self.current_layer_group = None

class BlueprintEditState:
    def __init__(self, world) -> None:
        self.world = world
        self.current_blueprint = None

class EntityEditState:
    def __init__(self, world, entity) -> None:
        self.world = world
        self.entity = entity
        self.current_blueprint = None