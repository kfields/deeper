import esper

from . import Space

class World(esper.World):
    def __init__(self, timed=False):
        super().__init__(timed)

    def cast_ray(self, ray):
        for ent, (space,) in self.get_components(Space):
            result = space.cast_ray(ray)
            if result:
                return result