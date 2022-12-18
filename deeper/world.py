import esper

from . import Space

class World(esper.World):
    def __init__(self, timed=False):
        super().__init__(timed)

    def create_entity_from_description(self, description) -> int:
        return super().create_entity(*components)

    def cast_ray(self, ray):
        for entity, (space,) in self.get_components(Space):
            result = space.cast_ray(entity, ray)
            if result:
                return result