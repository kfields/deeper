class MetaInfo:
    def __init__(self) -> None:
        self.abstract = False

class Builder:
    _meta = MetaInfo()

    #def __init__(self, name) -> None:
    #    self.name = name

    def build(self, blueprint, world, target=None):
        pass

class EntityBuilder(Builder):
    def build(self, world, blueprint, target=None):
        pass

class ComponentBuilder(Builder):
    def build(self, world, blueprint, target=None):
        pass