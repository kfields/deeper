import importlib
from inspect import isclass
from types import ModuleType
from typing import Coroutine, Dict, Iterable, List, Optional, Tuple, Type, Union, cast

#from deeper.widgets.component.component_widget import ComponentWidgetBuilder
from deeper.builder import Builder
import deeper.widgets.component

class ComponentWidgetKit:
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

    def find(self, component):
        if component.__class__ in self.builders:
            return self.builders[component.__class__]
        """
        if hasattr(blueprint, 'extends'):
            return self.find(blueprint.catalog.find(blueprint.extends))
        """
    def build(self, component):
        #print(blueprint.__dict__)
        builder = self.find(component)
        return builder.build(component)

    def create_builders(self):
        builder_classes = self.discover_builders(deeper.widgets.component)
        print(builder_classes)
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
            print(f'Module "{builders_path}" has no builders')
        return discovered_builders

