import glm
import imgui

from deeper.dimgui import Widget

from ...kits.setting_widget_kit import SettingWidgetKit

from ...kits.blueprint_widget_kit import BlueprintWidgetKit
from ...blueprints import EntityBlueprint
from .component_widget import ComponentWidget, ComponentWidgetBuilder

class SettingsPanel(Widget):
    def __init__(self, settings):
        self.settings = settings
        child = SettingWidgetKit.instance.build(settings)
        super().__init__([child])

class BlueprintsPanel(Widget):
    def __init__(self, blueprint):
        self.blueprint = blueprint

        children = []
        for child in blueprint.children:
            children.append(BlueprintWidgetKit.instance.build(child))
        super().__init__(children)

    def draw(self):
        imgui.text("name: ")
        imgui.same_line()
        imgui.text(self.blueprint.name)

        imgui.text("extends: ")
        imgui.same_line()
        imgui.text(self.blueprint.extends)

        imgui.text("category: ")
        imgui.same_line()
        imgui.text(self.blueprint.category)
        """
        changed, size = imgui.drag_float3(
            "Size", *self.blueprint.size, change_speed=0.1
        )
        if changed:
            self.block.size = size
        """
        for child in self.children:
            expanded, child.visible = imgui.collapsing_header(child.blueprint.name, child.visible)
            if expanded:
                child.draw()


class EntityBpWidget(ComponentWidget):
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.panels = [SettingsPanel(blueprint.settings), BlueprintsPanel(blueprint)]
        self.panel_names = ['Settings', 'Blueprints']
        self.current_index = 0
        self.current = None

        super().__init__(blueprint)

    def draw(self):
        clicked, self.current_index = imgui.combo(
            "View", self.current_index, self.panel_names
        )
        current = self.panels[self.current_index]
        """
        if current != self.current:
            if self.current:
                self.current.hide()
            current.show()
        """
        self.current = current
        self.current.draw()

class EntityBpWidgetBuilder(ComponentWidgetBuilder):
    key = EntityBlueprint
    cls = EntityBpWidget
