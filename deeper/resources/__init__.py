from importlib.resources import files

from crunge.engine.resource.resource_manager import ResourceManager

root = files("deeper.resources")

ResourceManager().add_path_variable("deeper", root)
