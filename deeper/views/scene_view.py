import pyglet.window.mouse as mouse
from arcade import key

from ..view import View
from ..scene import Scene

class SceneView(View):
    scene: Scene = None

    def __init__(self, window, scene, title=''):
        super().__init__(window, title)
        #self.camera = None
        self.camera = scene.camera
        self.scene = scene
        #self.create_scene()

    def create_scene(self):
        pass

    def on_show_view(self):
        super().on_show_view()
        self.scene.enable()

    def on_hide_view(self):
        super().on_hide_view()
        self.scene.disable()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.scene.resize(width, height)

    def on_update(self, delta_time: float):
        self.scene.update(delta_time)
        return super().on_update(delta_time)

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

    def draw(self):
        self.scene.draw()
        super().draw()
