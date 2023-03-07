from .component import Component

class Entity(Component):
    components: dict[object] = None
    def __init__(self) -> None:
        self.components = {}
