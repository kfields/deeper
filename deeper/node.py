from .component import Component
class Node(Component):
    def __init__(self, layer) -> None:
        super().__init__()
        self.layer = layer
