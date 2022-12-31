from ..blueprint import BlueprintBuilder, ComponentBlueprint

class SpriteVuBlueprint(ComponentBlueprint):
    pass

class SpriteVuBlueprintBuilder(BlueprintBuilder):
    key = 'SpriteVu'
    cls = SpriteVuBlueprint

class AnimatedSpriteVuBlueprint(ComponentBlueprint):
    pass

class AnimatedSpriteVuBlueprintBuilder(BlueprintBuilder):
    key = 'AnimatedSpriteVu'
    cls = AnimatedSpriteVuBlueprint