import imgui

from .widget import Widget

class Window(Widget):
    _parent: None
    def __init__(self, title, children=[], on_close:callable=None, flags:int=0):
        super().__init__(children=children)
        self.title = title
        self.on_close = on_close
        self.closable = True if on_close is not None else False
        self.flags = flags

    def draw(self):
        collapsed, opened = imgui.begin(self.title, self.closable, flags=self.flags)
        super().draw()
        imgui.end()
        if not opened and self.closable:
            self.on_close()