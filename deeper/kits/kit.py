import importlib
from inspect import isclass
from types import ModuleType
from typing import Coroutine, Dict, Iterable, List, Optional, Tuple, Type, Union, cast

from loguru import logger

from deeper.builder import Builder

class Kit:
    builder_type = Builder
    builders_path = None
    
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

    def create_builders(self):
        builder_classes = self.discover_builders(self.builders_path)
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
            if isclass(attr) and issubclass(attr, self.builder_type) and not attr._meta.abstract:
                discovered_builders.append(attr)
        if not discovered_builders:
            logger.debug(f'Module "{builders_path}" has no builders')
        return discovered_builders

