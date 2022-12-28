import importlib
from inspect import isclass
from types import ModuleType
from typing import Coroutine, Dict, Iterable, List, Optional, Tuple, Type, Union, cast

from loguru import logger

from deeper.builder import Builder
import deeper.widgets.component

from .kit import Kit

class ComponentWidgetKit(Kit):
    builders_path = deeper.widgets.component
    #builder_type = Builder

    def find(self, component):
        if component.__class__ in self.builders:
            return self.builders[component.__class__]

    def build(self, component):
        #print(blueprint.__dict__)
        builder = self.find(component)
        return builder.build(component)