from ..blueprint import BlueprintBuilder, ComponentBlueprint

class BlockBlueprint(ComponentBlueprint):
    pass

class BlockBlueprintBuilder(BlueprintBuilder):
    key = 'Block'
    cls = BlockBlueprint
