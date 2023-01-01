from ..constants import *
from ..blueprint import BlueprintBuilder, ComponentBlueprint

class BlockBlueprint(ComponentBlueprint):
    size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]

class BlockBlueprintBuilder(BlueprintBuilder):
    key = 'Block'
    cls = BlockBlueprint

    def build(self, catalog, name, config, parent):
        #print(config)
        if not 'size' in config:
            if hasattr(parent, 'size'):
                config['size'] = parent.size
        return super().build(catalog, name, config, parent)
