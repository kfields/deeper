import imgui

from deeper.dimgui import Widget

class Toolbutton(Widget):
    def __init__(self, text, selected=False):
        super().__init__()
        self.text = text
        self.selected = selected

    def draw(self):
        if self.selected:
            imgui.text(self.text)
        elif imgui.button(self.text):
            self.selected = True
            return True
            


class Toolbar(Widget):
    def __init__(self, children = []):
        super().__init__(children)
        if children:
            self.selection = children[0]

    def draw(self):
        for child in self.children:
            if child.draw():
                if self.selection:
                    self.selection.selected = False
                self.selection = child