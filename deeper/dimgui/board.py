import imgui

class Board:
    def __init__(self) -> None:
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Clipboard(Board):
    pass


class Dropboard(Board):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        imgui.set_drag_drop_payload('itemtype', b'payload')
