#import pyglet.window.mouse as mouse
#from arcade import key
import glm

from crunge.engine import Renderer
from crunge.engine.d2.renderer_2d import Renderer2D

from ..view import View
from ..scene import Scene

from ..camera import WorldCamera

class SceneView(View):
    scene: Scene = None

    def __init__(self, scene, title=''):
        super().__init__(title)
        self.scene = scene

    def _create(self, window):
        super()._create(window)
        self.scene.camera = WorldCamera(self.camera, glm.vec3(0, 0, 0), 1.0)

    def on_show(self):
        super().on_show()
        self.scene.enable()

    def on_hide(self):
        super().on_hide()
        self.scene.disable()

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.scene.resize(size)

    def update(self, delta_time: float):
        self.scene.update(delta_time)
        return super().update(delta_time)

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == key.NUM_ADD:
            self.camera.zoom = self.camera.zoom + .1
        elif symbol == key.NUM_SUBTRACT:
            self.camera.zoom = self.camera.zoom - .1

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == mouse.RIGHT:
            self.camera.pan(-dx, -dy)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.camera.zoom_pct = self.camera.zoom_pct + scroll_y * 10

    def draw(self, renderer: Renderer2D):
        # logger.debug("DemoView.draw()")
        self.renderer.texture_view = renderer.texture_view
        
        with self.renderer:
            self.scene.draw(self.renderer)

        super().draw(renderer)
