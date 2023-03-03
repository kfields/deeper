from uuid import uuid4

import glm
from . import ecs

from . import Block
from .event import EventSource, LayerDeletedEvent
from .processors import Processor
from .components.entity_group import EntityLayer
from .component import Component

class World(ecs.World):
    def __init__(self, timed=False):
        super().__init__(timed)
        self.events = EventSource()
        self.layers = []
    
    def create_entity(self, *components: object) -> int:
        layer = components[0]
        entity = super().create_entity(*components)
        for component_instance in components:
            if not isinstance(component_instance, Component):
                continue
            component_instance.create(self, entity, layer)
        return entity

    def delete_entity(self, entity: int, immediate: bool = False) -> None:
        block = self.component_for_entity(entity, Block)
        block.layer.mark()
        super().delete_entity(entity, immediate)

    def add_processor(self, processor: Processor, priority=0) -> None:
        processor.priority = priority
        self._processors.append(processor)
        self._processors.sort(key=lambda proc: proc.priority, reverse=True)

    def remove_processor(self, processor: Processor) -> None:
        self._processors.remove(processor)

    def create_layer(self, name):
        uid = uuid4()
        cls_name = f"Layer#{uid}"
        cls = type(cls_name, (EntityLayer,), {})
        layer = cls(name)
        self.add_layer(layer)
        return layer

    def add_layer(self, layer):
        self.layers.append(layer)

    def remove_layer(self, layer):
        self.events.publish(LayerDeletedEvent(layer))
        self.layers.remove(layer)

    def swap_layers(self, i, j):
        self.layers[i], self.layers[j] = self.layers[j], self.layers[i]
