import pyglet
import imgui

from deeper.dimgui import Widget, Window
from deeper.kits.component_widget_kit import ComponentWidgetKit

class EntityPanel(Widget):
    def __init__(self, children=...):
        super().__init__(children)

    def draw(self):
        for child in self.children:
            expanded, child.visible = imgui.collapsing_header(child.name, child.visible)
            if expanded:
                child.draw()
        return True

class EntityWindow(Window):
    def __init__(self, world, entity):
        self.world = world
        self.entity = entity
        components = world.components_for_entity(entity)
        children = []
        for component in components:
            children.append(ComponentWidgetKit.instance.build(component))
        #super().__init__("Entity", children)
        super().__init__("Entity", children=[EntityPanel(children)])
