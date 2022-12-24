from deeper.world import World
from deeper.catalog import Catalog
from deeper.architect import Architect

world = World()

catalog = Catalog.instance
#catalog.dump()
blueprint = catalog.find('DummyDoll')

architect = Architect.instance
entity = architect.build(blueprint, world)

