class MetaInfo:
    def __init__(self) -> None:
        self.abstract = False


class Builder:
    _meta = MetaInfo()

"""
class BlueprintBuilder(Builder):
    def build(self, catalog, name, config):
        pass
"""

class EntityBuilder(Builder):
    def build(self, world, blueprint, target=None):
        pass


class ComponentBuilder(Builder):
    def build(self, world, blueprint, target=None):
        pass
