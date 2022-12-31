import glm
import imgui

from deeper.blueprints.sprite_vu_blueprint import SpriteVuBlueprint, AnimatedSpriteVuBlueprint
from .blueprint_widget import BlueprintWidget, BlueprintWidgetBuilder

class SpriteVuBpWidget(BlueprintWidget):
    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.blueprint = blueprint

    def draw(self):
        changed, offset = imgui.drag_float2(
            "Offset", *self.blueprint.offset, change_speed=0.1
        )
        if changed:
            self.blueprint.offset = glm.vec2(*offset)

class SpriteVuBpWidgetBuilder(BlueprintWidgetBuilder):
    key = SpriteVuBlueprint
    cls = SpriteVuBpWidget


class AnimatedSpriteVuBpWidget(BlueprintWidget):
    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.blueprint = blueprint

    def draw(self):
        expanded, self.visible = imgui.collapsing_header("AnimatedSprite", self.visible)
        if not expanded:
            return
        changed, offset = imgui.drag_float2(
            "Offset", *self.blueprint.offset, change_speed=0.1
        )
        if changed:
            self.blueprint.offset = glm.vec2(*offset)


class AnimatedSpriteVuBpWidgetBuilder(BlueprintWidgetBuilder):
    key = AnimatedSpriteVuBlueprint
    cls = AnimatedSpriteVuBpWidget