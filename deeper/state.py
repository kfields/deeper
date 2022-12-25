class WorldEditState:
    def __init__(self, world) -> None:
        self.world = world
        self.current_blueprint = None

class BlueprintEditState:
    def __init__(self, world) -> None:
        self.world = world
        self.current_blueprint = None

class EntityEditState:
    def __init__(self, world, entity) -> None:
        self.world = world
        self.entity = entity
        self.current_blueprint = None