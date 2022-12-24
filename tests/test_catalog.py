from deeper.catalog import Catalog

catalog = Catalog.instance
catalog.dump()

blueprint = catalog.find('Wagon')
print('Wagon: ', blueprint.__dict__)