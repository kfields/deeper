from loguru import logger

from deeper.builder import Builder
import deeper.widgets.blueprint

from .kit import Kit

class BlueprintWidgetKit(Kit):
    builders_path = deeper.widgets.blueprint
    #builder_type = Builder

    def find(self, blueprint):
        if blueprint.__class__ in self.builders:
            return self.builders[blueprint.__class__]

    def build(self, blueprint):
        #print(blueprint.__dict__)
        builder = self.find(blueprint)
        return builder.build(blueprint)