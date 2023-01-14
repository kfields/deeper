from PIL import Image
import imgui
from arcade.resources import resolve_resource_path

from deeper.dimgui import Widget, Window

class BlueprintWidget(Widget):
    def __init__(self, blueprint):
        super().__init__()
        self.blueprint = blueprint
        self.selected = False
        self.texture = None

    def create(self, gui):
        super().create(gui)
        with Image.open(resolve_resource_path(self.blueprint.image)) as image:
            image.thumbnail((64, 64))
            self.texture = gui.window.ctx.texture(image.size, components=3, data=image.convert("RGB").tobytes())

    def draw(self):
        _, selected = imgui.selectable(self.blueprint.name, self.selected)
        imgui.same_line()
        imgui.image(self.texture.glo, *self.texture.size)
        return selected

class CategoryWidget(Widget):
    def __init__(self, category, callback):
        super().__init__()
        self.category = category
        self.callback = callback
        self.selection = None
        for blueprint in category.blueprints:
            if not blueprint._abstract:
                self.add_child(BlueprintWidget(blueprint))

    def show(self):
        pass

    def hide(self):
        if self.selection:
            self.selection.selected = False
        self.selection = None

    def draw(self):
        imgui.begin_child("entities", -1, -1, border=True)
        for widget in self.children:
            selected = widget.draw()
            if selected:
                if self.selection:
                    self.selection.selected = False
                self.selection = widget
                widget.selected = selected
                self.callback(widget.blueprint)
        imgui.end_child()

class CatalogPanel(Widget):
    def __init__(self, catalog, callback):
        super().__init__()
        self.catalog = catalog
        self.callback = callback
        self.category_names = []
        self.category_widgets = []
        self.current_index = 0
        self.current = None

        for category in catalog.categories.values():
            if not category._abstract:
                self.category_names.append(category.name)
                self.category_widgets.append(CategoryWidget(category, callback))

    def create(self, gui):
        super().create(gui)
        for widget in self.category_widgets:
            widget.create(gui)

    def draw(self):
        clicked, self.current_index = imgui.combo(
            "Category", self.current_index, self.category_names
        )
        current = self.category_widgets[self.current_index]
        if current != self.current:
            if self.current:
                self.current.hide()
            current.show()
        self.current = current
        self.current.draw()

class CatalogWindow(Window):
    def __init__(self, catalog, callback):
        super().__init__("Catalog", [CatalogPanel(catalog, callback)])
        self.catalog = catalog
