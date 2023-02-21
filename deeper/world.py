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
        #processor_instance.world = self
        self._processors.append(processor)
        self._processors.sort(key=lambda proc: proc.priority, reverse=True)

    def remove_processor(self, processor: Processor) -> None:
        self._processors.remove(processor)

    def cast_ray(self, ray):
        results = []
        for entity, block in self.get_component(Block):
            result = block.cast_ray(ray, entity)
            if result:
                results.append(result)
        if len(results) == 0:
            return None
        if len(results) == 1:
            return results[0]

        origin = ray.origin
        sorted_results = sorted(
            results, key=lambda result: glm.distance(result[1].position, origin)
        )
        return sorted_results[0]

    def create_layer(self, name):
        #cls_name = f"{name}Layer"
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
        print(layer)
        self.layers.remove(layer)
