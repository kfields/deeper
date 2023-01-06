import copy
from . import mergedeep
from .constants import *
from .builder import Builder
from .setting import decompose

class Blueprint:
    def __init__(self, catalog, name, config, parent=None):
        self.catalog = catalog
        self.name = name
        self.config = config
        self.category = None
        self.parent = parent
        self.children = []
        self._abstract = False
        self.base = None
        self.xconfig = self.configure(config)
        self.settings = self.create_settings(config)

    def __repr__(self) -> str:
        return f"<Blueprint name={self.name}>"
        # return f"<Blueprint {self.__dict__}>"

    def configure(self, config):
        if not config:
            return {}
        # print("config: ", config)
        if "extends" in config:
            self.base = self.catalog.find(config["extends"])
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
        xconfig = {}
        for key, value in blueprint.config.items():
            if key.startswith('_'):
                continue
            xconfig[key] = value

        for key, value in config.items():
            xconfig[key] = value
        """
        xconfig = copy.deepcopy(blueprint.xconfig)
        # xconfig = mergedeep.merge(xconfig, config, strategy=mergedeep.Strategy.TYPESAFE_REPLACE)
        xconfig = mergedeep.merge(
            xconfig, config, strategy=mergedeep.Strategy.REPLACE
        )
        # print("xconfig:", xconfig)

        return xconfig

    def create_settings(self, config):
        decomposed = decompose(config)
        obj = {"name": self.name, "value": decomposed}
        print(obj)
        return self.settings_class.parse_obj(obj)


class BlueprintBuilder(Builder):
    def build(self, catalog, name, config, parent):
        return self.cls(catalog, name, config, parent)
