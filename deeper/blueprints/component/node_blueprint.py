from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...constants import *
from ...settings.component.node_settings import NodeSettings
from ...blueprint import BlueprintBuilder
from .component_blueprint import ComponentBlueprint


class NodeBlueprint(ComponentBlueprint):
    id: Mapped[int] = mapped_column(ForeignKey('ComponentBlueprint.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'NodeBlueprint',
        'inherit_condition': (id == ComponentBlueprint.id),
    }

    settings_class = NodeSettings
    borrowed_settings = ['size']
    size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]


class NodeBlueprintBuilder(BlueprintBuilder):
    key = 'Node'
    cls = NodeBlueprint

    def build(self, catalog, name, config, entity, parent):
        # print(config)
        if not 'size' in config:
            if hasattr(entity, 'size'):
                config['size'] = entity.size
        return super().build(catalog, name, config, entity, parent)
