import pyglet
import imgui

from deeper.dimgui import Widget

class Toolbutton(Widget):
    def __init__(self, text, font):
        super().__init__()
        self.text = text
        self.font = font
        self.selected = False

    def select(self):
        self.selected = True

    def create(self, gui):
        super().create(gui)
        image = self.font.render_to_image(self.text, 32, 32)
        self.texture = image.get_texture()

    def draw(self):
        if self.selected:
            imgui.image(self.texture.id, self.texture.width, self.texture.height, (0,1), (1,0))
        elif imgui.image_button(self.texture.id, self.texture.width, self.texture.height, (0,1), (1,0)):
            self.select()
            return True


class Toolbar(Widget):
    def __init__(self, children = []):
        super().__init__(children)
        if children:
            children[0].select()
            self.selection = children[0]

    def draw(self):
        for child in self.children:
            if child.draw():
                if self.selection:
                    self.selection.selected = False
                self.selection = child