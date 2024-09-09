from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, reconstructor

from crunge.engine.loader.texture_loader import TextureLoader

from ...constants import *
from ...settings.component.sprite_animation_settings import SpriteAnimationSettings
from ...blueprint import BlueprintBuilder
from .component_blueprint import ComponentBlueprint

class SpriteAnimationBlueprint(ComponentBlueprint):
    id: Mapped[int] = mapped_column(ForeignKey('ComponentBlueprint.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'SpriteAnimationBlueprint',
        'inherit_condition': (id == ComponentBlueprint.id),
        
    }

    settings_class = SpriteAnimationSettings
    borrowed_settings = ['image', 'offset']
    offset = [0, 0]
    pingpong = False

    def __init__(self, catalog, name, config, entity, parent):
        super().__init__(catalog, name, config, entity, parent)
        self._texture = None

    @reconstructor
    def reconstruct(self):
        self._texture = None

    @property
    def texture(self):
        if not self._texture:
            #self._texture = arcade.load_texture(self.image)
            self._texture = TextureLoader().load(self.image)
        return self._texture

class SpriteAnimationBlueprintBuilder(BlueprintBuilder):
    key = 'SpriteAnimation'
    cls = SpriteAnimationBlueprint
