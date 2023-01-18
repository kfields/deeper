from loguru import logger

import deeper.entities

from .kit import Kit

class ComponentKit(Kit):
    builders_path = deeper.components

    def find(self, blueprint):
        if blueprint.name in self.builders:
            return self.builders[blueprint.name]
        if hasattr(blueprint, 'extends'):
            return self.find(blueprint.catalog.find(blueprint.extends))

    def build(self, blueprint, world):
        #logger.debug(blueprint.__dict__)
        builder = self.find(blueprint)
        components = []
        for child in blueprint.children:
            #logger.debug(child.__dict__)
            components.append(self.build(child, world))
        return builder.build(blueprint, world)
