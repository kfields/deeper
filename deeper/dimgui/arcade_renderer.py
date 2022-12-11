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
            window.push_handlers(
                self.on_mouse_motion,
                self.on_key_press,
                self.on_key_release,
                self.on_text,
                self.on_mouse_drag,
                self.on_mouse_press,
                self.on_mouse_release,
                self.on_mouse_scroll,
                self.on_resize,
            )
