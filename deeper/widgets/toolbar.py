import imgui

from deeper.dimgui import Widget
from .icon import IconButton

class ToolButton(IconButton):
    def __init__(self, text, font, callback):
        super().__init__(text, font, callback)
        self.selected = False

    def select(self):
        if self.selected:
            return True
        self.selected = True
        self.callback()
        return True

    def draw(self):        
        if self.selected:
            alpha = 1
        else:
            alpha = 0.6

        imgui.push_style_var(imgui.STYLE_ALPHA, alpha)
        if imgui.button(self.text):
            self.select()
        imgui.pop_style_var(1)
        return self.selected

class Toolbar(Widget):
    def __init__(self, children=[]):
        super().__init__(children)
        if children:
            children[0].select()
            self.selection = children[0]

    def draw(self):
        imgui.separator()
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.15, 0.15, 0.15)
        for child in self.children:
            if child.draw():
                if self.selection and self.selection != child:
                    self.selection.selected = False
                self.selection = child
        imgui.pop_style_color(1)
