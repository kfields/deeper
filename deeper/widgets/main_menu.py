import webbrowser

from .menu import MainMenubar, Menu, MenuItem

doc_url = 'https://kfields.github.io/deeper/index.html'

class MainMenu(MainMenubar):
    def __init__(self, children=[]):
        children = [
            Menu('File', [MenuItem('Quit', lambda: exit(1))]),
            Menu('View', [MenuItem('Metrics', lambda: exit(1))]),
            Menu('Help', [MenuItem('Documentation', lambda: webbrowser.open(doc_url, new=2, autoraise=True))]),
            *children
        ]
        super().__init__(children=children)
