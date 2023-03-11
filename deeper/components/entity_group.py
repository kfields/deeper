from deeper.event import LayerDirtyEvent, EventSource

class EntityGroup:
    def __init__(self, name: str) -> None:
        self.name = name

class EntityLayer(EntityGroup):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.events = EventSource()

    def mark(self):
        self.events.publish(LayerDirtyEvent())
