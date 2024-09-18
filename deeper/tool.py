import time

from crunge import sdl
from crunge.engine.view import View
from crunge.engine.controller import Controller

class Tool(Controller):
    def __init__(self, view: View, title='') -> None:
        super().__init__()
        self.view = view
        self.gui = view.gui
        self.window = view.window
        self.title = title
