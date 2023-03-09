from loguru import logger

from ..constants import *
from ..builder import Builder
from ..kits.component_kit import ComponentKit


class EntityBuilder(Builder):
    def build(self, blueprint, world, layer):
        #logger.debug(blueprint)
        layer.mark()
        components = [layer, blueprint]

        for component in blueprint.components:
            logger.debug(component.__dict__)
            components.append(ComponentKit.instance.build(component, world))
        return world.create_entity(*components)
