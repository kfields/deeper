import pyglet
import imgui
import arcade

from deeper.dimgui import Widget
from deeper.resources.icons.icons_material_design import IconsMaterialDesign

from .toolbar import Toolbar, Toolbutton

class MainMenu(Widget):
    def __init__(self):
        super().__init__()
        arcade.text.load_font(f':deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}')
        font = pyglet.font.load("Material Icons")
        self.add_child(Toolbar([Toolbutton(IconsMaterialDesign.ICON_NAVIGATION, font), Toolbutton(IconsMaterialDesign.ICON_APPROVAL, font)]))
        #self.add_child(Toolbar([Toolbutton('pick', selected=True), Toolbutton('stamp')]))

    def draw(self):
        if imgui.begin_main_menu_bar():
            # File
            if imgui.begin_menu('File', True):
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)
                imgui.end_menu()
            imgui.separator()
            super().draw()
            imgui.end_main_menu_bar()
