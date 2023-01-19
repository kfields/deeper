import glm
import imgui

from deeper.dimgui import Widget, Window


class LayerWidget(Widget):
    def __init__(self, layer):
        super().__init__()
        self.layer = layer
        self.selected = False

    def draw(self):
        clicked, selected = imgui.selectable(self.layer.name, self.selected)
        #imgui.same_line()
        return clicked


class LayersPanel(Widget):
    def __init__(self, scene, callback):
        self.scene = scene
        self.callback = callback
        self.selection = None
        children = []
        for layer in scene.layers:
            children.append(LayerWidget(layer))
        super().__init__(children)

    def draw(self):
        imgui.begin_child("layers", -1, -1, border=True)
        for widget in self.children:
            clicked = widget.draw()
            if clicked:
                if self.selection:
                    self.selection.selected = False
                self.selection = widget
                widget.selected = True
                self.callback(widget.layer)
        imgui.end_child()


class LayersWindow(Window):
    def __init__(self, scene, callback):
        super().__init__("Layers", [LayersPanel(scene, callback)])
        self.scene = scene
