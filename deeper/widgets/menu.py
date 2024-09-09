from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.imgui.widget import Widget

class MenuItem(Widget):
    def __init__(self, label, callback, shortcut=None, selected=False, enabled=True ):
        super().__init__()
        self.label = label
        self.callback = callback
        self.shortcut = shortcut
        self.selected = selected
        self.enabled = enabled

    def draw(self, renderer: Renderer):
        clicked, selected = imgui.menu_item(
            self.label, self.shortcut, self.selected, self.enabled
        )
        if clicked:
            self.callback()

class Menu(Widget):
    def __init__(self, label, children=[], enabled=True):
        super().__init__(children)
        self.label = label
        self.enabled = enabled

    def draw(self, renderer: Renderer):
        if imgui.begin_menu(self.label, self.enabled):
            super().draw(renderer)
            imgui.end_menu()


class Menubar(Widget):
    def __init__(self, children=[]):
        super().__init__(children=children)

    def draw(self, renderer: Renderer):
        if imgui.begin_menu_bar():
            super().draw(renderer)
            imgui.end_menu_bar()

class MainMenubar(Widget):
    def __init__(self, children=[]):
        super().__init__(children=children)

    def draw(self, renderer: Renderer):
        if imgui.begin_main_menu_bar():
            super().draw(renderer)
            imgui.end_main_menu_bar()
