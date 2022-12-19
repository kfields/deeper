class MetaInfo:
    def __init__(self) -> None:
        self.abstract = False

class Builder:
    _meta = MetaInfo()

    def __init__(self, name) -> None:
        self.name = name

    def build(self, world, blueprint):
        pass