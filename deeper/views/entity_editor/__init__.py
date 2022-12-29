import glm
import pyglet
import arcade
from arcade.resources import resolve_resource_path
from arcade import key

from deeper.view import WorldView
from deeper import Blueprint, Block
from deeper.constants import *
from deeper.camera import WorldCamera
from deeper.processors.rendering import RenderingProcessor
from deeper.widgets import MainMenu
from deeper.resources.icons.icons_material_design import IconsMaterialDesign

from deeper.tools.pick import PickTool

from deeper.widgets.toolbar import Toolbar, Toolbutton
from deeper.widgets.entity_window import EntityWindow
from deeper.widgets.blueprint_window import BlueprintWindow

class EntityEditor(WorldView):
    def __init__(self, window, edit_state):
        super().__init__(window, edit_state.world)
        self.edit_state = edit_state

        self.gui.default_font = self.gui.load_font(
            resolve_resource_path(f":deeper:fonts/Roboto-Regular.ttf"), 16
        )

        self.gui.add_child(EntityWindow(self.world, edit_state.entity))


        self.blueprint = self.world.component_for_entity(edit_state.entity, Blueprint)
        self.gui.add_child(BlueprintWindow(self.blueprint))

        self.block = self.world.component_for_entity(edit_state.entity, Block)
        pos = self.block.position
        self.camera = WorldCamera(self, pos, 1)

        self.tile_vu_list = []
        self.tile_list = arcade.SpriteList()

        self.add_processor(RenderingProcessor(self))

        self.pick_tool = PickTool(self, edit_state)

        self.use_tool(self.pick_tool)

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
                        ]
                    )
                ]
            )
        )

    def use_pick(self):
        self.use_tool(self.pick_tool)

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == key.NUM_ADD:
            self.camera.zoom = self.camera.zoom + .1
        elif symbol == key.NUM_SUBTRACT:
            self.camera.zoom = self.camera.zoom - .1

    def draw(self):
        self.camera.use()  # TODO: This is messing with ImGui on resize...
        self.tile_list.draw()

        # self.draw_aabbs()
        self.draw_aabb(self.block.aabb)

        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)

    def draw_aabbs(self):
        for block in self.block.children:
            self.draw_aabb(block)
