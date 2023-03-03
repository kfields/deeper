import webbrowser

from loguru import logger
from arcade.resources import resolve_resource_path

from deeper.constants import *

from .scene_view import SceneView
from ..widgets import MetricsWindow, CameraWindow, MainMenubar, Menu, MenuItem


doc_url = 'https://kfields.github.io/deeper/index.html'


class SceneEditor(SceneView):
    def __init__(self, window, world, title=""):
        super().__init__(window, world, title)
        self.windows = {}

        self.gui.default_font = self.gui.load_font(
            resolve_resource_path(':deeper:fonts/Roboto-Regular.ttf'), 16
        )

    def create_menubar(self, children):
        children = [
            Menu('File', [MenuItem('Quit', lambda: exit(1))]),
            self.create_view_menu(),
            Menu(
                'Help',
                [
                    MenuItem(
                        'Documentation',
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
            'View',
            [
                MenuItem('Metrics', lambda: self.open_window('Metrics')),
                MenuItem('Camera', lambda: self.open_window('Camera')),
                *children,
            ],
        )
        return menu

    def close_window(self, title):
        window = self.windows[title]
        self.windows.pop(title, None)
        self.gui.remove_child(window)

    def open_window(self, title):
        if title in self.windows:
            return
        on_close = lambda: self.close_window(title)
        window = None
        if title == 'Metrics':
            window = MetricsWindow(on_close=on_close)
        elif title == 'Camera':
            window = CameraWindow(self.camera, on_close=on_close)
        self.windows[title] = window
        self.gui.add_child(window)
