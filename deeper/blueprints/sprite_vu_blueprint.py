from ..constants import *
from ..blueprint import BlueprintBuilder, ComponentBlueprint

class SpriteVuBlueprint(ComponentBlueprint):
    offset = [0, 0]

class SpriteVuBlueprintBuilder(BlueprintBuilder):
    key = 'SpriteVu'
    cls = SpriteVuBlueprint

    def build(self, catalog, name, config, parent):
        #print(config)
        if not 'image' in config:
            if hasattr(parent, 'image'):
                config['image'] = parent.image
        return super().build(catalog, name, config, parent)

class AnimatedSpriteVuBlueprint(ComponentBlueprint):
    offset = [0, 0]

class AnimatedSpriteVuBlueprintBuilder(BlueprintBuilder):
    key = 'AnimatedSpriteVu'
    cls = AnimatedSpriteVuBlueprint

    def build(self, catalog, name, config, parent):
        #print(config)
        if not 'image' in config:
            if hasattr(parent, 'image'):
                config['image'] = parent.image
        if not 'offset' in config:
            if hasattr(parent, 'offset'):
                config['offset'] = parent.offset

        return super().build(catalog, name, config, parent)
