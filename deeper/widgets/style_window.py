import imgui

from deeper.dimgui import Window

class StyleWindow(Window):
    def __init__(self, on_close:callable=None):
        super().__init__('Style', on_close=on_close)

    def draw(self):
        collapsed, opened = imgui.begin(self.title, self.closable, flags=self.flags)
        imgui.show_style_editor()
        imgui.end()
        if not opened and self.closable:
            self.on_close()
