from .component import Component

class Entity(Component):
    components: dict[object] = None
    children: list["Entity"]

    def __init__(self) -> None:
        self.components = {}
        self.children = []

    def add_child(self, child: "Entity"):
        self.children.append(child)
