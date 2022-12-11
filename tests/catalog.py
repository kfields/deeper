import glob

import toml

from PIL import Image
import arcade
import imgui

from deeper.dimgui import Gui
#from deeper.resources import resource_path
from arcade.resources import resolve_resource_path


class Item:
    def __init__(self, window, name, config):
        print("name: ", name)
        self.name = name
        self.selected = False
        print("config: ", config)
        for key, value in config.items():
            print("config key, value: ", key, value)
            setattr(self, key, value)

        with Image.open(resolve_resource_path(self.image)) as image:
            image.thumbnail((64, 64))
            self.texture = window.ctx.texture(image.size, components=3, data=image.convert("RGB").tobytes())

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
        root = resolve_resource_path(":deeper:/catalog")
        #paths = glob.glob(path / "*.toml")
        paths = glob.glob(f"{root}/*.toml")
        for path in paths:
            cat = toml.load(path)
            print(cat)
            for cat_key, cat_items in cat.items():
                category = Category(cat_key)
                print("cat_items: ", cat_items)
                for it_key, it_items in cat_items.items():
                    print("it_items: ", it_items)
                    item = Item(self.window, it_key, it_items)
                    category.add_item(item)
                self.add_category(category)

    def add_category(self, category):
        self.categories.append(category)
        self.category_names.append(category.name)

    
class BasicExample(arcade.Window):

    def __init__(self):
        super().__init__(800, 600, "Basic Example", resizable=True)
        self.gui = Gui(self)
        self.title = 'Catalog'
        self.catalog = Catalog(self)
        self.items = []
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