import copy
from . import mergedeep
from .constants import *
from .builder import Builder


class Blueprint:
    def __init__(self, catalog, name, config, parent=None):
        self.catalog = catalog
        self.name = name
        self.category = None
        self.parent = parent
        self.children = []
        self._abstract = False
        self.config = self.configure(config)

    def __repr__(self) -> str:
        return f"<Blueprint name={self.name}>"
        # return f"<Blueprint {self.__dict__}>"

    def configure(self, config):
        if not config:
            return {}
        # print("config: ", config)
        if "extends" in config:
            config = self.extend(config)

        for key, value in config.items():
            # print("config key, value: ", key, value)
            setattr(self, key, value)

        # if (not self._abstract) and hasattr(self, 'components'):
        if hasattr(self, "components"):
            for key, value in self.components.items():
                #self.add_child(Blueprint(self.catalog, key, value, self))
                self.add_child(self.catalog.build(key, value, self))

        return config

    def add_child(self, child):
        self.children.append(child)

    def extend(self, config):
        blueprint = self.catalog.blueprints[config["extends"]]
        """
        newconfig = {}
        for key, value in blueprint.config.items():
            if key.startswith('_'):
                continue
            newconfig[key] = value

        for key, value in config.items():
            newconfig[key] = value
        """
        newconfig = copy.deepcopy(blueprint.config)
        # newconfig = mergedeep.merge(newconfig, config, strategy=mergedeep.Strategy.TYPESAFE_REPLACE)
        newconfig = mergedeep.merge(
            newconfig, config, strategy=mergedeep.Strategy.REPLACE
        )
        # print("newconfig:", newconfig)

        return newconfig


class BlueprintBuilder(Builder):
    def build(self, catalog, name, config, parent):
        return self.cls(catalog, name, config, parent)


class EntityBlueprint(Blueprint):
    size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]
    def __init__(self, catalog, name, config):
        super().__init__(catalog, name, config)


class ComponentBlueprint(Blueprint):
    def __init__(self, catalog, name, config, parent):
        super().__init__(catalog, name, config, parent)
