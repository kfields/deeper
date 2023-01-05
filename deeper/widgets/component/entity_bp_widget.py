import glm
import imgui

from ...kits.blueprint_widget_kit import BlueprintWidgetKit
from ...blueprints import EntityBlueprint
from .component_widget import ComponentWidget, ComponentWidgetBuilder

class EntityBpWidget(ComponentWidget):
    def __init__(self, blueprint):
        self.blueprint = blueprint

        children = []
        for child in blueprint.children:
            children.append(BlueprintWidgetKit.instance.build(child))
        super().__init__(blueprint, children)

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

class EntityBpWidgetBuilder(ComponentWidgetBuilder):
    key = EntityBlueprint
    cls = EntityBpWidget
