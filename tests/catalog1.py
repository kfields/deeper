import glob

import toml

from PIL import Image
import arcade
import imgui

from deeper.dimgui import Gui
#from deeper.resources import resource_path
from arcade.resources import resolve_resource_path


class Item:
    def __init__(self, window, name, image_path):
        self.name = name
        self.selected = False
        with Image.open(resolve_resource_path(image_path)) as image:
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
        root = resolve_resource_path(":deeper:/catalog")
        #paths = glob.glob(path / "*.toml")
        paths = glob.glob(f"{root}/*.toml")
        for path in paths:
            cat = toml.load(path)
            print(cat)
            for cat_key, cat_items in cat.items():
                category = Category(cat_key)
                cat_items = cat[cat_key]
                for it_key, it_items in cat_items:
                    item = Item(self.window, it_key, it_items["image"])
                    category.add_item(item)
                self.add_category(category)

    def add_category(self, category):
        self.categories.append(category)

    
class BasicExample(arcade.Window):

    def __init__(self):
        super().__init__(800, 600, "Basic Example", resizable=True)
        self.gui = Gui(self)
        self.title = 'Catalog'
        self.catalog = Catalog()
        self.items = []
        self.selection = None
        self.items.append(Item(self, 'Floor1', ":deeper:tiles/Floor1.png"))
        self.items.append(Item(self, 'FloorD3', ":deeper:tiles/FloorD3.png"))
        self.items.append(Item(self, 'TileStone1', ":deeper:tiles/TileStone1.png"))
        self.items.append(Item(self, 'TileStone5', ":deeper:tiles/TileStone5.png"))

    def on_draw(self):
        self.clear()

        imgui.new_frame()

        self.draw_catalog()

        self.gui.draw()

    def draw_catalog(self):
        imgui.begin(self.title)
        for item in self.items:
            #_, item.selected = imgui.selectable(item.text, item.selected)
            _, selected = imgui.selectable(item.name, item.selected)
            if selected:
                if self.selection:
                    self.selection.selected = False
                self.selection = item
                item.selected = selected
            item.draw()
        imgui.end()
    """
    def draw_catalog(self):
        imgui.begin(self.title)
        _, self.selected[0] = imgui.selectable(
            "1. I am selectable", self.selected[0]
        )
        _, self.selected[1] = imgui.selectable(
            "2. I am selectable too", self.selected[1]
        )
        imgui.end()
    """

if __name__ == '__main__':
    window = BasicExample()
    arcade.run()