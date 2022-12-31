import glm
import imgui

from deeper import EntityBlueprint
from .component_widget import ComponentWidget, ComponentWidgetBuilder
from deeper.kits.blueprint_widget_kit import BlueprintWidgetKit

class EntityBpWidget(ComponentWidget):
    def __init__(self, blueprint):
        #super().__init__(blueprint)
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

        changed, extents = imgui.drag_float3(
            "Extents", *self.blueprint.extents, change_speed=0.1
        )
        if changed:
            self.block.extents = extents

        for child in self.children:
            expanded, child.visible = imgui.collapsing_header(child.blueprint.name, child.visible)
            if expanded:
                child.draw()

class EntityBpWidgetBuilder(ComponentWidgetBuilder):
    key = EntityBlueprint
    cls = EntityBpWidget
