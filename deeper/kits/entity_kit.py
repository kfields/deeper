from loguru import logger

import deeper.entities
from deeper.constants import *
from .kit import Kit


class EntityKit(Kit):
    builders_path = deeper.entities

    def find(self, blueprint):
        if blueprint.name in self.builders:
            return self.builders[blueprint.name]
        if hasattr(blueprint, "extends"):
            return self.find(blueprint.catalog.find(blueprint.extends))

    def build(self, blueprint, world, layer, position=DEFAULT_VEC3):
        # logger.debug(blueprint.__dict__)
        builder = self.find(blueprint)
        return builder.build(blueprint, world, layer, position)
