from crunge import imgui
from crunge.engine import Renderer

from deeper.blueprints.component.sprite_animation_blueprint import SpriteAnimationBlueprint
from .blueprint_widget import BlueprintWidget, BlueprintWidgetBuilder


class SpriteAnimationBpWidget(BlueprintWidget):
    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.blueprint = blueprint

    def _draw(self):
        changed, rate = imgui.drag_float(
            'Rate', self.blueprint.rate, v_speed=0.1
        )
        if changed:
            self.blueprint.rate = rate


class SpriteAnimationBpWidgetBuilder(BlueprintWidgetBuilder):
    key = SpriteAnimationBlueprint
    cls = SpriteAnimationBpWidget