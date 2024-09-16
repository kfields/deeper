from loguru import logger

from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.imgui.widget import Widget


class Icon(Widget):
    def __init__(self, text):
        super().__init__()
        text += f"##{str(self.id)}" # Can't have buttons with the same text
        self.text = text

    def draw(self, renderer: Renderer):
        imgui.text(self.text)

class IconButton(Widget):
    def __init__(self, text, callback = lambda : None):
        super().__init__()
        text += f"##{str(self.id)}" # Can't have buttons with the same text
        self.text = text
        self.callback = callback

    def draw(self, renderer: Renderer):
        if imgui.button(self.text):
            self.callback()
            return True

class IconToggleButton(Widget):
    def __init__(self, on_text, off_text, on=False, callback = lambda on: None):
        super().__init__()
        self.on_text = on_text
        self.off_text = off_text
        self.on = on
        self.callback = callback

    def __str__(self) -> str:
        return f"IconToggleButton: on={self.on}"
    
    def __repr__(self) -> str:
        return self.__repr__()
    
    def draw(self, renderer: Renderer):
        text = self.on_text if self.on else self.off_text
        text += f"##{str(self.id)}" # Can't have buttons with the same text
        if imgui.button(text):
            logger.debug(self)
            self.on = not self.on
            self.callback(self.on)
            return True
