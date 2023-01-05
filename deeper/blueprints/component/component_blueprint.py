from ...blueprint import Blueprint

class ComponentBlueprint(Blueprint):
    def __init__(self, catalog, name, config, parent):
        super().__init__(catalog, name, config, parent)
