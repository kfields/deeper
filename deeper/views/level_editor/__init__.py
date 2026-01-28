from loguru import logger

from deeper.catalog import Catalog
from deeper.widgets import CatalogWindow, LayersWindow, MenuItem
from deeper.resources.icons import IconsMaterialDesign

from deeper.tools.pick_tool import PickTool
from deeper.tools.stamp import StampTool

from deeper.widgets.toolbar import Toolbar, ToolButton

from ..scene_editor import SceneEditor


class LevelEditor(SceneEditor):
    def __init__(self, edit_state):
        super().__init__(edit_state.scene, "Level Editor")
        self.edit_state = edit_state

    def _create(self):
        super()._create()
        self.open_window("Layers")

        self.catalog = Catalog.instance
        self.open_window("Catalog")

        self.pick_tool = PickTool(self, self.edit_state)
        self.stamp_tool = StampTool(self, self.edit_state)

        self.gui.add_child(
            self.create_menubar(
                children=[
                    Toolbar(
                        [
                            ToolButton(
                                IconsMaterialDesign.ICON_NAVIGATION, self.use_pick
                            ),
                            ToolButton(
                                IconsMaterialDesign.ICON_APPROVAL, self.use_stamp
                            ),
                        ]
                    )
                ]
            )
        )

    def enable(self):
        super().enable()
        self.tool = self.pick_tool

    def select_layer(self, layer):
        logger.debug(layer)
        self.edit_state.current_layer = layer

    def use_pick(self):
        self.tool = self.pick_tool

    def use_stamp(self):
        self.tool = self.stamp_tool

    def on_catalog(self, blueprint):
        self.edit_state.current_blueprint = blueprint

    def create_view_menu(self, children=[]):
        menu = super().create_view_menu(
            [
                MenuItem("Catalog", lambda: self.open_window("Catalog")),
                MenuItem("Layers", lambda: self.open_window("Layers")),
                *children,
            ],
        )
        return menu

    def open_window(self, title):
        if title in self.windows:
            return
        on_close = lambda: self.close_window(title)
        window = None
        if title == "Catalog":
            # window = CatalogWindow(self.catalog, self.on_catalog, on_close=on_close).create(self.gui)
            window = (
                CatalogWindow(self.catalog, self.on_catalog, on_close=on_close)
                .config(gui=self.gui)
                .create()
            )
        elif title == "Layers":
            # window = LayersWindow(self.scene, lambda layer: self.select_layer(layer), on_close=on_close).create(self.gui)
            window = (
                LayersWindow(
                    self.scene,
                    lambda layer: self.select_layer(layer),
                    on_close=on_close,
                )
                .config(gui=self.gui)
                .create()
            )
        else:
            return super().open_window(title)

        self.windows[title] = window
        self.gui.add_child(window)
