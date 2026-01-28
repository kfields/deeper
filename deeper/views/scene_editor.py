import webbrowser

from loguru import logger

from crunge import imgui
from crunge.engine import Scheduler
from crunge.engine.resource.resource_manager import ResourceManager

from deeper.resources.icons import IconsMaterialDesign

from ..scene_view import SceneView
from ..level import Level
from ..widgets import (
    MetricsWindow,
    StyleWindow,
    CameraWindow,
    MainMenubar,
    Menu,
    MenuItem,
)


doc_url = "https://kfields.github.io/deeper/index.html"

# Need to protect glyph_ranges from garbage collection
glyph_ranges = imgui.GlyphRanges([IconsMaterialDesign.ICON_MIN, IconsMaterialDesign.ICON_MAX, 0])

class SceneEditor(SceneView):
    def __init__(self, scene, title=""):
        super().__init__(scene, title)
        self.windows = {}

    def _create(self):
        super()._create()
        
        self.gui.load_default_font(
            ResourceManager().resolve_path(":deeper:/fonts/Roboto-Regular.ttf"), 16
        )

        self.gui.load_icon_font(
            ResourceManager().resolve_path(
                f":deeper:/icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}"
            ),
            16,
            glyph_ranges,
        )

    def new(self):
        Scheduler().schedule_once(lambda dt : self._new())

    def _new(self):
        from .level_editor import LevelEditor
        from ..state import LevelEditState
        from ..levels.basic_level import BasicLevel

        level = BasicLevel()
        view = LevelEditor(LevelEditState(level)).config(window=self.window).create()
        self.window.view = view

    def load(self):
        Scheduler().schedule_once(lambda dt: self._load())

    def _load(self):
        from .level_editor import LevelEditor
        from ..state import LevelEditState

        level = Level.load(ResourceManager().resolve_path(":deeper:/levels/test.json"))
        view = LevelEditor(LevelEditState(level)).config(window=self.window).create()
        self.window.view = view

    def save(self):
        self.world.save(ResourceManager().resolve_path(":deeper:/levels/"))

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
            window = CameraWindow(self.scene_camera, on_close=on_close)
        self.windows[title] = window
        self.gui.add_child(window)
