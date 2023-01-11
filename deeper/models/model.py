from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.ext.declarative import as_declarative, declared_attr

mapper_registry = registry()

class Model(metaclass=DeclarativeMeta):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

    # these are supplied by the sqlalchemy2-stubs, so may be omitted
    # when they are installed
    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor
    __mapper_args__ = {"eager_defaults": True}
