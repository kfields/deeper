import glob

import yaml

from PIL import Image
import arcade
import imgui

from deeper.dimgui import Gui
#from deeper.resources import resource_path
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
        #if 'extends' in value:
        #    item.extend(self.definitions[value['extends']])
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

    
class BasicExample(arcade.Window):

    def __init__(self):
        super().__init__(800, 600, "Basic Example", resizable=True)
        self.gui = Gui(self)
        self.title = 'Catalog'
        self.catalog = Catalog(self)
        self.selection = None
        self.current = 0

    def on_draw(self):
        self.clear()

        imgui.new_frame()
        self.draw_catalog()
        self.gui.draw()

    def draw_catalog(self):
        imgui.begin(self.title)
        clicked, self.current = imgui.combo(
            "Category", self.current, self.catalog.category_names
        )
        for item in self.catalog.categories[self.current].items:
            #_, item.selected = imgui.selectable(item.text, item.selected)
            _, selected = imgui.selectable(item.name, item.selected)
            if selected:
                if self.selection:
                    self.selection.selected = False
                self.selection = item
                item.selected = selected
            item.draw()
        imgui.end()

if __name__ == '__main__':
    window = BasicExample()
    arcade.run()