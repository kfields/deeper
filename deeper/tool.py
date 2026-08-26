from crunge.engine.screen import Screen
from crunge.engine.controller import Controller


class Tool(Controller):
    def __init__(self, screen: Screen, title="") -> None:
        super().__init__()
        self.screen = screen
        self.view = screen.view
        self.gui = screen.gui
        self.window = screen.window
        self.title = title
