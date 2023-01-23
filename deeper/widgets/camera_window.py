import glm
import imgui

from deeper.dimgui import Widget, Window

class CameraPanel(Widget):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def draw(self):
        imgui.input_float3(
            "Position", *self.camera.position, flags=imgui.INPUT_TEXT_READ_ONLY
        )
        changed, pct = imgui.drag_float(
            "Zoom", self.camera.zoom_pct, change_speed=10
        )
        if changed:
            self.camera.zoom_pct = pct

class CameraWindow(Window):
    def __init__(self, camera):
        super().__init__("Camera", [CameraPanel(camera)])
        self.camera = camera