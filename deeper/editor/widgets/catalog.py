from PIL import Image
import imgui
from arcade.resources import resolve_resource_path

from deeper.dimgui import Widget

class DefinitionWidget(Widget):
    def __init__(self, definition):
        super().__init__()
        self.definition = definition
        self.selected = False
        self.texture = None

    def create(self, gui):
        super().create(gui)
        with Image.open(resolve_resource_path(self.definition.image)) as image:
            image.thumbnail((64, 64))
            self.texture = gui.window.ctx.texture(image.size, components=3, data=image.convert("RGB").tobytes())

    def draw(self):
        _, selected = imgui.selectable(self.definition.name, self.selected)
        imgui.same_line()
        imgui.image(self.texture.glo, *self.texture.size)
        return selected

class CategoryWidget(Widget):
    def __init__(self, category):
        super().__init__()
        self.category = category
        for definition in category.definitions:
            self.add_child(DefinitionWidget(definition))

    def draw(self):
        imgui.begin_child("entities", 150, -50, border=True)
        super().draw()
        imgui.end_child()

class CatalogWidget(Widget):
    def __init__(self, catalog, callback):
        super().__init__()
        self.catalog = catalog
        self.callback = callback
        self.category_widgets = []
        self.current = 0
        self.selection = None

        for category in catalog.categories:
            self.category_widgets.append(CategoryWidget(category))

    def create(self, gui):
        super().create(gui)
        for widget in self.category_widgets:
            widget.create(gui)

    def draw(self):
        imgui.begin('Catalog')
        clicked, self.current = imgui.combo(
            "Category", self.current, self.catalog.category_names
        )
        imgui.begin_child("entities", 250, -50, border=True)
        for widget in self.category_widgets[self.current].children:
            selected = widget.draw()
            if selected:
                if self.selection:
                    self.selection.selected = False
                self.selection = widget
                widget.selected = selected
                self.callback(widget.definition)
        imgui.end_child()
        imgui.end()
