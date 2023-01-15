import pyglet
import imgui
import arcade

from deeper.dimgui import Widget


class MainMenu(Widget):
    def __init__(self, children=[]):
        super().__init__(children=children)

    def draw(self):
        if imgui.begin_main_menu_bar():
            super().draw()
            imgui.end_main_menu_bar()

    """
    def draw(self):
        if imgui.begin_main_menu_bar():
            # File
            if imgui.begin_menu('File', True):
                clicked, selected = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )
                if clicked:
                    exit(1)
                imgui.end_menu()
            # Catalog
            if imgui.begin_menu('Catalog', True):
                clicked, selected = imgui.menu_item(
                    "Export Yaml", 'Cmd+Q', False, True
                )
                if clicked:
                    exit(1)
                imgui.end_menu()

            imgui.separator()
            super().draw()
            imgui.end_main_menu_bar()
    """