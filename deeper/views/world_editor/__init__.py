import math
import glm
import pyglet
import arcade
from arcade.resources import resolve_resource_path
from arcade import key
import imgui

from deeper.view import WorldView
from deeper import Block, Cuboid
from deeper.constants import *
from deeper.camera import WorldCamera
from deeper.components.sprite_vu import SpriteVu
from deeper.processor.rendering import RenderingProcessor
from deeper.catalog import Catalog
from deeper.dimgui import Gui
from deeper.widgets import MainMenu, CatalogWidget
from deeper.resources.icons.icons_material_design import IconsMaterialDesign

from deeper.tools.pick import PickTool
from deeper.tools.stamp import StampTool

from deeper.widgets.toolbar import Toolbar, Toolbutton
from deeper.widgets.camera_window import CameraWindow

class WorldEditor(WorldView):
    def __init__(self, window, edit_state):
        super().__init__(window, edit_state.world)
        self.edit_state = edit_state

        self.gui.default_font = self.gui.load_font(
            resolve_resource_path(f":deeper:fonts/Roboto-Regular.ttf"), 16
        )

        self.catalog = Catalog()
        self.gui.add_child(CatalogWidget(self.catalog, self.on_catalog))

        self.camera = WorldCamera(self, glm.vec3(), 1.5)
        self.gui.add_child(CameraWindow(self.camera))
        #self.camera = WorldCamera(self, glm.vec3(4, 0, 4), 1.25)
        # self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*8, 0, CELL_DEPTH*8), 1)

        self.tile_vu_list = []
        self.tile_list = arcade.SpriteList()
        self.block = Block()

        self.create_blocks()

        self.add_processor(RenderingProcessor(self))

        self.pick_tool = PickTool(self, edit_state)
        self.stamp_tool = StampTool(self, edit_state)

        self.use_tool(self.pick_tool)
        #self.use_tool(self.stamp_tool)

        # TODO:Need glyph range which pyimgui does not support. :(
        # self.gui.load_font(resolve_resource_path(f':deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}'))

        arcade.text.load_font(
            f":deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}"
        )
        font = pyglet.font.load("Material Icons")
        self.gui.add_child(
            MainMenu(
                children=[
                    Toolbar(
                        [
                            Toolbutton(IconsMaterialDesign.ICON_NAVIGATION, font, self.use_pick),
                            Toolbutton(IconsMaterialDesign.ICON_APPROVAL, font, self.use_stamp),
                        ]
                    )
                ]
            )
        )

    def use_pick(self):
        self.use_tool(self.pick_tool)

    def use_stamp(self):
        self.use_tool(self.stamp_tool)

    def on_catalog(self, blueprint):
        # exit()
        self.edit_state.current_blueprint = blueprint

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == key.NUM_ADD:
            self.camera.zoom = self.camera.zoom + .1
        elif symbol == key.NUM_SUBTRACT:
            self.camera.zoom = self.camera.zoom - .1

    def create_blocks(self):
        extents = glm.vec3(CELL_WIDTH, .01, 1)
        for ty in range(0, 8):
            for tx in range(0, 8):
                position = glm.vec3(tx * CELL_WIDTH, 0, ty)
                # print("position: ", position)
                block = Block(position, extents)
                self.block.add_child(block)
                vu = SpriteVu(
                    arcade.Sprite(":deeper:tiles/_Grid/GRID.png",)
                )
                self.world.create_entity(block, vu)

    def draw(self):
        self.camera.use()  # TODO: This is messing with ImGui on resize...
        self.tile_list.draw()

        # self.draw_aabbs()

        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)

    def draw_aabbs(self):
        for block in self.block.children:
            self.draw_aabb(block.aabb)
