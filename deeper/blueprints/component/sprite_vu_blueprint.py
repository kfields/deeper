from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...constants import *
from ...settings.component.sprite_vu_settings import SpriteVuSettings, AnimatedSpriteVuSettings
from ...blueprint import BlueprintBuilder
from .component_blueprint import ComponentBlueprint

class SpriteVuBlueprint(ComponentBlueprint):
    id: Mapped[int] = mapped_column(ForeignKey("ComponentBlueprint.id"), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'SpriteVuBlueprint',
        'inherit_condition': (id == ComponentBlueprint.id),
        
    }

    settings_class = SpriteVuSettings
    borrowed_settings = ['image', 'offset']
    offset = [0, 0]


class SpriteVuBlueprintBuilder(BlueprintBuilder):
    key = "SpriteVu"
    cls = SpriteVuBlueprint
    """
    def build(self, catalog, name, config, parent):
        print(config)
        if not "image" in config:
            if hasattr(parent, "image"):
                #print(parent.image)
                config["image"] = parent.image
        if not "offset" in config:
            if hasattr(parent, "offset"):
                config["offset"] = parent.offset
        return super().build(catalog, name, config, parent)
    """

class AnimatedSpriteVuBlueprint(ComponentBlueprint):
    id: Mapped[int] = mapped_column(ForeignKey("ComponentBlueprint.id"), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'AnimatedSpriteVuBlueprint',
        'inherit_condition': (id == ComponentBlueprint.id),
    }

    settings_class = AnimatedSpriteVuSettings
    offset = [0, 0]
    borrowed_settings = ['image', 'offset']


class AnimatedSpriteVuBlueprintBuilder(BlueprintBuilder):
    key = "AnimatedSpriteVu"
    cls = AnimatedSpriteVuBlueprint
    """
    def build(self, catalog, name, config, parent):
        # print(config)
        if not "image" in config:
            if hasattr(parent, "image"):
                config["image"] = parent.image
        if not "offset" in config:
            if hasattr(parent, "offset"):
                config["offset"] = parent.offset

        return super().build(catalog, name, config, parent)
    """