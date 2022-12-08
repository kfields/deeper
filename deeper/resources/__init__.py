from arcade.resources import add_resource_handle
from importlib import resources

path = resources.path('deeper', 'resources')
#print(path)
add_resource_handle('deeper', path)