import imgui

from deeper.dimgui import Widget

class MenuItem(Widget):
    def __init__(self, label, callback, shortcut=None, selected=False, enabled=True ):
        super().__init__()
        self.label = label
        self.callback = callback
        self.shortcut = shortcut
        self.selected = selected
        self.enabled = enabled

    def draw(self):
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

    def draw(self):
        if imgui.begin_menu(self.label, self.enabled):
            super().draw()
            imgui.end_menu()


class Menubar(Widget):
    def __init__(self, children=[]):
        super().__init__(children=children)

    def draw(self):
        if imgui.begin_menu_bar():
            super().draw()
            imgui.end_menu_bar()

class MainMenubar(Widget):
    def __init__(self, children=[]):
        super().__init__(children=children)

    def draw(self):
        if imgui.begin_main_menu_bar():
            super().draw()
            imgui.end_main_menu_bar()
