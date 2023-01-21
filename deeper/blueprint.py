import copy

from loguru import logger

from sqlalchemy import String, Integer, JSON, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from . import mergedeep
from .constants import *
from .builder import Builder
from .setting import decompose
from .models import Model

class Blueprint(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    type: Mapped[str]

    parent_id = mapped_column(Integer, ForeignKey("Blueprint.id"))
    children = relationship("Blueprint", backref=backref("parent", remote_side=[id]), foreign_keys=[parent_id])

    base_id = mapped_column(Integer, ForeignKey("Blueprint.id"))
    derivatives = relationship("Blueprint", backref=backref("base", remote_side=[id]), foreign_keys=[base_id])

    config: Mapped[dict] = mapped_column(JSON)

    _abstract = False
    settings = None
    
    __mapper_args__ = {
        "polymorphic_identity": "Blueprint",
        "polymorphic_on": "type",
    }
    borrowed_settings = []

    def __init__(self, catalog, name, config, parent=None):
        super().__init__()
        self.catalog = catalog
        self.name = name
        self.config = config
        self.category = None
        if parent:
            parent.add_child(self)
        self.configure(config)

    def __repr__(self) -> str:
        return f"<Blueprint name={self.name}>"
        # return f"<Blueprint {self.__dict__}>"

    def add_child(self, child):
        self.children.append(child)

    def add_derivative(self, derivative):
        self.derivatives.append(derivative)

    def configure(self, config):
        pass

    def update(self):
        pass

    def extend(self, config):
        #xconfig = copy.deepcopy(self.base.xconfig)
        xconfig = {}
        for key, value in self.base.xconfig.items():
            if key.startswith('_'):
                continue
            xconfig[key] = copy.deepcopy(value)

        xconfig = mergedeep.merge(
            xconfig, config, strategy=mergedeep.Strategy.REPLACE
        )
        #xconfig = self.borrow(xconfig, self.parent)
        # print("xconfig:", xconfig)

        return xconfig

    def borrow(self, config, parent):
        for name in self.borrowed_settings:
            if not name in config:
                #print(name)
                #print(parent)
                if name in parent.xconfig:
                    value = parent.xconfig[name]
                    #print(value)
                    config[name] = value
        return config

    def create_settings(self, config):
        decomposed = decompose(config)
        obj = {"name": self.name, "value": decomposed}
        #print(obj)
        settings = self.settings_class.parse_obj(obj)
        settings.subscribe(self.on_setting)
        #for setting in settings.value:
        #    setting.subscribe(self.on_setting)
        return settings

    def apply_settings(self):
        self.config = self.settings.to_dict()
        #logger.debug(self.config)
        self.update()

    def apply_setting(self, setting):
        setattr(self, setting.name, setting.value)
        #logger.debug(setting)

    def on_setting(self, setting):
        #logger.debug(setting)
        #self.apply_setting(setting)
        self.apply_settings()

class BlueprintBuilder(Builder):
    def build(self, catalog, name, config, parent):
        return self.cls(catalog, name, config, parent)
