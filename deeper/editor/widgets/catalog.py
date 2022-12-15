import imgui

from deeper.dimgui import Widget

class CatalogWidget(Widget):
    def __init__(self, catalog):
        super().__init__()
        self.catalog = catalog
        self.current = 0
        self.selection = None

    def draw(self):
        imgui.begin('Catalog')
        clicked, self.current = imgui.combo(
            "Category", self.current, self.catalog.category_names
        )
        for item in self.catalog.categories[self.current].items:
            _, selected = imgui.selectable(item.name, item.selected)
            if selected:
                if self.selection:
                    self.selection.selected = False
                self.selection = item
                item.selected = selected
            item.draw()
        imgui.end()
