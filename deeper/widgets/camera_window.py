import glm
import imgui

from deeper.dimgui import Widget, Window

class CameraPanel(Widget):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def draw(self):
        changed, position = imgui.drag_float3(
            "Position", *self.camera.position, change_speed=0.1
        )
        if changed:
            self.camera.position = glm.vec3(*position)

        changed, zoom = imgui.drag_float(
            "Zoom", self.camera.zoom, change_speed=0.01
        )
        if changed:
            self.camera.zoom = zoom


class CameraWindow(Window):
    def __init__(self, camera):
        super().__init__("Camera", [CameraPanel(camera)])
        self.camera = camera