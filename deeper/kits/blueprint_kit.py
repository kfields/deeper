from loguru import logger

import deeper.blueprints

from .kit import Kit

class BlueprintKit(Kit):
    builders_path = deeper.blueprints

    def find(self, name):
        if name in self.builders:
            return self.builders[name]

    def build(self, catalog, name, config):
        #print(blueprint.__dict__)
        builder = self.find(name)
        return builder.build(catalog, name, config)
