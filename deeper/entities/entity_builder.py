from loguru import logger

from ..constants import *
from ..builder import Builder
from ..kits.component_kit import ComponentKit


class EntityBuilder(Builder):
    def build(self, blueprint, world, layer):
        #logger.debug(blueprint)
        #logger.debug(f"position: {position}")
        layer.mark()
        components = [layer, blueprint]
        for child in blueprint.children:
            #logger.debug(child.__dict__)
            components.append(ComponentKit.instance.build(child, world))
        return world.create_entity(*components)
