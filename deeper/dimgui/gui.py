import imgui

from . import ArcadeRenderer
from .widget import Widget

class Gui(Widget):
    def __init__(self, window, children=[]):
        self.window = window
        super().__init__(children)
        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def add_child(self, child):
        super().add_child(child)
        child.create(self)

    def load_font(self, font_path):
        io = imgui.get_io()
        new_font = io.fonts.add_font_from_file_ttf(str(font_path), 20)
        self.renderer.refresh_font_texture()

    def start_render(self):
        imgui.new_frame()

    def finish_render(self):
        self.draw()
        imgui.end_frame()
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
