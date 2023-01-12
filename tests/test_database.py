from deeper.catalog import Catalog
from deeper.database import Database

db = Database.instance
catalog = Catalog.instance
#catalog.dump()

#blueprint = catalog.find('Wagon')
#print('Wagon: ', blueprint.__dict__)

db.drop_all()
db.begin()

with db.Session() as session:
    with session.begin():
        for bp in catalog.blueprints.values():
            session.add(bp)

db.end()