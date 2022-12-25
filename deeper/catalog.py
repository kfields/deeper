import copy
import glob

import yaml

from arcade.resources import resolve_resource_path
from  . import mergedeep

"""
from functools import reduce

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key.startswith('_'):
            continue
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                #raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
"""

"""
def merge(source, destination):
    for key, value in source.items():
        if key.startswith('_'):
            continue
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            if not node:
                node = {}
            merge(value, node)
        else:
            destination[key] = value

    return destination
"""

class Blueprint:
    def __init__(self, catalog, name, config, parent=None):
        self.catalog = catalog
        self.name = name
        self.category = None
        self.parent = parent
        self.children = []
        self._abstract = False
        self.config = self.configure(config)

    def __repr__(self) -> str:
        return f"<Blueprint name={self.name}>"
        #return f"<Blueprint {self.__dict__}>"

    def configure(self, config):
        print("config: ", config)
        if not config:
            return {}
        #print("config: ", config)
        if 'extends' in config:
            config = self.extend(config)
        
        for key, value in config.items():
            #print("config key, value: ", key, value)
            setattr(self, key, value)

        #if (not self._abstract) and hasattr(self, 'components'):            
        if hasattr(self, 'components'):            
            for key, value in self.components.items():
                self.add_child(Blueprint(self.catalog, key, value, self))

        return config

    def add_child(self, child):
        self.children.append(child)

    def extend(self, config):
        blueprint = self.catalog.blueprints[config['extends']]
        """
        newconfig = {}
        for key, value in blueprint.config.items():
            if key.startswith('_'):
                continue
            newconfig[key] = value

        for key, value in config.items():
            newconfig[key] = value
        """
        #newconfig = copy.deepcopy(blueprint.config)
        #print('newconfig:', newconfig)
        #newconfig = merge(config, newconfig)
        #newconfig = merge({}, config, blueprint.config)
        newconfig = copy.deepcopy(blueprint.config)
        #newconfig = mergedeep.merge(newconfig, config, strategy=mergedeep.Strategy.TYPESAFE_REPLACE)
        newconfig = mergedeep.merge(newconfig, config, strategy=mergedeep.Strategy.REPLACE)
        print('newconfig:', newconfig)

        return newconfig


class Category:
    def __init__(self, name) -> None:
        self.name = name
        self.blueprints = []

    def add_blueprint(self, blueprint):
        self.blueprints.append(blueprint)


class Catalog:
    _instance = None
    @classmethod
    @property
    def instance(cls):
        if cls._instance:
            return cls._instance
        cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self.categories = {}
        self.category_names = []
        self.blueprints = {}
        self.build()

    def find(self, name):
        return self.blueprints[name]

    def build(self):
        root = resolve_resource_path(":deeper:/catalog")
        paths = glob.glob(f"{root}/*.yaml")
        for path in paths:
            #print(path)
            with open(path, 'r') as file:
                cat = yaml.full_load(file)
                #print(cat)
                for key, value in cat.items():
                    self.build_blueprint(key, value)

    def build_blueprint(self, key, value):
        blueprint = Blueprint(self, key, value)
        #print("blueprint: ", blueprint.__dict__)

        if '_abstract' in value:
            return self.add_blueprint(key, blueprint)

        category = None
        if blueprint.category in self.categories:
            category = self.categories[blueprint.category]
        else:
            category = Category(blueprint.category)
            self.add_category(category)
        category.add_blueprint(blueprint)
        self.add_blueprint(key, blueprint)


    def add_blueprint(self, key, value):
        self.blueprints[key] = value

    def add_category(self, category: Category):
        self.categories[category.name] = category
        self.category_names.append(category.name)

    def dump(self):
        for blueprint in self.blueprints.values():
            print(blueprint.__dict__)
