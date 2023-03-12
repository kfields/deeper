import copy

from loguru import logger

from sqlalchemy import String, Integer, JSON, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from . import mergedeep
from .constants import *
from .builder import Builder
from .setting import decompose
from .model import Model

class Blueprint(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    type: Mapped[str]

    entity_id = mapped_column(Integer, ForeignKey('Blueprint.id'))
    components = relationship('Blueprint', backref=backref('entity', remote_side=[id]), foreign_keys=[entity_id])

    parent_id = mapped_column(Integer, ForeignKey('Blueprint.id'))
    children = relationship('Blueprint', backref=backref('parent', remote_side=[id]), foreign_keys=[parent_id])

    base_id = mapped_column(Integer, ForeignKey('Blueprint.id'))
    derivatives = relationship('Blueprint', backref=backref('base', remote_side=[id]), foreign_keys=[base_id])

    config: Mapped[dict] = mapped_column(JSON)
    #xconfig: Mapped[dict] = mapped_column(JSON)

    _abstract = False
    settings = None
    
    __mapper_args__ = {
        'polymorphic_identity': 'Blueprint',
        'polymorphic_on': 'type',
    }
    borrowed_settings = []

    def __init__(self, catalog, name, config, entity=None, parent=None):
        super().__init__()
        self.catalog = catalog
        self.name = name
        self.config = config
        self.category = None
        if entity:
            entity.add_component(self)
        if parent:
            parent.add_child(self)
        self.configure(config)

    def __repr__(self) -> str:
        return f'<Blueprint name={self.name}>'
        # return f"<Blueprint {self.__dict__}>"

    def add_component(self, component):
        self.components.append(component)

    def add_child(self, child):
        self.children.append(child)

    def add_derivative(self, derivative):
        self.derivatives.append(derivative)

    def configure(self, config):
        pass

    def update(self):
        pass

    def extend(self, config):
        xconfig = {}
        for key, value in self.base.xconfig.items():
            if key.startswith('_'):
                continue
            xconfig[key] = copy.deepcopy(value)

        xconfig = mergedeep.merge(
            xconfig, config, strategy=mergedeep.Strategy.REPLACE
        )

        return xconfig

    def borrow(self, config, blueprint):
        for name in self.borrowed_settings:
            if not name in config:
                #print(name)
                #print(parent)
                if name in blueprint.xconfig:
                    value = blueprint.xconfig[name]
                    #print(value)
                    config[name] = value
        return config

    def create_settings(self, config):
        decomposed = decompose(config)
        obj = {'name': self.name, 'value': decomposed}
        #print(obj)
        settings = self.settings_class.parse_obj(obj)
        settings.subscribe(self.on_setting)
        return settings

    def apply_settings(self):
        self.config = self.settings.to_dict()
        #logger.debug(self.config)
        self.update()

    def on_setting(self, setting):
        #logger.debug(setting)
        self.apply_settings()

class BlueprintBuilder(Builder):
    def build(self, catalog, name, config, entity, parent=None):
        return self.cls(catalog, name, config, entity, parent)
