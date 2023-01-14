from pathlib import Path
from deeper.catalog import Catalog

catalog = Catalog.instance

catalog.save_yaml(Path('./catalog_dump'))
