import glm
import esper

from . import Block
from .components.group import LayerGroup


class World(esper.World):
    def __init__(self, timed=False):
        super().__init__(timed)
        self.layer_groups = []

    def cast_ray(self, ray):
        results = []
        for entity, (block,) in self.get_components(Block):
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

    def create_layer_group(self, name):
        cls_name = f"{name}Layer"
        cls = type(cls_name, (LayerGroup,), {})
        group = cls(name)
        self.add_layer_group(group)
        return group

    def add_layer_group(self, group):
        self.layer_groups.append(group)
