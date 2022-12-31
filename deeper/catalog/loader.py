import os
import yaml

'''
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
'''

def load(file):
    return yaml.load(file, Loader=Loader)


class Loader(yaml.FullLoader):
    """
    - !include path/to/file.yaml
    """
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super().__init__(stream)

    def _include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

    def _import(self, node):
        args = []
        kwargs = {}
        if isinstance(node, yaml.nodes.ScalarNode):  # type: ignore
            args = [self.construct_scalar(node)]
        elif isinstance(node, yaml.nodes.SequenceNode):  # type: ignore
            args = self.construct_sequence(node)
        elif isinstance(node, yaml.nodes.MappingNode):  # type: ignore
            kwargs = self.construct_mapping(node)
        else:
            raise TypeError('Un-supported YAML node {!r}'.format(node))
        """
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)
        """
        filename = os.path.join(self._root, args[0])
        print(filename)
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)[args[1]]

Loader.add_constructor('!include', Loader._include)
Loader.add_constructor('!import', Loader._import)
