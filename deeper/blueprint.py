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

    __mapper_args__ = {
        "polymorphic_identity": "Blueprint",
        "polymorphic_on": "type",
    }
    borrowed_settings = []

    def __init__(self, catalog, name, config, parent=None):
        self.catalog = catalog
        self.name = name
        self.config = config
        self.category = None
        #self.parent = parent
        if parent:
            parent.add_child(self)
        #self.children = []
        self._abstract = False
        #self.base = None
        #self.xconfig = self.configure(config)
        self.configure(config)
        self.settings = self.create_settings(config)
        #self.derivatives = []

    def __repr__(self) -> str:
        return f"<Blueprint name={self.name}>"
        # return f"<Blueprint {self.__dict__}>"

    def add_child(self, child):
        self.children.append(child)

    def add_derivative(self, derivative):
        self.derivatives.append(derivative)

    def configure(self, config):
        #if not config:
        #    return {}
        if not config:
            config = {}
        # print("config: ", config)
        if "extends" in config:
            #self.base = self.catalog.find(config["extends"])
            base = self.catalog.find(config["extends"])
            #self.base.add_derivative(self)
            base.add_derivative(self)
            config = self.extend(config)

        self.xconfig = config = self.borrow(config, self.parent)

        for key, value in config.items():
            # print("config key, value: ", key, value)
            setattr(self, key, value)

        # if (not self._abstract) and hasattr(self, 'components'):
        if hasattr(self, "components"):
            for key, value in self.components.items():
                #self.add_child(self.catalog.build(key, value, self))
                self.catalog.build(key, value, self)

        return config

    def update(self):
        self.xconfig = config = self.extend(self.config) if self.base else self.config
        #if not config:
        #    return
        if not config:
            config = {}
        self.xconfig = config = self.borrow(config, self.parent)
        for key, value in config.items():
            #print("config key, value: ", key, value)
            setattr(self, key, value)

        # if (not self._abstract) and hasattr(self, 'components'):
        if hasattr(self, "components"):
            for child in self.children:
                child.config = self.components[child.name]
                child.update()

        for derivative in self.derivatives:
            derivative.update()

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
                print(name)
                print(parent)
                if name in parent.xconfig:
                    value = parent.xconfig[name]
                    print(value)
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
        #print(self.config)
        self.update()

    def apply_setting(self, setting):
        setattr(self, setting.name, setting.value)
        logger.debug(setting)

    def on_setting(self, setting):
        logger.debug(setting)
        #self.apply_setting(setting)
        self.apply_settings()

class BlueprintBuilder(Builder):
    def build(self, catalog, name, config, parent):
        return self.cls(catalog, name, config, parent)
