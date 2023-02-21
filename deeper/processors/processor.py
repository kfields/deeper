from .. import ecs


class Processor(ecs.Processor):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def enable(self):
        self.world.add_processor(self)

    def disable(self):
        self.world.remove_processor(self)