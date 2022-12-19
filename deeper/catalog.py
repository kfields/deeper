import glob

import yaml

from arcade.resources import resolve_resource_path

class Blueprint:
    def __init__(self, catalog, name, config):
        self.catalog = catalog
        self.category = None
        print("config: ", config)
        if 'extends' in config:
            self.extend(self.catalog.blueprints[config['extends']])

        print("name: ", name)
        self.name = name

        for key, value in config.items():
            print("config key, value: ", key, value)
            setattr(self, key, value)

    def extend(self, blueprint):
        for key, value in vars(blueprint).items():
            if key.startswith('_'):
                continue
            setattr(self, key, value)


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
            print(path)
            with open(path, 'r') as file:
                cat = yaml.full_load(file)
                print(cat)
                for key, value in cat.items():
                    self.build_blueprint(key, value)

    def build_blueprint(self, key, value):
        blueprint = Blueprint(self, key, value)
        print("blueprint: ", blueprint.__dict__)

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
