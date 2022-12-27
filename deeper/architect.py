import importlib
from inspect import isclass
from types import ModuleType
from typing import Coroutine, Dict, Iterable, List, Optional, Tuple, Type, Union, cast

from loguru import logger

from .builder import Builder
import deeper.builders

class Architect:
    def __init__(self) -> None:
        self.builders = {}
        self.create_builders()

    _instance = None
    @classmethod
    @property
    def instance(cls):
        if cls._instance:
            return cls._instance
        cls._instance = cls()
        return cls._instance

    def add_builder(self, builder):
        self.builders[builder.key] = builder

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
            components.append(self.build(child, world))
        return builder.build(blueprint, world, target, components)

    def create_builders(self):
        builder_classes = self.discover_builders(deeper.builders)
        #print(builder_classes)
        for cls in builder_classes:
            self.add_builder(cls())

    def discover_builders(self, builders_path: Union[ModuleType, str]
    ) -> List[Type[Builder]]:
        if isinstance(builders_path, ModuleType):
            module = builders_path
        else:
            try:
                module = importlib.import_module(builders_path)
            except ImportError:
                raise RuntimeError(f'Module "{builders_path}" not found')
        discovered_builders = []
        possible_builders = getattr(module, "__builders__", None)
        try:
            possible_builders = [*possible_builders]  # type:ignore
        except TypeError:
            possible_builders = None
        if not possible_builders:
            possible_builders = [getattr(module, attr_name) for attr_name in dir(module)]
        for attr in possible_builders:
            if isclass(attr) and issubclass(attr, Builder) and not attr._meta.abstract:
                discovered_builders.append(attr)
        if not discovered_builders:
            logger.debug(f'Module "{builders_path}" has no builders')
        return discovered_builders

