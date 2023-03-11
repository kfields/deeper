from loguru import logger

from ..constants import *
from ..builder import Builder
from ..kits.component_kit import ComponentKit


class EntityBuilder(Builder):
    def build(self, blueprint, world, layer):
        #logger.debug(blueprint)
        layer.mark()
        components = [layer, blueprint]

        for bp_component in blueprint.components:
            #logger.debug(component.__dict__)
            components.append(ComponentKit.instance.build(bp_component, world))

        entity = world.create_entity(*components)

        for bp_child in blueprint.children:
            #logger.debug(child.__dict__)
            child = self.build(bp_child, world, layer)
            entity.add_child(child)

        return entity