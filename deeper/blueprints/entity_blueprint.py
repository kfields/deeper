from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..constants import *
from ..settings import EntitySettings
from ..blueprint import Blueprint


class EntityBlueprint(Blueprint):
    id: Mapped[int] = mapped_column(ForeignKey("Blueprint.id"), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'EntityBlueprint',
        'inherit_condition': (id == Blueprint.id),
    }

    settings_class = EntitySettings
    size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]

    def __init__(self, catalog, name, config):
        super().__init__(catalog, name, config)
