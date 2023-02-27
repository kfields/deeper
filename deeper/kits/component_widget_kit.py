from loguru import logger

from deeper.builder import Builder
import deeper.widgets.component

from .kit import Kit

class ComponentWidgetKit(Kit):
    builders_path = deeper.widgets.component
    #builder_type = Builder

    def find(self, component, cls=None):
        if not cls:
            cls = component.__class__
        if cls in self.builders:
            return self.builders[cls]
        else:
            base = cls.__bases__[0]
            if base == object:
                return None
            #print(base)
            return self.find(component, base) #TODO: What if multiple bases?

    def build(self, component):
        #print(component.__dict__)
        #print(component.__class__.__name__)
        builder = self.find(component)
        return builder.build(component)