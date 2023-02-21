from loguru import logger

import glm
import pyglet
from pyglet import clock
import arcade
from arcade.resources import resolve_resource_path
from arcade import key


from deeper.constants import *
from deeper.camera import WorldCamera
from deeper.processors import RenderingProcessor, AnimationProcessor
from deeper.catalog import Catalog
from deeper.widgets import MainMenu, CatalogWindow, LayersWindow
from deeper.resources.icons import IconsMaterialDesign

from deeper.tools.pick import PickTool
from deeper.tools.stamp import StampTool

from deeper.widgets.toolbar import Toolbar, ToolButton
from deeper.widgets.camera_window import CameraWindow

from ..scene_view import SceneView

class LevelEditor(SceneView):
    def __init__(self, window, edit_state):
        super().__init__(window, edit_state.world, "Level Editor")
        self.edit_state = edit_state

        self.gui.default_font = self.gui.load_font(
            resolve_resource_path(f":deeper:fonts/Roboto-Regular.ttf"), 16
        )

        self.gui.add_child(LayersWindow(self, lambda layer: self.select_layer(layer)))

        self.catalog = Catalog()
        self.gui.add_child(CatalogWindow(self.catalog, self.on_catalog))

        self.camera = WorldCamera(self.window, glm.vec3(), 1)
        self.gui.add_child(CameraWindow(self.camera))

        self.add_processors([RenderingProcessor(self), AnimationProcessor(self)])

        self.current_tool = self.pick_tool = PickTool(self, edit_state)
        self.stamp_tool = StampTool(self, edit_state)

        # TODO:Need glyph range which pyimgui does not support. :(
        # self.gui.load_font(resolve_resource_path(f':deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}'))

        font = pyglet.font.load("Material Icons")
        self.gui.add_child(
            MainMenu(
                children=[
                    Toolbar(
                        [
                            ToolButton(
                                IconsMaterialDesign.ICON_NAVIGATION, font, self.use_pick
                            ),
                            ToolButton(
                                IconsMaterialDesign.ICON_APPROVAL, font, self.use_stamp
                            ),
                        ]
                    )
                ]
            )
        )

    def select_layer(self, layer):
        logger.debug(layer.group)
        self.edit_state.current_layer = layer.group

    def use_pick(self):
        self.use_tool(self.pick_tool)

    def use_stamp(self):
        self.use_tool(self.stamp_tool)

    def on_catalog(self, blueprint):
        # exit()
        self.edit_state.current_blueprint = blueprint

    def draw(self):
        self.camera.use()
        super().draw()

        """
        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)
        """
