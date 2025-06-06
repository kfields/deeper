from deeper.setting import AttrSetting, Vec2SettingVType
from deeper.widgets.setting import DragWrapper
from ...kits.setting_widget_kit import SettingWidgetKit

from deeper.components.sprite_vu import SpriteVuComponent
from .component_widget import ComponentWidget, ComponentWidgetBuilder


class SpriteVuWidget(ComponentWidget):
    def __init__(self, component):
        children = []
        children.append(
            DragWrapper(
                SettingWidgetKit.instance.build(
                    AttrSetting('offset', component, Vec2SettingVType), change_speed=0.01
                )
            )
        )
        super().__init__(component, children)


class SpriteVuWidgetBuilder(ComponentWidgetBuilder):
    key = SpriteVuComponent
    cls = SpriteVuWidget
