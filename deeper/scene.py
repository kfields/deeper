from uuid import uuid4

import glm

from loguru import logger

from crunge.engine import Renderer

from .ecs import World
from .ecs.component import Component
from .processor import Processor

from . import Block
from .scene_layer import SceneLayer
#from .scene_camera import SceneCamera

from .event import EventSource, LayerDeletedEvent

class Scene(World):
    def __init__(self, timed:bool=False):
        super().__init__(timed)
        #self.camera: SceneCamera = None
        self.events = EventSource()
        self.layers: list[SceneLayer] = []

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

    def add_processors(self, processors: list[Processor]):
        for processor in processors:
            self.add_processor(processor)

    def remove_processors(self, processors: list[Processor]):
        for processor in processors:
            self.remove_processor(processor)

    def new_layer(self) -> SceneLayer:
        layer = self.create_layer("Unnamed")
        layer.enable()
        return layer

    def create_layer(self, name) -> SceneLayer:
        uid = uuid4()
        cls_name = f"Layer#{uid}"
        cls = type(cls_name, (SceneLayer,), {})
        layer = cls(self, name)
        self.add_layer(layer)
        return layer

    def add_layer(self, layer) -> None:
        self.layers.append(layer)

    def remove_layer(self, layer) -> None:
        self.events.publish(LayerDeletedEvent(layer))
        self.layers.remove(layer)

    def swap_layers(self, i, j) -> None:
        self.layers[i].mark()
        self.layers[j].mark()
        self.layers[i], self.layers[j] = self.layers[j], self.layers[i]

    def mark(self) -> None:
        for layer in self.layers:
            layer.mark()

    def enable(self) -> None:
        self.mark()
        for layer in self.layers:
            layer.enable()

    def disable(self) -> None:
        for layer in self.layers:
            layer.disable()
    
    def update(self, delta_time: float) -> None:
        self.process(delta_time)

    def cast_ray(self, ray) -> tuple:
        results = []
        for layer in self.layers:
            if not layer.visible:
                continue
            for entity, (_, block) in self.get_components(layer.__class__, Block):
                result = block.cast_ray(ray)
                if result:
                    results.append(result)
        if len(results) == 0:
            return None
        if len(results) == 1:
            return results[0]

        origin = ray.origin
        sorted_results = sorted(
            results, key=lambda result: glm.distance(result[0].position, origin)
        )
        return sorted_results[0]

    def draw(self, renderer: Renderer) -> None:
        for layer in self.layers:
            layer.draw(renderer)
