from ..constants import *
from ..blueprint import Blueprint

class EntityBlueprint(Blueprint):
    size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]
    def __init__(self, catalog, name, config):
        super().__init__(catalog, name, config)
