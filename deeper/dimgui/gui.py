import imgui

from . import ArcadeRenderer

class Gui:
    def __init__(self, window):
        self.window = window
        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def draw(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
