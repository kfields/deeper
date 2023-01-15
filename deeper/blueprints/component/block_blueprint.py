from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...constants import *
from ...settings.component.block_settings import BlockSettings
from ...blueprint import BlueprintBuilder
from .component_blueprint import ComponentBlueprint


class BlockBlueprint(ComponentBlueprint):
    id: Mapped[int] = mapped_column(ForeignKey("ComponentBlueprint.id"), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'BlockBlueprint',
        'inherit_condition': (id == ComponentBlueprint.id),
    }

    settings_class = BlockSettings
    borrowed_settings = ['size']
    size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]


class BlockBlueprintBuilder(BlueprintBuilder):
    key = "Block"
    cls = BlockBlueprint

    def build(self, catalog, name, config, parent):
        # print(config)
        if not "size" in config:
            if hasattr(parent, "size"):
                config["size"] = parent.size
        return super().build(catalog, name, config, parent)
