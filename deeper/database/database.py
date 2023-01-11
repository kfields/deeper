from asyncio import current_task

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.scoping import scoped_session

from deeper.blueprints import *
from deeper.models import Model

from .utils import json_serializer


class Database:

    _instance = None

    @classmethod
    @property
    def instance(cls):
        if cls._instance:
            return cls._instance
        cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.engine = None

    def begin(self):
        self.engine = engine = create_engine(
            #"sqlite://", echo=True, json_serializer=json_serializer
            "sqlite:///./deeper.db", echo=True, json_serializer=json_serializer
            #sqlite+aiosqlite:///./stattik.db
        )

        with engine.begin() as conn:
            Model.metadata.create_all(conn)

        session_factory = sessionmaker(engine)
        Database.Session = Session = scoped_session(session_factory)

    def end(self):
        self.end_session()

    def end_session(self):
        self.Session.commit()
        self.Session.remove()

    async def drop_all(self):
        self.begin()
        with self.engine.begin() as conn:
            Model.metadata.drop_all
