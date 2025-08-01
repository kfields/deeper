from pathlib import Path
import shutil
import glm

from crunge.engine.resource.resource_manager import ResourceManager

from crunge.engine.app import App
from .constants import *
from .levels.basic_level import BasicLevel

from .state import LevelEditState
from .views import LevelEditor
from .database import Database


class Deeper(App):
    def __init__(self):
        super().__init__(title="Deeper", resizable=True)
        self.scene = BasicLevel()

    def _create(self):
        super()._create()
        self.load_settings()
        self.view = LevelEditor(LevelEditState(self.scene))

    def destroy(self):
        self.save_settings()

    def load_settings(self):
        dst = Path("imgui.ini")
        if not dst.exists():
            src = ResourceManager().resolve_path(":deeper:/settings/imgui.ini")
            shutil.copyfile(src, dst)

    def save_settings(self):
        src = Path("imgui.ini")
        dst = ResourceManager().resolve_path(":deeper:/settings/imgui.ini")
        shutil.copyfile(src, dst)


def main():
    import faulthandler
    faulthandler.enable()

    db = Database.instance
    dbpath = Path("./deeper.db")
    db.begin(dbpath)
    with db.Session() as session:
        with session.begin():
            db.session = session
            Deeper().run().destroy()
    db.end()


if __name__ == "__main__":
    main()
