import glm
import esper

from . import Block
from .components.entity_group import EntityLayer


class World(esper.World):
    def __init__(self, timed=False):
        super().__init__(timed)
        self.layers = []

    def delete_entity(self, entity: int, immediate: bool = False) -> None:
        block = self.component_for_entity(entity, Block)
        block.layer.mark()
        super().delete_entity(entity, immediate)

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
        cls_name = f"{name}Layer"
        cls = type(cls_name, (EntityLayer,), {})
        layer = cls(name)
        self.add_layer(layer)
        return layer

    def add_layer(self, layer):
        self.layers.append(layer)
