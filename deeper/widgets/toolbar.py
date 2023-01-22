import imgui

from deeper.dimgui import Widget
from .icon import IconButton

class ToolButton(IconButton):
    def __init__(self, text, font, callback):
        super().__init__(text, font, callback)
        self.selected = False

    def select(self):
        if self.selected:
            return False
        self.selected = True
        self.callback()
        return True

    def draw(self):
        tint_color = (1, 1, 1, 0.6)
        #border_color=(0, 0, 0, 0)
        #frame_padding = -1
        if self.selected:
            tint_color = (1, 1, 1, 1)
            #border_color=(.1, .1, .1, 1)
        if imgui.image_button(
            self.texture.id,
            self.texture.width,
            self.texture.height,
            (0, 1),
            (1, 0),
            tint_color,
            #border_color,
            #frame_padding,
        ):
            return self.select()


class Toolbar(Widget):
    def __init__(self, children=[]):
        super().__init__(children)
        if children:
            children[0].select()
            self.selection = children[0]

    def draw(self):
        imgui.separator()
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.15, 0.15, 0.15)
        # imgui.push_style_var(imgui.STYLE_ALPHA, 0.9)
        for child in self.children:
            if child.draw():
                if self.selection:
                    self.selection.selected = False
                self.selection = child
        # imgui.pop_style_var(1)
        imgui.pop_style_color(1)
