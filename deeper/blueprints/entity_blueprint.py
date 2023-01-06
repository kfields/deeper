from ..constants import *
from ..settings import EntitySettings
from ..blueprint import Blueprint


class EntityBlueprint(Blueprint):
    settings_class = EntitySettings
    size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]

    def __init__(self, catalog, name, config):
        super().__init__(catalog, name, config)
