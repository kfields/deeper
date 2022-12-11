from arcade.resources import add_resource_handle
from importlib import resources

root = resources.path('deeper', 'resources')
#print(path)
add_resource_handle('deeper', root)

def resource_path(path):
    root / path
