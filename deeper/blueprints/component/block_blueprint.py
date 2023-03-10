from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...constants import *
from ...settings.component.block_settings import BlockSettings
from ...blueprint import BlueprintBuilder
#from .component_blueprint import ComponentBlueprint
from .node_blueprint import NodeBlueprint


class BlockBlueprint(NodeBlueprint):
    id: Mapped[int] = mapped_column(ForeignKey('NodeBlueprint.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'BlockBlueprint',
        'inherit_condition': (id == NodeBlueprint.id),
    }

    settings_class = BlockSettings
    #borrowed_settings = ['size', 'transform']
    #size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]
    #transform = [0, 0, 0]


class BlockBlueprintBuilder(BlueprintBuilder):
    key = 'Block'
    cls = BlockBlueprint
