import glm
import imgui

from deeper.blueprints.component.sprite_animation_blueprint import SpriteAnimationBlueprint
from .blueprint_widget import BlueprintWidget, BlueprintWidgetBuilder


class SpriteAnimationBpWidget(BlueprintWidget):
    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.blueprint = blueprint

    def draw(self):
        changed, rate = imgui.drag_float(
            "Rate", self.blueprint.rate, change_speed=0.1
        )
        if changed:
            self.blueprint.rate = rate


class SpriteAnimationBpWidgetBuilder(BlueprintWidgetBuilder):
    key = SpriteAnimationBlueprint
    cls = SpriteAnimationBpWidget