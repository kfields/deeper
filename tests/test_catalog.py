from deeper.catalog import Catalog

catalog = Catalog.instance
catalog.dump()

blueprint = catalog.find('TileStone0')
print('TileStone0: ', blueprint.__dict__)