import os
import yaml

'''
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
'''

def load(path):
    with open(path) as f:
        return yaml.load(f, Loader=Loader)


class Loader(yaml.SafeLoader):
    """
    - !include path/to/file.yml 
    - !data path/to/file.yml 
    """
    def __init__(self, stream):
        #self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def _include(self, node):

        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

    def _data(self, node):

        filename = os.path.join(os.getcwd(), 'data', self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

Loader.add_constructor('!include', Loader._include)
Loader.add_constructor('!data', Loader._data)
