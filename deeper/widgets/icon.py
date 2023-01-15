import imgui

from deeper.dimgui import Widget

class Icon(Widget):
    def __init__(self, text, font):
        super().__init__()
        self.text = text
        self.font = font

    def create(self, gui):
        super().create(gui)
        image = self.font.render_to_image(self.text, 32, 32)
        self.texture = image.get_texture()
        return self

    def draw(self):
        imgui.image(self.texture.id, self.texture.width, self.texture.height, (0,1), (1,0))

class IconButton(Widget):
    def __init__(self, text, font, callback = lambda : None):
        super().__init__()
        self.text = text
        self.font = font
        self.callback = callback

    def create(self, gui):
        super().create(gui)
        image = self.font.render_to_image(self.text, 32, 32)
        self.texture = image.get_texture()
        return self

    def draw(self):
        if imgui.image_button(self.texture.id, self.texture.width, self.texture.height, (0,1), (1,0)):
            self.callback()
            return True
