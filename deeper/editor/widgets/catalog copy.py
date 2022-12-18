from PIL import Image
import imgui
from arcade.resources import resolve_resource_path

from deeper.dimgui import Widget

"""
class Item(Description):
    def __init__(self, catalog, name, config):
        super().__init__(catalog, name, config)
        self.selected = False

        with Image.open(resolve_resource_path(self.image)) as image:
            image.thumbnail((64, 64))
            self.texture = catalog.window.ctx.texture(image.size, components=3, data=image.convert("RGB").tobytes())

    def draw(self):
        imgui.same_line()
        imgui.image(self.texture.glo, *self.texture.size)
"""

class DefinitionWidget(Widget):
    def __init__(self, definition):
        super().__init__()
        self.definition = definition
        self.selected = False

    def create(self, gui):
        super().create(gui)
        with Image.open(resolve_resource_path(self.definition.image)) as image:
            image.thumbnail((64, 64))
            self.texture = gui.window.ctx.texture(image.size, components=3, data=image.convert("RGB").tobytes())

    def draw(self):
        _, selected = imgui.selectable(self.definition.name, self.selected)
        return selected

class CategoryWidget(Widget):
    def __init__(self, category):
        super().__init__()
        self.category = category
        for definition in category.definitions:
            self.add_child(DefinitionWidget(definition))

    def draw(self):
        for definition in self.category.definitions:
            _, selected = imgui.selectable(definition.name, definition.selected)
            if selected:
                if self.selection:
                    self.selection.selected = False
                self.selection = definition
                definition.selected = selected
            definition.draw()

class CatalogWidget(Widget):
    def __init__(self, catalog):
        super().__init__()
        self.catalog = catalog
        self.category_widgets = []
        self.current = 0
        self.selection = None

        for category in catalog.categories:
            self.category_widgets.append(CategoryWidget(category))

    def draw(self):
        imgui.begin('Catalog')
        clicked, self.current = imgui.combo(
            "Category", self.current, self.catalog.category_names
        )
        for definition in self.catalog.categories[self.current].definitions:
            _, selected = imgui.selectable(definition.name, definition.selected)
            if selected:
                if self.selection:
                    self.selection.selected = False
                self.selection = definition
                definition.selected = selected
            definition.draw()
        imgui.end()
