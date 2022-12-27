import pyglet
import imgui

from deeper.dimgui import Window
from deeper.kits.component_widget_kit import ComponentWidgetKit

class EntityWindow(Window):
    #def __init__(self, world, entity, children = []):
    def __init__(self, world, entity):
        self.world = world
        self.entity = entity
        components = world.components_for_entity(entity)
        children = []
        for component in components:
            children.append(ComponentWidgetKit.instance.build(component))
        super().__init__("Entity", children)
    """
    def draw(self):
        imgui.begin('Catalog')
        imgui.end()
    """