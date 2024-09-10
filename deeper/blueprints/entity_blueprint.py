from pathlib import Path

from loguru import logger

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, reconstructor

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture_loader import TextureLoader

from PIL import Image

from ..constants import *
from ..settings import EntitySettings
from ..blueprint import Blueprint

skip_set = set(['components', 'children'])

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
        self._thumbnail = None

    #TODO:  Find a way to reconstruct the Catalog properly.  This was close but it can't find it's base ...
    """
    @reconstructor
    def reconstruct(self):
        from ..catalog import Catalog
        self.catalog = Catalog.instance
        self.configure(self.config)
    """
    @reconstructor
    def reconstruct(self):
        self._thumbnail = None

    @property
    def thumbnail(self):
        if not self._thumbnail:
            root = ResourceManager().resolve_path(':deeper:/catalog/thumbnails')
            path = root / f'{self.name}.png'
            if Path.exists(path):
                #self._thumbnail = Image.open(path)
                self._thumbnail = TextureLoader().load(path)
            else:
                img_path = ResourceManager().resolve_path(self.image)
                with Image.open(img_path) as image:
                    image.thumbnail((64, 64))
                    image.save(path)
                    self._thumbnail = image

        return self._thumbnail

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
            if key in skip_set:
                continue
            setattr(self, key, value)

        if (not self._abstract) and 'components' in xconfig:
            for key, value in xconfig['components'].items():
                self.catalog.build(key, value, self)

        if (not self._abstract) and 'children' in xconfig:
            for key, value in xconfig['children'].items():
                #self.catalog.build(key, value, None, self)
                child = EntityBlueprint(self.catalog, key, value)
                self.add_child(child)

        self.settings = self.create_settings(self.config)

    def update(self):
        #logger.debug('update')
        xconfig = self.extend(self.config) if self.base else self.config
        self.xconfig = xconfig
        #self.xconfig = config = self.borrow(config, self.parent)
        #logger.debug(f"xconfig: {config}")

        for key, value in xconfig.items():
            if key in skip_set:
                continue
            setattr(self, key, value)

        if 'components' in xconfig:
            for component in self.components:
                component.config = xconfig['components'][component.name]
                #logger.debug(component.config)
                component.update()

        #TODO:  Need to reconstruct
        """
        if 'children' in xconfig:
            for child in self.children:
                child.config = xconfig['children'][child.name]
                #logger.debug(child.config)
                child.update()
        """

        for derivative in self.derivatives:
            derivative.update()

        if not self.settings:
            self.settings = self.create_settings(self.config)
