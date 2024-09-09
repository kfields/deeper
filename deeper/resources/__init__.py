from importlib import resources

from crunge.engine.resource.resource_manager import ResourceManager

root = resources.path('deeper', 'resources')

ResourceManager().add_path_variable('deeper', root)

'''
from arcade.resources import add_resource_handle
from importlib import resources

root = resources.path('deeper', 'resources')
#print(path)
add_resource_handle('deeper', root)

def resource_path(path):
    root / path
'''