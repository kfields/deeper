import glm
import pyglet
from pyglet import clock
import arcade
from arcade.resources import resolve_resource_path
from arcade import key


from deeper.view import WorldView
from deeper import Block, Cuboid
from deeper.constants import *
from deeper.camera import WorldCamera
from deeper.components.sprite_vu import SpriteVu
from deeper.processors.rendering import RenderingProcessor
from deeper.catalog import Catalog
from deeper.widgets import MainMenu, CatalogWindow
from deeper.resources.icons.icons_material_design import IconsMaterialDesign

from deeper.tools.pick import PickTool
from deeper.tools.stamp import StampTool

from deeper.widgets.toolbar import Toolbar, ToolButton
from deeper.widgets.camera_window import CameraWindow

class WorldEditor(WorldView):
    def __init__(self, window, edit_state):
        super().__init__(window, edit_state.world, 'World Editor')
        self.edit_state = edit_state

        self.gui.default_font = self.gui.load_font(
            resolve_resource_path(f":deeper:fonts/Roboto-Regular.ttf"), 16
        )

        self.catalog = Catalog()
        self.gui.add_child(CatalogWindow(self.catalog, self.on_catalog))

        self.camera = WorldCamera(self.window, glm.vec3(), 1.5)
        self.gui.add_child(CameraWindow(self.camera))
        #self.camera = WorldCamera(self, glm.vec3(4, 0, 4), 1.25)
        # self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*8, 0, CELL_DEPTH*8), 1)

        self.tile_vu_list = []
        self.tile_list = arcade.SpriteList()
        self.block = Block()

        self.create_blocks()

        self.add_processor(RenderingProcessor(self))

        self.current_tool = self.pick_tool = PickTool(self, edit_state)
        self.stamp_tool = StampTool(self, edit_state)

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
                            ToolButton(IconsMaterialDesign.ICON_NAVIGATION, font, self.use_pick),
                            ToolButton(IconsMaterialDesign.ICON_APPROVAL, font, self.use_stamp),
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
        blueprint = self.catalog.find('Cell')
        size = glm.vec3(CELL_WIDTH, .01, 1)
        for ty in range(0, 8):
            for tx in range(0, 8):
                position = glm.vec3(tx * CELL_WIDTH, 0, ty)
                #position = glm.vec3(tx * CELL_WIDTH - CELL_HALF_WIDTH, 0, ty - CELL_HALF_DEPTH)
                # print("position: ", position)
                block = Block(position, size)
                self.block.add_child(block)
                vu = SpriteVu(
                    arcade.Sprite(":deeper:tiles/_Grid/GRID.png",)
                )
                self.world.create_entity(block, vu, blueprint)
    
    def draw(self):
        self.camera.use()
        self.tile_list.draw()

        # self.draw_aabbs()

        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)

    def draw_aabbs(self):
        for block in self.block.children:
            self.draw_aabb(block.aabb)
