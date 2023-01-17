from loguru import logger

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..constants import *
from ..settings import EntitySettings
from ..blueprint import Blueprint


class EntityBlueprint(Blueprint):
    id: Mapped[int] = mapped_column(ForeignKey("Blueprint.id"), primary_key=True)
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
        if "extends" in config:
            base = self.catalog.find(config["extends"])
            base.add_derivative(self)
            config = self.extend(config)

        self.xconfig = config = self.borrow(config, self.parent)

        for key, value in config.items():
            setattr(self, key, value)

        if (not self._abstract) and hasattr(self, 'components'):
            for key, value in self.components.items():
                self.catalog.build(key, value, self)

        self.settings = self.create_settings(self.config)

    def update(self):
        #logger.debug('update')
        self.xconfig = config = self.extend(self.config) if self.base else self.config
        self.xconfig = config = self.borrow(config, self.parent)
        for key, value in config.items():
            setattr(self, key, value)

        # if (not self._abstract) and hasattr(self, 'components'):
        if hasattr(self, "components"):
            for child in self.children:
                child.config = self.components[child.name]
                #logger.debug(child.config)
                child.update()

        for derivative in self.derivatives:
            derivative.update()

        if not self.settings:
            self.settings = self.create_settings(self.config)
