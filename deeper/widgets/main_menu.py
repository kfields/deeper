from .menu import MainMenubar, Menu, MenuItem

class MainMenu(MainMenubar):
    def __init__(self, children=[]):
        children = [
            Menu('File', [MenuItem('Quit', lambda: exit(1))]),
            *children
        ]
        super().__init__(children=children)
