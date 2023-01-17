import glm
import imgui

from deeper.dimgui import Widget

from ...kits.setting_widget_kit import SettingWidgetKit

from ...kits.blueprint_widget_kit import BlueprintWidgetKit
from ...blueprints import EntityBlueprint
from .component_widget import ComponentWidget, ComponentWidgetBuilder

class SettingsPanel(Widget):
    def __init__(self, blueprint):
        self.blueprint = blueprint
        settings = blueprint.settings
        self.settings = settings
        children = []
        bp = blueprint
        while bp:
            children.append(SettingWidgetKit.instance.build(bp.settings))
            bp = bp.base
        super().__init__(children)

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

        for child in self.children:
            expanded, child.visible = imgui.collapsing_header(child.blueprint.name, child.visible)
            if expanded:
                child.draw()


class EntityBpWidget(ComponentWidget):
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.panels = [SettingsPanel(blueprint), BlueprintsPanel(blueprint)]
        self.panel_names = ['Settings', 'Blueprints']
        self.current_index = 0
        self.current = None

        super().__init__(blueprint)

    def create(self, gui):
        super().create(gui)
        for panel in self.panels:
            panel.create(gui)
        return self

    def draw(self):
        changed, self.current_index = imgui.combo(
            "View", self.current_index, self.panel_names
        )
        current = self.panels[self.current_index]
        self.current = current
        self.current.draw()

class EntityBpWidgetBuilder(ComponentWidgetBuilder):
    key = EntityBlueprint
    cls = EntityBpWidget
