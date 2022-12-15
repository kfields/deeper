from imgui.integrations import compute_fb_scale

from .pyglet_mixin import  PygletMixin
from .arcade_gl_renderer import ArcadeGLRenderer

class ArcadeRenderer(PygletMixin, ArcadeGLRenderer):
    def __init__(self, window, attach_callbacks=True):
        super().__init__(window)
        window_size = window.get_size()
        viewport = window.get_viewport()
        viewport_size = viewport[1] - viewport[0], viewport[3] - viewport[2]

        self.io.display_size = window_size
        self.io.display_fb_scale = compute_fb_scale(window_size, viewport_size)

        self._map_keys()

        if attach_callbacks:
            self._attach_callbacks(window)
