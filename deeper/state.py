class WorldEditState:
    def __init__(self, world) -> None:
        self.world = world
        self.current_blueprint = None

class BlueprintEditState:
    def __init__(self, world) -> None:
        self.world = world
        self.current_blueprint = None