from pathlib import Path
import shutil

import arcade
from arcade.resources import resolve_resource_path

from .window import Window
from .constants import *
#from .world import World
from .levels.test_level import TestLevel

from .state import WorldEditState
from .views import LevelEditor
from .database import Database

from deeper.resources.icons import IconsMaterialDesign

class Deeper(Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'Deeper', resizable=True)
        #self.world = World()
        self.world = TestLevel()
    
    def create(self):
        self.load_settings()
        view = LevelEditor(self, WorldEditState(self.world))
        self.show_view(view)

    def destroy(self):
        self.save_settings()

    def load_settings(self):
        dst = Path('imgui.ini')
        if not dst.exists():
            src = resolve_resource_path(':deeper:/settings/imgui.ini')
            shutil.copyfile(src, dst)

    def save_settings(self):
        src = Path('imgui.ini')
        dst = resolve_resource_path(':deeper:/settings/imgui.ini')
        shutil.copyfile(src, dst)

def main():
    arcade.text.load_font(
        f':deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}'
    )

    db = Database.instance
    dbpath = Path('./deeper.db')
    db.begin(dbpath)
    with db.Session() as session:
        with session.begin():
            db.session = session
            app = Deeper()
            app.create()
            arcade.run()
            app.destroy()
    db.end()


if __name__ == "__main__":
    main()
