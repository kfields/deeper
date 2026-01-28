from loguru import logger

from crunge import imgui

from crunge.engine.imgui.widget import Window

from deeper.resources.icons import IconsMaterialDesign
from .icon import IconToggleButton, IconButton
from .menu import Menubar, Menu, MenuItem
from .selectable import SelectableBase, ExclusiveSelectableGroup, EditableSelectable
from ..scene import Scene
from ..scene_layer import SceneLayer


class LayerWidget(SelectableBase):
    def __init__(self, layer: SceneLayer, callback):
        self.layer = layer
        self.selectable = EditableSelectable(
            self.layer.name, lambda child: self.on_child_selected(child), width=128
        )
        super().__init__(
            layer.name,
            callback,
            selected=False,
            children=[
                IconButton(IconsMaterialDesign.ICON_GRID_ON),
                IconToggleButton(
                    IconsMaterialDesign.ICON_VISIBILITY,
                    IconsMaterialDesign.ICON_VISIBILITY_OFF,
                    layer.visible,
                    lambda on: self.set_visible(on),
                ),
                self.selectable,
            ],
        )

    def on_child_selected(self, child):
        self.callback(self)

    def select(self, selected=True):
        self.selectable.select(selected)

    @property
    def selected(self):
        return self.selectable.selected

    @selected.setter
    def selected(self, value):
        self.selectable.selected = value

    def set_visible(self, value):
        logger.debug(f"set_visible: layer={self.layer}, value={value}")
        self.layer.visible = value

    """
    @property
    def visible(self):
        return self.layer.visible
    
    @visible.setter
    def visible(self, value):
        self.layer.visible = value
    """

    def _draw(self):
        imgui.begin_group()
        super()._draw()
        imgui.end_group()

    def draw_child(self, child):
        super().draw_child(child)
        if child != self.children[-1]:
            imgui.same_line()


class LayersPanel(ExclusiveSelectableGroup):
    def __init__(self, scene: Scene, callback):
        self.scene = scene
        children = []
        for layer in scene.layers:
            children.append(LayerWidget(layer, callback))
        super().__init__(children, callback)
        children[0].select()

    def create_child(self, layer, callback):
        # return LayerWidget(layer, callback).create(self.gui)
        return LayerWidget(layer, callback).config(gui=self.gui).create()

    def on_swap(self, i, j):
        self.scene.swap_layers(i, j)

    def _draw(self):
        imgui.begin_child("layers", (-1, -1))
        # imgui.push_style_color(imgui.Col.COL_BUTTON, 0.0, 0.0, 0.0)
        # imgui.push_style_color(imgui.Col.COL_BUTTON.value, imgui.Vec4(0.0, 0.0, 0.0, 0.0))
        self.draw_sortable(self.on_swap)
        # imgui.pop_style_color(1)
        imgui.end_child()
        # super()._draw()

    def draw_child(self, child):
        super().draw_child(child)
        self.draw_child_context_popup(child)

    def draw_child_context_popup(self, child):
        if imgui.begin_popup_context_item(str(id(child))):
            selected = False
            clicked, selected = imgui.selectable("Delete", selected)
            if clicked:
                self.scene.remove_layer(child.layer)
                self.remove_child(child)
            imgui.end_popup()


class LayersWindow(Window):
    def __init__(self, scene, callback, on_close: callable = None):
        self.scene = scene
        self.callback = callback
        self.panel = LayersPanel(scene, lambda child: callback(child.layer))
        children = [
            Menubar([Menu("New", [MenuItem("Layer", lambda: self.new_layer())])]),
            self.panel,
        ]

        super().__init__(
            "Layers", children, on_close=on_close, flags=imgui.WindowFlags.MENU_BAR
        )
        self.scene = scene

    def new_layer(self):
        layer = self.scene.new_layer()
        self.panel.add_child(
            self.panel.create_child(layer, lambda child: self.callback(child.layer))
        )
