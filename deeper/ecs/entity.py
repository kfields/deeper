from .component import Component


class Entity(Component):
    def __init__(self) -> None:
        self.components: dict[object] = {}
        self.children: list["Entity"] = []

    def add_child(self, child: "Entity"):
        self.children.append(child)
