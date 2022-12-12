from . import Vu

class SpriteVu(Vu):
    def __init__(self, space, sprite) -> None:
        super().__init__(space)
        self.sprite = sprite