from loguru import logger

import imgui
import pyglet

from deeper.dimgui import Widget, Window
from deeper.resources.icons import IconsMaterialDesign
from .icon import IconToggleButton


class LayerWidget(Widget):
    def __init__(self, layer):
        self.layer = layer
        self.selected = False

        font = pyglet.font.load("Material Icons")

        super().__init__(
            [
                IconToggleButton(
                    IconsMaterialDesign.ICON_VISIBILITY,
                    IconsMaterialDesign.ICON_VISIBILITY_OFF,
                    font,
                    layer.visible,
                    lambda on: self.set_visible(on)
                )
            ]
        )

    def set_visible(self, value):
        logger.debug(value)
        self.layer.visible = value

    def draw(self):
        clicked, selected = imgui.selectable(self.layer.name, self.selected)
        imgui.next_column()
        super().draw()
        return clicked

    def draw_child(self, child):
        #imgui.same_line()
        super().draw_child(child)
        imgui.next_column()


class LayersPanel(Widget):
    def __init__(self, scene, callback):
        self.scene = scene
        self.callback = callback
        self.selection = None
        children = []
        for layer in scene.layers:
            children.append(LayerWidget(layer))
        self.select(children[0])
        super().__init__(children)

    def select(self, widget):
        if self.selection == widget:
            return
        if self.selection:
            self.selection.selected = False
        self.selection = widget
        widget.selected = True
        self.callback(widget.layer)

    def draw(self):
        imgui.begin_child("layers", -1, -1, border=True)
        imgui.columns(2, 'layeritems')
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.0, 0.0)
        for widget in self.children:
            clicked = widget.draw()
            if clicked:
                self.select(widget)
        imgui.pop_style_color(1)
        imgui.end_child()


class LayersWindow(Window):
    def __init__(self, scene, callback):
        super().__init__("Layers", [LayersPanel(scene, callback)])
        self.scene = scene
