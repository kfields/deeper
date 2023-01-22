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

class IconToggleButton(Widget):
    def __init__(self, on_text, off_text, font, on=False, callback = lambda on: None):
        super().__init__()
        self.on_text = on_text
        self.off_text = off_text
        self.font = font
        self.on = on
        self.callback = callback

    def create(self, gui):
        super().create(gui)
        image = self.font.render_to_image(self.on_text, 32, 32)
        self.on_texture = image.get_texture()
        image = self.font.render_to_image(self.off_text, 32, 32)
        self.off_texture = image.get_texture()
        return self

    def draw(self):
        texture = self.on_texture if self.on else self.off_texture
        if imgui.image_button(texture.id, texture.width, texture.height, (0,1), (1,0)):
            self.on = not self.on
            self.callback(self.on)
            return True
