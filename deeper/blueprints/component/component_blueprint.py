from loguru import logger

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...blueprint import Blueprint

class ComponentBlueprint(Blueprint):
    id: Mapped[int] = mapped_column(ForeignKey('Blueprint.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'ComponentBlueprint',
        'inherit_condition': (id == Blueprint.id),
    }

    def __init__(self, catalog, name, config, entity, parent):
        super().__init__(catalog, name, config, entity, parent)

    def configure(self, config):
        xconfig = self.borrow(config, self.entity)
        self.xconfig = xconfig

        for key, value in xconfig.items():
            setattr(self, key, value)

    def update(self):
        xconfig = self.extend(self.config) if self.base else self.config
        xconfig = self.borrow(xconfig, self.entity)
        self.xconfig = xconfig
        #logger.debug(config)
        for key, value in xconfig.items():
            setattr(self, key, value)
