from pathlib import Path

from PIL import Image
from crunge import imgui

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine import Renderer
from crunge.engine.imgui.widget import Widget, Window

from .menu import Menubar, Menu, MenuItem

class BlueprintWidget(Widget):
    def __init__(self, blueprint):
        super().__init__()
        self.blueprint = blueprint
        self.selected = False
        self.texture = None

    def _create(self):
        super()._create()
        """
        path = resolve_resource_path(self.blueprint.image)
        with Image.open(path) as image:
            image.thumbnail((64, 64))
            self.texture = gui.window.ctx.texture(image.size, components=3, data=image.convert('RGB').tobytes())
        """
        image = self.blueprint.thumbnail
        self.texture = self.gui.window.ctx.texture(image.size, components=3, data=image.convert('RGB').tobytes())
        return self

    def draw(self, renderer: Renderer):
        #clicked, selected = imgui.selectable(self.blueprint.name, self.selected, width=128)
        clicked, selected = imgui.selectable(self.blueprint.name, self.selected, size=(-1, 128))
        imgui.same_line()
        #imgui.image(self.texture.glo, *self.texture.size)
        return clicked

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

    def draw(self, renderer: Renderer):
        #imgui.begin_child('entities', -1, -1, border=True)
        imgui.begin_child('entities', (-1, -1), border=True)
        for widget in self.children:
            clicked = widget.draw(renderer)
            if clicked:
                if self.selection:
                    self.selection.selected = False
                self.selection = widget
                widget.selected = True
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

        for category in sorted(catalog.categories.values(), key=lambda category: category.name):
            if not category._abstract:
                self.category_names.append(category.name)
                self.category_widgets.append(CategoryWidget(category, callback))

    def _create(self):
        super()._create()
        for widget in self.category_widgets:
            widget.create(self.gui)
        return self

    def draw(self, renderer: Renderer):
        clicked, self.current_index = imgui.combo(
            'Category', self.current_index, self.category_names
        )
        current = self.category_widgets[self.current_index]
        if current != self.current:
            if self.current:
                self.current.hide()
            current.show()
        self.current = current
        self.current.draw(renderer)

class CatalogWindow(Window):

    def __init__(self, catalog, callback, on_close:callable=None):
        self.catalog = catalog
        children = [
            Menubar([
                Menu('File', [
                    MenuItem('Export Yaml', lambda: self.catalog.save_yaml(ResourceManager.resolve_path('{deeper}/catalog')))
                ])
            ]),
            CatalogPanel(catalog, callback)
        ]
        super().__init__('Catalog', children, on_close=on_close, flags=imgui.WINDOW_FLAGS_MENU_BAR)
