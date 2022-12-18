import glob

import yaml

from PIL import Image
import imgui

from arcade.resources import resolve_resource_path

class Description:
    def __init__(self, catalog, name, config):
        self.catalog = catalog
        print("config: ", config)
        if 'extends' in config:
            self.extend(self.catalog.descriptions[config['extends']])

        print("name: ", name)
        self.name = name

        for key, value in config.items():
            print("config key, value: ", key, value)
            setattr(self, key, value)

    def extend(self, description):
        for key, value in vars(description).items():
            if key.startswith('_'):
                continue
            setattr(self, key, value)


class Category:
    def __init__(self, name) -> None:
        self.name = name
        self.definitions = []

    def add_description(self, definition):
        self.definitions.append(definition)


class Catalog:
    def __init__(self) -> None:
        self.categories = []
        self.category_names = []
        self.category_map = {}
        self.descriptions = {}
        self.build()

    def build(self):
        root = resolve_resource_path(":deeper:/catalog")
        paths = glob.glob(f"{root}/*.yaml")
        for path in paths:
            print(path)
            with open(path, 'r') as file:
                cat = yaml.full_load(file)
                print(cat)
                for key, value in cat.items():
                    self.build_description(key, value)

    def build_description(self, key, value):
        description = Description(self, key, value)
        print("description: ", description.__dict__)

        if '_abstract' in value:
            return self.add_description(key, description)

        category = None
        if description.category in self.category_map:
            category = self.category_map[description.category]
        else:
            category = Category(description.category)
            self.add_category(category)
        category.add_description(description)


    def add_description(self, key, value):
        self.descriptions[key] = value

    def add_category(self, category):
        self.category_map[category.name] = category
        self.categories.append(category)
        self.category_names.append(category.name)
