import webbrowser

from loguru import logger
from pyglet import clock
from arcade.resources import resolve_resource_path
import imgui

from deeper.constants import *
from deeper.resources.icons import IconsMaterialDesign

from .scene_view import SceneView
from ..level import Level
from ..widgets import MetricsWindow, StyleWindow, CameraWindow, MainMenubar, Menu, MenuItem


doc_url = "https://kfields.github.io/deeper/index.html"


class SceneEditor(SceneView):
    def __init__(self, window, scene, title=""):
        super().__init__(window, scene, title)
        self.windows = {}

        self.gui.load_default_font(
            resolve_resource_path(":deeper:fonts/Roboto-Regular.ttf"), 16
        )

        glyph_ranges = imgui.GlyphRanges([IconsMaterialDesign.ICON_MIN, IconsMaterialDesign.ICON_MAX, 0])
        self.gui.load_icon_font(
            resolve_resource_path(f':deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}'), 16, glyph_ranges
        )

    def new(self):
        clock.schedule_once(lambda dt, *args, **kwargs : self._new(), 0)

    def _new(self):
        from .level_editor import LevelEditor
        from ..state import WorldEditState
        from ..levels.basic_level import BasicLevel
        level = BasicLevel()
        view = LevelEditor(self.window, WorldEditState(level))
        self.window.show_view(view)

    def load(self):
        clock.schedule_once(lambda dt, *args, **kwargs : self._load(), 0)

    def _load(self):
        from .level_editor import LevelEditor
        from ..state import WorldEditState
        level = Level.load(resolve_resource_path(":deeper:levels/test.json"))
        view = LevelEditor(self.window, WorldEditState(level))
        self.window.show_view(view)

    def save(self):
        self.world.save(resolve_resource_path(":deeper:levels/"))

    def create_menubar(self, children):
        children = [
            Menu(
                "File",
                [
                    MenuItem("New", lambda: self.new()),
                    MenuItem("Load", lambda: self.load()),
                    MenuItem("Save", lambda: self.save()),
                    MenuItem("Exit", lambda: exit(1)),
                ],
            ),
            self.create_view_menu(),
            Menu(
                "Help",
                [
                    MenuItem(
                        "Documentation",
                        lambda: webbrowser.open(doc_url, new=2, autoraise=True),
                    )
                ],
            ),
            *children,
        ]
        menubar = MainMenubar(children=children)
        return menubar

    def create_view_menu(self, children=[]):
        menu = Menu(
            "View",
            [
                MenuItem("Metrics", lambda: self.open_window("Metrics")),
                MenuItem("Style", lambda: self.open_window("Style")),
                MenuItem("Camera", lambda: self.open_window("Camera")),
                *children,
            ],
        )
        return menu

    def close_window(self, title):
        if not title in self.windows:
            return
        window = self.windows[title]
        self.windows.pop(title, None)
        self.gui.remove_child(window)

    def open_window(self, title):
        if title in self.windows:
            return
        on_close = lambda: self.close_window(title)
        window = None
        if title == "Metrics":
            window = MetricsWindow(on_close=on_close)
        elif title == "Style":
            window = StyleWindow(on_close=on_close)
        elif title == "Camera":
            window = CameraWindow(self.camera, on_close=on_close)
        self.windows[title] = window
        self.gui.add_child(window)
