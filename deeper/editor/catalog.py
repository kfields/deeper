import glob

import yaml

from PIL import Image
import imgui

from arcade.resources import resolve_resource_path

class Definition:
    def __init__(self, catalog, name, config):
        self.catalog = catalog
        print("config: ", config)
        if 'extends' in config:
            self.extend(self.catalog.definitions[config['extends']])

        print("name: ", name)
        self.name = name

        for key, value in config.items():
            print("config key, value: ", key, value)
            setattr(self, key, value)

    def extend(self, definition):
        for key, value in vars(definition).items():
            if key.startswith('_'):
                continue
            setattr(self, key, value)

class Item(Definition):
    def __init__(self, catalog, name, config):
        super().__init__(catalog, name, config)
        self.selected = False

        with Image.open(resolve_resource_path(self.image)) as image:
            image.thumbnail((64, 64))
            self.texture = catalog.window.ctx.texture(image.size, components=3, data=image.convert("RGB").tobytes())

    def draw(self):
        imgui.same_line()
        imgui.image(self.texture.glo, *self.texture.size)


class Category:
    def __init__(self, name) -> None:
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)


class Catalog:
    def __init__(self, window) -> None:
        self.window = window
        self.categories = []
        self.category_names = []
        self.category_map = {}
        self.definitions = {}
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
                    self.build_definition(key, value)

    def build_definition(self, key, value):
        if '_abstract' in value:
            return self.add_definition(key, Definition(self, key, value))
        self.build_item(key, value)

    def build_item(self, key, value):
        item = Item(self, key, value)
        print("item: ", item.__dict__)
        category = None
        if item.category in self.category_map:
            category = self.category_map[item.category]
        else:
            category = Category(item.category)
            self.add_category(category)
        category.add_item(item)


    def add_definition(self, key, value):
        self.definitions[key] = value

    def add_category(self, category):
        self.category_map[category.name] = category
        self.categories.append(category)
        self.category_names.append(category.name)
