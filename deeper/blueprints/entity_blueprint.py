from loguru import logger

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..constants import *
from ..settings import EntitySettings
from ..blueprint import Blueprint


class EntityBlueprint(Blueprint):
    id: Mapped[int] = mapped_column(ForeignKey('Blueprint.id'), primary_key=True)
    category: Mapped[str] = mapped_column(String(32), default='')
    __mapper_args__ = {
        'polymorphic_identity': 'EntityBlueprint',
        'inherit_condition': (id == Blueprint.id),
    }

    settings_class = EntitySettings
    size = [CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH]
    #image = ''
    #offset = [0, 0]

    def __init__(self, catalog, name, config):
        super().__init__(catalog, name, config)

    def configure(self, config):
        #logger.debug(f"config: {config}")
        xconfig = config
        if 'extends' in config:
            base = self.catalog.find(config['extends'])
            base.add_derivative(self)
            xconfig = self.extend(config)

        #xconfig = self.borrow(config, self.parent)
        self.xconfig = xconfig
        #logger.debug(f"xconfig: {xconfig}")

        for key, value in xconfig.items():
            if key == 'components':
                continue
            setattr(self, key, value)

        if (not self._abstract) and 'components' in xconfig:
            for key, value in xconfig['components'].items():
                self.catalog.build(key, value, self)

        self.settings = self.create_settings(self.config)

    def update(self):
        #logger.debug('update')
        xconfig = self.extend(self.config) if self.base else self.config
        self.xconfig = xconfig
        #self.xconfig = config = self.borrow(config, self.parent)
        #logger.debug(f"xconfig: {config}")

        for key, value in xconfig.items():
            if key == 'components':
                continue
            setattr(self, key, value)

        if 'components' in xconfig:
            for component in self.components:
                component.config = xconfig['components'][component.name]
                #logger.debug(component.config)
                component.update()

        for derivative in self.derivatives:
            derivative.update()

        if not self.settings:
            self.settings = self.create_settings(self.config)
