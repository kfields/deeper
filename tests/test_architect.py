from deeper.world import World
from deeper.catalog import Catalog
from deeper.architect import Architect
from deeper.builders.block import BlockBuilder
world = World()

catalog = Catalog.instance
#catalog.dump()
blueprint = catalog.find('TileStone0')

architect = Architect.instance
architect.add_builder(BlockBuilder())
entity = architect.build(world, blueprint)

