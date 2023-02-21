import glm
import pyglet
from pyglet import clock
import arcade
from arcade.resources import resolve_resource_path
from arcade import key

from deeper import Block
from deeper.blueprints import EntityBlueprint
from deeper.constants import *
from deeper.camera import WorldCamera
from deeper.processors import RenderingProcessor, AnimationProcessor
from deeper.widgets import MainMenu
from deeper.resources.icons import IconsMaterialDesign

from deeper.tools.pick import PickTool

from deeper.widgets.toolbar import Toolbar, ToolButton
from deeper.widgets.entity_window import EntityWindow
from deeper.widgets.component.component_window import ComponentWindow

from ..scene_view import SceneView

class EntityEditor(SceneView):
    def __init__(self, window, edit_state):
        super().__init__(window, edit_state.world, 'Entity Editor')
        self.edit_state = edit_state

        #TODO: Make helper method inside gui?
        self.gui.default_font = self.gui.load_font(
            resolve_resource_path(f":deeper:fonts/Roboto-Regular.ttf"), 16
        )

        self.gui.add_child(EntityWindow(self.world, edit_state.entity))


        self.block = self.world.component_for_entity(edit_state.entity, Block)

        self.blueprint = self.world.component_for_entity(edit_state.entity, EntityBlueprint)
        self.gui.add_child(ComponentWindow(self.blueprint))

        pos = self.block.position
        self.camera = WorldCamera(self.window, pos, 1)

        self.add_processors([RenderingProcessor(self), AnimationProcessor(self)])

        self.current_tool = self.pick_tool = PickTool(self, edit_state)


        # TODO:Need glyph range which pyimgui does not support. :(
        # self.gui.load_font(resolve_resource_path(f':deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}'))

        font = pyglet.font.load("Material Icons")
        self.gui.add_child(
            MainMenu(
                children=[
                    Toolbar(
                        [
                            ToolButton(IconsMaterialDesign.ICON_NAVIGATION, font, self.use_pick),
                            ToolButton(IconsMaterialDesign.ICON_CLOSE, font, self.close),
                        ]
                    )
                ]
            )
        )

    def close(self):
        #self.window.pop_view()
        clock.schedule_once(lambda dt, *args, **kwargs : self.window.pop_view(), 0)
    
    def use_pick(self):
        self.use_tool(self.pick_tool)

    def draw(self):
        self.camera.use()
        super().draw()

        self.draw_aabb(self.block.aabb)

        """
        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)
        """
