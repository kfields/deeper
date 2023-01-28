from loguru import logger

import imgui
import pyglet

from deeper.dimgui import Widget, Window
from deeper.resources.icons import IconsMaterialDesign
from .dragger import Dragger
from .icon import IconToggleButton, Icon, IconButton
from .menu import Menubar, Menu, MenuItem
from .selectable import SelectableBase, ExclusiveSelectableGroup, Selectable, EditableSelectable


class LayerWidget(SelectableBase):
    def __init__(self, layer, callback):
        self.layer = layer
        self.selectable = EditableSelectable(self.layer.name, lambda child: self.on_child_selected(child), width=128)
        font = pyglet.font.load("Material Icons")
        super().__init__(
            layer.name,
            callback,
            selected=False,
            children=[
                IconButton(IconsMaterialDesign.ICON_GRID_ON, font),
                #Dragger(IconButton(IconsMaterialDesign.ICON_GRID_ON, font), self.on_drag),
                self.selectable,
                IconToggleButton(
                    IconsMaterialDesign.ICON_VISIBILITY,
                    IconsMaterialDesign.ICON_VISIBILITY_OFF,
                    font,
                    layer.visible,
                    lambda on: self.set_visible(on)
                )
            ]
        )

    def on_drag(self):
        self.gui.dropboard.value = self
        imgui.button(str(self))

    def on_drop(self):
        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload('itemtype')
            if payload is not None:
                print('Received:', payload)
                #self.wrapped.value = self.gui.dropboard.value.value
                if imgui.begin_popup("drop-popup"):
                    imgui.text("Select one")
                    imgui.separator()
                    imgui.selectable("One")
                    imgui.selectable("Two")
                    imgui.selectable("Three")
                    imgui.end_popup()

            imgui.end_drag_drop_target()

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
        logger.debug(value)
        self.layer.visible = value

    def draw(self):
        imgui.begin_group()
        super().draw()
        imgui.end_group()
        #self.draw_context_popup()
        #self.on_drop()

    def draw_child(self, child):
        super().draw_child(child)
        if child != self.children[-1]:
            imgui.same_line()
    """
    def draw_context_popup(self):
        if imgui.begin_popup_context_item(str(id(self))):
            clicked, selected = imgui.selectable("Delete")
            imgui.end_popup()
    """

class LayersPanel(ExclusiveSelectableGroup):
    def __init__(self, scene, callback):
        self.scene = scene
        children = []
        for layer in scene.layers:
            children.append(LayerWidget(layer, callback))
        super().__init__(children, callback)
        children[0].select()
    
    def create_child(self, layer, callback):
        return LayerWidget(layer, callback).create(self.gui)

    def on_swap(self, i, j):
        self.scene.swap_layers(i, j)

    def draw(self):
        imgui.begin_child("layers", -1, -1)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.0, 0.0)
        #super().draw()
        self.draw_sortable(self.on_swap)
        imgui.pop_style_color(1)
        imgui.end_child()

    def draw_child(self, child):
        super().draw_child(child)
        self.draw_child_context_popup(child)

    def draw_child_context_popup(self, child):
        if imgui.begin_popup_context_item(str(id(child))):
            clicked, selected = imgui.selectable("Delete")
            if clicked:
                self.scene.remove_layer(child.layer)
                self.remove_child(child)
            imgui.end_popup()

class LayersWindow(Window):
    def __init__(self, scene, callback):
        self.scene = scene
        self.callback = callback
        self.panel = LayersPanel(scene, lambda child: callback(child.layer))
        children = [
            Menubar([
                Menu('New', [
                    MenuItem('Layer', lambda: self.new_layer())
                ])
            ]),
            self.panel
        ]

        super().__init__("Layers", children, flags=imgui.WINDOW_MENU_BAR)
        self.scene = scene

    def new_layer(self):
        layer = self.scene.new_layer()
        self.panel.add_child(self.panel.create_child(layer, lambda child: self.callback(child.layer)))
