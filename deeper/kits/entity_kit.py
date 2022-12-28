import importlib
from inspect import isclass
from types import ModuleType
from typing import Coroutine, Dict, Iterable, List, Optional, Tuple, Type, Union, cast

from loguru import logger

import deeper.entities

from .kit import Kit
from .component_kit import ComponentKit

class EntityKit(Kit):
    builders_path = deeper.entities

    def find(self, blueprint):
        if blueprint.name in self.builders:
            return self.builders[blueprint.name]
        if hasattr(blueprint, 'extends'):
            return self.find(blueprint.catalog.find(blueprint.extends))

    def build(self, blueprint, world, target=None):
        #print(blueprint.__dict__)
        builder = self.find(blueprint)
        components = []
        for child in blueprint.children:
            #print(child.__dict__)
            #components.append(self.build(child, world))
            components.append(ComponentKit.instance.build(child, world))
        return builder.build(blueprint, world, target, components)
