from pathlib import Path
import json

import glm

#from .world import World
from .scene import Scene
from .blueprints import EntityBlueprint
from .kits.entity_kit import EntityKit
from .catalog import Catalog
from .processors import RenderingProcessor, AnimationProcessor

class Level(Scene):
    def __init__(self, name: str, timed:bool=False):
        super().__init__(timed)
        self.name: str = name
        self.add_processors([RenderingProcessor(self), AnimationProcessor(self)])

    def save(self, path: Path):
        layers = []
        for layer in self.layers:
            layers.append(self.serialize_layer(layer))

        data = {
            'name': self.name,
            'layers': layers
        }
        #print(data)
        with open(path / f'{self.name}.json', "w") as out_file:
            json.dump(data, out_file, indent = 2)

    def serialize_layer(self, layer):
        entities = []
        for ent, (_, blueprint) in self.get_components(layer.__class__, EntityBlueprint):
            entities.append(self.serialize_entity(ent, blueprint))
        data = {
            'name': layer.name,
            'entities': entities
        }
        return data

    def serialize_entity(self, ent, blueprint: EntityBlueprint):
        data = {
            'blueprint': blueprint.name,
            'position': list(ent.position)
        }
        return data

    @classmethod
    def load(cls, path: Path) -> 'Level':
        with open(path, "r") as in_file:
            data = json.load(in_file)

        name = data['name']
        level = cls(name)
        level.deserialize(data)
        return level

    def deserialize(self, data):
        layers_data = data['layers']
        for layer_data in layers_data:
            self.deserialize_layer(layer_data)

    def deserialize_layer(self, layer_data):
        layer = self.create_layer(layer_data['name'])
        entities_data = layer_data['entities']
        for entity_data in entities_data:
            self.deserialize_entity(layer, entity_data)

    def deserialize_entity(self, layer, entity_data):
        catalog = Catalog.instance
        blueprint = catalog.find(entity_data['blueprint'])
        position = glm.vec3(entity_data['position'])
        EntityKit.instance.build(
            blueprint, self, layer, position
        )
