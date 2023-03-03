from loguru import logger

import glm
import pyglet


from deeper.constants import *
from deeper.camera import WorldCamera
from deeper.processors import RenderingProcessor, AnimationProcessor
from deeper.catalog import Catalog
from deeper.widgets import CatalogWindow, LayersWindow, MenuItem
from deeper.resources.icons import IconsMaterialDesign

from deeper.tools.pick import PickTool
from deeper.tools.stamp import StampTool

from deeper.widgets.toolbar import Toolbar, ToolButton

from ...scene import Scene
from ..scene_editor import SceneEditor

class LevelEditorScene(Scene):
    def __init__(self, world, camera):
        super().__init__(world, camera)
        self.add_processors([RenderingProcessor(self), AnimationProcessor(self)])
    
class LevelEditor(SceneEditor):
    def __init__(self, window, edit_state):
        super().__init__(window, edit_state.world, 'Level Editor')
        self.edit_state = edit_state

        self.open_window('Layers')

        self.catalog = Catalog()
        self.open_window('Catalog')

        self.current_tool = self.pick_tool = PickTool(self, edit_state)
        self.stamp_tool = StampTool(self, edit_state)

        font = pyglet.font.load('Material Icons')
        self.gui.add_child(
            self.create_menubar(
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

    def create_scene(self):
        self.camera = WorldCamera(self.window)
        self.scene = LevelEditorScene(self.world, self.camera)

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
        super().draw()

    def create_view_menu(self, children=[]):
        menu = super().create_view_menu(
            [
                MenuItem('Catalog', lambda: self.open_window('Catalog')),
                MenuItem('Layers', lambda: self.open_window('Layers')),
                *children,
            ],
        )
        return menu

    def open_window(self, title):
        if title in self.windows:
            return
        on_close = lambda: self.close_window(title)
        window = None
        if title == 'Catalog':
            window = CatalogWindow(self.catalog, self.on_catalog, on_close=on_close)
        elif title == 'Layers':
            window = LayersWindow(self.scene, lambda layer: self.select_layer(layer), on_close=on_close)
        else:
            return super().open_window(title)

        self.windows[title] = window
        self.gui.add_child(window)
