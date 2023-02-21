from pathlib import Path

import arcade

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
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        #self.world = World()
        self.world = TestLevel()
        #view = LevelEditor(self, WorldEditState(self.world))
        #self.show_view(view)
    
    def setup(self):
        view = LevelEditor(self, WorldEditState(self.world))
        self.show_view(view)

def main():
    arcade.text.load_font(
        f":deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}"
    )

    db = Database.instance
    dbpath = Path('./deeper.db')
    db.begin(dbpath)
    with db.Session() as session:
        with session.begin():
            db.session = session
            window = Deeper()
            window.setup()
            arcade.run()
    db.end()


if __name__ == "__main__":
    main()
