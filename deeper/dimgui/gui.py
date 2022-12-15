import imgui

from . import ArcadeRenderer
from .widget import Widget

class Gui(Widget):
    def __init__(self, window, children=[]):
        super().__init__(children)
        self.window = window
        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def load_font(self, font_path):
        io = imgui.get_io()
        new_font = io.fonts.add_font_from_file_ttf(str(font_path), 20)
        self.renderer.refresh_font_texture()

    def draw(self):
        super().draw()
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
