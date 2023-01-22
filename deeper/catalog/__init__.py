from pathlib import Path
import glob
import re

from sqlalchemy import select

from loguru import logger
from arcade.resources import resolve_resource_path

from deeper.database import Database
import deeper.blueprints

from ..kits import Kit

from ..blueprints import EntityBlueprint
from .yaml import load_yaml, dump_yaml


def pascal_to_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class Category:
    def __init__(self, name) -> None:
        self.name = name
        self.blueprints = []
        self._abstract = True

    def add_blueprint(self, blueprint):
        if not blueprint._abstract:
            self._abstract = False
        self.blueprints.append(blueprint)


class Catalog(Kit):
    builders_path = deeper.blueprints

    _instance = None

    @classmethod
    @property
    def instance(cls):
        if cls._instance:
            return cls._instance
        cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.categories = {}
        self.category_names = []
        self.blueprints = {}
        self.load()

    def find_builder(self, name):
        if name in self.builders:
            return self.builders[name]
    
    def build(self, name, config, parent):
        builder = self.find_builder(name)
        if not builder:
            print(name)
        return builder.build(self, name, config, parent)

    def find(self, name):
        return self.blueprints[name]

    def load(self):
        """
        root = resolve_resource_path(":deeper:/catalog_original")
        self.load_yaml(root)
        return
        """
        root = resolve_resource_path(":deeper:/catalog")
        db = Database.instance
        session = db.session
        first = session.query(EntityBlueprint).first()

        if not first:
            self.load_yaml(root)
            self.create_database()
        else:
            self.load_database()

    def create_database(self):
        logger.debug("create database")
        db = Database.instance
        session = db.session
        for bp in self.blueprints.values():
            session.add(bp)

    def load_database(self):
        logger.debug("load database")
        db = Database.instance
        session = db.session

        blueprints = session.query(EntityBlueprint).all()
        #print(blueprints)
        for bp in blueprints:
            bp.catalog = self
            bp.update()
            self.register_blueprint(bp)

    def load_yaml(self, root):
        paths = glob.glob(f"{root}/*.yaml")
        for path in paths:
            # print(path)
            with open(path, "r") as file:
                cat = load_yaml(file)
                # print(cat)
                for key, value in cat.items():
                    self.build_blueprint(key, value)

    def save_yaml(self, path):
        for category in self.categories.values():
            data = {}
            imports = []
            for blueprint in category.blueprints:
                data[blueprint.name] = blueprint.config
            for blueprint in category.blueprints:
                if blueprint.base and not blueprint.base.name in data:
                    imports.append(blueprint.base)
            with open(path / f"{pascal_to_snake(category.name)}.yaml", "w") as file:
                for blueprint in imports:
                    file.write(
                        f"""{blueprint.name}: !import
  - {pascal_to_snake(blueprint.category)}.yaml
  - {blueprint.name}\n"""
                    )
                dump_yaml(data, file)

    def build_blueprint(self, key, value):
        blueprint = EntityBlueprint(self, key, value)
        # print("blueprint: ", blueprint.__dict__)
        self.register_blueprint(blueprint)

    def register_blueprint(self, blueprint):
        category = None
        if blueprint.category in self.categories:
            category = self.categories[blueprint.category]
        else:
            category = Category(blueprint.category)
            self.add_category(category)
        category.add_blueprint(blueprint)
        self.add_blueprint(blueprint.name, blueprint)

    def add_blueprint(self, key, value):
        self.blueprints[key] = value

    def add_category(self, category: Category):
        self.categories[category.name] = category
        self.category_names.append(category.name)

    def dump(self):
        for blueprint in self.blueprints.values():
            print(blueprint.__dict__)
