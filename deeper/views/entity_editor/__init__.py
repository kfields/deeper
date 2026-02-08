from crunge.engine import Scheduler

from deeper import Block
from deeper.blueprints import EntityBlueprint
from deeper.resources.icons import IconsMaterialDesign

from deeper.tools.pick_tool import PickTool

from deeper.widgets.toolbar import Toolbar, ToolButton
from deeper.widgets.entity_dock import EntityDock
from deeper.widgets.component.component_dock import ComponentDock

from ..scene_editor import SceneEditor


class EntityEditor(SceneEditor):
    def __init__(self, edit_state):
        super().__init__(edit_state.scene, "Entity Editor")
        self.edit_state = edit_state

    def _create(self):
        super()._create()
        self.gui.add_child(
            EntityDock(self.scene, self.edit_state.entity)
        )

        self.block = self.scene.component_for_entity(self.edit_state.entity, Block)

        self.blueprint = self.scene.component_for_entity(
            self.edit_state.entity, EntityBlueprint
        )
        self.gui.add_child(
            ComponentDock(self.blueprint)
        )

        pos = self.block.position
        self.scene_camera.look_at(pos)

        self.tool = self.pick_tool = PickTool(self, self.edit_state)

        self.gui.add_child(
            self.create_menubar(
                children=[
                    Toolbar(
                        [
                            ToolButton(
                                IconsMaterialDesign.ICON_NAVIGATION, self.use_pick
                            ),
                            ToolButton(IconsMaterialDesign.ICON_CLOSE, self.close),
                        ]
                    )
                ]
            )
        )

    def close(self):
        Scheduler().schedule_once(lambda dt: self.window.pop_view(), 0)

    def use_pick(self):
        self.tool = self.pick_tool

    def _draw(self):
        self.draw_aabb(self.block.aabb)
        super()._draw()
