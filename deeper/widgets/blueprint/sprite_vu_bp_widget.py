import glm
import imgui

from deeper.components.sprite_vu import SpriteVu, AnimatedSpriteVu
from .blueprint_widget import BlueprintWidget, BlueprintWidgetBuilder

class SpriteVuBpWidget(BlueprintWidget):
    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.blueprint = blueprint

    def draw(self):
        expanded, self.visible = imgui.collapsing_header("Sprite", self.visible)
        if not expanded:
            return
        changed, offset = imgui.drag_float2(
            "Offset", *self.blueprint.offset, change_speed=0.1
        )
        if changed:
            self.blueprint.offset = glm.vec2(*offset)

class SpriteVuBpWidgetBuilder(BlueprintWidgetBuilder):
    key = SpriteVu
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
    key = AnimatedSpriteVu
    cls = AnimatedSpriteVuBpWidget