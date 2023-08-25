import imgui

from deeper.dimgui import Widget


class Icon(Widget):
    def __init__(self, text, font):
        super().__init__()
        self.text = text
        self.font = font

    def create(self, gui):
        super().create(gui)
        return self

    def draw(self):
        imgui.text(self.text)

class IconButton(Widget):
    def __init__(self, text, font, callback = lambda : None):
        super().__init__()
        self.text = text
        self.font = font
        self.callback = callback

    def create(self, gui):
        super().create(gui)
        return self

    def draw(self):
        if imgui.button(self.text):
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
        return self

    def draw(self):
        text = self.on_text if self.on else self.off_text
        if imgui.button(text):
            self.on = not self.on
            self.callback(self.on)
            return True
