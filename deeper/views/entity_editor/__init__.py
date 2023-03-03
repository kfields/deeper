import pyglet
from pyglet import clock

from deeper import Block
from deeper.blueprints import EntityBlueprint
from deeper.constants import *
from deeper.camera import WorldCamera
from deeper.processors import RenderingProcessor, AnimationProcessor
from deeper.resources.icons import IconsMaterialDesign

from deeper.tools.pick import PickTool

from deeper.widgets.toolbar import Toolbar, ToolButton
from deeper.widgets.entity_window import EntityWindow
from deeper.widgets.component.component_window import ComponentWindow

from ...scene import Scene
from ..scene_editor import SceneEditor


class EntityEditorScene(Scene):
    def __init__(self, world, camera):
        super().__init__(world, camera)
        self.add_processors([RenderingProcessor(self), AnimationProcessor(self)])

class EntityEditor(SceneEditor):
    def __init__(self, window, edit_state):
        super().__init__(window, edit_state.world, 'Entity Editor')
        self.edit_state = edit_state

        self.gui.add_child(EntityWindow(self.world, edit_state.entity))

        self.block = self.world.component_for_entity(edit_state.entity, Block)

        self.blueprint = self.world.component_for_entity(edit_state.entity, EntityBlueprint)
        self.gui.add_child(ComponentWindow(self.blueprint))

        pos = self.block.position
        #self.camera = WorldCamera(self.window, pos, 1)
        self.camera.look_at(pos)

        self.current_tool = self.pick_tool = PickTool(self, edit_state)

        font = pyglet.font.load('Material Icons')
        self.gui.add_child(
            self.create_menubar(
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

    def create_scene(self):
        self.camera = WorldCamera(self.window)
        self.scene = EntityEditorScene(self.world, self.camera)

    def close(self):
        #self.window.pop_view()
        clock.schedule_once(lambda dt, *args, **kwargs : self.window.pop_view(), 0)
    
    def use_pick(self):
        self.use_tool(self.pick_tool)

    def draw(self):
        super().draw()
        self.scene.draw_aabb(self.block.aabb)
