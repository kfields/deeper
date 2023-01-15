import os
import yaml

'''
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
'''

def load_yaml(file):
    return yaml.load(file, Loader=YamlLoader)

def dump_yaml(data, stream):
    yaml.dump(data, stream, Dumper=YamlDumper, default_flow_style=None, sort_keys=False)

class YamlLoader(yaml.FullLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super().__init__(stream)

    def _include(self, node):
        """
        - !include path/to/file.yaml
        """
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, YamlLoader)

    def _import(self, node):
        """
        - !import
            - path/to/file.yaml
            - key 
        """
        args = self.construct_sequence(node)

        filename = os.path.join(self._root, args[0])
        #print(filename)
        with open(filename, 'r') as f:
            return yaml.load(f, YamlLoader)[args[1]]

YamlLoader.add_constructor('!include', YamlLoader._include)
YamlLoader.add_constructor('!import', YamlLoader._import)

class YamlDumper(yaml.Dumper):
    pass