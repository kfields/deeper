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

    def __init__(self, catalog, name, config, parent=None):
        self.catalog = catalog
        self.name = name
        self.config = config
        self.category = None
        #self.parent = parent
        self.children = []
        self._abstract = False
        #self.base = None
        self.xconfig = self.configure(config)
        self.settings = self.create_settings(config)
        self.derivatives = []

    def __repr__(self) -> str:
        return f"<Blueprint name={self.name}>"
        # return f"<Blueprint {self.__dict__}>"

    def configure(self, config):
        if not config:
            return {}
        # print("config: ", config)
        if "extends" in config:
            self.base = self.catalog.find(config["extends"])
            self.base.add_derivative(self)
            config = self.extend(config)

        for key, value in config.items():
            # print("config key, value: ", key, value)
            setattr(self, key, value)

        # if (not self._abstract) and hasattr(self, 'components'):
        if hasattr(self, "components"):
            for key, value in self.components.items():
                self.add_child(self.catalog.build(key, value, self))

        return config

    def add_child(self, child):
        self.children.append(child)

    def add_derivative(self, derivative):
        self.derivatives.append(derivative)

    def extend(self, config):
        xconfig = copy.deepcopy(self.base.xconfig)
        xconfig = mergedeep.merge(
            xconfig, config, strategy=mergedeep.Strategy.REPLACE
        )
        # print("xconfig:", xconfig)

        return xconfig

    def create_settings(self, config):
        decomposed = decompose(config)
        obj = {"name": self.name, "value": decomposed}
        #print(obj)
        settings = self.settings_class.parse_obj(obj)
        for setting in settings.value:
            setting.subscribe(self.on_setting)
        return settings

    def apply_settings(self):
        self.config = self.settings.to_dict()
        #print(self.config)
        self.update()

    def apply_setting(self, setting):
        setattr(self, setting.name, setting.value)
        logger.debug(setting)

    def on_setting(self, setting):
        #self.apply_setting(setting)
        self.apply_settings()

    def update(self):
        self.xconfig = config = self.extend(self.config) if self.base else self.config
        if not config:
            return
        #self.config = self.settings.to_dict()
        for key, value in config.items():
            # print("config key, value: ", key, value)
            setattr(self, key, value)

        # if (not self._abstract) and hasattr(self, 'components'):
        if hasattr(self, "components"):
            for child in self.children:
                child.config = self.components[child.name]
                child.update()

        for derivative in self.derivatives:
            derivative.update()

class BlueprintBuilder(Builder):
    def build(self, catalog, name, config, parent):
        return self.cls(catalog, name, config, parent)
