from crunge import imgui

from crunge.engine.imgui.widget import Dock


class StyleDock(Dock):
    def __init__(self, on_close: callable = None):
        super().__init__("Style", on_close=on_close)


    def _begin(self):
        super()._begin()
        #collapsed, opened = imgui.begin(self.title, self.closable, flags=self.flags)
        imgui.show_style_editor()
        #imgui.end()
