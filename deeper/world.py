import esper

from . import Space

class World(esper.World):
    def __init__(self, timed=False):
        super().__init__(timed)

    def cast_ray(self, ray):
        results = []
        for entity, (space,) in self.get_components(Space):
            result = space.cast_ray(ray, entity)
            if result:
                results.append(result)
        if len(results) == 0:
            return None
        if len(results) == 1:
            return results[0]

        sorted_results = sorted(results, key=lambda result: -(result[1].position.y))
        return sorted_results[0]