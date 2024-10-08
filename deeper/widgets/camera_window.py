from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.imgui.widget import Widget, Window

from ..scene_camera import SceneCamera

class CameraPanel(Widget):
    def __init__(self, camera: SceneCamera):
        super().__init__()
        self.camera = camera

    def draw(self, renderer: Renderer):
        imgui.input_float3(
            'Position', tuple(self.camera.position), flags=imgui.InputTextFlags.READ_ONLY
        )
        changed, pct = imgui.drag_float(
            'Zoom', self.camera.zoom_pct, v_speed=10
        )
        if changed:
            self.camera.zoom_pct = pct

class CameraWindow(Window):
    def __init__(self, camera, on_close:callable=None):
        super().__init__('Camera', [CameraPanel(camera)], on_close=on_close)
        self.camera = camera