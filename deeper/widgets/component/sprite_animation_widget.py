from crunge import imgui

from deeper.components.sprite_animation import SpriteAnimation
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class SpriteAnimationWidget(ComponentWidget):
    def __init__(self, animation):
        super().__init__(animation)
        self.animation = animation

    def _draw(self):
        changed, rate = imgui.drag_float(
            "Rate",
            self.animation.rate,
            v_speed=0.01,
            v_min=0.01,
            v_max=1.0,
        )
        if changed:
            self.animation.rate = rate


class SpriteAnimationWidgetBuilder(ComponentWidgetBuilder):
    key = SpriteAnimation
    cls = SpriteAnimationWidget
