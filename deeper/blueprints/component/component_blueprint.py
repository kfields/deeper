from loguru import logger

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...blueprint import Blueprint

class ComponentBlueprint(Blueprint):
    id: Mapped[int] = mapped_column(ForeignKey("Blueprint.id"), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'ComponentBlueprint',
        'inherit_condition': (id == Blueprint.id),
    }

    def __init__(self, catalog, name, config, parent):
        super().__init__(catalog, name, config, parent)

    def configure(self, config):
        self.xconfig = config = self.borrow(config, self.parent)

        for key, value in config.items():
            setattr(self, key, value)

    def update(self):
        self.xconfig = config = self.extend(self.config) if self.base else self.config
        self.xconfig = config = self.borrow(config, self.parent)
        #logger.debug(config)
        for key, value in config.items():
            setattr(self, key, value)
